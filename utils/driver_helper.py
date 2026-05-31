from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, Playwright


class DriverHelper:
    """
    Equivalent of Java's DriverHelper.java
    Lazy-initialises a single browser instance; reuses it if already open.
    """
    _playwright: Playwright = None
    _browser: Browser = None
    _context: BrowserContext = None
    _page: Page = None

    @classmethod
    def get_page(cls) -> Page:
        if cls._page is None:
            cls._playwright = sync_playwright().start()
            cls._browser = cls._playwright.chromium.launch(headless=False)
            cls._context = cls._browser.new_context(viewport={"width": 1920, "height": 1080})
            cls._page = cls._context.new_page()
        return cls._page

    @classmethod
    def quit_driver(cls):
        if cls._page:
            cls._page.close()
            cls._page = None
        if cls._context:
            cls._context.close()
            cls._context = None
        if cls._browser:
            cls._browser.close()
            cls._browser = None
        if cls._playwright:
            cls._playwright.stop()
            cls._playwright = None
