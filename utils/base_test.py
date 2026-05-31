from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, Playwright


class BaseTest:
    """
    Equivalent of Java's BaseTest.java
    Manages a single static browser/page instance for all scenarios.
    """
    _playwright: Playwright = None
    _browser: Browser = None
    _context: BrowserContext = None
    _page: Page = None

    @classmethod
    def init_browser(cls):
        """🚀 Start browser — called from environment.py before_scenario"""
        cls._playwright = sync_playwright().start()
        cls._browser = cls._playwright.chromium.launch(headless=False)
        cls._context = cls._browser.new_context()
        cls._page = cls._context.new_page()
        cls._page.goto("https://practice.qabrains.com/")

    @classmethod
    def get_page(cls) -> Page:
        """📌 Get current Page instance"""
        return cls._page

    @classmethod
    def quit_browser(cls):
        """❌ Close browser — called from environment.py after_scenario"""
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
