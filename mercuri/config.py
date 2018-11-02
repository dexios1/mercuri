import os
from flask import Flask
# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = Flask(__name__).instance_path


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'mercuri.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
