""" Command Line Interface Module """
import optparse
import os
from random import choice
from string import ascii_uppercase
import re
from flask import Flask, Response, request
import json
import yaml
import time


app = Flask(__name__)

# [{ "username": X, "requestid": X, "client_ip": X, "authorized": False, "time": time.time()},]
auth_requests = []

# {"dn1": "user1", "dn2": "user2"}
dn_to_username = {}
register_ticket_timeout = 60


def dn_is_valid(dn):
    if re.match(r'^[a-zA-Z0-9_\-,\(\):]+$', dn):
        return True
    return False


def username_is_valid(username):
    if re.match(r'^[a-zA-Z0-9_\-]+$', username):
        return True
    return False


def requestid_is_valid(requestid):
    if re.match(r'^[a-zA-Z0-9]+$', requestid) and len(requestid) == 16:
        return True
    return False


def ip_is_valid(ip):
    if re.match(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$', ip):
        return True
    return False


def is_duplicate_register(username, requestid, auth_requests):
    for item in auth_requests:
        if item["username"] == username and item["requestid"] == requestid:
            # Request Is Already Registered
            return True
    return False


@app.route('/api/rest/request/list', methods = ['POST'])
def request_list():
    user_dn = request.headers.get('SSL_CLIENT_S_DN')

    # Valid DN
    if not dn_is_valid(user_dn):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    # Authorize User
    if user_dn not in dn_to_username:
        return Response(response=json.dumps({"response": "Authentication Failure"}), status=401, mimetype="application/json")

    username = dn_to_username[user_dn]

    # Verify Request
    if not username_is_valid(username):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    request_list = []
    count = 0
    for item in auth_requests:
        if item["username"] == username:
            if time.time() < item["time"]+register_ticket_timeout:
                request_list.append(item)
            else:
                # Request Expired
                del auth_requests[count]
        count += 1

    return Response(response=json.dumps(request_list), status=200, mimetype="application/json")


@app.route('/api/rest/request/auth', methods = ['POST'])
def request_auth():
    indata = request.get_json()
    user_dn = request.headers.get('SSL_CLIENT_S_DN')

    # Valid DN
    if not dn_is_valid(user_dn):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    # Authorize User
    if user_dn not in dn_to_username:
        return Response(response=json.dumps({"response": "Authentication Failure"}), status=401, mimetype="application/json")

    # Verify Request
    if "requestid" not in indata or "client_ip" not in indata or "authorized" not in indata:
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    username = dn_to_username[user_dn]
    requestid = indata['requestid']
    client_ip = indata['client_ip']
    authorized = indata['authorized']

    if not username_is_valid(username) or not requestid_is_valid(requestid) or not ip_is_valid(client_ip):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    # Authenticate Request
    count = 0
    for item in auth_requests:
        if item["username"] == username and item["requestid"] == requestid and item["client_ip"] == client_ip:
            if item["authorized"] == False and authorized == True and time.time() < item["time"]+register_ticket_timeout:
                auth_requests[count]["authorized"] = True
        count += 1

    return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")


@app.route('/api/client/request/register', methods = ['POST'])
def request_register():
    username = str(request.form['username'])
    requestid = str(request.form['requestid'])
    client_ip = request.remote_addr

    if not username_is_valid(username) or not requestid_is_valid(requestid) or not ip_is_valid(client_ip):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    if is_duplicate_register(username, requestid, auth_requests):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    auth_requests.append({"username": username, "requestid": requestid, "client_ip": client_ip, "authorized": False, "time": time.time()})

    return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")


@app.route('/api/client/request/status', methods = ['POST'])
def request_status():
    username = str(request.form['username'])
    requestid = str(request.form['requestid'])
    client_ip = request.remote_addr

    if not username_is_valid(username) or not requestid_is_valid(requestid) or not ip_is_valid(client_ip):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    count = 0
    for item in auth_requests:
        if item["username"] == username and item["requestid"] == requestid and item["client_ip"] == client_ip:
            if item["authorized"] == True:
                # Success
                del auth_requests[count]
                return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")
            else:
                # Delete auth_request, it failed anyway
                del auth_requests[count]
            break
        count += 1

    return Response(response=json.dumps({"response": "Authentication Failure"}), status=401, mimetype="application/json")


class Cli(object):
    """ Command Line Interface for pivportal """
    # Parse CLI Arguments
    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option("-p", "--port", dest="port",
                              help="port",
                              metavar="PORT",
                              default=None)
        parser.add_option("-l", "--listen", dest="listen",
                              help="Listen IP Address",
                              metavar="LISTEN",
                              default=None)
        parser.add_option("-d", "--debug", dest="debug",
                              help="debug",
                              metavar="DEBUG",
                              default=None)
        (options, args) = parser.parse_args()
        self.port = options.port
        self.listen = options.listen
        self.is_debug = options.debug

        # Set Defaults If Not Set On CLI
        if self.port is None:
            self.port = "8088"
        if self.listen is None:
            self.listen = "127.0.0.1"
        if self.is_debug is None:
            self.is_debug = False

        # Load Configurations if not set on CLI
        if os.path.isfile('/etc/pivportal-server.conf'):
            with open('/etc/pivportal-server.conf', 'r') as f:
                pivportal_conf = yaml.load(f)
                if "authorized_users" in pivportal_conf:
                    dn_to_username = dict(pivportal_confg["authorized_users"])
                if "port" in pivportal_conf:
                    if self.port is None:
                        self.port = str(pivportal_conf["port"])
                if "listen_address" in pivportal_conf:
                    if self.listen is None:
                        self.listen = str(pivportal_conf["listen_address"])
                if "register_ticket_timeout" in pivportal_conf:
                    register_ticket_timeout = int(pivportal_conf["register_ticket_timeout"])


    def run(self):
        """ EntryPoint Of Application """
        app.run(threaded=True, host=self.listen, port=self.port, debug=self.is_debug)