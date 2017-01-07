""" Command Line Interface Module """
from flask import Response, request
import json
import re
import jwt
import datetime
from functools import wraps

# Redis "requests" hash
# {"12345678": { "username": X, "client_ip": X, "authorized": False, "time": time.time()}}

# {"dn1": "user1", "dn2": "user2"}
dn_to_username = {}
register_ticket_timeout = 60


def dn_is_valid(dn):
    if re.match(r'^[a-zA-Z0-9_\-\,\(\)\+\=\:\s\. ]+$', dn):
        return True
    return False


def username_is_valid(username):
    if re.match(r'^[a-zA-Z0-9_\-]+$', username) and username in dn_to_username.values():
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
    if requestid in auth_requests:
        this_request = json.loads(auth_requests[requestid])
        if this_request["username"] == username:
            # Request Is Already Registered
            return True
    return False


def create_token(user, secret_key):
    payload = {
        # subject
        'sub': user,
        #issued at
        'iat': datetime.datetime.utcnow(),
        #expiry
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token.decode('unicode_escape')


def parse_token(token, secret_key):
    return jwt.decode(token, secret_key, algorithms='HS256')


def token_required(secret_key):
    def token_required_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            g = f.func_globals

            if not request.headers.get('Authorization'):
                return Response(response="Missing authorization header", status=401)
            try:
                payload = parse_token(request.headers.get('Authorization').split()[1], secret_key)
            except jwt.DecodeError:
                return Response(response="Token is invalid", status=401)
            except jwt.ExpiredSignature:
                return Response(response="Token has expired", status=401)

            # Set username for decorated func
            g["username"] = payload['sub']

            return f(*args, **kwargs)
        return decorated_function
    return token_required_decorator


def valid_client_cert_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g = f.func_globals

        if not request.headers.get('SSL_CLIENT_S_DN'):
            return Response(response="Missing Client DN Header", status=401)

        # Get Client DN
        user_dn = request.headers.get('SSL_CLIENT_S_DN')

        # Valid DN
        if not dn_is_valid(user_dn):
            return Response(response=json.dumps({"response": "  Invalid Request DN %s" % user_dn}), status=400, mimetype="application/json")

        # Authorize User
        if user_dn not in dn_to_username:
            return Response(response=json.dumps({"response": "Authentication Failure for DN %s" % user_dn}), status=401, mimetype="application/json")

        username = dn_to_username[user_dn]

        # Verify Request
        if not username_is_valid(username):
            return Response(response=json.dumps({"response": "  Invalid Request Username"}), status=400, mimetype="application/json")

        # Set username for decorated func
        g["username"] = username

        return f(*args, **kwargs)
    return decorated_function
