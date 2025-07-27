from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
from dotenv import load_dotenv
import os
import time

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()

USERNAME = os.getenv("USERNAME_")
PASSWORD = os.getenv("PASSWORD")
TO_WHATSAPP = os.getenv("TO_WHATSAPP")
FROM_WHATSAPP = os.getenv("FROM_WHATSAPP")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")

# --- SETUP SELENIUM ---
driver = webdriver.Chrome()
driver.get("https://erp.ppsu.ac.in/Login.aspx")
wait = WebDriverWait(driver, 15)

# --- LOGIN FLOW ---
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

    time.sleep(1)
    login_button.click()
    print("🚀 Login submitted.")
except Exception as e:
    print("❌ Error during login:", e)
    driver.save_screenshot("login_debug_error.png")
    driver.quit()
    exit()

# --- OPEN LMS PAGE & SCROLL TO ASSIGNMENTS ---
time.sleep(5)
driver.get("https://erp.ppsu.ac.in/StudentPanel/LMS/LMS_ContentStudentDashboard.aspx")
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# --- EXTRACT ASSIGNMENTS ---
assignments = []
try:
    rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'table')]/tbody/tr")
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) >= 4:
            subject = columns[1].text.strip()
            assignment = columns[2].text.strip()
            due_date = columns[3].text.strip().split("\n")[0]
            assignments.append(f"{subject} → {assignment}\n📅 Due: {due_date}")
except Exception as e:
    print("❌ Error fetching assignments:", e)

driver.quit()

# --- WHATSAPP NOTIFICATION ---
message_body = "📚 *Pending Assignments*\n\n" + "\n\n".join(assignments) if assignments else "✅ No pending assignments found!"

try:
    client = Client(TWILIO_SID, TWILIO_AUTH)
    message = client.messages.create(
        body=message_body,
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP
    )
    print("📩 WhatsApp message sent:", message.sid)
except Exception as e:
    print("❌ WhatsApp send failed:", e)
