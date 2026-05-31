"""
Behave lifecycle hooks — equivalent of Java Hooks.java
Senior QA approach: screenshot on failure, proper browser setup
"""
import sys
import os
import base64

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.base_test import BaseTest


def before_all(context, ):
    os.makedirs("reports/screenshots", exist_ok=True)


def before_scenario(context, scenario):
    BaseTest.init_browser()
    context.page = BaseTest.get_page()
    # Clear scenario-level page objects so they're recreated fresh
    for attr in ['login_page', 'logout_page', 'cart_page', 'registration_page',
                 'forgot_password_page']:
        if hasattr(context, attr):
            delattr(context, attr)


def after_step(context, step):
    """Take screenshot on every failed step."""
    if step.status == 'failed':
        try:
            page = BaseTest.get_page()
            if page:
                name = f"{context.scenario.name} - {step.name}".replace('/', '_')[:80]
                path = f"reports/screenshots/{name}.png"
                page.screenshot(path=path, full_page=True)
                print(f"📸 Screenshot saved: {path}")
        except Exception as e:
            print(f"⚠ Screenshot failed: {e}")


def after_scenario(context, scenario):
    BaseTest.quit_browser()
