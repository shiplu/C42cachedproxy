import os
import configparser

import json
import consul
import datetime
from cachedproxy.environment import ENVIRONTMENTS


def factory(environment, consul_host):
    if environment in ENVIRONTMENTS:
        return ConfigConsul(ENVIRONTMENTS[environment], consul_host)
    else:
        return ConfigIni("config.ini")


class Config(object):
    """
    Base config object
    """
    @property
    def user_id(self):
        raise Exception("Not implemented")

    @property
    def email(self):
        raise Exception("Not implemented")

    @property
    def password(self):
        raise Exception("Not implemented")

    @property
    def api_token(self):
        raise Exception("Not implemented")

    @property
    def service_id(self):
        raise Exception("Not implemented")

    @property
    def event_id(self):
        raise Exception("Not implemented")


class ConfigConsul(Config):
    def __init__(self, environment, consul_host):
        self.consul_client = consul.Consul(host=consul_host)
        self.environment = environment
        self.data = {}
        self.threshold = datetime.timedelta(seconds=300)
        # Make sure the last_updated is already too old
        self.last_updated = datetime.datetime.now() - 2 * self.threshold

    def get_config(self, name):
        """
        Return a config value, periodically retrieve it again from consul
        """
        if(datetime.datetime.now() - self.last_updated > self.threshold):
            _, data = self.consul_client.kv.get("config/{}/cachedproxy".format(self.environment))
            self.data = json.loads(data['Value'])
            self.last_updated = datetime.datetime.now()
        return self.data[name]

    @property
    def user_id(self):
        return self.get_config("user_id")

    @property
    def email(self):
        return self.get_config("email")

    @property
    def password(self):
        return self.get_config("password")

    @property
    def api_token(self):
        return self.get_config("api_token")

    @property
    def service_id(self):
        return self.get_config("service_id")

    @property
    def event_id(self):
        return self.get_config("event_id")


class ConfigIni(Config):
    def __init__(self, filename):
        parser = configparser.ConfigParser()
        parser.read(os.path.dirname(os.path.abspath(__file__)) + "/../{}".format(filename))

        self.data = {}
        if 'Default' in parser.sections():
            self.data = parser.sections()['Default']

    @property
    def user_id(self):
        return self.data.get("user_id")

    @property
    def email(self):
        return self.data.get("email")

    @property
    def password(self):
        return self.data.get("password")

    @property
    def api_token(self):
        return self.data.get("api_token")

    @property
    def service_id(self):
        return self.data.get("service_id")

    @property
    def event_id(self):
        return self.data.get("event_id")
