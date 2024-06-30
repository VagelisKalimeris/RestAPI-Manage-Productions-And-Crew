class PaginationResult:
    """
    Response template for pagination results.
    """
    def __init__(self, total_records: int, current_page: int, total_pages: int):
        self.total_records = total_records
        self.current_page = current_page
        self.total_pages = total_pages