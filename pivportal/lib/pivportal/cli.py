""" Command Line Interface Module """
import optparse
from flask import Flask, Response, request
from random import choice
from string import ascii_uppercase


app = Flask(__name__)

# [{ "username": X, "requestid": X, "client_ip"; X, "authorized": False},]
auth_requests = []


@app.route('/api/request/list', methods = ['POST'])
def request_list():
    username = str(request.form['username'])
    print("verify request was from the user authed connection")

    return str(requestid)


@app.route('/api/request/register', methods = ['POST'])
def request_register():
    username = str(request.form['username'])
    requestid = ''.join(choice(ascii_uppercase) for i in range(16))
    clientip = request.remote_addr
    print(username)
    print(requestid)

    # Verify username is safe!!!

    auth_requests.append({"username": username, "requestid": requestid, "client_ip": clientip, "authorized": False})

    return str(requestid)


@app.route('/api/request/status', methods = ['POST'])
def request_status():
    username = str(request.form['username'])
    requestid = str(request.form['requestid'])
    clientip = request.remote_addr
    print(username)
    print(requestid)

    # Verify username and requestid is SAFE!!!

    for item in auth_requests:
        if item["username"] == username and item["requestid"] == requestid and item["client_ip"] == clientip:
            if item["authorized"] == True:
                # Success
                pass

    return str(requestid)


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