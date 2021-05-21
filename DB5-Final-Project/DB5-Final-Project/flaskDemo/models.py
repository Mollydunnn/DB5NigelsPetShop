from datetime import date
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Inventory(db.Model):
      __table__ = db.Model.metadata.tables['Inventory']
      


class Order1(db.Model):
    __table__ = db.Model.metadata.tables['Order1']


class OrderLine(db.Model):
    __table__ = db.Model.metadata.tables['OrderLine']


class Animal(db.Model):
    __table__ = db.Model.metadata.tables['Animal']

class Adoption(db.Model):
    __table__ = db.Model.metadata.tables['Adoption']
    
class Immunization(db.Model):
    __table__ = db.Model.metadata.tables['Immunization']
    
class AnimalImmunization(db.Model):
    __table__ = db.Model.metadata.tables['AnimalImmunization']

  
