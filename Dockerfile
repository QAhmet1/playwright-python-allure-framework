
FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy 
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p allure-results
CMD ["pytest", "tests/", "--alluredir=allure-results", "-n", "2"]