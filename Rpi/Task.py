import os
import time
import pexpect
import json
import threading

from state import State
import bt_full as BT
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
        RC.reRead()
        data = json.dumps(RC.cf).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)
        return 
    
    elif mode == "phone requests for setting user key":
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

        os.system("rm mylog.log")

        while True:
            data = conn_dict['Phone'].recv(1024).decode('utf-8')
            obj = json.loads(data)
            print(obj, 'msg' in obj.keys())
            if 'msg' in obj.keys():
                process.send(obj['msg'] + "\n")
                break

        process.expect(pexpect.EOF)
        print("END of set phone key")

        time.sleep(5)
        RC.reRead()
        data = json.dumps(RC.cf).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)

        return

    elif mode == "phone requests for setting user line key":

        data = {"task":"get line key","msg":"get line key"}
        data = json.dumps(data).encode('utf-8') + b'\n'

        conn_dict['Phone'].send(data)
        
        print("Waiting for user to input line key...")

        while True:
            print("here")
            data = conn_dict['Phone'].recv(1024).decode('utf-8')
            print("---" + data + "---")
            obj = json.loads(data)
            print(obj, 'msg' in obj.keys())
            if 'msg' in obj.keys():
                os.system("python ./set_config.py --user_line_key " + obj['msg'])
                print("done")
                break
        
        RC.reRead()
        data = json.dumps(RC.cf).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)

        return 

    elif mode == "phone requests for setting bluetooth threshold":
        os.system("touch mylog.log")
        process = pexpect.spawn('python set_config.py --set_bluetooth_threshold',timeout=300)
        process.logfile = open("./mylog.log","wb")
        process.expect("Please put your phone in your room, press ENTER when you're done")

        os.system("cat mylog.log")

        log_content = ""
        with open("mylog.log","r") as f:
            log_content = f.read()
        log_content += '\n'

        data = {"task":"print log","msg":"*".join(log_content.split("\n"))}
        data = json.dumps(data).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)

        while True:
            data = conn_dict['Phone'].recv(1024).decode('utf-8')
            obj = json.loads(data)
            print(obj, 'msg' in obj.keys())
            if 'msg' in obj.keys(): 
                process.send("\n")
                break

        #####################################################################################

        process.expect("Please put your phone near the door, press ENTER when you're done")

        os.system("cat mylog.log")

        log_content = ""
        with open("mylog.log","r") as f:
            log_content = f.read()
        

        data = {"task":"print log","msg":"*".join(log_content.split("\n"))}
        data = json.dumps(data).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)

        os.system("rm mylog.log")

        while True:
            data = conn_dict['Phone'].recv(1024).decode('utf-8')
            obj = json.loads(data)
            print(obj, 'msg' in obj.keys())
            if 'msg' in obj.keys(): 
                process.send("\n")
                break

        process.expect(pexpect.EOF)

        #############################################################################


        time.sleep(3)

        RC.reRead()
        print(RC.cf)
        data = json.dumps(RC.cf).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)

        return

    elif mode == "STM32_1":
        # received data: int len = sprintf(acc_json,"{\"h\":%f,\"t\":%f,\"m\":%s}",humidity,temprature,message);
        humidity, temprature, message = obj['h'], obj['t'], obj['m']
        print(State.getUserState())
        # message : {"door opening", "door closing", "door stopped"}
        if message == "door opening":
            if State.getUserState() == "Not At Home":
                RSSI = BT.detect_rssi()
                if RSSI == "can't detect key":      # Someone gets in while you're out
                    thief()
                else:
                    print("rssi start =",RSSI)      # User arrives home
                    print("message =",message)
            else:
                RSSI=BT.detect_rssi()
                if RSSI == "can't detect key":
                    State.atHome=False              # Probably something wrong, reset state to "Not at home"
        elif message == "door closing":
            if State.getUserState() == "At Home":
                RSSI = BT.detect_rssi()
                if RSSI == "at the door" : #leave home
                    conn_dict['STM32_2'].sendall("Send Outdoor Data".encode(encoding='utf8'))
                    mutex.acquire()
                    State.changeUserState()     # change to "Not at home"
                    print("in STM32_1")
                    print("out_humidity=%f  out_temprature=%f "%(out_humidity,out_temprature))
                    line_message="humidity:%d temprature:%d out door humidity:%d outdoor temprature:%d"%(humidity,temprature,out_humidity,out_temprature)
                    sendLineMessage(RC.getLineKey(),line_message)
                elif RSSI=="can't detect key":
                    State.changeUserState()
                else:
                    print("Seems it needs to do nothing")
                    '''
                    maybe:
                        Someone gets out when you're at home
                        [Needs to be corrected somewhere]
                            Error: you're at the door and going out
                    '''
            else:
                RSSI=BT.detect_rssi()
                if RSSI == "at the door" : #back to home
                    State.changeUserState()
                elif RSSI=="inside the room":       # correct state
                    State.atHome=True
                else :
                    thief()

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


