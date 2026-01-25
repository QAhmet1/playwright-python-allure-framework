from playwright.sync_api import Page, expect
from core.decorators import ui_step

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @ui_step
    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    @ui_step
    def click_element(self, selector: str):
        # Smart waiting is built-in with Playwright, but we can add extra logging here
        self.page.wait_for_selector(selector, state="visible")
        self.page.click(selector)

    @ui_step
    def fill_text(self, selector: str, text: str, secret: bool = False):
        self.page.wait_for_selector(selector, state="visible")
        # Masking logs for passwords
        display_text = "****" if secret else text
        print(f"      └─ Action: Typing '{display_text}' into {selector}")
        self.page.fill(selector, text)

    @ui_step
    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector)