import os
import smtplib
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('MAIL')
EMAIL_PASSWORD = os.environ.get('PASS')
EMAIL_CONTACTS = os.environ.get('CONTACTS')

contacts = EMAIL_CONTACTS
def send_email(found_skins):
    msg = EmailMessage()
    msg['Subject'] = 'SKINS!!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts
    content = f'Parece que encontramos unas skins en un oferta Julio :3'
    for skin in found_skins:
        found = f"\n  - {skin['champion']}, con la skin {skin['skin']}"
        content = content + found
    msg.set_content(content)
    with open('screenshot.png','rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
        
    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)