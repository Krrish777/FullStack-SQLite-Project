import json
from backend.table import Table
from backend.row_codec import encode_row, decode_row
from utils.logger import get_logger

logger = get_logger(__name__)

CATALOG_TABLE = "__catalog"
CATALOG_SCHEMA = [
    ("table_name", "TEXT"),
    ("root_page", "INT"),
    ("columns", "TEXT"),  # JSON-encoded list of (name, type)
]

class Catalog:
    def __init__(self):
        self.table_schemas = {}  # table_name -> {columns: [(name, type)], root_page: int}
        self._ensure_catalog_table()
        self.load()

    def _ensure_catalog_table(self):
        # Create catalog table if it doesn't exist
        tbl = Table(CATALOG_TABLE)
        if tbl.root_page_num == 1 and not any(True for _ in tbl.scan_page(tbl.root_page_num)):
            # Insert the catalog's own schema as the first row
            row = {
                "table_name": CATALOG_TABLE,
                "root_page": 1,
                "columns": json.dumps(CATALOG_SCHEMA),
            }
            tbl.insert(1, encode_row(row))
            tbl.save_root_page(tbl.load_root_page())
            logger.info("Bootstrapped __catalog table.")
        tbl.close()

    def load(self):
        self.table_schemas = {}
        tbl = Table(CATALOG_TABLE)
        for _, value in tbl.scan_page(tbl.root_page_num):
            if not value or value.strip() == b'':
                continue
            try:
                row = decode_row(value)
            except ValueError as e:
                logger.error(f"Failed to decode row in catalog: {e}")
                continue
            self.table_schemas[row["table_name"]] = json.loads(row["columns"])
            tbl.close()
            logger.info(f"Loaded schema for table '{row['table_name']}' from catalog.")

    def create_table(self, table_name, columns, root_page):
        tbl = Table(CATALOG_TABLE)
        # Find next available key
        max_id = 0
        for key, _ in tbl.scan_page(tbl.root_page_num):
            max_id = max(max_id, key)
        row = {
            "table_name": table_name,
            "root_page": root_page,
            "columns": json.dumps(columns),
        }
        tbl.insert(max_id + 1, encode_row(row))
        tbl.save_root_page(tbl.load_root_page())
        tbl.close()
        self.load()
        logger.info(f"Added table '{table_name}' to catalog.")
        
    def drop_table(self, table_name):
        tbl = Table(CATALOG_TABLE)
        rows = []
        for key, value in tbl.scan_page(tbl.root_page_num):
            if not value or value.strip() == b'':
                continue
            try:
                row = decode_row(value)
            except ValueError as e:
                logger.error(f"Failed to decode row in catalog: {e}")
                continue
            if row.get("table_name") != table_name:
                rows.append((key, value))
        # Clear the catalog table
        root_page = tbl.load_root_page()
        root_page.cells = []
        tbl.save_root_page(root_page)
        # Re-insert only the rows for tables not being dropped
        for idx, (key, value) in enumerate(rows, 1):
            tbl.insert(idx, value)
        tbl.close()
        self.load()

    def get_schema(self, table_name):
        return self.table_schemas.get(table_name, None)
