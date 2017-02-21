"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from config.settings import base


class Authenticator(object):

    def authenticate(self, username, password):

        """Mock version of authenticate needed because we don't have access to the LDAP server"""

        return False
        
        #return username == base.get_config('TEST_USERNAME') and password == base.get_config('TEST_CORRECT_PWD')
