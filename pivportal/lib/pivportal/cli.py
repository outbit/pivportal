""" Command Line Interface Module """
import optparse
from flask import Flask, Response, request


app = Flask(__name__)


@app.route('/getpersonbyid', methods = ['POST'])
def getPersonById():
    personId = int(request.form['personId'])
    return str(personId)  # back to a string to produce a proper response


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