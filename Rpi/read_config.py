# [reference] https://iter01.com/539736.html

import configparser
import os

class RC:
    
    cf = None

    @staticmethod
    def initialize(config_path = "./config.ini"):
        RC.reRead(config_path)

    @staticmethod
    def reRead(config_path = "./config.ini"):
        RC.cf = configparser.ConfigParser()
        RC.cf.read(config_path)
        print(RC.cf.sections())

    # Get Socket Information

    @staticmethod
    def getSocketIP():
        return RC.cf.get('socket info', 'ip')
    
    @staticmethod
    def getSocketPort():
        return int(RC.cf.get('socket info', 'port'))

    # Get Bluetooth Information

    @staticmethod
    def getRSSIThreshold():
        return [int(i) for i in RC.cf.get('bluetooth', 'rssi_threshold').split(',')]

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


if __name__ == '__main__':
    os.system("cat ./config.ini")