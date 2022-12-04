import socket
import json
import numpy as np
import matplotlib.pyplot as plot

# class RingBuffer:
#     def __init__(self,size_max):
#         self.max = size_max
#         self.data = []

#     class __Full: 
#         def append(self, x):
#             self.data[self.cur] = x
#             self.cur = (self.cur+1) % self.max
#         def get(self):
#             return self.data[self.cur:]+self.data[:self.cur]

#     def append(self,x):
#         self.data.append(x)
#         if len(self.data) == self.max:
#             self.cur = 0
#             self.__class__ = self.__Full

#     def get(self):
#         return self.data

HOST = '' # IP address
PORT = 6533 # Port to listen on (use ports > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Starting server at: ", (HOST, PORT))
    conn, addr = s.accept()
    # RBX=RingBuffer(10)
    # RBY=RingBuffer(10)
    # RBZ=RingBuffer(10)
    # RBGX=RingBuffer(10)
    # RBGY=RingBuffer(10)
    # RBGZ=RingBuffer(10)
    # RBT=RingBuffer(10)
    with conn:
        print("Connected at", addr)
        # f=plot.figure() 
        while True:
            data = conn.recv(1024).decode('utf-8')
            print("Received from socket server:", data)
            if (data.count('{') != 1):
            # Incomplete data are received.
                choose = 0
                buffer_data = data.split('}')
                while buffer_data[choose][0] != '{':
                    choose += 1
                data = buffer_data[choose] + '}'

            obj = json.loads(data)
            print(obj)
            message=obj['m']
            temprature=obj['t']
            humidity=obj['h']
            # t = obj['s']
            # x=obj['x']
            # y=obj['y']
            # z=obj['z']
            # gx=obj['gx']
            # gy=obj['gy']
            # gz=obj['gz']
            # message=obj['m']
            # RBX.append(x)
            # RBY.append(y)
            # RBZ.append(z)
            # RBGX.append(gx)
            # RBGY.append(gy)
            # RBGZ.append(gz)
            # RBT.append(t)
            # f.clear()
            # ax = f.subplots(2,3,sharex='col',sharey='row')
            # ax[0][0].scatter(RBT.get(), RBX.get(), c='blue')
            # print(RBT.get())
            # ax[0][1].scatter(RBT.get(), RBY.get(), c='c')
            # ax[0][2].scatter(RBT.get(), RBZ.get(), c='g')
            # ax[1][0].scatter(RBT.get(), RBGX.get(), c='k')
            # ax[1][1].scatter(RBT.get(), RBGY.get(), c='m')
            # ax[1][2].scatter(RBT.get(), RBGZ.get(), c='r') 
            # name_list=['ax','ay','az','gx','gy','gz']
            # for i in range(2): 
            #     for j in range(3):
            #         ax[i][j].set_xlabel("sample num")
            #         ax[i][j].legend([name_list[3*i+j]])
            # f.canvas.draw()
            # f.canvas.flush_events()
            # plot.pause(0.5)