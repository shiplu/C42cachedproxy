import tornado.ioloop
import tornado.web


class EventWithSubscription(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def main():
    app = tornado.web.Application([
        (r"/events-with-subscriptions/([^/]+)", EventWithSubscription),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
