from playwright.sync_api import Page


class SearchPage:
    """Equivalent of Java's SearchPage.java"""

    def __init__(self, page: Page):
        self.page = page
        self.search_box = page.locator("#small-searchterms")
        self.search_btn = page.locator("input[value='Search']")

    def search_item(self, item: str):
        self.search_box.fill(item)
        self.search_btn.click()
