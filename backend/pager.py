"""
Serialization: turning an in-memory Python object into a byte sequence that can be:
 - stored in a file
 - sent over a network
 - Written to a database

Serialized page: [13, 0, 2, 0, 0, 0, 27, 0, 0, 0, 0, 0, 10, 0, 5, 65, 108, 105, 99, 101, 0, 20, 0, 3, 66, 111, 98]
Let's split this into sections:
Part 1: Page Header Bytes 0 to 10
Byte_range   Meaning        Bytes                       Values
0 to 0      Page Type        13              0x0D (13) for leaf node, 0x05 (5) for internal node
1 to 2      Num Keys         [0, 2]          2 (number of keys in the page)
3 to 6      Free Start       [0, 0, 0, 27]   27 (offset where free space starts)
7 to 10     Right Sibling    [0, 0, 0, 0]    0 (pointer to the next page, only used in leaf nodes)
so far this says
- It's a leaf node (0x0D)
- It has 2 keys
- Cells start at byte 27
- It has no right sibling (0)

Part 2: Cell Data Bytes 11 to 20
Byte_range      Meaning        Bytes                        Values
11 to 12         Key           [0, 10]                  10 (first key)
13-14         Value Length     [0, 5]                   5 (length of the value)
15-19           Value          [65, 108, 105, 99, 101]  "Alice" (the value for the first key)

Interpreted as:
key=10,value="Alice"

Part 3: Cell Data Bytes 21 to 30
Byte_range      Meaning        Bytes                        Values
21-22           Key           [0, 20]                  20 (second key)
23-24         Value Length     [0, 3]                   3 (length of the value)
25-27           Value          [66, 111, 98]            "Bob" (the value for the second key)

Interpreted as:
key=20,value="Bob"
"""
import os
import shutil
from utils.logger import get_logger

logger = get_logger(__name__)

PAGE_SIZE = 4096  # Size of a B-Tree page in bytes
ROOT_PAGE_HEADER_SIZE = 4  # 4 bytes for root page number at file start

class PageHeader:
    def __init__(self, page_type: int, num_keys: int = 0, free_start:int = 0, right_sibling: int=0):
        self.page_type = page_type
        self.num_keys = num_keys
        self.free_start = free_start
        self.right_sibling = right_sibling
        logger.debug(f"Initialized PageHeader: page_type={page_type}, num_keys={num_keys}, free_start={free_start}, right_sibling={right_sibling}")
        
    def to_bytes(self) -> bytes:
        header_bytes = (
                self.page_type.to_bytes(1, 'big') +
                self.num_keys.to_bytes(2, 'big') +
                self.free_start.to_bytes(4, 'big') +
                self.right_sibling.to_bytes(4, 'big')
                )
        logger.debug(f"Serialized PageHeader to bytes: {header_bytes}")
        return header_bytes
        
    @staticmethod
    def from_bytes(data: bytes) -> 'PageHeader':
        if len(data) < 11:
            logger.error(f"Data must be at least 11 bytes long, got {len(data)} bytes")
            raise ValueError(f"Data must be at least 11 bytes long, got {len(data)} bytes")
        header = PageHeader(
            page_type=data[0],
            num_keys=int.from_bytes(data[1:3], 'big'),
            free_start=int.from_bytes(data[3:7], 'big'),
            right_sibling=int.from_bytes(data[7:11], 'big')
            )
        logger.debug(f"Deserialized PageHeader from bytes: {header.__dict__}")
        return header
            
class BTreePage:
    def __init__(self, is_leaf: bool):
        self.is_leaf = is_leaf
        self.header = PageHeader(page_type=0x0D if is_leaf else 0x05)
        self.cells: list = []  # List of tuples (key, value) for leaf nodes or (key, child_page_number) for internal nodes
        self.children: list = [] if not is_leaf else None
        logger.debug(f"Initialized BTreePage: is_leaf={is_leaf}")

    def is_full(self, next_key=None, next_value=None):
        # Calculate the size if we add another cell
        if self.is_leaf:
            content = b"".join(
                key.to_bytes(2, 'big') +
                len(value).to_bytes(2, 'big') +
                value for key, value in self.cells
            )
            if next_key is not None and next_value is not None:
                content += (
                    next_key.to_bytes(2, 'big') +
                    len(next_value).to_bytes(2, 'big') +
                    next_value
                )
        else:
            content = b""
            # Internal: leftmost child, then (key, child_page_number) for each cell
            if self.children and len(self.children) > 0:
                content += self.children[0].to_bytes(4, 'big')
            for i, (key, child_page_number) in enumerate(self.cells):
                content += key.to_bytes(2, 'big') + child_page_number.to_bytes(4, 'big')
            # If next_key/next_value is provided, simulate adding another cell/child
            if next_key is not None and next_value is not None:
                # next_value is expected to be a child_page_number for internal nodes
                content += next_key.to_bytes(2, 'big') + next_value.to_bytes(4, 'big')
        total_size = len(self.header.to_bytes()) + len(content)
        logger.info(f"is_full: is_leaf={self.is_leaf}, num_cells={len(self.cells)}, total_size={total_size}")
        return total_size > PAGE_SIZE
    
    def add_leaf_cell(self, key: int, value: bytes):
        idx = 0
        while idx < len(self.cells) and self.cells[idx][0] < key:
            idx += 1
        self.cells.insert(idx, (key, value))
        self.header.num_keys = len(self.cells)
        
    def find_child_index(self, key: int) -> int:
        for i, (k, _) in enumerate(self.cells):
            if k >= key:
                return i
        return len(self.cells)
    
    def insert_internal_cell(self, key: int, child_page_number: int):
        idx = self.find_child_index(key)
        self.cells.insert(idx, (key, child_page_number))
        self.header.num_keys = len(self.cells)
        # Maintain children: insert child_page_number after idx
        if self.children is not None:
            self.children.insert(idx + 1, child_page_number)
        
    def split_internal_page(self, pager):
        mid = len(self.cells) // 2
        right_cells = self.cells[mid + 1:]
        left_cells = self.cells[:mid]
        median_key = self.cells[mid][0]
        
        right_page = BTreePage(is_leaf=False)
        right_page.cells = right_cells
        right_page.header.num_keys = len(right_cells)
        # Set children for right page
        if self.children:
            right_page.children = self.children[mid + 1:]
        else:
            right_page.children = []
        
        self.cells = left_cells
        self.header.num_keys = len(left_cells)
        if self.children:
            self.children = self.children[:mid + 1]
        
        new_right_page_number = pager.allocate_page()
        pager.write_page(new_right_page_number, right_page.to_bytes())
        logger.info(f"Split internal page, median_key={median_key}, new_right_page_number={new_right_page_number}")
        return median_key, new_right_page_number

    def add_internal_cell(self, key: int, child_page_number: int):
        if self.header.page_type != 0x05:
            logger.error("Cannot add internal cell to leaf page")
            raise ValueError("Cannot add internal cell to leaf page")
        self.cells.append((key, child_page_number))
        self.header.num_keys += 1
        if self.children is not None:
            self.children.append(child_page_number)
        logger.debug(f"Added internal cell: key={key}, child_page_number={child_page_number}")

    def to_bytes(self) -> bytes:
        if self.is_leaf:
            content = b"".join(
                key.to_bytes(2, 'big') +
                len(value).to_bytes(2, 'big') +
                value for key, value in self.cells
            )
        else:
            content = b""
            if self.children and len(self.children) > 0:
                content += self.children[0].to_bytes(4, 'big')
            for i, (key, child_page_number) in enumerate(self.cells):
                content += key.to_bytes(2, 'big') + child_page_number.to_bytes(4, 'big')
        self.header.free_start = 11 + len(content)
        page_bytes = self.header.to_bytes() + content
        if len(page_bytes) > PAGE_SIZE:
            logger.error("Serialized page exceeds PAGE_SIZE")
            raise ValueError("Serialized page exceeds PAGE_SIZE")
        logger.debug(f"Serialized BTreePage to bytes: {len(page_bytes)} bytes")
        return page_bytes

    def split_leaf_page(self, pager):
        logger.info(f"split_leaf_page called: num_cells={len(self.cells)}")
        mid = len(self.cells) // 2
        right_cells = self.cells[mid:]
        left_cells = self.cells[:mid]
        
        right_page = BTreePage(is_leaf=True)
        right_page.cells = right_cells
        right_page.header.num_keys = len(right_cells)
        
        self.cells = left_cells
        self.header.num_keys = len(left_cells)
        
        new_right_page_number = pager.allocate_page()
        pager.write_page(new_right_page_number, right_page.to_bytes())
        
        median_key = right_cells[0][0] 
        logger.debug(f"Splitting leaf page, median_key={median_key}, new_right_page_number={new_right_page_number}")
        return median_key, new_right_page_number
    
    @staticmethod
    def from_bytes(data: bytes) -> 'BTreePage':
        if all(b == 0 for b in data[:11]):
            logger.info("from_bytes called with empty page data, returning empty BTreePage")
            return BTreePage(is_leaf=True)  # Return an empty leaf page if the header is all zeros
        header = PageHeader.from_bytes(data[:11])
        is_leaf = (header.page_type == 0x0D)
        page = BTreePage(is_leaf=is_leaf)
        page.header = header
        offset = 11
        if is_leaf:
            for _ in range(header.num_keys):
                key = int.from_bytes(data[offset:offset + 2], 'big')
                value_length = int.from_bytes(data[offset + 2:offset + 4], 'big')
                value = data[offset + 4:offset + 4 + value_length]
                page.cells.append((key, value))
                offset += 4 + value_length
        else:
            page.children = []
            leftmost_child = int.from_bytes(data[offset:offset + 4], 'big')
            page.children.append(leftmost_child)
            offset += 4
            for _ in range(header.num_keys):
                key = int.from_bytes(data[offset:offset + 2], 'big')
                child_page_number = int.from_bytes(data[offset + 2:offset + 6], 'big')
                page.cells.append((key, child_page_number))
                page.children.append(child_page_number)
                offset += 6
        logger.info(f"Loaded page with {len(page.cells)} cells")
        return page  
    
    def update_leaf_cell(self, key, new_value):
        for idx, (k, _) in enumerate(self.cells):
            if k == key:
                self.cells[idx] = (key, new_value)
                logger.debug(f"Updated leaf cell: key={key}, new_value={new_value}")
                return True
        raise KeyError(f"Key {key} not found in leaf page")
    
    def delete_leaf_cell(self, key):
        for idx, (k, _) in enumerate(self.cells):
            if k == key:
                del self.cells[idx]
                self.header.num_keys -= 1
                logger.debug(f"Deleted leaf cell: key={key}")
                return True
        raise KeyError(f"Key {key} not found in leaf page")

class Pager:
    def __init__(self, filename: str):
        self.filename = filename
        file_exists = os.path.exists(filename)
        self.file = open(filename, 'r+b') if file_exists else open(filename, 'w+b')
        logger.info(f"Opened file for Pager: {filename}")
        if not file_exists:
            # Write initial root page number = 1
            self.file.seek(0)
            self.file.write((1).to_bytes(4, 'big'))
            self.file.flush()
            logger.info(f"Initialized new file with root page number 1: {filename}")

    def read_root_page_number(self) -> int:
        self.file.seek(0)
        data = self.file.read(4)
        if len(data) < 4:
            logger.warning(f"File too small for root page number, defaulting to 1")
            return 1
        root_page = int.from_bytes(data, 'big')
        logger.info(f"READ_ROOT_PAGE_NUMBER: {root_page}")
        return root_page

    def write_root_page_number(self, page_number: int):
        self.file.seek(0)
        self.file.write(page_number.to_bytes(4, 'big'))
        self.file.flush()
        logger.info(f"WRITE_ROOT_PAGE_NUMBER: {page_number}")

    def read_page(self, page_number: int) -> bytes:
        if page_number < 1:
            raise ValueError(f"Invalid page number: {page_number}")
        offset = ROOT_PAGE_HEADER_SIZE + (page_number - 1) * PAGE_SIZE
        self.file.seek(offset)
        data = self.file.read(PAGE_SIZE)
        if len(data) < PAGE_SIZE:
            # Pad with zeros if page is not fully written yet
            logger.debug(f"Read page {page_number}: padded with zeros to {PAGE_SIZE} bytes")
            data = data + b'\x00' * (PAGE_SIZE - len(data))
        else:
            logger.debug(f"Read page {page_number}: {len(data)} bytes")
        return data

    def write_page(self, page_number: int, data: bytes):
        import shutil
        dir_path = os.path.dirname(self.filename) or "."
        total, used, free = shutil.disk_usage(dir_path)
        logger.info(f"Before write: {free // (1024*1024)} MB free on {dir_path}")
        if len(data) > PAGE_SIZE:
            raise ValueError(f"Page data too large: {len(data)} > {PAGE_SIZE}")
        offset = ROOT_PAGE_HEADER_SIZE + (page_number - 1) * PAGE_SIZE
        self.file.seek(offset)
        self.file.write(data.ljust(PAGE_SIZE, b'\x00'))  # Pad with zeros if necessary
        self.file.flush()
        logger.info(f"Wrote page {page_number}: {len(data)} bytes")

    def allocate_page(self):
        self.file.seek(0, os.SEEK_END)
        file_size = self.file.tell()
        # Subtract 4 bytes for root page header
        if file_size < ROOT_PAGE_HEADER_SIZE:
            file_size = ROOT_PAGE_HEADER_SIZE
        num_pages = (file_size - ROOT_PAGE_HEADER_SIZE) // PAGE_SIZE
        new_page_number = num_pages + 1
        logger.info(f"Allocating new page: {new_page_number}")
        return new_page_number

    def close(self):
        self.file.flush()
        os.fsync(self.file.fileno())
        self.file.close()
        logger.info(f"Closed Pager file: {self.filename}")