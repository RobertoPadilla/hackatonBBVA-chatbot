# Download the helper library from https://www.twilio.com/docs/python/install
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

message = client.messages.create(
    body='Hello there!',
    persistent_action=['geo:37.787890,-122.391664|375 Beale St'],
    from_='whatsapp:+14155238886',
    to='whatsapp:+5215582403665'
)

print(message.sid)
