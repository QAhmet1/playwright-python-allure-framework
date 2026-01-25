
import functools
import time
import os
from datetime import datetime

def ui_step(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        page_instance = args[0].page
        step_name = func.__name__.replace("_", " ").title()
        
        print(f"\n[STEP] 🚀 Starting: {step_name}")
        start_time = time.time()
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Highlight the error and take a screenshot
            timestamp = datetime.now().strftime("%H-%M-%S")
            screenshot_path = f"reports/screenshots/ERROR_{step_name}_{timestamp}.png"
            
            os.makedirs("reports/screenshots", exist_ok=True)
            
            page_instance.screenshot(path=screenshot_path, full_page=True)
            
            print(f"[STEP] ❌ FAILED: {step_name}")
            print(f"      📸 Screenshot saved: {screenshot_path}")
            raise e
    return wrapper