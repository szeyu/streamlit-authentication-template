import yagmail
import random
import string
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_otp():
    otp = ''.join(random.choices(string.digits, k=4))
    return otp

def send_email(email, otp):
    sender_email = os.getenv('sender_mail')
    password = os.getenv('sender_mail_pass')  # This should be your App Password if 2FA is enabled
    
    # Initialize the Yagmail SMTP client
    yag = yagmail.SMTP(sender_email, password)
    
    # Send the email
    subject = "OTP Verification"
    body = f"Your OTP is: {otp}"
    yag.send(to=email, subject=subject, contents=body)
    
    print(f"OTP sent to {email} successfully.")

