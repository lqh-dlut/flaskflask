#content database information
HOSTNAME = 'localhost'
PORT = 3306
USERNAME = "root"
PASSWORD = "root"
DATABASE = "flaskdb"

#redis inf
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False

#mail inf
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = '1367445047@qq.com'
MAIL_PASSWORD = 'uwelvyyelpkpgihc'
MAIL_DEFAULT_SENDER = ('刘启昊', '1367445047@qq.com')

#celery
CELERY_BROKER_URL='redis://localhost:6379/0',
CELERY_RESULT_BACKEND='redis://localhost:6379/0'
