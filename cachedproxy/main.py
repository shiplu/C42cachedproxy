import signal
from functools import partial
from datetime import timedelta

import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, parse_command_line, options

from cachedproxy import config
from cachedproxy import environment
from cachedproxy import handlers
from cachedproxy import drivers
from cachedproxy import util


define("env", default="local",
       help="Application environment. One of these values %s"
       % list(environment.ENVIRONTMENTS.keys()))

define("config-server", default=None,
       help="Configuration server (Consul) hostname. "
       "If no server is provided or its unreachable use 'config.ini' file")

define("shutdown-waittime", default=3,
       help="Maximum number of seconds to wait to process running requests"
       " before shutdown")


def main():
    parse_command_line()
    config_object = config.factory(options.env, options.config_server)
    cache = drivers.factory(config_object.cache_driver,
                            host=config_object.cache_host,
                            port=config_object.cache_port,
                            ttl=timedelta(minutes=4.2).seconds)
    routes = [(r"/events-with-subscriptions/([^/]+)", handlers.EventWithSubscription)]
    app = tornado.web.Application(routes, cache=cache,
                                  config=config_object)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8888)

    signal.signal(signal.SIGTERM, partial(util.sig_handler, server, options.shutdown_waittime))
    signal.signal(signal.SIGINT, partial(util.sig_handler, server, options.shutdown_waittime))
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
