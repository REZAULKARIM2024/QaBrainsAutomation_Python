"""Equivalent of Java's LoginSteps.java"""
from behave import when, then
from pages.login_page import LoginPage
from utils.base_test import BaseTest


def _login_page(context):
    if not hasattr(context, 'login_page'):
        context.login_page = LoginPage(BaseTest.get_page())
    return context.login_page


@when("User enters valid username and password")
def login_valid(context):
    _login_page(context).login("qa_testers@qabrains.com", "Password123")


@when("User enters invalid username and password")
def login_invalid(context):
    _login_page(context).login("wrong@test.com", "wrongpass")


@then("User should be logged in successfully")
def verify_login(context):
    assert _login_page(context).is_login_successful(), "❌ Login failed!"


@then("Error message should be displayed")
def verify_error(context):
    assert _login_page(context).is_error_displayed(), "❌ Error message not displayed!"
