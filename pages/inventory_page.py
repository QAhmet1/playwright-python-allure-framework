from core.base_page import BasePage
from core.decorators import ui_step

class InventoryPage(BasePage):
    # --- Static Locators ---
    _HEADER_TITLE = ".title"
    _SHOPPING_CART_BADGE = ".shopping_cart_badge"
    _SORT_CONTAINER = ".product_sort_container"
    _FIRST_ITEM_NAME = ".inventory_item_name >> nth=0"
    _ADD_TO_CART_BTNS = "button[data-test^='add-to-cart']"
    _PRODUCT_PRICES = ".inventory_item_price"

    # --- Dynamic Locator Generators ---
    def _get_add_to_cart_btn(self, product_name):
        formatted_name = product_name.lower().replace(" ", "-")
        return f"[data-test='add-to-cart-{formatted_name}']"

    @ui_step
    def is_on_inventory_page(self):
        title_text = self.page.locator(self._HEADER_TITLE).inner_text()
        return title_text == "Products"

    @ui_step
    def add_product_to_cart(self, product_name):
        selector = self._get_add_to_cart_btn(product_name)
        self.click_element(selector)
        return self

    @ui_step
    def get_cart_count(self):
        if self.page.locator(self._SHOPPING_CART_BADGE).is_visible():
            return self.page.locator(self._SHOPPING_CART_BADGE).inner_text()
        return "0"

    @ui_step
    def sort_products_by(self, option_value):
        self.page.select_option(self._SORT_CONTAINER, value=option_value)
        return self

    @ui_step
    def go_to_cart(self):
        self.click_element(self._SHOPPING_CART_BADGE)
        # Transition to cart page
        from pages.cart_page import CartPage
        return CartPage(self.page)


    @ui_step
    def get_all_product_prices(self):
        """
        Collects all prices from the page and returns them as a list of floats.
        """
        price_elements = self.page.locator(self._PRODUCT_PRICES).all_inner_texts()
        
        # cleaned texts: ["$9.99", "$15.99"] -> [9.99, 15.99]
        clean_prices = [float(p.replace("$", "")) for p in price_elements]
        
        return clean_prices