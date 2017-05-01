"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'HOST': '127.0.0.1',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'test',
    }
}
