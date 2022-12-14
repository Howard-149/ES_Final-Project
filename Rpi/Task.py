import os
import time
import pexpect
import json
import threading

from state import State
import bt_full as BT
from send_Line_notification import sendLineMessage
from read_config import RC
from TodoList import TodoList

mutex = threading.Lock()
mutex.acquire()
out_humidity, out_temprature=0,0


TodoList.reRead()

def thief(action):
    print("Someone get in!!!")
    print("Probably thief {} the door!!!".format(action))
    sendLineMessage(RC.getLineKey(),"Someone get in!\nProbably thief {} the door !!!".format(action),
    "https://images.twgreatdaily.com/images/image/cZM/cZM9CW8BMH2_cNUgCq82.jpg")
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
            # print("here")
            data = conn_dict['Phone'].recv(1024).decode('utf-8')
            # print("---" + data + "---")
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

        

        while True:
            data = conn_dict['Phone'].recv(1024).decode('utf-8')
            obj = json.loads(data)
            print(obj, 'msg' in obj.keys())
            if 'msg' in obj.keys(): 
                process.send("\n")
                process.expect(pexpect.EOF)
                break
        #############################################################################


        # time.sleep(3)

        RC.reRead()
        # print(RC.cf)
        data = json.dumps(RC.cf).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)
        
        os.system("cat mylog.log")
        os.system("rm mylog.log")
        return

    elif mode == "phone requests for todoList":
        with open("./todoList.json","rb") as f:
            data = json.dumps(json.load(f)).encode('utf-8') + b'\n'
            conn_dict['Phone'].send(data)
        return

    elif mode == "phone requests for adding new todo":
        TodoList.reRead()
        TodoList.addTodo(obj['data'])
        data = json.dumps(TodoList.todoList).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)
        return

    elif mode == "phone requests for deleting todo at index i":
        TodoList.reRead()
        TodoList.deleteTodo(int(obj['index']))
        data = json.dumps(TodoList.todoList).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)
        return

    elif mode == "phone requests for editing todo of id i":
        TodoList.reRead()
        TodoList.editTodo(obj['id'],obj['data'])
        data = json.dumps(TodoList.todoList).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)

    elif mode == "phone requests for changing status of id i":
        TodoList.reRead()
        TodoList.changeStatus(obj['id'],obj['status'])
        
    

    elif mode == "STM32_1":
        # received data: int len = sprintf(acc_json,"{\"h\":%f,\"t\":%f,\"m\":%s}",humidity,temprature,message);
        humidity, temprature, message = obj['h'], obj['t'], obj['m']
        print(State.getUserState())
        # message : {"door opening", "door closing", "door stopped"}
        if message == "door opening":
            if State.getUserState() == "Not At Home":
                RSSI = BT.detect_rssi()
                if RSSI == "can't detect key":      # Someone gets in while you're out
                    thief("open")
                # else:
                    # print("rssi start =",RSSI)      # User arrives home
                    # print("message =",message)
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
                    line_message = "[INDOOR]\n    humidity:{}\n    temprature:{}\n[OUTDOOR]\n    humidity:{}\n    temprature:{}\n".format(humidity,temprature,out_humidity,out_temprature)
                    if out_humidity >= 50:  line_message += "\nPlease remember to bring the umbrella with you^^\n"
                    sendLineMessage(RC.getLineKey(),line_message)
                    #############################no test##############################
                    TodoList.reRead()
                    
                    line_message="Todo-List : \n"
                    for todo in TodoList.todoList:
                        if todo["status"] == "0":
                            line_message += "    ???  "
                        elif todo["status"] == "1":
                            line_message += "    ???  "
                        
                        line_message += todo["task"]
                        line_message += "\n"
                    
                        
                    sendLineMessage(RC.getLineKey(),line_message)
                    ###################################################################
                elif RSSI=="can't detect key":
                    State.changeUserState()
                # else:
                    # print("Seems it needs to do nothing")
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
                    thief("close")

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


