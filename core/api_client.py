import allure
import json

class APIClient:
    def __init__(self, request_context):
        self.request = request_context
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.headers = {
            "Content-Type": "application/json"
        }

    def set_token(self, token):
        """Sets the authorization token for the requests."""
        self.headers["Authorization"] = f"Bearer {token}"

    def _log_to_allure(self, method, url, response, payload=None):
        """Logs request and response details to Allure report."""
        status = response.status
        content = f"🚀 METHOD: {method}\n🔗 URL: {url}\n✅ STATUS: {status}\n"
        
        if payload:
            content += f"📤 PAYLOAD: {json.dumps(payload, indent=2)}\n"
        
        try:
            body = response.json()
            content += f"📥 RESPONSE: {json.dumps(body, indent=2)}"
        except:
            content += "📥 RESPONSE: (Empty or Not JSON)"

        allure.attach(content, name=f"{method} {url.split('/')[-1]}", attachment_type=allure.attachment_type.TEXT)

    def call(self, method, endpoint, **kwargs):
        """Sends an HTTP request using Playwright's request context."""
        url = f"{self.base_url}{endpoint}"
        kwargs["headers"] = {**self.headers, **kwargs.get("headers", {})}
        
        method_func = getattr(self.request, method.lower())
        response = method_func(url, **kwargs)
        self._log_to_allure(method.upper(), url, response, kwargs.get("data"))
        return response