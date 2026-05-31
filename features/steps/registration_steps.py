"""Equivalent of Java's RegistrationSteps.java"""
from behave import when, then
from pages.registration_page import RegistrationPage
from utils.base_test import BaseTest


def _reg_page(context):
    if not hasattr(context, 'registration_page'):
        context.registration_page = RegistrationPage(BaseTest.get_page())
    return context.registration_page


@when("User navigates to registration page")
def user_navigates_to_registration_page(context):
    _reg_page(context).open_registration_page()


@when('User enters valid registration details with email "{email}"')
def user_enters_valid_registration_details_with_email(context, email):
    _reg_page(context).enter_registration_details(
        "Ranajit Chowdhury", "United States", "Engineer",
        email, "Password123", "Password123"
    )


@when('User enters registration details with email "{email}"')
def user_enters_registration_details_with_email(context, email):
    _reg_page(context).enter_registration_details(
        "Ranajit Chowdhury", "United States", "Engineer",
        email, "Password123", "Password123"
    )


@when("User clicks on register button")
def user_clicks_on_register_button(context):
    _reg_page(context).click_register()


@then("User should be registered successfully")
def user_should_be_registered_successfully(context):
    assert _reg_page(context).is_registration_successful(), "❌ Registration failed!"


@then("Email validation error message should be displayed")
def email_validation_error_message_should_be_displayed(context):
    assert _reg_page(context).is_email_validation_message_displayed(), \
        "❌ Email validation error not shown!"
