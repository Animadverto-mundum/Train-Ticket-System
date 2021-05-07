import os

DEBUG = True

SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:wgtwgt0017@127.0.0.1:3306/railway?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True