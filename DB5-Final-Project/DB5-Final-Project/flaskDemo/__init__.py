from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import mysql.connector as mysql
from sqlalchemy import create_engine

''' Connect to MySQL database '''
#try:
#   conn = mysql.connector.connect(host='45.55.59.121',
#                                  database='DB5',      
 #                                  user='DB5',
 #                                  password='studentDB5')
 
   
#finally:
#   conn.close()
#    print ("done")


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://DB5:studentDB5@45.55.59.121/DB5'
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
