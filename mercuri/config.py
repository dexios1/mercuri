import os
from flask import Flask
# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = Flask(__name__).instance_path


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['christopher.dare@st.vvu.edu.gh']
    LANGUAGES = ['en', 'es']
    SENTRY_URL = "https://bb0a3cdad37040938b082d9a446edfd7@sentry.io/1331904"
