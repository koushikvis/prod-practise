import time
import os
import smtplib
import mimetypes
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from email.message import EmailMessage

# Replace this with your actual driver initialization
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    return driver

# Initialize WebDriver
driver = get_driver()

# Define report path
report_path = os.path.join(os.path.expanduser("~"), "Documents", "MetaRobots_Report.html")

# Start writing the report
with open(report_path, "w", encoding="utf-8") as report_file:
    report_file.write("<html><head><title>Meta Robots Report</title></head><body>")
    report_file.write("<h1>Meta Robots Tag Validation Report</h1><table border='1'>")
    report_file.write("<tr><th>URL</th><th>Meta Robots Content</th><th>Status</th></tr>")

    url = "https://fedrevdev.cosmicnet.xyz/tpa"  # Define the URL

    try:
        driver.get(url)
        time.sleep(2)

        try:
            meta_tag = driver.find_element(By.XPATH, "//meta[@name='robots']")
            meta_content = meta_tag.get_attribute("content")
            status = "✅ Meta Tag is present"
        except NoSuchElementException:
            meta_content = "N/A"
            status = "❌ Meta Tag Not Found"

    except Exception as e:
        meta_content = "N/A"
        status = f"❌ Failed to Load Page ({str(e)})"

    # Write the result to the report
    report_file.write(f"<tr><td>{url}</td><td>{meta_content}</td><td>{status}</td></tr>")

# Close WebDriver
driver.quit()

# Finish writing the report
with open(report_path, "a", encoding="utf-8") as report_file:
    report_file.write("</table></body></html>")

print(f"Report generated: {report_path}")

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "koushik.v@appinessworld.com"
SENDER_PASSWORD = "iymzfbprdnsnluzz"
RECIPIENT_EMAIL = "koushik.v@appinessworld.com"

msg = EmailMessage()
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL
msg["Subject"] = "Meta Robots Report"
msg.set_content("Attached is the Meta Robots Report.")

# Attach the report
mime_type, _ = mimetypes.guess_type(report_path)
mime_type = mime_type or "application/octet-stream"

with open(report_path, "rb") as attachment:
    msg.add_attachment(attachment.read(), maintype=mime_type, subtype="html", filename="MetaRobots_Report.html")

# Send email
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

    print("Email sent successfully!")

except Exception as e:
    print(f"Failed to send email: {e}")
