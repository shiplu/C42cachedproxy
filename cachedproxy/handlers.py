import requests
import tornado.web
from tornado.log import app_log

from cachedproxy.api import Calendar42


class BaseRequestHandler(tornado.web.RequestHandler):
    """Base hanlders for all handlers."""

    def initialize(self):
        """Add convenient way to access app config and cache"""
        self.config = self.settings.get('config', {})
        self.cache = self.settings.get('cache', {})

        self.api = Calendar42(self.config.api_token)


class EventWithSubscription(BaseRequestHandler):

    def get(self, event_id):

        try:
            event = self.api.events(event_id)
            subscriptions = self.api.event_subscriptions(event_id)
            subscriber_names = [datum["subscriber"]["first_name"]
                                for datum in subscriptions["data"]]
            self.write({
                "id": event_id,
                "title": event["data"][0]["title"],
                "names": subscriber_names})
        except requests.exceptions.HTTPError as he:
            self.set_status(he.response.status_code)
