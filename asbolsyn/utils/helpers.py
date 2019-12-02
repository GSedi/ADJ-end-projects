import os
from datetime import date
from django.conf import settings


def create_log_dir_if_not_exists(name):
    dir = os.path.join(settings.BASE_DIR, 'logs/') \
          + date.today().year.__str__()\
          + '/' + date.today().month.__str__()\
          + '/' + date.today().day.__str__()\
          + f'/{name}/'

    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir + name + '.log'
