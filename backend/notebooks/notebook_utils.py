import os
import json
import sys
import django
from pathlib import Path


def goto_root_dir():
    if Path(os.getcwd()).name == 'notebooks':
        os.chdir('..')
        print('working dir changed to project root')
    else:
        print('working dir is already at the root')


def init_django():
    goto_root_dir()

    print('django setup')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    django.setup()

    for k in list(sys.modules.keys()):
        if k.startswith('_split_settings'):
            del sys.modules[k]

    print('done')


def read_json(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def read_txt(file_name):
    with open(file_name) as f:
        return f.read()
