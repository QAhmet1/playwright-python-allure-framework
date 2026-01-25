import pytest
from pages.login_page import LoginPage
import allure

@allure.epic("Shopping Cart System")
@allure.feature("Purchase Flow")
class TestPurchaseFlow:
    """
    Test suite for validating the end-to-end purchase and sorting flows.
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """
        Setup: Initialize the login page and authenticate before each test.
        """
        self.login_page = LoginPage(page)
        self.inventory_page = self.login_page.open_app().login_with_env_creds()

    @allure.story("Cart Management")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verifies that a specific product can be added to the shopping cart successfully.")
    def test_should_add_backpack_to_cart(self, page):
        """
        Equivalent to test("should add backpack", async ({ page }) => { ... })
        """
        product = "Sauce Labs Backpack"
        
        with allure.step(f"Add '{product}' to cart"):
            self.inventory_page.add_product_to_cart(product)
        
        with allure.step("Verify cart badge count is '1'"):
            assert self.inventory_page.get_cart_count() == "1"
        
        print(f"\n✅ {product} added to cart successfully.")
        

    @allure.story("Sorting Functionality")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Ensures that the sorting UI is functional for 'Price Low to High'.")
    def test_should_sort_products_by_price_low_to_high(self, page):
        """
        Tests the sorting functionality.
        """
        with allure.step("Sort products by price: Low to High"):
            self.inventory_page.sort_products_by("lohi")
        
        with allure.step("Verify user is still on the inventory page"):
            assert self.inventory_page.is_on_inventory_page()

    @allure.story("Sorting Logic")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Validates the mathematical correctness of price sorting from Low to High.")
    def test_price_sorting_logic(self, page):
        """
        Validates that prices are mathematically sorted from Low to High.
        """
        with allure.step("Apply sorting: Low to High"):
            self.inventory_page.sort_products_by("lohi")
            
        with allure.step("Compare product prices with a mathematically sorted list"):
            prices = self.inventory_page.get_all_product_prices()
            assert prices == sorted(prices), f"Prices are not correctly sorted! Expected: {sorted(prices)}, Actual: {prices}"
   

    @allure.feature("Purchase Flow")
    @allure.story("E2E Complete Purchase")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Complete checkout flow starting from login to the success message confirmation.")
    def test_complete_purchase_e2e(self, page):
        """
        Full End-to-End purchase flow from login to finish.
        """
        from faker import Faker
        fake = Faker()
        
        with allure.step("Add product and navigate to cart"):
            cart_page = (self.inventory_page
                         .add_product_to_cart("Sauce Labs Backpack")
                         .go_to_cart())
        
        with allure.step("Initiate checkout process"):
            checkout_page = cart_page.proceed_to_checkout()
        
        with allure.step("Fill personal information and complete checkout"):
            success_msg = (checkout_page
                           .fill_information(fake.first_name(), fake.last_name(), fake.zipcode())
                           .finish_checkout()
                           .get_success_message())
        
        with allure.step("Verify successful order message"):
            assert "Thank you for your order" in success_msg