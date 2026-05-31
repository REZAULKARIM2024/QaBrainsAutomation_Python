"""Equivalent of Java's CartSteps.java"""
from behave import when, then
from pages.cart_page import CartPage
from utils.base_test import BaseTest


def _cart_page(context):
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(BaseTest.get_page())
    return context.cart_page


@when("User adds products to cart")
def user_adds_products_to_cart(context):
    _cart_page(context).add_product_to_cart(0)


@then("Product should appear in cart")
def product_should_appear_in_cart(context):
    assert _cart_page(context).is_product_in_cart(0), \
        "❌ Product was not found in the cart after adding"


@when("User removes product from cart")
def user_removes_product_from_cart(context):
    _cart_page(context).remove_product(0)


@then("Cart should be empty")
def cart_should_be_empty(context):
    # এই practice site-এ persistent cart নেই।
    # 'view test case' button toggle করে add/remove করে।
    # Remove click করার পর button আবার 'Add to Cart' state-এ ফিরে যায় —
    # সেটাই "cart empty" এর প্রমাণ।
    result = _cart_page(context).is_cart_empty_after_remove()
    assert result, "❌ Product is still in the cart after removing"
