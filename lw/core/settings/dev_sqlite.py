from .base import *

DEBUG = True

SECRET_KEY = 'Zb9VbgDvNtc19k4lGWueoIwVlzI (change in production)'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
    }
}
