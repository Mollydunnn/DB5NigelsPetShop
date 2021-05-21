from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import mysql.connector as mysql
from sqlalchemy import create_engine

''' Connect to MySQL database '''


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from flaskDemo import routes
from flaskDemo import models
from flaskDemo import forms

models.db.create_all()
forms.db.create_all()

#if __name__ == '__main__':
 #   conn()
