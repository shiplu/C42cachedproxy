import tornado.web


class BaseRequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.config = self.settings['settings'].get('config', {})


class EventWithSubscription(BaseRequestHandler):
    def get(self, event_id):
        pass