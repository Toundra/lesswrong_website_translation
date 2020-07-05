from .base import *

# FIXME: doesn't work without debug, quick fix
DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET_KEY', '')

try:
    from .local import *
except ImportError:
    pass
