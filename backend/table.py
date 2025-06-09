from backend.pager import Pager, BTreePage, PageHeader
from utils.logger import get_logger

logger = get_logger(__name__)

MAX_KEYS = 32  # Simulate a page size limit (adjust as needed)
MIN_KEYS = MAX_KEYS // 2

class Table:
    def __init__(self, table_name: str, schema=None):
        self.table_name = table_name
        self.filename = f"{table_name}.tbl"
        self.schema = schema
        logger.info(f"Initializing Table for '{self.table_name}', file: {self.filename}")
        try:
            self.pager = Pager(self.filename)
            logger.debug(f"Pager created for file: {self.filename}")
        except Exception as e:
            logger.error(f"Failed to initialize Pager for {self.filename}: {e}")
            raise
        # Always get root page number from Pager
        self.root_page_num = self.pager.read_root_page_number()
        logger.info(f"Root page number initialized to {self.root_page_num} for table '{self.table_name}'")

    def insert(self, key, value):
        split = self._insert_recursive(self.root_page_num, key, value)
        if split is not None:
            median_key, right_page_number = split
            new_root = BTreePage(is_leaf=False)
            new_root.cells = [(median_key, right_page_number)]
            new_root.header.num_keys = 1
            new_root.children = [self.root_page_num, right_page_number]
            new_root_page_num = self.pager.allocate_page()
            self.pager.write_page(new_root_page_num, new_root.to_bytes())
            logger.info(f"About to write new root page number: {new_root_page_num}")
            self.root_page_num = new_root_page_num
            self.pager.write_root_page_number(new_root_page_num)
            logger.info(f"Root page split, new root page created: {new_root_page_num}")

    def _insert_recursive(self, page_number: int, key, value):
        page = self.load_page(page_number)
        logger.info(f"_insert_recursive: page_number={page_number}, is_leaf={page.is_leaf}, num_cells={len(page.cells)} BEFORE")
        if page.is_leaf:
            if not page.is_full(key, value):
                page.add_leaf_cell(key, value)
                logger.info(f"_insert_recursive: page_number={page_number}, is_leaf={page.is_leaf}, num_cells={len(page.cells)} AFTER add_leaf_cell")
                self.save_page(page_number, page)
                return None
            else:
                logger.debug(f"Leaf page {page_number} is full, splitting")
                page.add_leaf_cell(key, value)
                logger.info(f"_insert_recursive: page_number={page_number}, is_leaf={page.is_leaf}, num_cells={len(page.cells)} AFTER add_leaf_cell (split)")
                median_key, right_page_number = page.split_leaf_page(self.pager)
                self.save_page(page_number, page)
                return median_key, right_page_number
        else:
            idx = page.find_child_index(key)
            if idx >= len(page.children):
                logger.error(f"Child index {idx} out of range for children {page.children}")
                raise IndexError(f"Child index {idx} out of range for children {page.children}")
            child_page_number = page.children[idx]
            if child_page_number < 1:
                logger.error(f"Attempted to descend to invalid child page {child_page_number} for key={key} in page {page_number}")
                raise ValueError(f"Invalid child page number: {child_page_number}")
            logger.debug(f"Descending to child page {child_page_number} for key={key}")
            split = self._insert_recursive(child_page_number, key, value)
            if split is not None:
                median_key, right_page_number = split
                page.insert_internal_cell(median_key, right_page_number)
                if page.is_full():
                    logger.debug(f"Internal page {page_number} is full, splitting")
                    median_key, right_page_number = page.split_internal_page(self.pager)
                    self.save_page(page_number, page)
                    return (median_key, right_page_number)
                self.save_page(page_number, page)
            return None

    def delete(self, key):
        """
        Delete a key from the B-Tree, handling underflow/merge if needed.
        """
        self._delete_recursive(self.root_page_num, key, parent_page_num=None, parent_index=None)

    def _delete_recursive(self, page_number, key, parent_page_num, parent_index):
        page = self.load_page(page_number)
        if page.is_leaf:
            # Delete the key from the leaf
            deleted = page.delete_leaf_cell(key)
            self.save_page(page_number, page)
            # Underflow check
            if len(page.cells) < MIN_KEYS and parent_page_num is not None:
                self._handle_leaf_underflow(page_number, parent_page_num, parent_index)
            # If root is empty and not a leaf, shrink tree
            if parent_page_num is None and len(page.cells) == 0 and not page.is_leaf:
                # Promote only child as new root
                new_root_num = page.children[0]
                self.root_page_num = new_root_num
                self.pager.write_root_page_number(new_root_num)
                logger.info(f"Root shrunk, new root page number: {new_root_num}")
            return deleted
        else:
            # Find child to descend
            idx = page.find_child_index(key)
            child_page_num = page.children[idx]
            self._delete_recursive(child_page_num, key, page_number, idx)
            # After recursion, check for underflow in child
            child_page = self.load_page(child_page_num)
            if len(child_page.cells) < MIN_KEYS:
                self._handle_internal_underflow(child_page_num, page_number, idx)
            self.save_page(page_number, page)
            # If root is empty and not a leaf, shrink tree
            if parent_page_num is None and len(page.cells) == 0 and not page.is_leaf:
                new_root_num = page.children[0]
                self.root_page_num = new_root_num
                self.pager.write_root_page_number(new_root_num)
                logger.info(f"Root shrunk, new root page number: {new_root_num}")

    def _handle_leaf_underflow(self, page_number, parent_page_num, parent_index):
        """
        Handle underflow in a leaf node by borrowing from or merging with a sibling.
        """
        page = self.load_page(page_number)
        parent = self.load_page(parent_page_num)
        # Try left sibling
        left_sibling_num = parent.children[parent_index - 1] if parent_index > 0 else None
        right_sibling_num = parent.children[parent_index + 1] if parent_index + 1 < len(parent.children) else None
        if left_sibling_num is not None:
            left_sibling = self.load_page(left_sibling_num)
            if len(left_sibling.cells) > MIN_KEYS:
                # Borrow from left
                borrowed = left_sibling.cells.pop(-1)
                page.cells.insert(0, borrowed)
                left_sibling.header.num_keys = len(left_sibling.cells)
                page.header.num_keys = len(page.cells)
                # Update parent separator key
                parent.cells[parent_index - 1] = (page.cells[0][0], parent.cells[parent_index - 1][1])
                self.save_page(left_sibling_num, left_sibling)
                self.save_page(page_number, page)
                self.save_page(parent_page_num, parent)
                return
        if right_sibling_num is not None:
            right_sibling = self.load_page(right_sibling_num)
            if len(right_sibling.cells) > MIN_KEYS:
                # Borrow from right
                borrowed = right_sibling.cells.pop(0)
                page.cells.append(borrowed)
                right_sibling.header.num_keys = len(right_sibling.cells)
                page.header.num_keys = len(page.cells)
                # Update parent separator key
                parent.cells[parent_index] = (right_sibling.cells[0][0], parent.cells[parent_index][1])
                self.save_page(right_sibling_num, right_sibling)
                self.save_page(page_number, page)
                self.save_page(parent_page_num, parent)
                return
        # Merge with sibling if can't borrow
        if left_sibling_num is not None:
            left_sibling = self.load_page(left_sibling_num)
            left_sibling.cells.extend(page.cells)
            left_sibling.header.num_keys = len(left_sibling.cells)
            # Remove pointer and separator from parent
            del parent.children[parent_index]
            del parent.cells[parent_index - 1]
            self.save_page(left_sibling_num, left_sibling)
            self.save_page(parent_page_num, parent)
            # Optionally, deallocate page_number
        elif right_sibling_num is not None:
            right_sibling = self.load_page(right_sibling_num)
            page.cells.extend(right_sibling.cells)
            page.header.num_keys = len(page.cells)
            # Remove pointer and separator from parent
            del parent.children[parent_index + 1]
            del parent.cells[parent_index]
            self.save_page(page_number, page)
            self.save_page(parent_page_num, parent)
            # Optionally, deallocate right_sibling_num
        # If parent underflows, will be handled recursively

    def _handle_internal_underflow(self, page_number, parent_page_num, parent_index):
        """
        Handle underflow in an internal node by borrowing from or merging with a sibling.
        """
        page = self.load_page(page_number)
        parent = self.load_page(parent_page_num)
        left_sibling_num = parent.children[parent_index - 1] if parent_index > 0 else None
        right_sibling_num = parent.children[parent_index + 1] if parent_index + 1 < len(parent.children) else None
        if left_sibling_num is not None:
            left_sibling = self.load_page(left_sibling_num)
            if len(left_sibling.cells) > MIN_KEYS:
                # Borrow from left: move parent's separator down, move left's last child up
                sep_key, _ = parent.cells[parent_index - 1]
                borrowed_cell = left_sibling.cells.pop(-1)
                borrowed_child = left_sibling.children.pop(-1)
                page.cells.insert(0, (sep_key, page.children[0]))
                page.children.insert(0, borrowed_child)
                parent.cells[parent_index - 1] = (borrowed_cell[0], parent.cells[parent_index - 1][1])
                left_sibling.header.num_keys = len(left_sibling.cells)
                page.header.num_keys = len(page.cells)
                self.save_page(left_sibling_num, left_sibling)
                self.save_page(page_number, page)
                self.save_page(parent_page_num, parent)
                return
        if right_sibling_num is not None:
            right_sibling = self.load_page(right_sibling_num)
            if len(right_sibling.cells) > MIN_KEYS:
                # Borrow from right: move parent's separator down, move right's first child up
                sep_key, _ = parent.cells[parent_index]
                borrowed_cell = right_sibling.cells.pop(0)
                borrowed_child = right_sibling.children.pop(0)
                page.cells.append((sep_key, right_sibling.children[0]))
                page.children.append(borrowed_child)
                parent.cells[parent_index] = (borrowed_cell[0], parent.cells[parent_index][1])
                right_sibling.header.num_keys = len(right_sibling.cells)
                page.header.num_keys = len(page.cells)
                self.save_page(right_sibling_num, right_sibling)
                self.save_page(page_number, page)
                self.save_page(parent_page_num, parent)
                return
        # Merge with sibling if can't borrow
        if left_sibling_num is not None:
            left_sibling = self.load_page(left_sibling_num)
            sep_key, _ = parent.cells[parent_index - 1]
            # Merge separator and page into left sibling
            left_sibling.cells.append((sep_key, page.children[0]))
            left_sibling.cells.extend(page.cells)
            left_sibling.children.extend(page.children[1:])
            left_sibling.header.num_keys = len(left_sibling.cells)
            del parent.children[parent_index]
            del parent.cells[parent_index - 1]
            self.save_page(left_sibling_num, left_sibling)
            self.save_page(parent_page_num, parent)
            # Optionally, deallocate page_number
        elif right_sibling_num is not None:
            right_sibling = self.load_page(right_sibling_num)
            sep_key, _ = parent.cells[parent_index]
            # Merge separator and right sibling into page
            page.cells.append((sep_key, right_sibling.children[0]))
            page.cells.extend(right_sibling.cells)
            page.children.extend(right_sibling.children[1:])
            page.header.num_keys = len(page.cells)
            del parent.children[parent_index + 1]
            del parent.cells[parent_index]
            self.save_page(page_number, page)
            self.save_page(parent_page_num, parent)
            # Optionally, deallocate right_sibling_num
        # If parent underflows, will be handled recursively

    def save_root_page(self, page: BTreePage):
        logger.debug(f"Saving root page with {len(page.cells)} cells")
        try:
            self.pager.write_page(self.root_page_num, page.to_bytes())
            logger.info(f"Root page saved successfully for table '{self.table_name}'")
        except Exception as e:
            logger.error(f"Error saving root page for table '{self.table_name}': {e}")
            raise

    def load_root_page(self) -> BTreePage:
        try:
            raw = self.pager.read_page(self.root_page_num)
            logger.debug(f"Loading root page {self.root_page_num}, first 11 bytes: {list(raw[:11])}")
            if all(b == 0 for b in raw[:11]):
                logger.info("Page is empty, returning new leaf page")
                return BTreePage(is_leaf=True)
            logger.debug("Page is not empty, parsing from bytes")
            return BTreePage.from_bytes(raw)
        except Exception as e:
            logger.error(f"Error loading root page for table '{self.table_name}': {e}")
            raise

    def load_page(self, page_number: int) -> BTreePage:
        raw = self.pager.read_page(page_number)
        return BTreePage.from_bytes(raw)

    def save_page(self, page_number: int, page: BTreePage):
        self.pager.write_page(page_number, page.to_bytes())

    def scan_page(self, page_number: int):
        page = self.load_page(page_number)
        logger.info(f"SCAN_PAGE: page_number={page_number}, is_leaf={page.is_leaf}, num_cells={len(page.cells)}, children={getattr(page, 'children', None)}")
        if page.is_leaf:
            for key, value in page.cells:
                yield (key, value, page_number)  # Yield page_number for each row
        else:
            n = len(page.cells)
            if not page.children or len(page.children) != n + 1:
                logger.error(f"Internal page {page_number} children/cells mismatch: children={page.children}, cells={page.cells}")
                raise ValueError(f"Internal page {page_number} children/cells mismatch")
            for i in range(n):
                yield from self.scan_page(page.children[i])
            yield from self.scan_page(page.children[-1])

    def close(self):
        logger.info(f"Closing table '{self.table_name}'")
        try:
            self.pager.close()
            logger.debug(f"Pager closed for file: {self.filename}")
        except Exception as e:
            logger.error(f"Error closing pager for table '{self.table_name}': {e}")
            raise