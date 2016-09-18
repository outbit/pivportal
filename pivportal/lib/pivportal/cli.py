""" Command Line Interface Module """
import optparse
from flask import Flask, Response, request
from random import choice
from string import ascii_uppercase
import re
import json


app = Flask(__name__)

# [{ "username": X, "requestid": X, "client_ip"; X, "authorized": False},]
auth_requests = []


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


def is_duplicate_register(username, requestid, client_ip):
    for item in auth_requests:
        if item["username"] == username and item["requestid"] == requestid and item["client_ip"] == client_ip:
            # Request Is Already Registered
            return True
    return False


@app.route('/api/rest/request/list', methods = ['POST'])
def request_list():
    indata = request.get_json()
    user_serial = request.headers.get('SSL_CLIENT_S_DN')

    # TODO: Do something with this!!! Verify the user
    print(user_serial)

    if "username" not in indata:
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    username = indata["username"]

    if not username_is_valid(username):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    request_list = []
    for item in auth_requests:
        if item["username"] == username:
            request_list.append(item)

    return Response(response=json.dumps(request_list), status=200, mimetype="application/json")


@app.route('/api/rest/request/auth', methods = ['POST'])
def request_auth():
    indata = request.get_json()
    user_serial = request.headers.get('SSL_CLIENT_S_DN')

    # TODO: Do something with this!!! Verify the user
    print(user_serial)

    if "username" not in indata or "requestid" not in indata or "client_ip" not in indata or "authorized" not in indata:
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    username = indata['username']
    requestid = indata['requestid']
    client_ip = indata['client_ip']
    authorized = indata['authorized']

    if not username_is_valid(username) or not requestid_is_valid(requestid) or not ip_is_valid(client_ip):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    # Authenticate Request
    count = 0
    for item in auth_requests:
        if item["username"] == username and item["requestid"] == requestid and item["client_ip"] == client_ip:
            if item["authorized"] == False and authorized == True:
                auth_requests[count]["authorized"] = True
        count += 1

    #return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")
    return "success"


@app.route('/api/client/request/register', methods = ['POST'])
def request_register():
    username = str(request.form['username'])
    requestid = str(request.form['requestid'])
    client_ip = request.remote_addr

    if not username_is_valid(username) or not requestid_is_valid(requestid) or not ip_is_valid(client_ip):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    if is_duplicate_register(username, requestid, client_ip):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    auth_requests.append({"username": username, "requestid": requestid, "client_ip": client_ip, "authorized": False})

    #return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")
    return "success"


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
                #return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")
                del auth_requests[count]
                return "success"
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
                              default="8088")
        parser.add_option("-l", "--listen", dest="listen",
                              help="Listen IP Address",
                              metavar="LISTEN",
                              default="127.0.0.1")
        parser.add_option("-d", "--debug", dest="debug",
                              help="debug",
                              metavar="DEBUG",
                              default=False)
        (options, args) = parser.parse_args()
        self.port = options.port
        self.listen = options.listen
        self.is_debug = options.debug

    def run(self):
        """ EntryPoint Of Application """
        app.run(threaded=True, host=self.listen, port=self.port, debug=self.is_debug)