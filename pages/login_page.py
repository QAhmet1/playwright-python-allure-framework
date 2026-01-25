from core.base_page import BasePage
from core.config import Config
from core.decorators import ui_step

class LoginPage(BasePage):
    # --- Locators ---
    _USERNAME = "#user-name"
    _PASSWORD = "#password"
    _LOGIN_BTN = "#login-button"
    _ERROR_MESSAGE = "h3[data-test='error']"

    @ui_step
    def open_app(self):
        """
        EN: Opens the application using the URL from Config.
        """
        self.navigate(Config.BASE_URL)
        return self

    @ui_step
    def login(self, username, password):
        """
        EN: Generic login method for any credentials.
        """
        self.fill_text(self._USERNAME, username)
        self.fill_text(self._PASSWORD, password, secret=True)
        self.click_element(self._LOGIN_BTN)
        return self

    @ui_step
    def login_with_env_creds(self):
        """
        EN: Logs in using credentials from the environment config.
        """
        self.login(Config.USER_NAME, Config.PASSWORD)
        
        # Page Transition
        from pages.inventory_page import InventoryPage
        return InventoryPage(self.page)

    @ui_step
    def get_error_message(self):
        """
        EN: Returns the error message text visible on the page.
        """
        return self.page.locator(self._ERROR_MESSAGE).inner_text()