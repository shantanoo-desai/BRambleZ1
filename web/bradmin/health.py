#Health API
import json
import subprocess
import urllib2

from IPy import IP

from flask import render_template, redirect, url_for, request, jsonify
from flask.ext.mako import MakoTemplates

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

from bradmin import app, db
import bradmin.radio

import gevent
from gevent import Greenlet

mako = MakoTemplates(app)

class ChatNamespace(BaseNamespace, BroadcastMixin):
    nicknames = []

    def initialize(self):
        self.logger = app.logger
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, thing):
        print "on_join"
        print thing
        self.emit('you_joined', 'barbaz');
        self.broadcast_event('foo', 'bar');
        return True

statusNamespaces = {}
class StatusNamespace(BaseNamespace, BroadcastMixin):
    def initialize(self):
        # add ourself to the map of status sockets for the broadcast function to use
        statusNamespaces[self.socket.sessid] = self

    # this is in status for no good reason. Should factor someday.
    def on_radio(self, msg):
        if msg == 'doFactoryRestore':
            bradmin.radio.doFactoryRestore()

    def disconnect(self, silent=True):
        del statusNamespaces[self.socket.sessid]
        super(StatusNamespace, self).disconnect(silent)

def broadcastStatus(event, msg):
    for sessid, namespace in statusNamespaces.iteritems():
        namespace.emit(event, msg)

class HealthCheck(Greenlet):
    def __init__(self, interval=30):
        super(HealthCheck, self).__init__()
        self.interval = interval
        self.start()
    def _run(self):
        while True:
            gevent.sleep(self.interval)
            self.do_check()

class LowpanAPICheck(HealthCheck):
    def __init__(self, interval=30):
        super(LowpanAPICheck, self).__init__(interval);
    def do_check(self):
	print "LowpanAPICheck::do_check"
	

class RadioCheck(HealthCheck):
    def __init__(self, interval=30):
        self.fails = 0
        super(RadioCheck, self).__init__(interval);
    def do_check(self):
	print "RadioCheck::do_check"
	
        # check ok
        self.fails = 0

class TunnelCheck(HealthCheck):
    def __init__(self, interval=30):
        self.fails = 0
        super(TunnelCheck, self).__init__(interval);
    def do_check(self):
	print "TunnelCheck::do_check"
	
        # check ok
        self.fails = 0
