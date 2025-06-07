from backend.pager import Pager, BTreePage, PageHeader

class Table:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.filename = f"{table_name}.tbl"
        self.pager = Pager(self.filename)

    def load_root_page(self) -> BTreePage:
        raw = self.pager.read_page(1)
        if all(b == 0 for b in raw[:11]):
            return BTreePage(is_leaf=True)
        return BTreePage.from_bytes(raw)

    def save_root_page(self, page: BTreePage):
        self.pager.write_page(1, page.to_bytes())

    def close(self):
        self.pager.close()
