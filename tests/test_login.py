from pages.login_page import LoginPage
from core.config import Config
import pytest
import os
import allure

@allure.epic("Identity & Access Management")
@allure.feature("Authentication")
@allure.story("Happy Path Login")
@allure.severity(allure.severity_level.BLOCKER)
def test_elite_login_check(page):
    # 1. Arrange
    login_page = LoginPage(page)
    
    # 2. Act 
    with allure.step("Navigate to application and perform login"):
        login_page.open_app().login_with_env_creds()
    
    # 3. Assert 
    with allure.step("Verify redirection to inventory page"):
        # Fixed: Removed the trailing underscore from 'inventory.html'
        assert "inventory.html" in page.url
        
    allure.dynamic.description(f"Successful login verified for URL: {page.url}")
    print(f"\n✅ Successfully logged into {Config.BASE_URL} on {os.getenv('TEST_ENV', 'QA').upper()}!")