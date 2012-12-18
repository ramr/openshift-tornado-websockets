#!/bin/env python

import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options

import application as app


# Return the libs path (this path is appended to module search path/sys.path).
def get_libs_path():
   zpath = os.getenv("OPENSHIFT_REPO_DIR")
   zpath = zpath if zpath else "./"
   return os.path.abspath(os.path.join(zpath, "libs") )


# Return the interface we need to bind to.
def get_bind_interface():
   ipaddr = os.getenv("OPENSHIFT_PYTHON_IP") or os.getenv("OPENSHIFT_DIY_IP")
   return(ipaddr if ipaddr else "127.0.0.1")


#  Server main.
def start_tornado():
   #  Tornado server address and port number.
   tornado.options.define("address", default=get_bind_interface(),
                          help="network address/interface to bind to")
   tornado.options.define("port", default=8080, help="port number to bind to",
                          type=int)
   tornado.options.parse_command_line()

   zoptions = tornado.options.options
   zserver = tornado.httpserver.HTTPServer(app.Application() )
   zserver.listen(zoptions.port, zoptions.address)
   tornado.ioloop.IOLoop.instance().start()


#
#  __main__:  main code.
#
if __name__ == "__main__":
   sys.path.append(get_libs_path() )
   start_tornado()

