from core.base_page import BasePage
from core.decorators import ui_step

class CheckoutPage(BasePage):
    _FIRST_NAME = "#first-name"
    _LAST_NAME = "#last-name"
    _POSTAL_CODE = "#postal-code"
    _CONTINUE_BTN = "#continue"
    _FINISH_BTN = "#finish"
    _SUCCESS_HEADER = ".complete-header"

    @ui_step
    def fill_information(self, f_name, l_name, zip_code):
        self.fill_text(self._FIRST_NAME, f_name)
        self.fill_text(self._LAST_NAME, l_name)
        self.fill_text(self._POSTAL_CODE, zip_code)
        self.click_element(self._CONTINUE_BTN)
        return self

    @ui_step
    def finish_checkout(self):
        self.click_element(self._FINISH_BTN)
        return self

    @ui_step
    def get_success_message(self):
        return self.page.locator(self._SUCCESS_HEADER).inner_text()