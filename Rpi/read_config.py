# [reference] https://iter01.com/539736.html

import configparser
import json
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
    def initialize(config_path = "./config.json"):
        RC.reRead(config_path)

    @staticmethod
    def reRead(config_path = "./config.json"):
        with open("./config.json","rb") as f:
            RC.cf = json.load(f)

    # Get Socket Information

    @staticmethod
    def getSocketIP():
        return RC.cf['socket info']['ip']
    
    @staticmethod
    def getSocketPort():
        return int(RC.cf['socket info']['port'])

    @staticmethod
    def getRawSocketPort():
        return RC.cf['socket info']['port']

    # Get Bluetooth Information

    @staticmethod
    def getRSSIThreshold():
        return RC.cf['bluetooth']['rssi_threshold']

    # Get User Information

    @staticmethod
    def getUserName():
        return RC.cf['user']['user_name']

    @staticmethod
    def getUserPhoneKey():
        return RC.cf['user']['user_phone_key']

    @staticmethod
    def getIftttEvent():
        return RC.cf['user']['user_ifttt_event']

    @staticmethod
    def getIftttKey():
        return RC.cf['user']['user_ifttt_key']

    @staticmethod
    def getLineKey():
        return RC.cf['user']['user_line_key']

    @staticmethod
    def check():

        RC.reRead()
        checking = True

        print('\n\n')

        if RC.getSocketIP() == "None":
            checking = False
            setconfig_usage("ip","ip","XXX.XXX.XXX.XXX")

        if RC.getRawSocketPort() == "None":
            checking = False
            setconfig_usage("port","port","[Int]")

        if RC.getUserPhoneKey() == "None":
            checking = False
            print("Please set config [{}] first".format("phone MAC address"))
            print("command:")
            print("     python set_config.py --{}".format("set_user_phone_key"))
            print("     python set_config.py --{} {}".format("user_phone_key","[Your phone MAC address]"))

        if RC.getLineKey() == "None":
            checking = False
            setconfig_usage("Line authorization key","user_line_key","[Your Line authorization key]")
        
        if not checking:
            print("######################################################################")
            print("More information for setting config :")
            os.system('python set_config.py --help')
        

        return checking




if __name__ == '__main__':
    os.system("jq . ./config.json")