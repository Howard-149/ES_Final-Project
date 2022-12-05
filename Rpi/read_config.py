# [reference] https://iter01.com/539736.html

import configparser

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