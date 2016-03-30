import sendgrid
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

import config as cfg

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = cfg.DatabaseConfig['SQLALCHEMY_DATABASE_URI']

login_manager = LoginManager(app)
db = SQLAlchemy(app)

client = sendgrid.SendGridClient(cfg.MailConfig['SENDGRID_API_KEY'])

from app import views, models
