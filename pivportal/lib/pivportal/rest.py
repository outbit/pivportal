""" Command Line Interface Module """
import re
import os
from flask import Flask, Response, request

import json
import time
import pivportal.security


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/api/rest/user/login', methods = ['POST'])
@pivportal.security.valid_client_cert_required
def user_login():
    dat = None
    status = 200

    # Authenticate user, return a token
    dat = json.dumps({ "token": pivportal.security.create_token(username, app.secret_key) })

    # http response
    return(Response(response=dat, status=status, mimetype="application/json"))

@app.route('/api/rest/user/info', methods = ['POST'])
@pivportal.security.token_required(app.secret_key)
@pivportal.security.valid_client_cert_required
def user_info():
    return Response(response=json.dumps({"response": "success", "username": username}), status=200, mimetype="application/json")


@app.route('/api/rest/request/list', methods = ['POST'])
@pivportal.security.token_required(app.secret_key)
@pivportal.security.valid_client_cert_required
def request_list():

    request_list = []
    count = 0
    for item in pivportal.security.auth_requests:
        if item["username"] == username:
            if time.time() < item["time"]+pivportal.security.register_ticket_timeout:
                request_list.append(item)
            else:
                # Request Expired
                del pivportal.security.auth_requests[count]
        count += 1

    return Response(response=json.dumps(request_list), status=200, mimetype="application/json")


@app.route('/api/rest/request/auth', methods = ['POST'])
@pivportal.security.token_required(app.secret_key)
@pivportal.security.valid_client_cert_required
def request_auth():
    indata = request.get_json()

    # Verify Request
    if "requestid" not in indata or "client_ip" not in indata or "authorized" not in indata:
        return Response(response=json.dumps({"response": "  invalid request missing data"}), status=400, mimetype="application/json")

    requestid = indata['requestid']
    client_ip = indata['client_ip']
    authorized = indata['authorized']

    if not pivportal.security.requestid_is_valid(requestid) or not pivportal.security.ip_is_valid(client_ip):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    # Authenticate Request
    count = 0
    for item in pivportal.security.auth_requests:
        if item["username"] == username and item["requestid"] == requestid and item["client_ip"] == client_ip:
            if item["authorized"] == False and authorized == True and time.time() < item["time"]+pivportal.security.register_ticket_timeout:
                pivportal.security.auth_requests[count]["authorized"] = True
        count += 1

    return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")


@app.route('/api/client/request/register', methods = ['POST'])
def request_register():
    username = str(request.form['username'])
    requestid = str(request.form['requestid'])
    client_ip = request.remote_addr

    if not pivportal.security.username_is_valid(username) or not pivportal.security.requestid_is_valid(requestid) or not pivportal.security.ip_is_valid(client_ip):
        # client_ip is None when testing, so its ok
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    if pivportal.security.is_duplicate_register(username, requestid, pivportal.security.auth_requests):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    pivportal.security.auth_requests.append({"username": username, "requestid": requestid, "client_ip": client_ip, "authorized": False, "time": time.time()})

    return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")


@app.route('/api/client/request/status', methods = ['POST'])
def request_status():
    username = str(request.form['username'])
    requestid = str(request.form['requestid'])
    client_ip = request.remote_addr

    if not pivportal.security.username_is_valid(username) or not pivportal.security.requestid_is_valid(requestid) or not pivportal.security.ip_is_valid(client_ip):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    count = 0
    for item in pivportal.security.auth_requests:
        if item["username"] == username and item["requestid"] == requestid and item["client_ip"] == client_ip:
            if item["authorized"] == True:
                # Success
                del pivportal.security.auth_requests[count]
                return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")
            else:
                # Delete auth_request, it failed anyway
                del pivportal.security.auth_requests[count]
            break
        count += 1

    return Response(response=json.dumps({"response": "Authentication Failure"}), status=401, mimetype="application/json")
