import os
import pexpect
import sys
import json
import time
import threading

from state import State

import bt_full as BT

from ifttt import send_ifttt
from send_Line_notification import sendLineMessage


from read_config import RC

mutex = threading.Lock()
mutex.acquire()
out_humidity, out_temprature=0,0


def thief():
    print("Probably thief get in !!!")
    sendLineMessage(RC.getLineKey(),"Probably thief get in !!!")
    return

def Task(mode, obj, conn_dict):
    global mutex
    global out_humidity, out_temprature
    if mode == "phone requests for config":
        data = json.dumps(RC.cf).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)
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
        conn_dict['Phone'].send(data)
        # conn.send("*".join(log_content.split("\n")).encode() + b"\n")

        # os.system("rm mylog.log")

        while True:
            data = conn_dict['Phone'].recv(1024).decode('utf-8')
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

    elif mode == "STM32_1":
        # received data: int len = sprintf(acc_json,"{\"h\":%f,\"t\":%f,\"m\":%s}",humidity,temprature,message);
        humidity, temprature, message = obj['h'], obj['t'], obj['m']
        print(State.getUserState())
        # message : {"door opening", "door closing", "door stopped"}
        if message == "door opening":
            if State.getUserState() == "Not At Home":
                RSSI = BT.detect_rssi()
                if RSSI == "can't detect key":
                    thief()
                else:
                    print("rssi start =",RSSI)
                    print("message =",message)
            else:
                RSSI=BT.detect_rssi()
                if RSSI == "can't detect key":
                    State.atHome=False
        elif message == "door closing":
            if State.getUserState() == "At Home":
                RSSI = BT.detect_rssi()
                if RSSI == "at the door" : #leave home
                    conn_dict['STM32_2'].sendall("Send Outdoor Data".encode(encoding='utf8'))
                    mutex.acquire()
                    State.changeUserState()
                    print("in STM32_1")
                    print("out_humidity=%f  out_temprature=%f "%(out_humidity,out_temprature))
                    # send_ifttt(humidity, temprature, 0)
                    line_message="humidity:%d temprature:%d out door humidity:%d outdoor temprature:%d"%(humidity,temprature,out_humidity,out_temprature)
                    sendLineMessage(RC.getLineKey(),line_message)
                elif RSSI=="can't detect key":
                    State.changeUserState()
            else:
                RSSI=BT.detect_rssi()
                if RSSI == "at the door" : #back to home
                    State.changeUserState()
                elif RSSI=="inside the room":
                    State.atHome=True

        elif message == "door stopped":
            print(message)

        else:
            print("Error when receiving data")
            exit(1)

        State.addDoorState(message)
        return 
    elif mode == "STM32_2": 
        out_humidity,out_temprature = obj['h'],obj['t']
        mutex.release()

