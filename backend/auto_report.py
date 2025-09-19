import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ----------------- Cấu hình -----------------
URL = "https://main.djzhq4z6s3tou.amplifyapp.com/report"
USERNAME = "your_username"  # đổi thành username của bạn
PASSWORD = "your_password"  # đổi thành password của bạn

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

CSV_FILE = os.path.join(DATA_DIR, "report.csv")
EXCEL_FILE = os.path.join(DATA_DIR, "report.xlsx")

# ----------------- Chrome không headless để debug -----------------
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # comment để nhìn trình duyệt
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(URL)
    print("Mở trang:", driver.current_url)
    time.sleep(2)

    # --- Chờ input username xuất hiện ---
    try:
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_input.send_keys(USERNAME)
    except:
        print("❌ Không tìm thấy input username")
        print(driver.page_source[:1000])  # in 1000 ký tự đầu để debug
        raise

    # --- Chờ input password ---
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(PASSWORD)
    except:
        print("❌ Không tìm thấy input password")
        print(driver.page_source[:1000])
        raise

    # --- Click submit ---
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    print("Đã click login, chờ load trang report...")
    time.sleep(5)  # chờ load bảng

    # --- Chờ bảng xuất hiện ---
    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
    except:
        print("❌ Không tìm thấy bảng dữ liệu")
        print(driver.page_source[:1000])
        raise

    # --- Lấy dữ liệu ---
    rows = table.find_elements(By.TAG_NAME, "tr")
    headers = [c.text for c in rows[0].find_elements(By.TAG_NAME, "th")]
    data = []
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols:
            data.append([c.text for c in cols])

    # --- Xuất CSV/Excel ---
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(CSV_FILE, index=False)
    df.to_excel(EXCEL_FILE, index=False)
    print(f"✅ Đã xuất CSV/Excel vào {DATA_DIR}")

finally:
    print("Đóng trình duyệt...")
    driver.quit()
