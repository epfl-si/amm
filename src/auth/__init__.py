"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from config.settings import base


def get_configured_authenticator():
    mod = __import__('auth.' + base.get_config('AMM_AUTHENTICATOR_CLASS'), fromlist=['Authenticator'])
    return getattr(mod, 'Authenticator')()
