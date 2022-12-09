# [reference] https://iter01.com/539736.html

import configparser
import os

def setconfig_usage(parameter_name, parameter, example):
    print("Please set config [{}] first".format(parameter_name))
    print("command:")
    print("     python set_config.py --{} {}".format(parameter,example))
    return 

def setconfig_usage(parameter_name, parameter):
    print("Please set config [{}] first".format(parameter_name))
    print("command:")
    print("     python set_config.py --{}".format(parameter))

class RC:
    
    cf = None

    @staticmethod
    def initialize(config_path = "./config.ini"):
        RC.reRead(config_path)

    @staticmethod
    def reRead(config_path = "./config.ini"):
        RC.cf = configparser.ConfigParser()
        RC.cf.read(config_path)

    # Get Socket Information

    @staticmethod
    def getSocketIP():
        return RC.cf.get('socket info', 'ip')
    
    @staticmethod
    def getSocketPort():
        return int(RC.cf.get('socket info', 'port'))

    @staticmethod
    def getRawSocketPort():
        return int(RC.cf.get('socket info', 'port'))

    # Get Bluetooth Information

    @staticmethod
    def getRSSIThreshold():
        return int(RC.cf.get('bluetooth', 'rssi_threshold'))

    # Get User Information

    @staticmethod
    def getUserName():
        return RC.cf.get('user','user_name')

    @staticmethod
    def getUserPhoneKey():
        return RC.cf.get('user','user_phone_key')

    @staticmethod
    def getIftttEvent():
        return RC.cf.get('user','user_ifttt_event')

    @staticmethod
    def getIftttKey():
        return RC.cf.get('user','user_ifttt_key')

    @staticmethod
    def getLineKey():
        return RC.cf.get('user','user_line_key')

    @staticmethod
    def check():
        RC.reRead()
        checking = True

        

        if RC.getSocketIP() == "None":
            checking = False
            setconfig_usage("ip","ip","XXX.XXX.XXX.XXX")

        if RC.getRawSocketPort() == "None":
            checking = False
            setconfig_usage("port","port","[Int]")

        if RC.getUserPhoneKey() == "None":
            checking = False
            setconfig_usage("phone MAC address","set_user_phone_key")

        if RC.getLineKey() == "None":
            checking = False
            setconfig_usage("Line authorization key","user_line_key","[Your Line authorization key]")
        


        return checking




if __name__ == '__main__':
    os.system("cat ./config.ini")