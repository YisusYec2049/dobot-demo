import time
from firebase_admin import credentials, initialize_app, db # type: ignore
import os
import keyboard

firebase_url = "https://prueba-dobot-default-rtdb.firebaseio.com/"
cred_path = os.path.abspath("./serviceAccountKey_save.json")

cred = credentials.Certificate(cred_path)
initialize_app(cred, {"databaseURL": firebase_url})

firebase_db = db.reference('/test_firebase/data_post')

X = 0
Y = 0
Z = 0
RL = 0
RR = 0

def move_up():
    global Z
    # Lógica para mover el brazo hacia arriba
    if Z < 300:
        Z = Z + 5
    else:
        print("Pasó del limite")

def move_down():
    global Z
    # Lógica para mover el brazo hacia abajo
    if Z > 0:
        Z = Z - 5
    else:
        print("Pasó del limite")

def move_left():
    global Y
    # Lógica para mover el brazo hacia la izquierda
    if Y > 0:
        Y = Y - 5
    else:
        print("Pasó del limite")

def move_right():
    global Y
    # Lógica para mover el brazo hacia la derecha
    if Y < 300:
        Y = Y + 5
    else:
        print("Pasó del limite")
    
def move_ahead():
    global X
    # Lógica para mover el brazo hacia adelante
    if X < 300:
        X = X + 5
    else:
        print("Pasó del limite")
    
def move_back():
    global X
    # Lógica para mover el brazo hacia atrás
    if X > 0:
        X = X - 5
    else:
        print("Pasó del limite")

def sent_data_to_firebase(sign):
    data = {
        'sign': sign,
        'timestamp': time.time() 
    }
    result = firebase_db.push(data)
    print("Datos enviados a Firebase:", data)
    return result
      
try:
    while True:
        if keyboard.is_pressed("up"):
            move_up()
            print(X,Y,Z)
            sent_data_to_firebase([X,Y,Z])
        elif keyboard.is_pressed("down"):
            move_down()
            print(X,Y,Z)
            sent_data_to_firebase([X,Y,Z])
        elif keyboard.is_pressed("left"):
            move_left()
            print(X,Y,Z)
            sent_data_to_firebase([X,Y,Z])
        elif keyboard.is_pressed("right"):
            move_right()
            print(X,Y,Z)
            sent_data_to_firebase([X,Y,Z])
        elif keyboard.is_pressed("e"):
            move_ahead()
            print(X,Y,Z)
            sent_data_to_firebase([X,Y,Z])
        elif keyboard.is_pressed("q"):
            move_back()
            print(X,Y,Z)
            sent_data_to_firebase([X,Y,Z])
        elif keyboard.is_pressed("esc"):
            break  # Sal del bucle si se presiona la tecla Esc
        time.sleep(0.1)  # Evita la detección continua de teclas
        
except KeyboardInterrupt:
    pass
finally:
    # Detén el brazo robótico y cierra la conexión
    print("Programa finalizado")
    time.sleep(2)