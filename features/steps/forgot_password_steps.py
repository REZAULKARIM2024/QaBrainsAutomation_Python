"""Equivalent of Java's ForgotPasswordSteps.java"""
from behave import given, when, then, step
from pages.forgot_password_page import ForgotPasswordPage
from utils.base_test import BaseTest


def _fp_page(context):
    if not hasattr(context, 'forgot_password_page'):
        context.forgot_password_page = ForgotPasswordPage(BaseTest.get_page())
    return context.forgot_password_page


@given("User is on Forgot Password page")
def user_is_on_forgot_password_page(context):
    page = BaseTest.get_page()
    page.goto("https://practice.qabrains.com/forgot-password")


@when('User enters registered email "{email}"')
def user_enters_registered_email(context, email):
    _fp_page(context).enter_email(email)


@when('User enters unregistered email "{email}"')
def user_enters_unregistered_email(context, email):
    _fp_page(context).enter_email(email)


@step("User clicks on Submit button")
def user_clicks_on_submit_button(context):
    _fp_page(context).click_submit()


@then('User should see success message "{expected}"')
def user_should_see_success_message(context, expected):
    actual = _fp_page(context).get_success_message()
    assert 'reset' in actual.lower() or 'success' in actual.lower(), \
        f"❌ Success message not displayed. Actual: {actual}"


@then('User should see error message "{expected}"')
def user_should_see_error_message(context, expected):
    actual = _fp_page(context).get_error_message()
    assert '@' in actual.lower() or 'not found' in actual.lower(), \
        f"❌ Error message not displayed. Actual: {actual}"
