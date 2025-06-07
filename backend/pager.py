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

PAGE_SIZE = 4096  # Size of a B-Tree page in bytes

class PageHeader:
    def __init__(self, page_type: int, num_keys: int = 0, free_start:int = 0, right_sibling: int=0):
        self.page_type = page_type
        self.num_keys = num_keys
        self.free_start = free_start
        self.right_sibling = right_sibling
        
    def to_bytes(self) -> bytes:
        """
        This method converts the PageHeader instance to a byte representation.
        The byte order is little-endian, and the fields are packed as follows:
        - page_type: 1 byte
        - num_keys: 2 bytes
        - free_start: 4 bytes
        - right_sibling: 4 bytes
        The total size of the byte representation is 11 bytes.
        """
        return (
                self.page_type.to_bytes(1, 'big') + # This is a flag to identify the type of page 0x0d(13) for leaf node, 0x05(5) for internal node
                self.num_keys.to_bytes(2, 'big') + # Number of keys (entries) stored in the page
                self.free_start.to_bytes(4, 'big') + # Offset (byte position) where the free space starts for appending new entries.
                self.right_sibling.to_bytes(4, 'big') # Pointer to the next page (only used in leaf nodes).
                )
        
    @staticmethod
    def from_bytes(data: bytes) -> 'PageHeader':
        """
        This static method creates a PageHeader instance from a byte representation.
        """
        if len(data) < 11:
            raise ValueError(f"Data must be at least 11 bytes long, got {len(data)} bytes")
        return PageHeader(
            page_type=data[0],
            num_keys=int.from_bytes(data[1:3], 'big'),
            free_start=int.from_bytes(data[3:7], 'big'),
            right_sibling=int.from_bytes(data[7:11], 'big')
            )
            
class BTreePage:
    def __init__(self, is_leaf: bool):
        self.header = PageHeader(page_type=0x0D if is_leaf else 0x05)
        self.cells: List[Tuple[int, Union[bytes, int]]] = []  # List of tuples (key, value) for leaf nodes or (key, child_page_number) for internal nodes or page_ptr
        
    def add_leaf_cell(self, key: int, value: bytes):
        """
        Adds a cell to a leaf page.
        """
        if self.header.page_type != 0x0D:
            raise ValueError("Cannot add leaf cell to non-leaf page")
        self.cells.append((key, value))
        self.header.num_keys += 1
        
    def add_internal_cell(self, key: int, child_page_number: int):
        """
        Adds a cell to an internal page.
        """
        if self.header.page_type != 0x05:
            raise ValueError("Cannot add internal cell to leaf page")
        self.cells.append((key, child_page_number))
        self.header.num_keys += 1
        
    def to_bytes(self) -> bytes:
        content = b"".join(
            key.to_bytes(2, 'big') +
            len(value).to_bytes(2, 'big') +
            value for key, value in self.cells
        )
        self.header.free_start = len(self.header.to_bytes()) + len(content)
        return self.header.to_bytes() + content
    
    @staticmethod
    def from_bytes(data: bytes) -> 'BTreePage':
        header = PageHeader.from_bytes(data[:11])
        page = BTreePage(is_leaf=(header.page_type == 0x0D))
        page.header = header
        offset = 11
        for _ in range(header.num_keys):
            key = int.from_bytes(data[offset:offset + 2], 'big')
            value_length = int.from_bytes(data[offset + 2:offset + 4], 'big')
            value = data[offset + 4:offset + 4 + value_length]
            page.cells.append((key, value))
            offset += 4 + value_length
        return page
    
class Pager:
    def __init__(self, filename: str):
        self.filename = filename
        self.file = open(filename, 'r+b') if os.path.exists(filename) else open(filename, 'w+b')
        
    def read_page(self, page_number: int) -> bytes:
        self.file.seek((page_number -1) * PAGE_SIZE) # Seek to the start of the page
        data = self.file.read(PAGE_SIZE)
        if len(data) < PAGE_SIZE:
            data += b'\x00' * (PAGE_SIZE - len(data))  # Pad with zeros if necessary
        return data
    
    def write_page(self, page_number: int, data: bytes):
        if len(data) > PAGE_SIZE:
            raise ValueError("Data exceeds page size")
        self.file.seek((page_number - 1) * PAGE_SIZE)
        self.file.write(data.ljust(PAGE_SIZE, b'\x00'))  # Pad with zeros if necessary
        
    def close(self):
        self.file.flush()
        self.file.close()



