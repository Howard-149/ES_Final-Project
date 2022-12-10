import argparse
import json

import os

from bt_full import *

config_path = "./config.json"
with open(config_path,"rb") as f:
    conf = json.load(f)

parser = argparse.ArgumentParser()

# section: socket info
parser.add_argument("--ip", help = "Set Socket IP", type = str)
parser.add_argument("--port", help = "Set Socket Port", type = str)

# section: user
parser.add_argument("--user_name", help = "Set User Name", type = str)
parser.add_argument("--user_phone_key", help = "Set User Phone Key", type = str)
parser.add_argument("--set_user_phone_key", help = "Set User Phone Key by choosing your device", action="store_true")
parser.add_argument("--user_ifttt_event", help = "Set User Ifttt Event", type = str)
parser.add_argument("--user_ifttt_key", help = "Set User Ifttt Key", type = str)
parser.add_argument("--user_line_key", help = "Set User Line Authorization Key", type = str)

args = parser.parse_args()

doSomething = False

def setConfig(node,key,newValue):
    global doSomething
    doSomething = True
    conf[node][key] = newValue
    with open(config_path,'w') as f:
        json.dump(conf,f)


def setUserPhoneKey():
    global doSomething
    doSomething = True

    print("Scanning for bluetooth devices:")

    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)

    number_of_devices = len(devices)

    print(number_of_devices,"devices found")
    num=0
    addrlist = []
    namelist = []
    for addr, name, device_class in devices:

        print("\n")

        print("Device number: %d" %(num))

        print("Device Name: %s" % (name))

        print("Device MAC Address: %s" % (addr))

        print("Device Class: %s" % (device_class))

        print("\n")
        addrlist.append(addr)
        namelist.append(name)
        num+=1
    if num == 0:
        print("Find no device")
        return
    key=int(input("Enter your device number: "))
    addr = addrlist[key]
    name = namelist[key]
    setConfig('user','user_name',name)
    setConfig('user','user_phone_key',addr)
    return 


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

if args.user_line_key:
    setConfig('user','user_line_key',args.user_line_key)

if args.set_user_phone_key:
    setUserPhoneKey()

if not doSomething :
    os.system("python set_config.py --h")
