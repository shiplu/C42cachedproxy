import tornado.web


class BaseRequestHandler(tornado.web.RequestHandler):
    """Base hanlders for all handlers."""
    def initialize(self):
        """Add convenient way to access app config and cache"""
        self.config = self.settings.get('config', {})
        self.cache = self.settings.get('cache', {})


class EventWithSubscription(BaseRequestHandler):

    def get(self, event_id):
        """GET handler for event id event_id.
        It returns all the events with its subscription
        in the following format.
            {
                "id": "$EVENT_ID",
                "title": "Test Event",
                "names": ["Bob", "Ella"]
            }
        """
