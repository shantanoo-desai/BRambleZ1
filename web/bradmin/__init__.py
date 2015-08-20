import json

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask.ext.bcrypt import Bcrypt

# default config

DEBUG = True
SECRET_KEY = 'no so secret'
CFG_FILE = '/etc/bradmin.cfg'
CACHE_ROOT = '.'

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.from_object(__name__)

try:
    app.config.from_pyfile(app.config['CFG_FILE'])
except IOError:
    pass


from fileStore import *
db = fileStore(app.config['CACHE_ROOT'] + '/db')

# load config from the database
conf = None
try:
    conf = json.loads(db.get('conf/bradmin'))    
except IOError:
    # load default config
    conf = { 
        'password': bcrypt.generate_password_hash('default')
        }
    db.store('conf/bradmin', json.dumps(conf, sort_keys=True, indent=4))

application = app

import bradmin.login
import bradmin.push

#web pages
import bradmin.frontpage
import bradmin.radio
import bradmin.mesh

#API
import bradmin.br
import bradmin.coap
import bradmin.rplinfo

#socket.io sockets
import bradmin.sockets

#detect distribution
distro = 'arch'
try:
   with open('/etc/apt/sources.list') as f: 
       distro = 'debian'
except IOError as e:
    pass

#load up the radio
try:
    bradmin.radio.load_radio()
except IOError:
    pass