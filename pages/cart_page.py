from core.base_page import BasePage
from core.decorators import ui_step

class CartPage(BasePage):
    _CHECKOUT_BTN = "#checkout"
    _CART_ITEM = ".cart_item"

    @ui_step
    def proceed_to_checkout(self):
        self.click_element(self._CHECKOUT_BTN)
        # Transition to an CheckoutPage
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.page)