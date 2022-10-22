# Download the helper library from https://www.twilio.com/docs/python/install
import os
from pydoc import describe
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

for sms in client.api.messages.stream():
    if sms.direction == 'inbound':
        print(sms.current_location)
