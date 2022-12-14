import socket
import json
from threading import Thread
import time
from Task import Task
from ifttt import *


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
conn_dict={}
addr_dict={}


def accept_client():
    while True:    
        conn, addr = s.accept()
        print("Connected at", addr)
        data = conn.recv(1024).decode('utf-8')
        print("Received from socket client:", data)
        if (data.count('{') != 1):
            print("error in json data")
        obj = json.loads(data)
        if obj['client']=='STM32_1':
            conn_dict['STM32_1']=conn
            addr_dict['STM32_1']=addr
            thread=Thread(target=message_handle, args=(conn_dict['STM32_1'],addr_dict['STM32_1']))
            thread.setDaemon(True)
            thread.start()
        elif obj['client']=='STM32_2':
            conn_dict['STM32_2']=conn
            addr_dict['STM32_2']=addr
            thread=Thread(target=message_handle, args=(conn_dict['STM32_2'],addr_dict['STM32_2']))
            thread.setDaemon(True)
            thread.start()
        elif obj['client']=='Phone':
            conn_dict['Phone']=conn
            addr_dict['Phone']=addr
            continue
        else:
            print('error')

def JsonLoading(conn):
    data = conn.recv(1024).decode('utf-8')
    if len(data) == 0 :
        # s.close()
        print('client closed connection.')
        return "Error",{}
    
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
        # conn_dict['STM32_2'].sendall("Send Outdoor Data".encode(encoding='utf8'))
    elif 'client' in obj.keys():
        if obj['client'] == 'Phone':
            mode = obj['task']
    else:
        mode = "STM32_2"
    return mode, obj

def message_handle(conn,addr):
    # print("Connected at", addr)
    print("Waiting for Task")
    while True:
        mode, obj = JsonLoading(conn)
        print(mode,obj)
        if mode == "Error":
            break
        thread=Thread(target=Task, args=(mode,obj,conn_dict))
        thread.setDaemon(True)
        thread.start()



def startServer(HOST,PORT):
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    global s
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print("Starting server at: ", (HOST, PORT)) 
        # s.bind((HOST, PORT))
        # while True:
            # s.listen()
            # print("Starting server at: ", (HOST, PORT))
    thread=Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    while True:
        time.sleep(0.1)
            # conn, addr = s.accept()
            # with conn:




