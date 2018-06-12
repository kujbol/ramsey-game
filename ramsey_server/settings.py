import os

from envparse import env
import logging


log = logging.getLogger('app')
log.setLevel(logging.DEBUG)

f = logging.Formatter(
    '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
log.addHandler(ch)

root_dir = os.path.dirname(os.path.dirname(__file__))
env.read_envfile(os.path.join(root_dir, 'ramsey_server/.env'))

SITE_HOST = env.str('HOST')
SITE_PORT = os.environ.get('PORT', env.str('PORT'))
SECRET_KEY = env.str('SECRET_KEY')
