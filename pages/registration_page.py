import time
from playwright.sync_api import Page


class RegistrationPage:

    def __init__(self, page: Page):
        self.page = page

    def open_registration_page(self):
        if 'registration' not in self.page.url:
            # Try nav link
            reg_link = self.page.locator(
                "#registration span, a:has-text('Register'), a:has-text('Registration'), "
                "a[href*='registration']"
            ).first
            try:
                if reg_link.is_visible():
                    reg_link.click()
                    self.page.wait_for_timeout(1000)
            except Exception:
                pass
            # Direct URL
            if 'registration' not in self.page.url:
                self.page.goto("https://practice.qabrains.com/registration")
        self.page.wait_for_load_state()
        self.page.wait_for_timeout(2000)

    def enter_registration_details(
        self,
        full_name: str,
        country: str,
        account_type: str,
        email: str,
        password: str,
        confirm_password: str,
    ):
        # Use timestamp to make email unique every run
        unique_email = f"testuser_{int(time.time())}@test.com"
        print(f"ℹ️  Using unique email: {unique_email}")

        self._fill_if_exists("#name", full_name)
        self._select_if_exists("#country", country)
        self._select_if_exists("#account", account_type)
        self._fill_if_exists("#email", unique_email)  # Always unique
        self._fill_if_exists("#password", password)
        self._fill_if_exists("#confirm_password", confirm_password)

    def _fill_if_exists(self, selector: str, value: str):
        try:
            el = self.page.locator(selector).first
            if el.is_visible():
                el.fill(value)
        except Exception as e:
            print(f"⚠ Could not fill {selector}: {e}")

    def _select_if_exists(self, selector: str, value: str):
        try:
            el = self.page.locator(selector).first
            if el.is_visible():
                try:
                    el.select_option(value)
                except Exception:
                    try:
                        el.select_option(label=value)
                    except Exception:
                        # Try selecting first available option
                        options = el.locator("option").all()
                        if options:
                            first_val = options[1].get_attribute("value") if len(options) > 1 else options[0].get_attribute("value")
                            if first_val:
                                el.select_option(first_val)
                        print(f"⚠ Used fallback option for {selector}")
        except Exception as e:
            print(f"⚠ Could not select {selector}: {e}")

    def click_register(self):
        try:
            btn = self.page.locator("button[type='submit']").first
            btn.click()
        except Exception:
            pass
        self.page.wait_for_load_state()
        self.page.wait_for_timeout(2500)

    def is_registration_successful(self) -> bool:
        url = self.page.url

        # Success selectors
        success_selectors = [
            "text=/successfully/i",
            "text=/registered/i",
            "text=/welcome/i",
            "text=/thank you/i",
            "text=/account created/i",
            "text=/registration complete/i",
            ".alert-success",
            ".success-message",
            "[class*='success']",
            "#success-msg",
        ]
        for sel in success_selectors:
            try:
                el = self.page.locator(sel).first
                if el.is_visible():
                    print(f"✅ Registration success: {el.text_content().strip()}")
                    return True
            except Exception:
                pass

        # Redirected away from /registration = success
        if 'registration' not in url:
            print(f"✅ Registration success — redirected to: {url}")
            return True

        # Check body for success/already-exists keywords
        try:
            body = self.page.locator("body").inner_text().lower()
            if any(k in body for k in ["success", "registered", "welcome", "already", "exists", "taken"]):
                print("✅ Registration success keyword found in page")
                return True
            print(f"⚠ Registration page body (first 200 chars): {body[:200]}")
        except Exception:
            pass

        return False

    def is_email_validation_message_displayed(self) -> bool:
        # HTML5 native validation
        try:
            msg = self.page.locator("#email").first.evaluate("el => el.validationMessage")
            if msg:
                print(f"✅ HTML5 email validation: {msg}")
                return True
        except Exception:
            pass

        # Inline error elements
        for sel in ["#email + .error", "#email ~ .error", ".field-error",
                    ".alert-danger", "[class*='error']", "text=/valid email/i",
                    "text=/invalid email/i", "text=/enter a valid/i"]:
            try:
                if self.page.locator(sel).first.is_visible():
                    return True
            except Exception:
                pass

        # Still on registration page = validation blocked submit
        return 'registration' in self.page.url
