"""Equivalent of Java's LogoutSteps.java"""
from behave import given, when, then
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from utils.base_test import BaseTest


def _pages(context):
    page = BaseTest.get_page()
    if not hasattr(context, 'login_page'):
        context.login_page = LoginPage(page)
    if not hasattr(context, 'logout_page'):
        context.logout_page = LogoutPage(page)


@given("User is logged in")
def login_first(context):
    _pages(context)
    context.login_page.login("qa_testers@qabrains.com", "Password123")
    assert context.login_page.is_login_successful(), "❌ Pre-condition login failed!"


@when("User clicks on logout button")
def logout(context):
    _pages(context)
    context.logout_page.click_logout()


@then("User should be logged out successfully")
def verify_logout(context):
    _pages(context)
    assert context.logout_page.is_logout_successful(), "❌ Logout failed!"
