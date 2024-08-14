import firebase_admin
from firebase_admin import credentials, initialize_app, db
import time
import threading
import DobotDllType as dType
import json
from firebase import firebase
import requests

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll and get the CDLL object
api = dType.load()
#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):
    
    #Clean Command Queued
    dType.SetQueuedCmdClear(api)
    
    #Async Motion Params Setting
    
    dType.SetHOMEParams(api, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    
    print(dType.GetPose(api))
  
    # Move code "X front/back" "R action"
    def move(list):
        
        dType.SetPTPCmd(api,dType.PTPMode.PTPMOVLXYZMode, *list, 0)

    
    
    print(dType.GetPose(api))




firebase_url = "https://prueba-dobot-default-rtdb.firebaseio.com/"
firebase_db_ref = "test_firebase/data_post"

def read_data_from_firebase():
    try:
        response = requests.get(f"{firebase_url}/{firebase_db_ref}.json")
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        result = response.json()
        print("Datos leídos desde Firebase:", result)

        if isinstance(result, dict) and result:
            # Obtener la última entrada en 'data_post'
            last_entry_key = list(result.keys())[-1]
            data = result[last_entry_key]
            print("Datos leídos desde Firebase:", data)
            
            # Construir la URL para eliminar el registro
            delete_url = f"{firebase_url}/{firebase_db_ref}/{last_entry_key}.json"
            # Enviar una solicitud DELETE para eliminar el registro
            delete_response = requests.delete(delete_url)
            delete_response.raise_for_status()  # Verifica si la eliminación fue exitosa
            print(f"Elemento con clave '{last_entry_key}' eliminado.")
            return data
        else:
            print("No data")
    except requests.exceptions.HTTPError as e:
        print("Error al leer datos desde Firebase:", e)
        return None

def send_data_to_dobot(data):
    try:
        # Extraer la lista de coordenadas del diccionario
        coords_str = data.get('sign', [])
        # Convertir los datos de string a enteros
        coords = [int(val) for val in coords_str]
        print("Datos convertidos a enteros:", coords)
        # Enviar los datos al Dobot
        move(coords)
        print("Datos enviados al Dobot:", coords)
    except ValueError as e:
        print(f"Error al convertir datos a enteros: {e}")


while True:
    firebase_data = read_data_from_firebase()
    if firebase_data:
        send_data_to_dobot(firebase_data)
    time.sleep(2)


#Disconnect Dobot
dType.DisconnectDobot(api)