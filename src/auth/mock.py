from config.settings import base


class Authenticator(object):

    def authenticate(self, username, password):

        return username == base.get_config('TEST_USERNAME') and password == base.get_config('TEST_CORRECT_PWD')
