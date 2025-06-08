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

    def save_root_page(self, page: BTreePage):
        logger.debug(f"Saving root page with {len(page.cells)} cells")
        try:
            self.pager.write_page(1, page.to_bytes())
            logger.info(f"Root page saved successfully for table '{self.table_name}'")
        except Exception as e:
            logger.error(f"Error saving root page for table '{self.table_name}': {e}")
            raise

    def load_root_page(self) -> BTreePage:
        try:
            raw = self.pager.read_page(1)
            logger.debug(f"Loading root page, first 11 bytes: {list(raw[:11])}")
            if all(b == 0 for b in raw[:11]):
                logger.info("Page is empty, returning new leaf page")
                return BTreePage(is_leaf=True)
            logger.debug("Page is not empty, parsing from bytes")
            return BTreePage.from_bytes(raw)
        except Exception as e:
            logger.error(f"Error loading root page for table '{self.table_name}': {e}")
            raise

    def close(self):
        logger.info(f"Closing table '{self.table_name}'")
        try:
            self.pager.close()
            logger.debug(f"Pager closed for file: {self.filename}")
        except Exception as e:
            logger.error(f"Error closing pager for table '{self.table_name}': {e}")
            raise