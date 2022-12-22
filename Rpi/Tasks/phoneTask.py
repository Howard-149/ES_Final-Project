import os
import time
import pexpect
import json

from read_config import RC

def phoneTask(mode, obj, conn_dict):
    if mode == "phone requests for config":
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

        time.sleep(2)

        print("done")
        conn_dict['Phone'].send(json.dumps({"task":"done"}).encode('utf-8')+b'\n')

        RC.reRead()
        print(RC.cf)
        data = json.dumps(RC.cf).encode('utf-8') + b'\n'
        conn_dict['Phone'].send(data)

        return