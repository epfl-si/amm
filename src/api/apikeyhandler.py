"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import api.redis
import api.apikey


class ApiKeyHandler(object):
    def __init__(self):
        pass

    def validate(self, access, secret):
        """Check that the APIkey is valid"""
        if access is None or secret is None:
            return None

        username = api.redis.exists(access, secret)

        if username:
            return username
        return None

    def get_keys(self, username):
        """Returns the APIKeys of the given user"""
        return api.redis.get_apikeys(username=username)

    def generate_keys(self, username):
        """Generate an APIKey for the given user"""
        thekey = api.apikey.APIKey.generate()
        api.redis.save_key(username, thekey)
        return thekey
