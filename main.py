from email import message
from fastapi import FastAPI, Request
from twilio_client import client as twilio_client
from pydantic import BaseModel
import requests

class SendMessageIn(BaseModel):
    body: str
    to: str

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API Blue Fireflies"}


@app.post("/send_message")
async def send_message(message: SendMessageIn):
    response = twilio_client.messages.create(
        body=message.body,
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{message.to}'
    )

    return {"message": response.sid}

@app.post("/callback")
async def callback(request: Request):
    # message = {"to": "whatsapp:+5215582403665"}
    message = {}
    
    for param in request.query_params:
        message['body'] = param
        print(message)
    params = request.query_params
    return {"message": params}