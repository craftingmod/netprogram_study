import smtplib
from email.message import EmailMessage
from openpyxl import load_workbook

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

sender = input("Enter your email address: ")
password = input("Enter your app password: ")

load_wb = load_workbook("email_list.xlsx")

load_ws = load_wb["Sheet1"] # WorkSheet

for row in load_ws.rows:
  recipient = row[0].value

  msg = EmailMessage()
  msg["Subject"] = "휴강 공지"
  msg["From"] = sender
  msg.set_content("오늘 수업은 정상적으로 진행합니다.")
  msg["To"] = recipient

  s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)