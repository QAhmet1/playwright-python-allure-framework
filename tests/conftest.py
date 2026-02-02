import pytest
import os
import json
from core.config import Config
from datetime import datetime
import allure
import platform
import time
from allure_commons.types import AttachmentType
from core.api_client import APIClient
from pages.api_actions import PostService
import getpass
from core.db_client import DBClient


def pytest_addoption(parser):
    parser.addoption(
        "--env", 
        action="store", 
        default="qa", 
        help="Environment to run tests: qa or prod"
    )

def pytest_configure(config):
    env = config.getoption("--env").lower()
    os.environ["TEST_ENV"] = env
    
    if not hasattr(config, '_metadata'):
        config._metadata = {}
    config._metadata['Project'] = 'Elite Playwright Automation'
    config._metadata['Environment'] = env.upper()
    config._metadata['Run Time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 3. Smart Browser Context Fixture
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, tmp_path_factory):
    """
    Customizing browser context for smart reports (Video, Trace, Viewport).
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "reports/videos/",
        "accept_downloads": True
    }

@pytest.fixture
def page(browser):
    context = browser.new_context(record_video_dir="videos/")
    page = context.new_page()
    yield page
    context.close()

def pytest_sessionfinish(session, exitstatus):
    """
    Customizing Allure Environment, Executor, and Categories details.
    """
    if hasattr(session.config, "workerinput"):
        return

    allure_dir = session.config.getoption("--alluredir")
    env_name = session.config.getoption("--env") or "qa"
    
    if allure_dir and os.path.exists(allure_dir):
        is_github = os.getenv('GITHUB_ACTIONS') == 'true'
        is_docker = os.path.exists('/.dockerenv')
        
        if is_github:
            exec_context = "GitHub Actions"
            executor_type = "github"
            report_url = f"https://github.com/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}"
            build_name = f"CI_Build_{os.getenv('GITHUB_RUN_NUMBER')}"
        elif is_docker:
            exec_context = "Docker Container"
            executor_type = "docker"
            report_url = "N/A" # Konteynır içinden URL genelde statik olmaz
            build_name = f"Docker_Build_{datetime.now().strftime('%H%M')}"
        else:
            exec_context = "Local Machine"
            executor_type = "local"
            report_url = "http://localhost:49702"
            build_name = f"Local_Build_{datetime.now().strftime('%H%M')}"

        # 1. Environment.properties
        try: 
            user = getpass.getuser() 
        except Exception: 
            user = "ci-runner" 
            
        user_name = f"{user}@{platform.node()}"
        system_platform = "macOS" if platform.system() == "Darwin" else platform.system()
        
        env_details = (
           f"Environment={env_name.upper()}\n"
            f"Execution_Context={exec_context}\n"
            f"Execution_User={user_name}\n"
            f"Platform={system_platform}\n"
            f"Execution_Time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Browser=Chromium\n"
            f"Playwright_Version=1.57.0\n"
            f"Docker_Image=python:v1.57.0-jammy\n"
            f"Framework=Elite-Playwright-Pytest\n"
        )
        with open(os.path.join(allure_dir, "environment.properties"), "w") as f:
            f.write(env_details)

        # 2. Executor.json
        executor_info = {
            "name": user_name,
            "type": executor_type,
            "reportName": f"Elite Framework - {exec_context}",
            "buildName": build_name,
            "reportUrl": report_url
        }
        with open(os.path.join(allure_dir, 'executor.json'), 'w') as f:
            json.dump(executor_info, f, indent=4)

        # 3. Categories.json
        categories_info = [
            {
                "name": "Infrastructure issues",
                "matchedStatuses": ["broken", "failed"],
                "messageRegex": ".*Timed out.*|.*Network.*"
            },
            {
                "name": "Assertion errors",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*AssertionError.*"
            },
            {
                "name": "Outdated Tests",
                "matchedStatuses": ["broken"],
                "messageRegex": ".*AttributeError.*"
            }
        ]
        with open(os.path.join(allure_dir, 'categories.json'), 'w') as f:
            json.dump(categories_info, f, indent=4)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="FAILED_SCREENSHOT",
                attachment_type=allure.attachment_type.PNG
            )

@pytest.fixture(scope="session")
def api_client_fixture(playwright):
    """Creates a global API client instance."""
    request_context = playwright.request.new_context()
    client = APIClient(request_context)
    yield client
    request_context.dispose()



@pytest.fixture
def post_service(api_client_fixture):
    """Her seferinde import etmek yerine servisi hazır sunar."""
    return PostService(api_client_fixture)


@pytest.fixture(scope="session")
def db_client():
    """Initializes the DBClient instance."""
    return DBClient(db_path="automation_test.db")

@pytest.fixture(scope="function", autouse=False)
def setup_database_schema(db_client):
    """
    Setup: Create the relational schema (tables) before tests.
    This ensures tables exist and are empty for each test that uses this fixture.
    """
    # Create Departments table
    db_client.execute_non_query("DROP TABLE IF EXISTS departments")
    db_client.execute_non_query("""
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            dept_name TEXT
        )
    """)
    
    # Create Employees table with relational structure
    db_client.execute_non_query("DROP TABLE IF EXISTS employees")
    db_client.execute_non_query("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            dept_id INTEGER,
            FOREIGN KEY (dept_id) REFERENCES departments (id)
        )
    """)
    
    # Seed common base data
    db_client.execute_non_query("INSERT INTO departments VALUES (1, 'QA'), (2, 'Dev')")
    
    yield db_client