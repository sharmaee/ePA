import os
from portal.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'portal.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}
