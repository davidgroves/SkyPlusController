Usage.
======

Run this on a machine on the same LAN as a Sky Set Top Box.

Examples :-

```
# Set the channel to Sky Sports 1 HD.
$ ./skyremote.py 4 0 1

# Pause the TV
$ ./skyremote.py pause
```

For the full set of controls, look at the button dict in the code.

How it Works.
=============

The Sky box multicast SSDP packets announcing it's existence. Then
you can find the services via URI's like :-

- http://skyboxip:49153/description5.xml
- You must set your user agent as "SKY_skyplus" or it will ignore you.
- But this isn't actually needed to control the box, just to parse
the xml 

I reverse engineered the protocol from wireshark pcaps based on the
ipad app to make this work. I'm doing very crude sending of things
to the sockets that the ipad app does.

Known Issues / Bugs.
====================

- Debugging code is ugly because I couldn't be bothered to make
  bytes to string conversions work with logging.
  
- Tested on my STB and my STB alone. Other STB hardware or software
  will not work.
  
- I haven't tested this with SkyQ, but I don't think it will work.

- If you have multiple STB's, it will control a random one.

- I don't actually test that we get what we expect, because as this
  is reverse engineered, I've no idea what I actually expect to expect.
  
Credits and Acknowledgments.
============================

ssdp.py from Dan Krause, see https://gist.github.com/dankrause/6000248
and https://github.com/davea/doxieapi/blob/master/doxieapi/ssdp.py
