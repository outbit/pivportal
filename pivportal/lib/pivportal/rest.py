""" Command Line Interface Module """
import re
import os
from flask import Flask, Response, request

import json
import time
import pivportal.security

from flask_redis import FlaskRedis


def create_app():
    app = Flask(__name__)
    redis_store = FlaskRedis()
    redis_store.init_app(app)
    return (app, redis_store)


(app, redis_store) = create_app()
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
    auth_requests = redis_store.hgetall("requests")
    for requestid in auth_requests:
        this_request = json.loads(auth_requests[requestid])
        if this_request["username"] == username:
            if time.time() < this_request["time"]+pivportal.security.register_ticket_timeout:
                this_request["requestid"] = requestid # requestid needed for request_list
                request_list.append(this_request)
            else:
                # Request Expired
                redis_store.hdel("requests", requestid)

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
    auth_requests = redis_store.hgetall("requests")
    if requestid in auth_requests:
        this_request = json.loads(auth_requests[requestid])
        if this_request["username"] == username and this_request["client_ip"] == client_ip:
            if this_request["authorized"] == False and authorized == True and time.time() < this_request["time"]+pivportal.security.register_ticket_timeout:
                this_request["authorized"] = True
                redis_store.hmset("requests", {requestid: json.dumps(this_request)})

    return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")


@app.route('/api/client/request/register', methods = ['POST'])
def request_register():
    username = str(request.form['username'])
    requestid = str(request.form['requestid'])
    client_ip = request.remote_addr

    if not pivportal.security.username_is_valid(username) or not pivportal.security.requestid_is_valid(requestid) or not pivportal.security.ip_is_valid(client_ip):
        # client_ip is None when testing, so its ok
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    if pivportal.security.is_duplicate_register(username, requestid, redis_store.hgetall("requests")):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    this_request = {"username": username, "client_ip": client_ip, "authorized": False, "time": time.time()}
    redis_store.hmset("requests", {requestid: json.dumps(this_request)})

    return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")


@app.route('/api/client/request/status', methods = ['POST'])
def request_status():
    username = str(request.form['username'])
    requestid = str(request.form['requestid'])
    client_ip = request.remote_addr

    if not pivportal.security.username_is_valid(username) or not pivportal.security.requestid_is_valid(requestid) or not pivportal.security.ip_is_valid(client_ip):
        return Response(response=json.dumps({"response": "  invalid request"}), status=400, mimetype="application/json")

    auth_requests = redis_store.hgetall("requests")
    if requestid in auth_requests:
        this_request = json.loads(auth_requests[requestid])
        if this_request["username"] == username and this_request["client_ip"] == client_ip:
            if this_request["authorized"] == True:
                # Success
                redis_store.hdel("requests", requestid)
                return Response(response=json.dumps({"response": "success"}), status=200, mimetype="application/json")
            else:
                # Delete auth_request, it failed anyway
                redis_store.hdel("requests", requestid)

    return Response(response=json.dumps({"response": "Authentication Failure"}), status=401, mimetype="application/json")
