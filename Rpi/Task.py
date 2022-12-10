import json

from state import State

import bt_full as BT

from ifttt import send_ifttt
from send_Line_notification import sendLineMessage

from read_config import RC

def thief():
    print("Probably thief get in !!!")
    sendLineMessage(RC.getLineKey(),"Probably thief get in !!!")
    return

def Task(mode, obj, conn):

    if mode == "Phone":
        data = json.dumps(RC.cf).encode('utf-8') + b'\n'
        conn.send(data)
        return 


    # received data: int len = sprintf(acc_json,"{\"h\":%f,\"t\":%f,\"m\":%s}",humidity,temprature,message);
    humidity, temprature, message = obj['h'], obj['t'], obj['m']
    
    # message : {"door opening", "door closing", "door stopped"}
    if message == "door opening":
        if State.getUserState() == "Not At Home":
            RSSI = BT.detect_rssi()
            if RSSI == "can't detect key":
                thief()
            else:
                print("rssi start =",RSSI)
                print("message =",message)
                
    elif message == "door closing":
        if State.getUserState() == "At Home":
            RSSI = BT.detect_rssi()
            if RSSI == "at the door" :
                State.changeUserState()
                send_ifttt(humidity, temprature, 0)

    elif message == "door stopped":
        print(message)

    else:
        print("Error when receiving data")
        exit(1)

    State.addDoorState(message)
    return 
