import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def sendMessage(msg: str, send_to:str):
    message = client.messages.create(
        body=msg,
        from_=os.getenv('TWILIO_NUMBER'),
        to=send_to
    )

    return message.sid