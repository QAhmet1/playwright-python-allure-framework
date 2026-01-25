import pytest
from pages.login_page import LoginPage
import allure


@allure.epic("Identity & Access Management")
@allure.feature("Authentication")
@allure.story("Negative Login Scenarios")
class TestLoginNegative:
    """
    Test suite for validating various failed login attempts and error messages.
    """

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.login_page = LoginPage(page)
        with allure.step("Navigate to the application"):
            self.login_page.open_app()


    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Data-driven test to verify that different invalid credentials trigger correct error messages.")
    @pytest.mark.parametrize("user, pw, expected_error", [
        ("locked_out_user", "secret_sauce", "locked out"),
        ("non_existent_user", "secret_sauce", "do not match"),
        ("standard_user", "wrong_password", "do not match"),
        ("", "", "Username is required")
    ])
    def test_login_failure_scenarios(self, page, user, pw, expected_error):
        # Dynamic Allure Title for each parameter
        allure.dynamic.title(f"Login Failure Test: {expected_error}")
        
        with allure.step(f"Login attempt with user: '{user}'"):
            self.login_page.login(user, pw)
        
        with allure.step(f"Verify that error message contains: '{expected_error}'"):
            actual_error = self.login_page.get_error_message()
            assert expected_error in actual_error
            
        print(f"\n✅ Case '{expected_error}' verified successfully.")