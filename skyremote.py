#!/usr/bin/env python3

import ssdp
import sys
import socket
import math

# Global for debugging.
DEBUG = False

# Define the command codes for the buttons.
button = {
    'power': 0,
    'select': 1,
    'backup': 2,
    'channelup': 6,
    'channeldown': 7,
    'interactive': 8,
    'help': 9,
    'services': 10,
    'tvguide': 11,
    'i': 14,
    'text': 15,
    'up': 16,
    'down': 17,
    'left': 18,
    'right': 19,
    'red': 32,
    'green': 33,
    'yellow': 34,
    'blue': 35,
    '0': 48,
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57,
    'play': 64,
    'pause': 65,
    'stop': 66,
    'record': 67,
    'fastforward': 69,
    'rewind': 71,
    'boxoffice': 240,
    'sky': 241
}


def press(stbaddr, b):
    # Open the socket
    sock = socket.create_connection((stbaddr, 49160))

    # Expect banner
    data = sock.recv(4096)
    if (DEBUG):
        print ("RECV: ", data)

    # Send the banner
    data = "SKY 000.001\n".encode('ASCII')
    if (DEBUG):
        print("SENT: ", data)
    sock.sendall(bytes(data))

    # Expect two zeroes
    data = sock.recv(4096)
    if (DEBUG):
        print ("RECV: ", data)

    # Send a zero
    data = b'\x01'
    if (DEBUG):
        print("SENT: ", data)
    sock.sendall(data)

    # Expect four zeroes
    data = sock.recv(4096)
    if (DEBUG):
        print ("RECV: ", data)

    # Send a zero
    data = b'\x00'
    if (DEBUG):
        print("SENT: ", data)
    sock.sendall(data)

    # Expect 24 zeroes
    data = sock.recv(4096)
    if (DEBUG):
        print ("RECV: ", data)

    # Send actual command
    code = button[b]
    data1 = [4, 1, 0, 0, 0, 0, math.floor(224 + (code / 16)), code % 16]
    data2 = [4, 0, 0, 0, 0, 0, math.floor(224 + (code / 16)), code % 16]

    if (DEBUG):
        print("SENT:", data1)
    sock.sendall(bytes(data1))
    if (DEBUG):
        print("SENT:", data2)
    sock.sendall(bytes(data2))
    sock.close()

def findstb():
    # Use SSDP to discover the set top box.
    stbip = ''
    services = ssdp.discover("urn:schemas-nds-com:service:SkyRemote:1")

    if (services):
        for service in services:
            stbip = service.location.split('//')[1].split(':')[0]
            if (DEBUG):
                print("Found a Set Top Box at: " + stbip)
    return stbip

def main():
    stbip = findstb()
    for button in sys.argv[1:]:
        press(stbip, button)

if __name__ == '__main__':
    main()
