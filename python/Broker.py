#!/usr/bin/env python

import WebHandler

import time
import ConfigParser
import BaseHTTPServer

config = ConfigParser.ConfigParser()
config.read('ovirt.conf')

hostName = config.get('Server', 'HostName')
portNumber = config.getint('Server', 'PortNumber')

server_class = BaseHTTPServer.HTTPServer
httpd = server_class((hostName, portNumber), WebHandler.WebHandler)
print time.asctime(), "Server Starts - %s:%s" % (hostName, portNumber)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print time.asctime(), "Server Stops - %s:%s" % (hostName, portNumber)
