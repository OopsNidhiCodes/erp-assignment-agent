from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
from twilio.rest import Client

load_dotenv()

USERNAME = os.getenv("USERNAME_")
PASSWORD = os.getenv("PASSWORD")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TO_WHATSAPP = os.getenv("TO_WHATSAPP")
FROM_WHATSAPP = os.getenv("FROM_WHATSAPP")

# ✅ Headless Chrome setup
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

driver.get("https://erp.ppsu.ac.in/Login.aspx")

# Step 1: Click "Student"
student_radio = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Student']")))
driver.execute_script("arguments[0].click();", student_radio)
print("✅ Clicked Student")
time.sleep(2)

try:
    username_input = wait.until(EC.presence_of_element_located((By.ID, "txtUsername")))
    password_input = driver.find_element(By.ID, "txtPassword")
    login_button = driver.find_element(By.ID, "btnLogin")

    username_input.clear()
    username_input.send_keys(USERNAME)
    password_input.clear()
    password_input.send_keys(PASSWORD)
    login_button.click()
    print("🚀 Login submitted.")
    time.sleep(5)

    # ✅ Navigate to LMS Dashboard
    driver.get("https://erp.ppsu.ac.in/StudentPanel/LMS/LMS_ContentStudentDashboard.aspx")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    pending_section = driver.find_element(By.ID, "ContentPlaceHolder1_divPendingAssignment")
    message = pending_section.text.strip()

    print("📩 Pending Assignment Message:\n", message)

    # ✅ Send WhatsApp Message via Twilio
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP,
        body=f"📚 Pending Assignments:\n{message}"
    )
    print("✅ WhatsApp Message Sent")

except Exception as e:
    print("❌ Error:", e)

driver.quit()
