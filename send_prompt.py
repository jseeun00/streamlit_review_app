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

def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # chromedriver 경로: ENV -> which -> 오류
    env_drv = os.getenv("CHROMEDRIVER_BIN")
    if env_drv and Path(env_drv).is_file():
        driver_path = env_drv
    elif (drv := shutil.which("chromedriver")):
        driver_path = drv
    else:
        raise FileNotFoundError(
            "chromedriver를 찾을 수 없습니다. chromium-driver 설치를 확인하세요."
        )
    service = Service(driver_path)

    # chromium 바이너리 경로: ENV -> which -> 오류
    env_chrome = os.getenv("CHROME_BIN")
    if env_chrome and Path(env_chrome).is_file():
        chrome_path = env_chrome
    elif (bin1 := shutil.which("chromium")):
        chrome_path = bin1
    elif (bin2 := shutil.which("chromium-browser")):
        chrome_path = bin2
    else:
        raise FileNotFoundError(
            "Chromium 바이너리를 찾을 수 없습니다. chromium 설치를 확인하세요."
        )
    options.binary_location = chrome_path

    return webdriver.Chrome(service=service, options=options)


def send_to_gemini(prompt: str):
    driver = None
    try:
        # 시스템 드라이버로 초기화
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
    # 브라우저는 닫지 않고 유지


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_prompt.py \"<your prompt here>\"")
        sys.exit(1)
    prompt_text = sys.argv[1]
    send_to_gemini(prompt_text)

    send_to_gemini(prompt_text)


