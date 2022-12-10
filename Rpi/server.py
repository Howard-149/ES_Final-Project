import socket
import json
from Task import Task
from ifttt import *

def JsonLoading(conn):
    data = conn.recv(1024).decode('utf-8')
    print("Received from socket client:", data)
    if (data.count('{') != 1):
        return "Error", {}
        # choose = 0
        # buffer_data = data.split('}')
        # while buffer_data[choose][0] != '{':
        #     choose += 1
        # data = buffer_data[choose] + '}'
    obj = json.loads(data)
    if "m" in obj.keys():
        mode = "STM32_1"
    elif 'client' in obj.keys():
        if obj['client'] == 'Phone':
            mode = obj['task']
    else:
        mode = "STM32_2"
    return mode, obj

def startServer(HOST,PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            s.listen()
            print("Starting server at: ", (HOST, PORT))
            conn, addr = s.accept()
            with conn:
                print("Connected at", addr)
                print("Waiting for Task")
                while True:
                    mode, obj = JsonLoading(conn)
                    print(mode,obj)
                    if mode == "Error":
                        break
                    Task(mode, obj, conn)