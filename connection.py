import DobotDllType as dType

api = dType.load()
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:", state)

if state == dType.DobotConnect.DobotConnect_NoError:
    print("Dobot conectado exitosamente.")
    # Realiza operaciones de prueba si es necesario
else:
    print("Error de conexión:", state)

dType.DisconnectDobot(api)
