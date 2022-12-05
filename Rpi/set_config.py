import argparse
import configparser
import numpy as np
import copy

conf = configparser.ConfigParser()
config_path = "config.ini"
conf.read(config_path)

parser = argparse.ArgumentParser()

# section: socket info
parser.add_argument("--ip", help = "Set Socket IP", type = str)
parser.add_argument("--port", help = "Set Socket Port", type = str)

# section: user
parser.add_argument("--user_name", help = "Set User Name", type = str)
parser.add_argument("--user_phone_key", help = "Set User Phone Key", type = str)
parser.add_argument("--user_ifttt_event", help = "Set User Ifttt Event", type = str)
parser.add_argument("--user_ifttt_key", help = "Set User Ifttt Key", type = str)

args = parser.parse_args()

def setConfig(node,key,newValue):
    conf.set(node, key, newValue)
    fh = open(config_path, 'w')
    conf.write(fh)
    fh.close()

if args.ip:
    setConfig('socket info','ip',args.ip)
    
if args.port:
    setConfig('socket info','port',args.port)

if args.user_name:
    setConfig('user','user_name',args.user_name)

if args.user_phone_key:
    setConfig('user','user_phone_key',args.user_phone_key)

if args.user_ifttt_event:
    setConfig('user','user_ifttt_event',args.user_ifttt_event)

if args.user_ifttt_key:
    setConfig('user','user_ifttt_key',args.user_ifttt_key)