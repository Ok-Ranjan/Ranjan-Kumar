import os
import sendgrid
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv() # load .env file
sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
email = Mail(
    from_email='ranjan.cse82@gmail.com',
    to_emails='ranjannp802114@gmail.com',
    subject='SendGrid Direct Test',
    plain_text_content='Hello from SendGrid API direct test!'
)

try:
    response = sg.send(email)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(f"Error: {e}")
