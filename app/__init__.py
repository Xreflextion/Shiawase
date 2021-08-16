"""
Defines what we get from an imported package to use in our app
Initializes packages as variables
"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import SMTPHandler # this + ^ will send errors to ur email
from flask_mail import Mail
from flask_jsglue import JSGlue

app = Flask(__name__) #app becomes instance of Flask class
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login' #Tells LoginManager which view function is in charge of logging in users
bootstrap = Bootstrap(app)
mail = Mail(app)
jsglue = JSGlue(app)


from app import routes, models, errors
# ^App means app folder
"""
routes = different URLs in Flask application, each route is handled with a 'view function'
models = module to define structure of database
"""

# if not app.debug: # Only emails when not in debugging mode
#     if app.config["MAIL_SERVER"]:
#         auth = None
#     else:
#         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#         secure = None
#         if app.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler( # Creates SMTPHandler 
#             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#             toaddrs=app.config['ADMINS'], subject='Error in Website',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR) # So you only get emails for errors
#         app.logger.addHandler(mail_handler) # Adds handler to app.logger
