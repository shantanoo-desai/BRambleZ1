#CoAP API
import subprocess
import urllib

from flask import request, jsonify
from flask.ext.login import login_required

from bradmin import app

COAP_TIMEOUT = 10

@app.route("/coap", methods=['POST'])
@login_required
def doCoap():
    """ take request as: { "ip": ip, "path": path, "method": method, "body", body }  """
    """ return raw result """
    r = request.json
    print r
    if r['method'].upper() == 'GET':
        return jsonify(response=get('coap://[%s]/%s' % (r['ip'], r['path'])).rstrip())

def get(url):
    # using SMCP for accessing routes
    return subprocess.check_output(['smcpctl', 'get', '--timeout', str(COAP_TIMEOUT), url])

def post(url, data):
    d = urllib.quote_plus(str(data))
    return subprocess.check_output(['smcpctl', 'post', url, d])

if __name__ == "__main__":
    import sys
    get(sys.argv[1])