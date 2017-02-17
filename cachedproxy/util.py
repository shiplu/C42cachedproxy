import time

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.log import app_log


def sig_handler(server, shutdown_waittime, sig, frame):
    io_loop = tornado.ioloop.IOLoop.instance()

    def stop_loop(deadline):
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            app_log.info('Waiting for next tick')
            io_loop.add_timeout(now + 1, stop_loop, deadline)
        else:
            io_loop.stop()
            app_log.info('Shutdown finally')

    def shutdown():
        app_log.info('Stopping http server')
        server.stop()
        app_log.info('Will shutdown in %s seconds ...', shutdown_waittime)
        stop_loop(time.time() + shutdown_waittime)

    app_log.warning('Caught signal: %s', sig)
    io_loop.add_callback_from_signal(shutdown)
