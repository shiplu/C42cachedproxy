import tornado.ioloop
import tornado.web
from tornado.options import define, parse_command_line, options
import pprint
from cachedproxy import config
from cachedproxy import environment


define("env", default="local",
       help="Application environment. One of these values %s"
       % list(environment.ENVIRONTMENTS.keys()))

define("config-server", default=None,
       help="Configuration server (Consul) hostname. If no server is provided or its unreachable use 'config.ini' file")


class EventWithSubscription(tornado.web.RequestHandler):
    def get(self):
        self.write("Settings:\n")
        self.write(pprint.pformat(self.settings, indent=4))


def main():
    parse_command_line()
    app = tornado.web.Application([
        (r"/events-with-subscriptions/([^/]+)", EventWithSubscription),
    ], settings={"config": config.factory(options.env)})
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
