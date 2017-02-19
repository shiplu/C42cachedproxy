import requests
from urllib.parse import urlencode


class Calendar42(object):
    default_endpoint = "https://demo.calendar42.com/api/v2"

    def __init__(self, token, endpoint=None):
        self.token = token
        self.endpoint = endpoint if endpoint else self.default_endpoint

    def __repr__(self):
        return "[%s]" % self.endpoint

    def _get_uri(self, resource, **params):
        params = params if params else {}
        uri = "%s/%s" % (self.endpoint, resource)
        if params:
            uri = "%s?%s" % (uri, urlencode(params))
        return uri

    def _do_request(self, uri):
        auth_header = "Token %s" % self.token
        resp = requests.get(uri, headers={"Accept": "application/json",
                                          "Authorization": auth_header})

        resp.raise_for_status()
        return resp.json()

    def events(self, event_id):
        return self._do_request(self._get_uri("events/%s" % event_id))

    def event_subscriptions(self, event_id):
        uri = self._get_uri("event-subscriptions", event_ids=[event_id])
        return self._do_request(uri)
