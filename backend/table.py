from backend.pager import Pager, BTreePage, PageHeader
from utils.logger import get_logger

logger = get_logger(__name__)

class Table:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.filename = f"{table_name}.tbl"
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
            self.root_page_num = new_root_page_num
            self.pager.write_root_page_number(new_root_page_num)
            logger.info(f"Root page split, new root page created: {new_root_page_num}")

    def _insert_recursive(self, page_number: int, key, value):
        page = self.load_page(page_number)
        logger.debug(f"Inserting key={key}, value={value} into page {page_number}")
        if page.is_leaf:
            if not page.is_full(key, value):
                page.add_leaf_cell(key, value)
                self.save_page(page_number, page)
                return None
            else:
                logger.debug(f"Leaf page {page_number} is full, splitting")
                page.add_leaf_cell(key, value)
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
        if page.is_leaf:
            for key, value in page.cells:
                yield (key, value)
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