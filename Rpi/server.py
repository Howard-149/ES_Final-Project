import socket
import json
from Task import Task
from ifttt import *

def JsonLoading(conn):
    data = conn.recv(1024).decode('utf-8')
    print("Received from socket server:", data)
    if (data.count('{') != 1):
        choose = 0
        buffer_data = data.split('}')
        while buffer_data[choose][0] != '{':
            choose += 1
        data = buffer_data[choose] + '}'
    obj = json.loads(data)
    if "m" in obj.keys():
        mode = "STM32_1"
    else:
        mode = "STM32_2"
    return mode, obj

def startServer(HOST,PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Starting server at: ", (HOST, PORT))
        conn, addr = s.accept()
        with conn:
            print("Connected at", addr)
            print("Waiting for Task")
            while True:
                mode, obj = JsonLoading(conn)
                Task(mode, obj)