import sys
import time
import os
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

def send_to_gemini(prompt: str):
    driver = None
    try:
        # init_driver()를 통해 system-installed 드라이버만 사용
        driver = init_driver()
        driver.get("https://gemini.google.com/app")
        print("→ Gemini 페이지 열림, 로그인 완료 후 기다려 주세요.")

        wait = WebDriverWait(driver, 15)
        editor = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor"))
        )

        ActionChains(driver).double_click(editor).perform()
        driver.execute_script(
            "arguments[0].innerText = arguments[1];",
            editor,
            prompt
        )
        print("✅ 프롬프트 입력 완료. 결과를 확인하세요.")

        time.sleep(60)
    except Exception as e:
        print(f"❌ 자동화 오류: {e}")
    # 브라우저를 닫지 않고 유지


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_prompt.py \"<your prompt here>\"")
        sys.exit(1)
    prompt_text = sys.argv[1]
    send_to_gemini(prompt_text)


