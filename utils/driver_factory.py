import threading
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, Playwright


class DriverFactory:
    """
    Thread-local equivalent of Java's DriverFactory.java
    Each thread gets its own Playwright / Browser / Page.
    """
    _local = threading.local()

    @classmethod
    def get_page(cls) -> Page:
        return getattr(cls._local, 'page', None)

    @classmethod
    def init_driver(cls):
        cls._local.playwright = sync_playwright().start()
        cls._local.browser = cls._local.playwright.chromium.launch(headless=False)
        cls._local.context = cls._local.browser.new_context()
        cls._local.page = cls._local.context.new_page()
        cls._local.page.goto("https://practice.qabrains.com/")

    @classmethod
    def quit_driver(cls):
        page: Page = getattr(cls._local, 'page', None)
        context: BrowserContext = getattr(cls._local, 'context', None)
        browser: Browser = getattr(cls._local, 'browser', None)
        playwright: Playwright = getattr(cls._local, 'playwright', None)

        if page:
            page.close()
            cls._local.page = None
        if context:
            context.close()
            cls._local.context = None
        if browser:
            browser.close()
            cls._local.browser = None
        if playwright:
            playwright.stop()
            cls._local.playwright = None
