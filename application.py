import os
import tornado.web
import tornado.websocket

# Constants.
APP_NAME        = u"Tornado On OpenShift"
APP_VERSION     = u"1.0"
COOKIE_SECRET   = u"Rock_You_Like_A_Hurricane"
TORNADO_PNG_URI = u"http://www.tornadoweb.org/en/stable/_images/tornado.png"


# The tornado application.
class Application(tornado.web.Application):
   def __init__(self):
      repodir  = get_repo_dir()
      settings = dict()

      settings["title"]         = APP_NAME
      settings["cookie_secret"] = u"Rock_You_Like_A_Hurricane"
      settings["static_path"]   = os.path.join(repodir, "static")
      settings["template_path"] = os.path.join(repodir, "templates")
      settings["xsrf_cookies"]  = True
      settings["debug"]         = True if hot_deploy_marker() else False

      handlers = [ (r"/",            HomePageHandler),
                   (r"/about",       AboutAppHandler),
                   (r"/health",      HealthPageHandler),
                   (r"/tornado.png", TornadoImageHandler),
                   (r"/ws-echo",     WebSocketEchoHandler)
                 ]

      tornado.web.Application.__init__(self, handlers, **settings)


# Get the repo directory.
def get_repo_dir():
   repodir = os.getenv("OPENSHIFT_REPO_DIR")
   return(repodir if repodir else os.path.abspath('./') )


# Check if hot deployment is enabled.
def hot_deploy_marker():
   repodir  = get_repo_dir()
   hdmarker = os.path.join(repodir, ".openshift", "markers", "hot_deploy")
   return os.path.exists(hdmarker)
 

# Handle the home page/index request.
# @route("/").
class HomePageHandler(tornado.web.RequestHandler):
   def get(self):
      self.render("index.html")


# Handle the about request.
# @route("/about").
class AboutAppHandler(tornado.web.RequestHandler):
   def get(self):
      self.write(" - ".join([APP_NAME , APP_VERSION]) + "\n")


# Handle the health request.
# @route("/health").
class HealthPageHandler(tornado.web.RequestHandler):
   def get(self):
      self.write("1\n")


# Handle the tornado image request.
# @route("/tornado.png").
class TornadoImageHandler(tornado.web.RequestHandler):
   def get(self):
      self.redirect(TORNADO_PNG_URI, True)


# WebSocket echo handler.
# @route("/ws-echo").
class WebSocketEchoHandler(tornado.websocket.WebSocketHandler):
   def open(self):
      self.write_message(u"ws-echo: 418 I'm a teapot (as per RFC 2324)")

   def on_message(self, message):
      self.write_message(u"ws-echo: " + message)

   def check_origin(self, origin):
      return True

