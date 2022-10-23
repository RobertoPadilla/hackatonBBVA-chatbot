import os
from dotenv import load_dotenv
import dialogflow
import twiliolib
import datetime
from google.api_core.exceptions import InvalidArgument
from flask import Flask, request
import filter_locations

load_dotenv()

app = Flask(__name__)

def get_context(session):
    context_name = ''
    context_client = dialogflow.ContextsClient()
    context_path = context_client.list_contexts(parent=session)
    for cont in context_path:
        context_name = cont.name

    if context_name != '':
        context = context_client.get_context(name=context_name)
        return context.name.split('/')[-1]

    return context_name

def get_device(context):
    if context == '':
        return None

    if context == 'practicaja':
        return 'PRACTDUAL'

    if context == 'dispensador':
        return 'DISPENSADOR'

@app.route('/bot', methods=['POST'])
def bot():
    mobnum = request.values.get('From')
    latitude = request.values.get('Latitude', '')
    longitude = request.values.get('Longitude', '')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        os.getenv('DIALOG_PROJECT_ID'),
        'session'
    )

    if '' not in [latitude, longitude]:
        device = get_device(get_context(session))

        nearest_locations = filter_locations.nearest(latitude, longitude, device=device, quantity=10)
        
        faster_locations = filter_locations.fastest(nearest_locations, latitude, longitude, 3)

        for index, location in faster_locations.iterrows():
            n_latitude = location['Latitud']
            n_longitude = location['Longitud']
            minutes = str(datetime.timedelta(seconds=location['seconds']))
            twiliolib.sendMessage(f"La {index} más cercana es: https://www.google.com/maps/search/?api=1&query={n_latitude}%2C{n_longitude}, queda a *{minutes}* de ti.", mobnum)

        twiliolib.sendMessage("Espero haber sido útil. Muchas gracias por solicitar mi ayuda 🫢 byeee. 🫂", mobnum)
        return {"result": "success"}

    message = request.values.get('Body')
    text_input = dialogflow.types.TextInput(text=message, language_code='es')
    query_input = dialogflow.types.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    twiliolib.sendMessage(response.query_result.fulfillment_text, mobnum)
    
    return response.query_result.fulfillment_text


if __name__ == '__main__':
    app.run(port=8000)