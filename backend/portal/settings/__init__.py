import sys
from split_settings.tools import include
from tendo import singleton


try:
    singleton.SingleInstance()
    include('base.py', 'celery.py', 'email.py', 'database.py', 'logging.py', 'local_settings.py')
except Exception as e:
    print("Error occurred while loading settings: ")
    print(e)
    sys.exit(-1)
