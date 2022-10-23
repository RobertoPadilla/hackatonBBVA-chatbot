import io
import os
import pandas as pd
from pandas import DataFrame
import numpy as np
import requests
from dotenv import load_dotenv
from google.cloud import storage
from math import radians, cos, sin, asin, sqrt

load_dotenv()

# Get google bucket storage
client = storage.Client.from_service_account_json(
    os.path.join(os.getcwd(), 'hackaton-2022-atm-ea198af6ede3.json'), project='hackaton-2022-atm'
)
bucket = client.get_bucket('dataset-hackaton2022')

def convert_to_float(num):
    """Transform given strings into float numbers """
    if isinstance(num, str):
        return float(num)

    return num

def traffic(lat1, long1, lat2, long2):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={lat2}%2C{long2}&destinations={lat1}%2C{long1}&units=imperial&key={os.getenv('GOOGLE_API_KEY')}"
    
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()
    
    return response['rows'][0]['elements'][0]['duration']['value']

def dist(lat1, long1, lat2, long2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Credits: https://medium.com/analytics-vidhya/finding-nearest-pair-of-latitude-and-longitude-match-using-python-ce50d62af546
    """
    # convert string to float
    lat1, long1, lat2, long2 = map(convert_to_float, [lat1, long1, lat2, long2])

    # convert decimal degrees to radians
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])

    # haversine formula
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def nearest(lat, long, device=None, quantity=1):
    location = {
        "latitud": lat,
        "longitud": long
    }
    
    # TODO: Crear un nuevo dataset de sucursales
    # Reading csv from bucket
    df = pd.read_csv(io.BytesIO(bucket.blob(blob_name='atms-raw.csv').download_as_string()), encoding="UTF-8", sep=',')

    # Filtering by subsidiary
    df.drop_duplicates(subset = ['Latitud', 'Longitud'], inplace = True)
    
    df = df[df['ETV'] == 'APODERADO']

    # Building column 'kilometros' based on haversine formula
    df['kilometros'] = df.apply(lambda row: dist(row['Latitud'], row['Longitud'], location['latitud'], location['longitud']), axis=1)

    if device is not None:
        df = df[df['Tipo dispositivo'] == device]

    df = df.sort_values(by=['kilometros']).head(n=quantity)
    df.index = np.arange(1, len(df) + 1)
    return df

def fastest(dataframe: DataFrame, orig_lat, orig_long, quantity=1):
    dataframe['seconds'] = dataframe.apply(lambda row: traffic(row['Latitud'], row['Longitud'], orig_lat, orig_long), axis=1)

    df = dataframe.sort_values(by=['seconds']).head(n=quantity)

    return df