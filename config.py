import os #operating system
basedir = os.path.abspath(os.path.dirname(__file__))
# config = like the settings for an app
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'u-will-never-guess' #Password to prevent hackers
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db') #Creates URI (path) to SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False #So it doesn't send application a msg when changes are made

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None # For encrypted connections
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['lillian.ye06@gmail.com']