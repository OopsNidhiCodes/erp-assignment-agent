from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from twilio.rest import Client
import os
import time

# Load environment variables
load_dotenv()
USERNAME = os.getenv("USERNAME_")
PASSWORD = os.getenv("PASSWORD")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TO_WHATSAPP = os.getenv("TO_WHATSAPP")
FROM_WHATSAPP = os.getenv("FROM_WHATSAPP")

# ✅ Configure Chrome options
options = Options()
options.add_argument("--headless")  # Required for GitHub Actions
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")

# ✅ Initialize WebDriver (no Service needed in GitHub Actions)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# --- LOGIN ---
driver.get("https://erp.ppsu.ac.in/Login.aspx")
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
except Exception as e:
    print("❌ Error during login:", e)
    driver.save_screenshot("login_debug_error.png")
    driver.quit()
    exit()

# --- NAVIGATE TO LMS PAGE ---
driver.get("https://erp.ppsu.ac.in/StudentPanel/LMS/LMS_ContentStudentDashboard.aspx")
time.sleep(7)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

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

# --- SEND WHATSAPP MESSAGE ---
message_body = (
    "📚 *Pending Assignments*\n\n" + "\n\n".join(assignments)
    if assignments else "✅ No pending assignments found!"
)

try:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message_body,
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP
    )
    print("📩 WhatsApp message sent:", message.sid)
except Exception as e:
    print("❌ WhatsApp send failed:", e)