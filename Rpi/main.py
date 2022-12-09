from read_config import RC
from state import State
from server import startServer
from Task import Task

# config_path = './config.ini'

if __name__ == '__main__':
    RC.initialize()
    if not RC.check():
        exit(1)

    State.changeUserState()

    HOST = RC.getSocketIP()
    PORT = RC.getSocketPort()

    startServer(HOST,PORT)






