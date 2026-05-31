from playwright.sync_api import Page


class LogoutPage:

    def __init__(self, page: Page):
        self.page = page

    def click_logout(self):
        self.page.wait_for_timeout(2000)
        print(f"ℹ️  Looking for logout. URL: {self.page.url}")

        # Step 1: Try direct logout URL (most reliable)
        logout_urls = [
            "https://practice.qabrains.com/logout",
            "https://practice.qabrains.com/signout",
            "https://practice.qabrains.com/sign-out",
            "https://practice.qabrains.com/auth/logout",
        ]

        # Step 2: Try opening dropdown/user menu first
        dropdown_selectors = [
            "[class*='user-menu']",
            "[class*='account-menu']",
            "[class*='profile']",
            "[class*='avatar']",
            "[class*='user-icon']",
            "[class*='nav-user']",
            "button:has-text('Account')",
            "button:has-text('My Account')",
            ".header-account",
            "[data-toggle='dropdown']",
        ]
        for sel in dropdown_selectors:
            try:
                el = self.page.locator(sel).first
                if el.is_visible():
                    print(f"✅ Opening user dropdown: {sel}")
                    el.click()
                    self.page.wait_for_timeout(800)
                    break
            except Exception:
                pass

        # Step 3: Find logout button/link
        logout_selectors = [
            "a:has-text('Logout')",
            "a:has-text('Log Out')",
            "a:has-text('Log out')",
            "a:has-text('Sign Out')",
            "a:has-text('Sign out')",
            "button:has-text('Logout')",
            "button:has-text('Log Out')",
            "[href*='logout']",
            "[href*='log-out']",
            "[href*='sign-out']",
            "[href*='signout']",
            "[data-action='logout']",
            "[class*='logout']",
        ]
        for sel in logout_selectors:
            try:
                btn = self.page.locator(sel).first
                if btn.is_visible():
                    print(f"✅ Logout button via: {sel}")
                    btn.click()
                    self.page.wait_for_load_state()
                    self.page.wait_for_timeout(2000)
                    return
            except Exception:
                pass

        # Step 4: Try direct logout URLs as last resort
        print("ℹ️  Trying direct logout URLs...")
        for url in logout_urls:
            try:
                self.page.goto(url)
                self.page.wait_for_load_state()
                self.page.wait_for_timeout(1500)
                # Check if we got redirected (= logout worked)
                if self.page.url != url:
                    print(f"✅ Logout via direct URL: {url}")
                    return
            except Exception:
                pass

        # Debug: print all links
        print("❌ Logout not found. All links on page:")
        for el in self.page.locator("a, button").all():
            try:
                txt = el.text_content().strip()
                href = el.get_attribute("href") or ""
                cls = el.get_attribute("class") or ""
                if txt:
                    print(f"   → '{txt}' href='{href}' class='{cls[:50]}'")
            except Exception:
                pass

        try:
            self.page.screenshot(path="reports/screenshots/logout_debug.png", full_page=True)
            print("📸 Saved logout_debug.png")
        except Exception:
            pass

        # Check if user is actually logged in
        has_login_form = self.page.locator(
            "button.btn-submit, button:has-text('Login')"
        ).count() > 0

        if has_login_form:
            raise RuntimeError(
                "❌ User is NOT logged in — credentials may be wrong. "
                "Check: qa_testers@qabrains.com / Password123. "
                "See reports/screenshots/logout_debug.png"
            )
        raise RuntimeError(
            "❌ Logged in but logout button not found. "
            "See reports/screenshots/logout_debug.png for page state."
        )

    def is_logout_successful(self) -> bool:
        self.page.wait_for_timeout(1000)
        url = self.page.url

        # Login form reappeared = logged out
        has_login = self.page.locator(
            "button.btn-submit, button:has-text('Login'), a[href*='auth/login']"
        ).count() > 0

        # No logout elements = logged out
        no_logout = self.page.locator(
            "a:has-text('Logout'), [href*='logout'], [href*='sign-out']"
        ).count() == 0

        on_public = 'login' in url or url.rstrip('/') == "https://practice.qabrains.com"

        print(f"Logout check → URL={url} | hasLoginBtn={has_login} | noLogout={no_logout}")
        return has_login or no_logout or on_public
