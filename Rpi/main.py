from ifttt import *
from read_config import RC
from server import *

config_path = './config.ini'
rc = RC(config_path)

HOST = rc.getSocketIP()
PORT = rc.getSocketPort()



# ret_msg = send_ifttt(rc.getIftttKey(),rc.getIftttEvent(),'0','0','0')
# print(ret_msg)
# startServer(HOST,PORT)





