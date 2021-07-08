import os
__version__ = "2021.6.24"
RXN_ROOT = os.path.dirname(os.path.abspath(__file__))
RXN_FILES = os.path.join(RXN_ROOT, 'files')

# the uri has this format: mongodb://{username}:{password}@{host}:{port}/{database}
MONGODB_URI = os.environ.get("MONGODB_URI")
