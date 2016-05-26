# BRambleZ1
Visualisation tool for Zolertia Z1 based on BRamble by [Mariano Alvira](https://github.com/malvira), with modifications for Zolertia Z1 motes. Visualize your Multi-hop Network and access CoAP Resources on it.

## Installation Guide
Cloning the directory:

    https://github.com/shantanoo-desai/BRambleZ1.git
    
### Dependencies
For Ubuntu/Debian based machines:
```
	apt-get update
	apt-get install cython libjs-jquery python-flask python-pip python-dev ipv6calc
```
For Flask dependencies:
```
	pip install Flask-OpenID Flask-Login Flask-Principal Flask-Bcrypt Flask-Mako IPy gevent-socketio
```
### Back-end CoAP
BRambleZ1 uses [SMCP](https://github.com/darconeous/smcp). Please install SMCP by visiting the repository.

## Running BRambleZ1
Make a shebang command to avoid writing `python runserver.py` each time.
```
	$cd BrambleZ1/web
	$chmod a+x runserver.py
	$./runserver.py

```
## Border Router setup and Motes

### Border Router
The Border Router used here is [Erbium-br](https://github.com/shantanoo-desai/erbium-br). A border-router without *HTTP* but with
*Erbium Engine* on it and implementation of `rplinfo` for Routing Information based on CoAP 

(__NOTE__: Refer to the README in erbium-br for changing in Buffer size during compilation)

## Motes in the network
Motes are programmed with [CoAPZ1](https://github.com/shantanoo-desai/coapZ1)  using Erbium in Contiki-OS. One can add/remove resources according to one's wish but _DO NOT_ remove `rplinfo.c` and `rplinfo.h` (Needed for visualization)

## STEPS

### Erbium-br
upload the `erbr.c` on a Z1 mote and observe this:

    make connect-router

and if the prefix is _NOT SET_ press the *USR* button on the mote. After that observe the Router Address in JSON format:

```
	*** Address:bbbb::1 => bbbb:0000:0000:0000
	Got configuration message of type P
	Setting prefix bbbb::
	{"addrs":["bbbb::c30c:0:0:1373","fe80::c30c:0:0:1373",]}
```

### BRambleZ1

do the following:

1. Connect the Erbium-br as shown above

2. in a new terminal 
```
	cd BrambleZ1/web
	./runserver.py
```
Observe similar to this:
```
	grep_radio_ip
	Radio ips are [u'bbbb::c30c:0:0:1373', u'fe80::c30c:0:0:1373']
	get_radio_channel
	Radio set to channel 26
```
3. On Mozilla Firefox type the following:
```
	localhost:5000/
```
4. You will be directed to the Login Page and the password is "default"

5. after login, you will be directed to `mesh.html` where the visualisation will occur.


# Changing Border-Router IP Address
in `radio.py` in the **bradmin** folder a Section is marked for changing the border-router IPv6 Address. 
Put your _global IPv6_ and _link-local_ address according to examples in the variable `addrstr`

# License
Issued under the GNU GPLv3, similar to Mariano Alvira's BRamble repository
### Mentions
Thanks to [Kiril Petrov](http://github.com/retfie) for mentioning the modifications
