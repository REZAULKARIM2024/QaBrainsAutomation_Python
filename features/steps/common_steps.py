"""
Equivalent of Java's CommonSteps.java
Shared steps used across multiple feature files.
"""
from behave import given, then, step
from utils.base_test import BaseTest


def _page(context):
    return BaseTest.get_page()


@given("User launches the application")
def user_launches_the_application(context):
    page = _page(context)
    assert "practice.qabrains.com" in page.url, f"❌ App did not launch. URL: {page.url}"


@then("Home page should load successfully")
def home_page_should_load_successfully(context):
    page = _page(context)
    page.wait_for_load_state()
    assert "practice.qabrains.com" in page.url, f"❌ Home page did not load. URL: {page.url}"


@step("User is on homepage")
def user_is_on_homepage(context):
    page = _page(context)
    base = "https://practice.qabrains.com"
    if page.url.rstrip('/') != base:
        page.goto(base + "/")
    page.wait_for_load_state()


@then("Products should be added successfully")
def products_should_be_added_successfully(context):
    page = _page(context)
    cart_has_items = (
        page.locator(".cart-count, .cart-badge, .cart-item, [class*='cart']").count() > 0
    )
    assert cart_has_items, "❌ No products found in cart after adding"
