from playwright.sync_api import Page


class HomePage:
    """Equivalent of Java's HomePage.java"""

    def __init__(self, page: Page):
        self.page = page
        self.home_header = page.locator("header")
        self.catalog_link = page.locator("a[href*='catalog']")
        self.about_link = page.locator("a[href*='about']")
        self.blog_link = page.locator("a[href*='blog']")
        self.wish_list_link = page.locator("a[href*='wishlist']")
        self.refer_friend_link = page.locator("a[href*='refer']")
        self.search_box = page.locator("[name='q']")
        self.search_button = page.locator("button[type='submit']")
        self.no_result_message = page.locator("text=No results, text=no products")

    def click_catalog(self):
        self.catalog_link.click()

    def click_about(self):
        self.about_link.click()

    def click_blog(self):
        self.blog_link.click()

    def click_wish_list(self):
        self.wish_list_link.click()

    def click_refer_friend(self):
        self.refer_friend_link.click()

    def enter_search_text(self, text: str):
        self.search_box.fill(text)

    def click_search_button(self):
        self.search_button.click()

    def is_home_page_displayed(self) -> bool:
        return self.home_header.is_visible()

    def is_no_result_displayed(self) -> bool:
        return self.no_result_message.first.is_visible()
