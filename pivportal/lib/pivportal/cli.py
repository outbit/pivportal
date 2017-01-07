""" Command Line Interface Module """
import optparse
import os
import yaml

import pivportal.security
import pivportal.rest


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
        parser.add_option("-r", "--redis", dest="redis",
                              help="redis URL",
                              metavar="REDIS",
                              default=None)
        parser.add_option("-d", "--debug", dest="debug",
                              help="debug",
                              metavar="DEBUG",
                              default=None)
        (options, args) = parser.parse_args()
        self.port = options.port
        self.listen = options.listen
        self.redis_url = options.redis
        self.is_debug = options.debug

        # Set Defaults If Not Set On CLI
        if self.port is None:
            self.port = "8088"
        if self.listen is None:
            self.listen = "127.0.0.1"
        if self.redis_url is None:
            self.redis_url = "redis://localhost:6379/0"
        if self.is_debug is None:
            self.is_debug = False

        # Load Configurations if not set on CLI
        if os.path.isfile('/etc/pivportal-server.conf'):
            with open('/etc/pivportal-server.conf', 'r') as f:
                pivportal_conf = yaml.load(f)
                if "authorized_users" in pivportal_conf:
                    pivportal.security.dn_to_username = dict(pivportal_conf["authorized_users"])
                if "port" in pivportal_conf:
                    if self.port is None:
                        self.port = str(pivportal_conf["port"])
                if "listen_address" in pivportal_conf:
                    if self.listen is None:
                        self.listen = str(pivportal_conf["listen_address"])
                if "redis" in pivportal_conf:
                    if self.redis_url is None:
                        self.redis_url = str(pivportal_conf["redis"])
                if "register_ticket_timeout" in pivportal_conf:
                    pivportal.security.register_ticket_timeout = int(pivportal_conf["register_ticket_timeout"])


    def run(self):
        """ EntryPoint Of Application """
        pivportal.rest.app.config["REDIS_URL"] = self.redis_url
        pivportal.rest.app.run(threaded=True, host=self.listen, port=self.port, debug=self.is_debug)
