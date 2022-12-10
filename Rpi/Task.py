import os
import pexpect
import sys
import json
import time

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

    if mode == "phone requests for config":
        data = json.dumps(RC.cf).encode('utf-8') + b'\n'
        conn.send(data)
        return 
    
    elif mode == "phone requests for setting user key":
        # old_stdout = sys.stdout
        # sys.stdout = mystdout = StringIO()
        ## the thing printed here will be stored at mystdout
        
        os.system("touch mylog.log")
        
        process = pexpect.spawn('python set_config.py --set_user_phone_key',timeout=40)
        process.logfile = open("./mylog.log","wb")
        
        process.expect("Enter your device number: ")


        os.system("cat mylog.log")

        log_content = ""
        with open("mylog.log","r") as f:
            log_content = f.read()

        data = {"task":"print log","msg":"*".join(log_content.split("\n"))}
        data = json.dumps(data).encode('utf-8') + b'\n'
        conn.send(data)
        # conn.send("*".join(log_content.split("\n")).encode() + b"\n")

        # os.system("rm mylog.log")

        while True:
            data = conn.recv(1024).decode('utf-8')
            obj = json.loads(data)
            print(obj, 'msg' in obj.keys())
            if 'msg' in obj.keys():
                process.send(obj['msg'] + "\n")
                break

        process.expect(pexpect.EOF)

        
        
        # process.expect("number: ",timeout = None)
        # process.send('0\n')
        
        #
        # sys.stdout = old_stdout

        print("END of set phone key")

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
