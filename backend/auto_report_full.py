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
USERNAME = "phuongnamphatvn@gmail.com"  # đổi thành username của bạn
PASSWORD = "'Samcovina@123#"  # đổi thành password của bạn

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
os.makedirs(DATA_DIR, exist_ok=True)

CSV_FILE = os.path.join(DATA_DIR, "report.csv")
EXCEL_FILE = os.path.join(DATA_DIR, "report.xlsx")

# ----------------- Chrome options -----------------
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # comment nếu muốn thấy trình duyệt
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # --- Mở trang login ---
    driver.get(URL)
    print("Mở trang:", driver.current_url)
    time.sleep(2)

    # --- Chờ và nhập username ---
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_input.send_keys(USERNAME)

    # --- Chờ và nhập password ---
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys(PASSWORD)

    # --- Click login ---
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    print("Đã click login, chờ load report...")

    # --- Chờ bảng dynamic load xong ---
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )

    # --- Lấy dữ liệu từ table ---
    rows = table.find_elements(By.TAG_NAME, "tr")
    headers = [c.text for c in rows[0].find_elements(By.TAG_NAME, "th")]
    data = []
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols:
            data.append([c.text for c in cols])

    # --- Xuất CSV và Excel ---
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(CSV_FILE, index=False)
    df.to_excel(EXCEL_FILE, index=False)
    print(f"✅ Dữ liệu đã xuất: {CSV_FILE}, {EXCEL_FILE}")

finally:
    driver.quit()
    print("Đóng trình duyệt.")
