#RPLINFO API for routes and parents
import json

from flask import request, jsonify

from bradmin import app
import bradmin.coap

@app.route("/rplinfo/<ip>/routes")
def routes(ip):
    print "rplinfo.routes(%s)" % ip

    num = 0
    try:
        num = int(bradmin.coap.get("coap://[%s]/rplinfo/routes" % ip).rstrip())
    except:
        print "rplinfo.routes: except: num = [%s]" % num

    routes = []
    for i in range(0, num):
        r = json.loads(bradmin.coap.get("coap://[%s]/rplinfo/routes?index=%d" % (ip,i) ).rstrip())
        routes.append(r)

    print "rplinfo.routes: routes = %s" % routes
    return jsonify(routes = routes)

@app.route("/rplinfo/<ip>/parents")
def parents(ip):
    print "rplinfo.parents(%s)" % ip

    num = 0
    try:
        num = int(bradmin.coap.get("coap://[%s]/rplinfo/parents" % ip).rstrip())
    except:
        print "rplinfo.parents: except: num = [%s]" % num

    parents = []
    for i in range(0, num):
        p = json.loads(bradmin.coap.get("coap://[%s]/rplinfo/parents?index=%d" % (ip,i) ).rstrip())
        parents.append(p)

    print "rplinfo.parents: parents = %s" % parents
    return jsonify(parents = parents)