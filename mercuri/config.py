from flask import Flask
from environs import Env
basedir = Flask(__name__).instance_path
env = Env()
env.read_env()


class Config(object):
    ENV = env.str('FLASK_ENV', default='production')
    DEBUG = ENV == 'development'
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
    SECRET_KEY = env.str('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = env.str('MAIL_SERVER')
    MAIL_PORT = env.int('MAIL_PORT') or 25
    MAIL_USE_TLS = env.str('MAIL_USE_TLS') is not None
    MAIL_USERNAME = env.str('MAIL_USERNAME')
    MAIL_PASSWORD = env.str('MAIL_PASSWORD')
    ADMINS = ['christopher.dare@st.vvu.edu.gh']
    LANGUAGES = ['en', 'es']
    SENTRY_URL = env.str('SENTRY_URL')
    #  because we don't want this kind of logging to happen in development but only on heroku:
    # LOG_TO_STDOUT = env.int('LOG_TO_STDOUT')
