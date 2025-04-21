from . import environ

env = environ.Env()

# If True returns traceback on HTTP 500
DEBUG = env.bool("DEBUG", False)

# For example http://192.168.1.2/values
SOURCE_DATA_URL = env.str("SOURCE_DATA_URL")
