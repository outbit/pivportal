""" Command Line Interface Module """
import optparse


class Cli(object):
    """ Command Line Interface for pivportal """
        # Parse CLI Arguments
        parser = optparse.OptionParser()
        parser.add_option("-p", "--port", dest="port",
                          help="port",
                          metavar="PORT",
                          default="8088")
        parser.add_option("-l", "--listen", dest="listen",
                          help="Listen IP Address",
                          metavar="LISTEN",
                          default="127.0.0.1")
        (options, args) = parser.parse_args()

    def run(self):
        """ EntryPoint Of Application """
        pass