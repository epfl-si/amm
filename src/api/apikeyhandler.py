"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from .apikey import APIKey
from .redis import exists, get_apikeys, save_key


class ApiKeyHandler:
    @staticmethod
    def validate(access, secret):
        """
        Check that the APIkey is valid
        """
        if access is None or secret is None:
            return None

        username = exists(access, secret)

        if username:
            return username
        return None

    @staticmethod
    def get_keys(username):
        """
        Returns the APIKeys of the given user
        """
        return get_apikeys(username=username)

    @staticmethod
    def generate_keys(username):
        """
        Generate an APIKey for the given user
        """
        the_key = APIKey()
        save_key(username, the_key)
        return the_key
