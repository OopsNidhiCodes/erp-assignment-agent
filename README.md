
# 📚 PPSU ERP WhatsApp Assignment Notifier 🤖💬

This Python-based automation bot logs into the PPSU ERP portal, scrapes pending assignments, and sends them directly to your WhatsApp every day at 5 PM using Twilio.

## 🔥 Features
- ✅ Auto login to PPSU ERP using Selenium
- ✅ Scrapes **pending assignments** from the LMS dashboard
- ✅ Sends assignment details as a WhatsApp message via Twilio API
- ✅ Scheduled daily automation (ideal for Render/cron setup)

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/OopsNidhiCodes/erp-assignment-notifier.git
cd erp-assignment-notifier
```

### 2. Create a `.env` File
Add your credentials like this:

```
USERNAME=your_erp_username
PASSWORD=your_erp_password
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TO_WHATSAPP=whatsapp:+91your_number
FROM_WHATSAPP=whatsapp:+14155238886
```

> 💡 Make sure you have joined Twilio’s WhatsApp sandbox.

---

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4. Run the Script
```bash
python main.py
```

You’ll get a WhatsApp message like:
```
📝 You have 2 pending assignments:
• DBMS – Normalization Sheet – Due: July 28
• SE – ER Diagram – Due: July 29
```

---

## ⏰ Automate Daily at 5 PM

You can deploy this script on:

- [Render](https://render.com/) using a cron job
- [GitHub Actions](https://docs.github.com/en/actions)
- Local Task Scheduler / `cron` (Linux/macOS)

---

## 📁 Folder Structure
```
erp-agent/
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## ✨ Author
Made with 💖 and automation magic by [Nidhi Makwana](https://github.com/OopsNidhiCodes)

---

## ⚠️ Disclaimer
This project is for educational purposes. Use responsibly and do not share credentials.
