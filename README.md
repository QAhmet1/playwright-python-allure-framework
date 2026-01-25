# 🚀 Elite Playwright Pytest Framework

[![Playwright Tests](https://github.com/QAhmet1/playwright-python-allure-framework/actions/workflows/main.yml/badge.svg)](https://github.com/QAhmet1/playwright-python-allure-framework/actions/workflows/main.yml)
[![Live Report](https://img.shields.io/badge/Allure-Live_Report-yellowgreen?style=for-the-badge&logo=allure)](https://QAhmet1.github.io/playwright-python-allure-framework/)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)

A high-performance, enterprise-level automated testing framework built with **Python**, **Playwright**, and **Pytest**. This project demonstrates advanced QA automation patterns, including CI/CD integration, parallel execution, and comprehensive reporting.

---

## 📊 Live Test Report
You can view the latest test execution results here:
👉 **[Live Allure Report](https://QAhmet1.github.io/playwright-python-allure-framework/)**

---

## 🔥 Key Features

- **Multi-Browser Support:** Cross-browser testing on Chromium, Firefox, and WebKit.
- **Parallel Execution:** Fast execution using `pytest-xdist`.
- **API & UI Testing:** Unified framework for both end-to-end UI flows and REST API validation.
- **CI/CD Pipeline:** Fully automated via **GitHub Actions** with daily scheduled runs (07:00 AM Belgium Time).
- **Professional Reporting:** In-depth **Allure Reports** including screenshots, video recordings, and historical trends.
- **Dynamic Configuration:** Environment-based setup (QA/PROD) using `python-dotenv`.
- **Page Object Model (POM):** Clean, maintainable, and scalable architectural design.

---

## 🏗️ Project Structure

```text
├── core/               # Configuration and core logic
├── data/               # Test data and environment files
├── pages/              # Page Object Model (POM) classes
├── tests/              # Test suites (UI & API)
├── .github/workflows/  # CI/CD pipeline definitions
├── conftest.py         # Pytest fixtures and hooks
└── pytest.ini          # Pytest configuration

🚀 Installation & Usage
1. Repository Setup

git clone https://github.com/QAhmet1/playwright-python-allure-framework.git
cd playwright-python-allure-framework

2. Environment Setup
pip install -r requirements.txt
playwright install --with-deps

3. Execution Commands
# Full execution with Allure report generation
npm run elite-run

# Targeted environment execution
pytest --env qa

⚙️ CI/CD Implementation
The framework utilizes GitHub Actions for continuous validation:

Scheduling: Automated cron jobs ensure daily system stability.

Manual Dispatch: Supports manual triggers with environment-specific (QA/Prod) parameterization.

Artifact Management: Detailed logs and media attachments are preserved for every failed regression.

👨‍💻 About the Author
Ahmet Demir Senior QA Automation Engineer

Experience: 5+ Years in Web, Mobile, API, and Database Automation.

Core Competencies: Playwright, Selenium, Appium, Pytest, and CI/CD Orchestration.

This repository serves as a showcase for professional automation patterns. Contributions and discussions are welcome!



