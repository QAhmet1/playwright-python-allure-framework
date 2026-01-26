# Change v1.40.0 to v1.57.0 as requested by the error log
FROM mcr.microsoft.com/playwright/python:v1.57.0-jammy

# The rest of the file stays the same
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p allure-results
CMD ["pytest", "tests/", "--alluredir=allure-results", "-n", "2"]