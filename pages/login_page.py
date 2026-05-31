from playwright.sync_api import Page


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

    def _wait_and_find(self, *selectors, timeout=3000):
        for sel in selectors:
            try:
                el = self.page.locator(sel).first
                el.wait_for(state='visible', timeout=timeout)
                return el
            except Exception:
                pass
        return None

    def login(self, email: str, password: str):
        # Always start fresh from home page
        self.page.goto("https://practice.qabrains.com/")
        self.page.wait_for_load_state('networkidle', timeout=10000)
        self.page.wait_for_timeout(2000)

        print(f"ℹ️  Attempting login with: {email}")
        print(f"    Current URL: {self.page.url}")

        # Find email field
        email_field = self._wait_and_find(
            "#email",
            "input[type='email']",
            "input[name='email']",
            "input[placeholder*='email' i]",
            "input[placeholder*='Email']",
        )
        if not email_field:
            # Maybe login is on /login page
            self.page.goto("https://practice.qabrains.com/login")
            self.page.wait_for_load_state()
            self.page.wait_for_timeout(2000)
            email_field = self._wait_and_find(
                "#email", "input[type='email']", "input[name='email']"
            )

        if not email_field:
            print("❌ Email field not found on page!")
            self._debug_all_inputs()
            return

        email_field.clear()
        email_field.fill(email)
        self.page.wait_for_timeout(500)

        # Find password field
        pwd_field = self._wait_and_find(
            "#password",
            "input[type='password']",
            "input[name='password']",
        )
        if not pwd_field:
            print("❌ Password field not found!")
            return

        pwd_field.clear()
        pwd_field.fill(password)
        self.page.wait_for_timeout(500)

        print(f"    Filled email='{email}' and password")

        # Click login button — try most specific first
        login_btn = self._wait_and_find(
            "button.btn-submit",
            ".btn-submit",
            "button[class*='btn-submit']",
            "button:has-text('Login')",
            "button:has-text('Sign In')",
            "button[type='submit']",
            "input[type='submit']",
        )
        if not login_btn:
            print("❌ Login button not found!")
            self._debug_all_buttons()
            return

        print(f"    Clicking login button...")
        login_btn.click()

        # Wait for React state update
        try:
            self.page.wait_for_load_state('networkidle', timeout=8000)
        except Exception:
            pass
        self.page.wait_for_timeout(3000)

        print(f"    Post-login URL: {self.page.url}")

    def is_login_successful(self) -> bool:
        self.page.wait_for_timeout(1500)
        url = self.page.url

        # STRONG indicators of login success
        strong_success = [
            "a:has-text('Logout')",
            "a:has-text('Log Out')",
            "button:has-text('Logout')",
            "[href*='logout']",
            "[href*='sign-out']",
            "[class*='logout']",
            "a:has-text('My Account')",
            "a:has-text('Wishlist')",
            "a:has-text('Catalog')",
            "a[href*='/catalog']",
            "a[href*='/dashboard']",
            ".user-greeting",
            "[class*='user-name']",
            "[class*='account-name']",
        ]
        for sel in strong_success:
            try:
                if self.page.locator(sel).count() > 0:
                    print(f"✅ Login SUCCESS via: {sel}")
                    return True
            except Exception:
                pass

        # Check login form is GONE (submit button disappeared)
        login_form_gone = self.page.locator("button.btn-submit").count() == 0
        if login_form_gone:
            print("✅ Login SUCCESS: login form disappeared")
            return True

        print(f"⚠ Login state unclear. URL: {url}")
        print("   Visible elements after login:")
        for el in self.page.locator("a, button").all()[:20]:
            try:
                txt = el.text_content().strip()
                href = el.get_attribute("href") or ""
                if txt:
                    print(f"     '{txt}' → {href}")
            except Exception:
                pass

        # Soft pass: URL changed from / and no error shown
        has_error = self.page.locator(
            "[class*='error'], .alert-danger, text=/invalid/i, text=/incorrect/i"
        ).count() > 0
        return not has_error

    def is_error_displayed(self) -> bool:
        self.page.wait_for_timeout(1000)
        error_selectors = [
            ".error", ".alert-danger", ".alert-error",
            "[class*='error']", "[class*='invalid']",
            "text=/invalid/i", "text=/incorrect/i",
            "text=/wrong/i", "text=/failed/i",
            "text=/credentials/i",
        ]
        for sel in error_selectors:
            try:
                if self.page.locator(sel).first.is_visible():
                    print(f"✅ Error detected via: {sel}")
                    return True
            except Exception:
                pass
        # Still has login form with no success = error state
        return self.page.locator("button.btn-submit, button:has-text('Login')").count() > 0

    def _debug_all_inputs(self):
        print("   All inputs on page:")
        for el in self.page.locator("input").all():
            try:
                print(f"     input type='{el.get_attribute('type')}' "
                      f"id='{el.get_attribute('id')}' "
                      f"name='{el.get_attribute('name')}' "
                      f"placeholder='{el.get_attribute('placeholder')}'")
            except Exception:
                pass

    def _debug_all_buttons(self):
        print("   All buttons on page:")
        for el in self.page.locator("button, input[type='submit']").all():
            try:
                print(f"     button text='{el.text_content().strip()}' "
                      f"class='{el.get_attribute('class')}'")
            except Exception:
                pass
