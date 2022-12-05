# [reference] https://iter01.com/539736.html

import configparser

class RC:
    def __init__(self, config_path = "./config.ini"):
        self.reRead(config_path)

    def reRead(self,config_path = "./config.ini"):
        self.cf = configparser.ConfigParser()
        self.cf.read(config_path)

    # Get Socket Information

    def getSocketIP(self):
        return self.cf.get('socket info', 'ip')

    def getSocketPort(self):
        return int(self.cf.get('socket info', 'port'))

    # Get User Information

    def getUserName(self):
        return self.cf.get('user','user_name')

    def getUserPhoneKey(self):
        return self.cf.get('user','user_phone_key')

    def getIftttEvent(self):
        return self.cf.get('user','user_ifttt_event')

    def getIftttKey(self):
        return self.cf.get('user','user_ifttt_key')