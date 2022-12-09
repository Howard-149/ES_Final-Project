import bluetooth
import bluetooth
import bluetooth._bluetooth as bt
import struct
import array
import fcntl
import time
import sys

import argparse
from read_config import *

BT_ADDR=''

class BluetoothRSSI(object):
    """Object class for getting the RSSI value of a Bluetooth address.
    Reference: https://github.com/dagar/bluetooth-proximity
    """
    def __init__(self, addr):
        self.addr = addr
        self.hci_sock = bt.hci_open_dev()
        self.hci_fd = self.hci_sock.fileno()
        self.bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.bt_sock.settimeout(10)
        self.connected = False
        self.cmd_pkt = None

    def prep_cmd_pkt(self):
        """Prepares the command packet for requesting RSSI"""
        reqstr = struct.pack("6sB17s", bt.str2ba(self.addr), bt.ACL_LINK, bytes("\0" * 17,encoding='utf-8'))
        request = array.array("b", reqstr)
        handle = fcntl.ioctl(self.hci_fd, bt.HCIGETCONNINFO, request, 1)
        handle = struct.unpack("8xH14x", request.tobytes())[0]
        self.cmd_pkt = struct.pack('H', handle)

    def connect(self):
        """Connects to the Bluetooth address"""
        self.bt_sock.connect_ex((self.addr, 1))  # PSM 1 - Service Discovery
        self.connected = True

    def get_rssi(self):
        """Gets the current RSSI value.
        @return: The RSSI value (float) or None if the device connection fails
                 (i.e. the device is nowhere nearby).
        """
        try:
            # Only do connection if not already connected
            if not self.connected:
                self.connect()
            if self.cmd_pkt is None:
                self.prep_cmd_pkt()
            # Send command to request RSSI
            rssi = bt.hci_send_req(
                self.hci_sock, bt.OGF_STATUS_PARAM,
                bt.OCF_READ_RSSI, bt.EVT_CMD_COMPLETE, 4, self.cmd_pkt)
            # print(rssi)
            if rssi[0]==2:
                print("disconnected")
                self.connected=False
                return 1000
            rssi = struct.unpack('b', rssi[3].to_bytes(1, byteorder='big'))[0]
            return rssi
        except IOError:
            # Happens if connection fails (e.g. device is not in range)
            self.connected = False
            return 1000


def scan():

    print("Scanning for bluetooth devices:")

    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)

    number_of_devices = len(devices)

    print(number_of_devices,"devices found")
    num=0
    addrlist=[]

    for addr, name, device_class in devices:

        print("\n")

        print("Device number: %d" %(num))

        print("Device Name: %s" % (name))

        print("Device MAC Address: %s" % (addr))

        print("Device Class: %s" % (device_class))

        print("\n")

        addrlist.append(addr)
        num+=1
    
    key=int(input("Enter your device number: "))
    
    global BT_ADDR 
    BT_ADDR= addrlist[key]
    print("BT_ADDR = %s" %(BT_ADDR))
    return

#BT_ADDR = '78:F2:38:09:8D:5B'  # You can put your Bluetooth address here
#NUM_LOOP = 5

def print_usage():
     print  ("Usage: python test_address.py <bluetooth-address> [number-of-requests]")

def detect_rssi():
    addr=RC.getUserPhoneKey()
    btrssi = BluetoothRSSI(addr=addr)
    avg=0
    for i in range(0,10):
        # print("rssi:", btrssi.get_rssi())
        avg+=btrssi.get_rssi()
        time.sleep(0.2)
    if avg>100:
        return "can't detect key"
    elif avg>-10:
        return "inside the room"
    else:
        return "at the door"

def getUserState():
    if RC.getUserPhoneKey()=="None":
        return "can't detect key"
    return detect_rssi()


if __name__ == '__main__':
    RC.initialize()
    print(getUserState())
