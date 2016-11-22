Usage (Sky Remote CLI).
=======================

Run this on a machine on the same LAN as a Sky Set Top Box.

Examples :-

```
# Set the channel to Sky Sports 1 HD.
$ ./skyremote.py 4 0 1

# Pause the TV
$ ./skyremote.py pause
```

For the full set of controls, look at the button dict in the code.

Setup (Alexa Skill).
====================

Preamble.
---------

This is a PITA because of how things work.

- We cannot just run an Alexa service in the amazon cloud via a lambda
function or whatever, because we need to run the service within your
firewall.
- We cannot just emulate a locally controllable device using something
like the WeMo protocol, as that only supports "On/Off" type functionality
and we need more. The Phillips home automation devices offer more control
but nothing that would be actually useful for a STB.
- I cannot run a generic webservice and make it avalible to more than
myself because you need to speak to your specific home to control your
STB.
- Assuming you have a dynamic IPv4 address, that is 
going to be a problem too.

Therefore, to make this work.

- You need to configure an Alexa service.
- You need locally running code on a device (like a home server
or a home raspberry pi).
- You need either a static IPv4 address or Dynamic DNS to give you
a static hostname.
- You need to use an SSL certifiate, even for your own in dev apps.
Thankfully this can be a self-signed certificate.
- You need a webserver to do the SSL and forward it to the alexa.py
app. I use nginx, but other options like apache would be fine.

Network Setup.
--------------

- You must have a DNS name that points to the IPv4 address of your home 
internet connection.
- You must forward TCP4/443 through your home router to your home 
server.


Home Server.
------------

- Get a copy of this project on your home computer or pi.
- Run "openssl req -nodes -x509 -newkey rsa:4096 -keyout key.pem -out 
cert.pem -days 365" to generate a certificate.
    - Most of the details are irrelevent, but the Common Name field
    must match the DNS you will assign to your home internet connection.   
- Configure your web server so it listens on HTTPS on TCP/443, with 
the x509 certificate you have generated and forwards that as plain HTTP
to your machine on TCP port 8080. See the nginx directory for examples.
Obviously replace home.yourdomain.com with the FQDN that resolves to
your home address.
- Run your webserver (in my case nginx) and alexa.py.

Configuring the Amazon Skill.
-----------------------------

- Go to https://developer.amazon.com and sign in. You will need
to accept T&C's and have a credit card on file with Amazon, but nothing
you do here will result in your credit card being charged.

- In the Alexa tab at the top, create a new "Custom Skill".

- In the "Skills Information" section.
    - Skill Type: Custom.
    - Language: English UK.
    - Invocation Name: You will say "Alexa, Tell $THIS sky one" to use
    the app, so name this what suits you. I went with "Sky Plus".
    - Audio Player: No
    
- In the "Interaction Model" section.
    - Intent Schema: Paste in the contents of interaction-schema.json
    - Custom Slot Types: Add a slot type called "CHANNEL". Run the
    printchannels.py script and paste the output in here. This is the
    list of channel names the app needs to listen out for.
    - Sample Utterances: Paste in the contents of sample-utterances.txt
    
- In the "Configuriaton" section.
    - Service Endpoint Type: HTTPS.
    - Geographic Region: Europe (I assume).
    - In the URI bar, paste the URI to your home dynamic DNS address
    (or static if you have that). It must be a DNS name, not just an IP
    address.
    - Account Linking: No.

- In the SSL Certificate tab, pick "I will upload a self-signed cert"
and paste in the contents of the certificate you generated on your
home server and configured your webserver to use.

- The other tabs aren't important as you aren't publishing this.

Usage (Alexa Skill).
====================

Say :- 
- Alexa, tell sky plus pause.
- Alexa, tell sky plus place.
- Alexa, tell sky plus bbc two.
- Alexa, tell sky plus sky sports one.

Known Issues / Bugs.
====================

- Debugging code is ugly because I couldn't be bothered to make
  bytes to string conversions work with logging.
- Tested on my STB and my STB alone. Other STB hardware or software
  may not work.
- I haven't tested this with SkyQ, but I don't think it will work.
- If you have multiple STB's, it will control a random one. This is
fixable but as I only have one STB it isn't a priority for me.
- I don't actually test that we get what we expect, because as this
  is reverse engineered, I've no idea what I actually expect to expect
  when communicating with the STB.
  
Likely Future Enchancements.
============================

Rework comms methods to avoid local webservice.

- Have code run in Amazon Lambda.
- Pop buttons to press on SQS queue.
- Have local agent consume entries in that queue and use local code
to "press buttons".

Credits and Acknowledgments.
============================

ssdp.py from Dan Krause, see https://gist.github.com/dankrause/6000248
and https://github.com/davea/doxieapi/blob/master/doxieapi/ssdp.py

Using the alexandra library at 
http://alexandra.readthedocs.io/en/latest/
