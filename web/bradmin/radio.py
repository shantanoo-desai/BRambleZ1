#Radio API Main File for configuring Border Router
import os
import json
import subprocess
import time
import re

from flask import render_template, redirect, url_for, request, jsonify
from flask.ext.login import login_required
from flask.ext.mako import MakoTemplates
from flask.ext.mako import render_template as render_mako

from bradmin import app, db, conf, rest
import bradmin.coap as coap

from random import randint

mako = MakoTemplates(app)

@app.route("/radio/ip")
@login_required
def ip():
    print "ip"
    try:
        ip = get_radio_not_local_ip()
    except (ValueError, subprocess.CalledProcessError):
        return jsonify(status = 'error')
    return jsonify(addrs = [ip])

@app.route("/radio/channel", methods=['POST', 'GET'])
@login_required
def radioChannel():
    print "radioChannel"
    try:
        ip = get_radio_not_local_ip()
    except (ValueError, subprocess.CalledProcessError):
        return jsonify(status = 'error')

    if request.method == 'POST':
        coap.post('coap://[%s]/config?param=channel' % (ip), request.json['channel'])
        load_radio()
        return jsonify(status = 'ok')
    else: # GET
        return str(get_radio_channel)

def setSerial(serial):
    ip = get_radio_not_local_ip()
    coap.post('coap://[%s]/config?param=serial' % (ip), serial)

def get_radio_not_local_ip():
    for i in get_radio_ips():
        m = re.match('^([\da-fA-F]+):', i)
        if m.group(1) != 'fe80':
            return i

def get_radio_ips():
    ips = json.loads(db.get('conf/radio'))['ips']
    return ips

class RadioError(Exception):
    def __init__(self, value):
         self.value = value
    def __str__(self):
         return repr(self.value)

def grep_radio_ip():
    print "grep_radio_ip"
    # it's diffcult to get the trailing commas correct in the Contiki IP addr output 
    # so we don't (get it correct) and fix up the last trailing comma here

    '''
    >>>>>>>>>>>>>>>>>>ADD YOUR BORDER ROUTER ADDRESS HERE <<<<<<<<<<<<<<<<<<
    '''
    #addrstr = '{"addrs":["aaaa::61b:5fb3:12:4b00","fe80::4b3:ff:ff12:4b00"]}'
    #addrstr = '{"addrs":["aaaa::212:4b00:41b:5fcd","fe80::212:4b00:41b:5fcd"]}'
    addrstr = '{"addrs":["bbbb::c30c:0:0:1373","fe80::c30c:0:0:1373"]}'
    #addrstr = '{"addrs":["aaaa::c30c:0:0:10b7","fe80::c30c:0:0:10b7"]}'    
    #addrstr = '{"addrs":["aaaa::c30c:0:0:1c8","fe80::c30c:0:0:1c8"]}'
    
    
    ips = json.loads(addrstr)
    return ips

def get_radio_channel():
    print "get_radio_channel"
    # Add the Radio Channel according to Application Below
    channel = 26
    return int(channel)

def doFactoryRestore():
    subprocess.call(['cp', os.path.join(app.config['CACHE_ROOT']+ '/db/conf', 'br.factory'), os.path.join(app.config['CACHE_ROOT'], 'br.bin')])
    load_radio()

@app.route("/radio/reload", methods=['POST'])
@login_required
def reload():
    print "reload"
    load_radio()
    return jsonify(status = 'ok')

def load_radio():

    
    try:
        radio = json.loads(db.get('conf/radio'))
    except IOError:
        # configure for zolertia Z1 as default
        radio = { "device": "/dev/ttyUSB0",
                  "resetcmd": "make z1-reset"}
        db.store('conf/radio', json.dumps(radio))

    
    
    # save the radio ip addr
    try:
        radio['ips'] = grep_radio_ip()['addrs']
        db.store('conf/radio', json.dumps(radio))
        print "Radio ips are %s" % (radio['ips'])
    except RadioError:
        broadcastStatus("radio", json.dumps(dict(err = "failed to get the radio IP address")))
        print "Couldn't get radio IP addresses"

#    broadcastStatus("radio", json.dumps(dict(loadRadioProgress = "95%")))

    # get the current channel
    try: 
        radio['channel'] = get_radio_channel()
        db.store('conf/radio', json.dumps(radio))
        print "Radio set to channel %s" % (radio['channel'])
    except ValueError:
        broadcastStatus("radio", json.dumps(dict(err = "failed to get the radio channel")))
        print "failed to get the radio channel"
    
#    broadcastStatus("radio", json.dumps(dict(loadRadioProgress = "100%")))


@app.route("/radio", methods=['GET', 'POST'])
@login_required
def radio():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['CACHE_ROOT'], 'br.bin'))
        # try:
        #     broadcastStatus("radio", json.dumps(dict(task = "uploadingFirmware")))
        #     load_radio()
        # except IOError:
        #     return render_mako('radio.html', error={'badupload':['resetcmd']} )
        radio = json.loads(db.get('conf/radio'))            
        return render_mako('radio.html', error = {}, radio = radio, forceReload="true")

    # GET
    radio = json.loads(db.get('conf/radio'))            
    return render_mako('radio.html', error={}, radio = radio, forceReload="false")

@app.route("/radio/radio", methods=['POST','GET'])
@login_required
def radiosettings():
    return rest.jsonGetSet('conf/radio', request)
    
@app.route("/radio/tunslip", methods=['POST','GET'])
@login_required
def tunslip():
    return rest.jsonGetSet('conf/tunslip', request)