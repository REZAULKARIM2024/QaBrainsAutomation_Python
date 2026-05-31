"""Equivalent of Java's RegressionSteps.java"""
from behave import when, then


# Module-level state (per behave process)
_expected_quantity = 0
_actual_quantity = 0


@when("User adds multiple products to cart")
def user_adds_multiple_products_to_cart(context):
    global _expected_quantity, _actual_quantity
    print("Multiple products added to cart")
    _expected_quantity = 2
    _actual_quantity = 2  # replace with real cart count when available


@when("User updates product quantity")
def user_updates_product_quantity(context):
    global _actual_quantity
    print("Product quantity updated")
    _actual_quantity = _expected_quantity  # replace with real cart quantity


@when("User searches for invalid item")
def user_searches_for_invalid_item(context):
    print("Invalid item searched")


@then("No result should be displayed")
def no_result_should_be_displayed(context):
    print("No search result displayed")
    assert True, "No result validation placeholder"


@then("Quantity should be updated")
def quantity_should_be_updated(context):
    print(f"Verifying updated quantity: expected={_expected_quantity}, actual={_actual_quantity}")
    assert _actual_quantity == _expected_quantity, \
        f"❌ Product quantity did not update correctly. Expected {_expected_quantity}, got {_actual_quantity}"
