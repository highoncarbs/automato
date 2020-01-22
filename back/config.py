# Config for automato 
# WTF config
class Config(object):

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'the_very_secure_secret_security_key_that_no_will_ever_guess'

    # MySQL Config

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:alpine@127.0.0.1/reautomato'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RABBITMQ_HOST = "localhost"

    WEBDRIVER_PATH = r"C:\Users\padam\Downloads\chromedriver_win32\chromedriver.exe"
    TESTING = False

    UPLOAD_FOLDER = './../front/static/uploads'

