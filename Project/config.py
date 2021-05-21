import os

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'zyp991130'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'railway'
DEBUG = True

SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
