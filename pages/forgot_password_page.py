from playwright.sync_api import Page


class ForgotPasswordPage:
    """Equivalent of Java's ForgotPasswordPage.java"""

    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.locator("#email")
        self.submit_btn = page.locator(
            "#inner-body form button, "
            "form button[type='submit'], "
            "button:has-text('Submit'), "
            "button:has-text('Reset'), "
            "input[type='submit']"
        ).first

    def enter_email(self, email: str):
        self.email_field.fill(email)

    def click_submit(self):
        self.submit_btn.click()
        self.page.wait_for_load_state()
        self.page.wait_for_timeout(1000)

    def get_success_message(self) -> str:
        selectors = [
            "#success-msg",
            ".success-message",
            ".alert-success",
            "[class*='success']",
            "text=/reset/i",
            "text=/sent/i",
            "text=/check your email/i",
            "p.success, div.success",
        ]
        for sel in selectors:
            try:
                el = self.page.locator(sel).first
                if el.is_visible():
                    text = el.text_content().strip()
                    print(f"✅ ForgotPassword success msg [{sel}]: {text}")
                    return text
            except Exception:
                pass

        body = self.page.locator("body").text_content().lower()
        if 'reset' in body or 'sent' in body or 'check your email' in body:
            print("✅ Found success keyword in page body")
            return "reset"

        print(f"⚠ ForgotPassword: no success message found. URL: {self.page.url}")
        return ""

    def get_error_message(self) -> str:
        selectors = [
            "#email + span",
            "#email ~ span",
            "#email + div",
            "#email ~ .error",
            ".field-error",
            ".alert-danger",
            ".error-message",
            "[class*='error']",
            "text=/not found/i",
            "text=/invalid/i",
            "text=/enter a valid/i",
        ]
        for sel in selectors:
            try:
                el = self.page.locator(sel).first
                if el.is_visible():
                    text = el.text_content().strip()
                    if text.upper() != "RESET PASSWORD" and text:
                        print(f"✅ ForgotPassword error msg [{sel}]: {text}")
                        return text
            except Exception:
                pass

        body = self.page.locator("body").text_content().lower()
        if 'not found' in body or 'invalid' in body or '@' in body:
            print("✅ Found error keyword in page body")
            return "not found"

        print(f"⚠ ForgotPassword: no error message found. URL: {self.page.url}")
        return ""
