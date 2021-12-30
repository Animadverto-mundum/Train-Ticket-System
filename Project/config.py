import os

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'



PASSWORD =''

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'railway'
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True


SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)

UPLOAD_FOLDER=r'User/static/avatar/'
UPLOAD_FOLDER_SAVE=r'static/avatar/'
FACE_FOLDER=r'User/static/face/'
ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg'])