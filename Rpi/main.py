from read_config import RC
from state import State
from server import startServer
from Task import Task

# config_path = './config.ini'

RC.initialize()

State.changeUserState()

HOST = RC.getSocketIP()
PORT = RC.getSocketPort()

startServer(HOST,PORT)





