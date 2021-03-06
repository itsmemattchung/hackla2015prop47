from .base import *

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Allow all host headers
ALLOWED_HOSTS = ['*']

DEBUG = False
