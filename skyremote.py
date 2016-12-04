#!/usr/bin/env python3

import ssdp
import sys
import socket
import math
import time

# Global for debugging.
DEBUG = True
# Set True for Sky Q
Q = False

# Define the command codes for the buttons.
button = {
    'power': 0,
    'select': 1,
    'backup': 2,
    'dismiss': 2,
    'channelup': 6,
    'channeldown': 7,
    'interactive': 8,
    'sidebar': 8,
    'help': 9,
    'services': 10,
    'search': 10,
    'tvguide': 11,
    'home': 11,
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

channels = {
    "bbc one": ["1", "0", "1"],
    "bbc 1": ["1", "0", "1"],
    "bbc two": ["1", "0", "2"],
    "bbc 2": ["1", "0", "2"],
    "sky one": ["1", "0", "6"],
    "sky 1": ["1", "0", "6"],
    "sky atlantic": ["1", "0", "8"],
    "w": ["1", "0", "9"],
    "gold": ["1", "1", "0"],
    "dave": ["1", "1", "1"],
    "comedy central": ["1", "1", "2"],
    "universal": ["1", "1", "3"],
    "scyfy": ["1", "1", "4"],
    "sci fi": ["1", "1", "4"],
    "scy fi": ["1", "1", "4"],
    "sigh fi": ["1", "1", "4"],
    "sigh five": ["1", "1", "4"],
    "bbc one": ["1", "1", "5"],
    "bbc 1": ["1", "1", "5"],
    "bbc four": ["1", "1", "6"],
    "bbc 4": ["1", "1", "6"],
    "london live": ["1", "1", "7"],
    "itv 2": ["1", "1", "8"],
    "itv two": ["1", "1", "8"],
    "itv 3": ["1", "1", "9"],
    "itv three": ["1", "1", "9"],
    "itv 4": ["1", "2", "0"],
    "itv four": ["1", "2", "0"],
    "sky arts": ["1", "2", "1"],
    "sky living": ["1", "2", "2"],
    "itv encore": ["1", "2", "3"],
    "eye tv encore": ["1", "2", "3"],
    "fox": ["1", "2", "4"],
    "tlc": ["1", "2", "5"],
    "tea l c": ["1", "2", "5"],
    "tea l see": ["1", "2", "5"],
    "mtv": ["1", "2", "6"],
    "em tea vee": ["1", "2", "6"],
    "comedy central extra": ["1", "2", "8"],
    "sky two": ["1", "2", "9"],
    "sky 2": ["1", "2", "9"],
    "sky 1 + 1": ["1", "3", "0"],
    "sky 1 plus 1": ["1", "3", "0"],
    "sky one plus 1": ["1", "3", "0"],
    "sky one plus one": ["1", "3", "0"],
    "sky 1 plus one": ["1", "3", "0"],
    "itv 1 plus 1": ["1", "3", "1"],
    "itv 1 plus one": ["1", "3", "1"],
    "itv one plus one": ["1", "3", "1"],
    "itv one plus 1": ["1", "3", "1"],
    "alibi": ["1", "3", "2"],
    "good food": ["1", "3", "3"],
    "s4c": ["1", "3", "4"],
    "s four c": ["1", "3", "4"],
    "s four see": ["1", "3", "4"],
    "ess four see": ["1", "3", "4"],
    "channel 4 + 1": ["1", "3", "5"],
    "channel four plus one": ["1", "3", "5"],
    "channel 4 plus one": ["1", "3", "5"],
    "channel 4 plus 1": ["1", "3", "5"],
    "e 4 hd": ["1", "3", "6"],
    "e four hd": ["1", "3", "6"],
    "e 4 h d": ["1", "3", "6"],
    "e four h d": ["1", "3", "6"],
    # Gaps
    "bbc two england": ["1", "4", "1"],
    "bbc two alba": ["1", "4", "1"],
    "quest": ["1", "4", "4"],
    "challenge": ["1", "4", "5"],
    "cbs reality": ["1", "4", "6"],
    "cbs reality plus one": ["1", "4", "7"],
    "cbs reality plus 1": ["1", "4", "7"],
    "cbs reality + one": ["1", "4", "7"],
    "cbs reality + 1": ["1", "4", "7"],
    "cbs action": ["1", "4", "8"],
    "cbs drama": ["1", "4", "9"],
    "universal plus one": ["1", "5", "0"],
    "universal + one": ["1", "5", "0"],
    "universal plus 1": ["1", "5", "0"],
    "universal + 1": ["1", "5", "0"],
    "e": ["1", "5", "1"],
    "pick": ["1", "5", "2"],
    "viceland": ["1", "5", "3"],
    "tlc": ["1", "5", "4"],
    "tea l see": ["1", "5", "4"],
    "really": ["1", "5", "5"],
    "lifetime": ["1", "5", "6"],
    "sony": ["1", "5", "7"],
    "drama": ["1", "5", "8"],
    "spike": ["1", "6", "0"],
    "pick + 1": ["1", "6", "3"],
    "pick plus 1": ["1", "6", "3"],
    "pick + one": ["1", "6", "3"],
    "pick plus one": ["1", "6", "3"],
    # Gaps
    "dmax": ["1", "6", "7"],
    "sky atlantic + 1": ["1", "7", "0"],
    "sky atlantic plus 1": ["1", "7", "0"],
    "five": ["1", "7", "1"],
    "real lives": ["1", "7", "2"],
    "real lives + 1": ["1", "7", "3"],
    "real lives + one": ["1", "7", "3"],
    "real lives plus 1": ["1", "7", "3"],
    "real lives plus one": ["1", "7", "3"],
    "5 usa": ["1", "7", "4"],
    "five usa": ["1", "7", "4"],
    "my five": ["1", "7", "5"],
    "my 5": ["1", "7", "5"],
    "5 star": ["1", "7", "6"],
    "five star": ["1", "7", "6"],
    "5 plus 1": ["1", "7", "7"],
    "five plus 1": ["1", "7", "7"],
    "5 plus one": ["1", "7", "7"],
    "five plus one": ["1", "7", "7"],
    "itv": ["1", "7", "8"],
    "true entertainment": ["1", "8", "3"],
    "true crime": ["1", "8", "5"],
    "bet": ["1", "8", "7"],
    "propeller": ["1", "8", "9"],
    "irish": ["1", "9", "1"],
    "irish tv": ["1", "9", "1"],
    "a m c": ["1", "9", "2"],
    # Gaps
    "home": ["1", "9", "6"],
    "lifetime + 1": ["1", "9", "7"],
    "lifetime + one": ["1", "9", "7"],
    "lifetime plus 1": ["1", "9", "7"],
    "lifetime plus one": ["1", "9", "7"],
    "true tv": ["1", "9", "8"],
    "your tv": ["1", "9", "9"],
    "channel 4": ["2", "2", "7"],
    "channel four": ["2", "2", "7"],
    "channel 4": ["2", "2", "7"],
    "channel four": ["2", "2", "7"],
    "a i t": ["2", "3", "2"],
    "lifetime": ["2", "3", "6"],
    "home and leisure": ["2", "3", "7"],
    "property": ["2", "3", "8"],
    "property tv": ["2", "3", "8"],
    "home and health": ["2", "4", "0"],
    "home and health plus one": ["2", "4", "1"],
    "discovery shed": ["2", "4", "2"],
    "good food plus 1": ["2", "4", "3"],
    "good food plus one": ["2", "4", "3"],
    "good food + one": ["2", "4", "3"],
    "good food + 1": ["2", "4", "3"],
    "home plus 1": ["2", "4", "4"],
    "home plus one": ["2", "4", "4"],
    "home + one": ["2", "4", "4"],
    "home food + 1": ["2", "4", "4"],
    "travel": ["2", "4", "9"],
    "travel plus one": ["2", "5", "1"],
    "travel plus 1": ["2", "5", "1"],
    "travel + one": ["2", "5", "1"],
    "travel + 1": ["2", "5", "1"],
    "wellbeing": ["2", "5", "2"],
    "horse and country": ["2", "5", "3"],
    "holiday and cruise": ["2", "5", "6"],
    "holiday and cruise tv": ["2", "5", "6"],
    "fashion 1": ["2", "5", "7"],
    "fashion one": ["2", "5", "7"],
    "fashion 1": ["2", "5", "7"],
    "showcase 3": ["2", "6", "1"],
    "show case 3": ["2", "6", "1"],
    "showcase three": ["2", "6", "1"],
    "show case three": ["2", "6", "1"],
    "forces tv": ["2", "6", "4"],
    "show biz": ["2", "6", "6"],
    "showbiz": ["2", "6", "6"],
    "sky premiere": ["3", "0", "1"],
    "sky premiere plus 1": ["3", "0", "2"],
    "sky cinema plus one": ["3", "0", "2"],
    "sky cinema christmas": ["3", "0", "3"],
    "sky cinema greats": ["3", "0", "4"],
    "sky cinema disney": ["3", "0", "5"],
    "sky cinema family": ["3", "0", "6"],
    "sky cinema action and adventure": ["3", "0", "7"],
    "sky cinema action": ["3", "0", "7"],
    "sky cinema comedy": ["3", "0", "8"],
    "sky cinema thriller": ["3", "0", "9"],
    "sky cinema hits": ["3", "1", "0"],
    "sky cinema sci fi and horror": ["3", "1", "1"],
    "sky cinema select": ["3", "1", "2"],
    "film four": ["3", "1", "5"],
    "film four plus one": ["3", "1", "6"],
    "film four plus 1": ["3", "1", "6"],
    "tcm": ["3", "1", "7"],
    "tcm plus one": ["3", "1", "8"],
    "horror": ["3", "1", "9"],
    "horror plus one": ["3", "1", "9"],
    "sony movie": ["3", "2", "3"],
    "sony movie channel": ["3", "2", "3"],
    "sony movie plus one": ["3", "2", "4"],
    "sony movie channel plus one": ["3", "2", "4"],
    "movies 4 men": ["3", "2", "5"],
    "movies 4 men plus one": ["3", "2", "5"],
    "movies four men": ["3", "2", "5"],
    "movies four men plus one": ["3", "2", "5"],
    "christmas twenty four": ["3", "2", "7"],
    "christmas 24": ["3", "2", "7"],
    "christmas twenty four plus one": ["3", "2", "8"],
    "christmas 24 plus one": ["3", "2", "8"],
    "nollywood movies": ["3", "2", "9"],
    "mtv music": ["3", "5", "0"],
    "mtv base": ["3", "5", "1"],
    "mtv hits": ["3", "5", "2"],
    "viva": ["3", "5", "3"],
    "mtv dance": ["3", "5", "4"],
    "mtv rocks": ["3", "5", "5"],
    "mtv christmas": ["3", "5", "6"],
    "vh1": ["3", "5", "7"],
    "v h 1": ["3", "5", "7"],
    "v h one": ["3", "5", "7"],
    "four music": ["3", "6", "2"],
    "kiss": ["3", "6", "3"],
    "magic": ["3", "6", "4"],
    "chart show": ["3", "6", "5"],
    "the vault": ["3", "6", "6"],
    "scuzz": ["3", "6", "7"],
    "kerrang": ["3", "6", "8"],
    "vintage": ["3", "6", "9"],
    "chilled": ["3", "7", "0"],
    "stars": ["3", "7", "1"],
    "chart show hits": ["3", "7", "2"],
    "flava": ["3", "7", "4"],
    "clubland": ["3", "8", "3"],
    "sky sports one": ["4", "0", "1"],
    "sky sports 1": ["4", "0", "1"],
    "sky sports two": ["4", "0", "2"],
    "sky sports 2": ["4", "0", "2"],
    "sky sports three": ["4", "0", "3"],
    "sky sports 3": ["4", "0", "3"],
    "sky sports four": ["4", "0", "4"],
    "sky sports 4": ["4", "0", "4"],
    "sky sports five": ["4", "0", "5"],
    "sky sports 5": ["4", "0", "5"],
    "sky sports news": ["4", "0", "6"],
    "sky sports mix": ["4", "0", "7"],
    "sky sports f1": ["4", "0", "8"],
    "euro sport 1": ["4", "1", "0"],
    "euro sport one": ["4", "1", "0"],
    "eurosport 1": ["4", "1", "0"],
    "eurosport one": ["4", "1", "0"],
    "euro sport two": ["4", "1", "1"],
    "euro sport 2": ["4", "1", "1"],
    "eurosport 2": ["4", "1", "1"],
    "eurosport two": ["4", "1", "1"],
    "bt sport 1": ["4", "2", "7"],
    "b t sport 1": ["4", "2", "7"],
    "bt sport one": ["4", "2", "7"],
    "b t sport one": ["4", "2", "7"],
    "bt sport 2": ["4", "3", "3"],
    "b t sport 2": ["4", "3", "3"],
    "bt sport two": ["4", "3", "3"],
    "b t sport two": ["4", "3", "3"],
    "at the races": ["4", "1", "5"],
    "bt sport 3": ["4", "1", "6"],
    "b t sport 3": ["4", "1", "6"],
    "bt sport three": ["4", "1", "6"],
    "b t sport three": ["4", "1", "6"],
    "espn": ["4", "2", "6"],
    "e s p n": ["4", "2", "6"],
    "box nation": ["4", "9", "0"],
    "bike": ["4", "6", "4"],
    "front runner": ["4", "6", "8"],
    "ginx": ["4", "7", "8"],
    "jinx": ["4", "7", "0"],
    "sky sports box office": ["4", "9", "2"],
    "sky news": ["5", "0", "1"],
    "bloomberg": ["5", "0", "2"],
    "bloom berg": ["5", "0", "2"],
    "bbc news": ["5", "0", "3"],
    "bbc parliament": ["5", "0", "4"],
    "cnbc": ["5", "0", "5"],
    "see nbc": ["5", "0", "5"],
    "sea nbc": ["5", "0", "5"],
    "sea n b c": ["5", "0", "5"],
    "see n b c": ["5", "0", "5"],
    "see n n": ["5", "0", "6"],
    "c n n": ["5", "0", "6"],
    "nhk world": ["5", "0", "7"],
    "n h k world": ["5", "0", "7"],
    "euronews": ["5", "0", "8"],
    "euro news": ["5", "0", "8"],
    "fox news": ["5", "0", "9"],
    "n d t v": ["5", "1", "2"],
    "andy tv": ["5", "1", "2"],
    "russia today": ["5", "1", "2"],
    "france 24": ["5", "1", "3"],
    "france twenty four": ["5", "1", "3"],
    "france twentyfour": ["5", "1", "3"],
    "al jazeera": ["5", "1", "4"],
    "aljazeera": ["5", "1", "4"],
    "discovery": ["5", "2", "0"],
    "discovery plus one": ["5", "2", "1"],
    "i d": ["5", "2", "2"],
    "eye dee": ["5", "2", "2"],
    # Gaps
    "national geographic": ["5", "2", "6"],
    "national geographic wild": ["5", "2", "8"],
    "history": ["5", "2", "9"],
    "history plus one": ["5", "3", "0"],
    "history two": ["5", "3", "1"],
    "cartoon netowork": ["6", "0", "1"],
    "nickelodeon": ["6", "0", "4"],
    "nickel odeon": ["6", "0", "4"],
    "nickle odeon": ["6", "0", "4"],
    "nickelodeon plus one": ["6", "0", "5"],
    "nickel odeon plus one": ["6", "0", "5"],
    "nickle odeon plus one": ["6", "0", "5"],
    "disney xd": ["6", "0", "7"],
    "disney xd plus one": ["6", "0", "8"],
    "disney junior": ["6", "1", "1"],
    "see beebies": ["6", "1", "4"],
    "c beebies": ["6", "1", "4"],
    "cbbs": ["6", "1", "4"],
    "nick junior": ["6", "1", "5"],
    "pop": ["6", "1", "6"],
    "tinypop": ["6", "1", "7"],
    "nick junior two": ["6", "2", "0"],
    "nick junior 2": ["6", "2", "0"],
    "citv": ["6", "2", "1"],
    "see itv": ["6", "2", "1"],
    "sea itv": ["6", "2", "1"],
    "bbc red button": ["9", "8", "0"]
}


def press(stbaddr, b):

    if Q:
        port = 5900
    else:
        port = 49500
    # Open the socket
    sock = socket.create_connection((stbaddr, port))

    # Expect banner for Sky+
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

def channel(stbaddr, c):
    try:
        buttons = channels[c.lower()]
    except KeyError:
        print("Error: No Channel " + c.lower())
        try:
            buttons = channels[c.lower().lstrip("channel ")]
        except KeyError:
            print("Error: Still no channel stripping channel from start")
            return("Sorry, I don't know channel " + c)

    for button in buttons:
        press(stbaddr, button)
        time.sleep(0.1)

    return ("Setting channel to " + c)


def findstb():
    # Use SSDP to discover the set top box.
    stbip = ''
    services = ssdp.discover("urn:schemas-nds-com:service:SkyRemote:1")

    if (services):
        for service in (x for x in services if x.st == "urn:schemas-nds-com:service:SkyRemote:1"):
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
