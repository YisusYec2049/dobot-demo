import time
from firebase_admin import credentials, initialize_app, db
import os

firebase_url = "https://prueba-dobot-default-rtdb.firebaseio.com/"
cred_path = os.path.abspath("./serviceAccountKey_save.json")


cred = credentials.Certificate(cred_path)
initialize_app(cred, {"databaseURL": firebase_url})

firebase_db = db.reference('/test_firebase/data_post')

def sent_data_to_firebase(sign):
    data = {
        'sign': sign,
        'timestamp': time.time() 
    }
    result = firebase_db.push(data)
    print("Datos enviados a Firebase:", data)
    return result

while True:
    x = input('Ingrese la coordenada X: ')
    y = input('Ingrese la coordenada y: ')
    z = input('Ingrese la coordenada z: ')

    list_coords= [x, y, z]
    sent_data_to_firebase(list_coords)
    time.sleep(2)


