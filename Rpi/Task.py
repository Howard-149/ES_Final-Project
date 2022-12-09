from ifttt import send_ifttt
from state import State
from bt_full import getUserState

def getRSSI():
    return 0

def thief():
    return

def Task(mode, obj):
    # received data: int len = sprintf(acc_json,"{\"h\":%f,\"t\":%f,\"m\":%s}",humidity,temprature,message);
    humidity, temprature, message = obj['h'], obj['t'], obj['m']
    
    # message : {"door opening", "door closing", "door stopped"}
    if message == "door opening":
        if State.getUserState() == "Not At Home":
            RSSI = getRSSI()
            if RSSI >= 0:
                thief()
    elif message == "door closing":
        if State.getUserState() == "At Home":
            RSSI = getRSSI()
            if RSSI < 0 :
                State.changeUserState()
                send_ifttt(humidity, temprature, 0)

    elif message == "door stopped":
        print(message)

    else:
        print("Error when receiving data")
        exit(1)

    State.addDoorState(message)
    return 
