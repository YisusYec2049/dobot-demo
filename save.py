# PORTS

from firebase import firebase
import time


firebase_url = "https://iadobot-default-rtdb.firebaseio.com"
firebase = firebase.FirebaseApplication(firebase_url, None)

def read_data_from_firebase():
    result = firebase.get('test_firebase/data_post', None)

    if result:
        data = list(result.values())[-1]
    print("Datos leídos desde Firebase:", data)
    return data

def send_data_to_dobot(data):
    cad = f"{data}"
    print("Datos enviados al  Dobot:", data)

while True:
    firebase_data = read_data_from_firebase()

    if firebase_data:
        send_data_to_dobot(firebase_data)

    time.sleep(2)