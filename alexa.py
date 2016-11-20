#!/usr/bin/env python3

import alexandra
import skyremote

app = alexandra.Application()

@app.launch
def launch_handler():
    return alexandra.reprompt('What would you like to do?')

@app.intent('Pause')
def pause_intent(slots, session):
    skyremote.press(stbip, "pause")
    return alexandra.respond("Pausing")

@app.intent('Play')
def play_intent(slots, session):
    skyremote.press(stbip, "play")
    return alexandra.respond("Playing")

@app.intent('Channel')
def channel_intent(slots, session):
    print(slots['channelToSet'])
    response = skyremote.channel(stbip, slots['channelToSet'])
    return alexandra.respond(response)

if __name__ == '__main__':
    stbip = skyremote.findstb()
    app.run('0.0.0.0', 8080, debug=True)