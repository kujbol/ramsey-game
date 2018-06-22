import os

from envparse import env

root_dir = os.path.dirname(os.path.dirname(__file__))
env.read_envfile(os.path.join(root_dir, 'ramsey_server/.env'))


class Settings:
    SITE_HOST = env.str('HOST')
    SITE_PORT = os.environ.get('PORT', env.str('PORT'))
    SECRET_KEY = env.str('SECRET_KEY')

