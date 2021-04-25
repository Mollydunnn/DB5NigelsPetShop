from datetime import date
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))


class Person(db.Model, UserMixin):
    # __table__ = db.Model.metadata.tables['Person']
    __table_args__ = {'extend_existing': True}
    PersonID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(25), unique=True, nullable=False)
    Password = db.Column(db.String(25), nullable=False)
    Name = db.Column(db.String(25), unique=True, nullable=False)
    ShippingAddress = db.Column(db.String(40), nullable=True)
    BillingAddress = db.Column(db.String(40), nullable=True)
    EmployeePosition= db.Column(db.String(25), nullable=True)
    #EmployeeType= db.Column(db.Boolean, nullable=True)
    #CustomerType= db.Column(db.Boolean, nullable=True)

    #def __repr__(self):
        #return f"Person('{self.Username}', '{self.Name}')"

class Inventory(db.Model):
      __table__ = db.Model.metadata.tables['Inventory']
      


class Order1(db.Model):
    __table__ = db.Model.metadata.tables['Order1']
   # __table_args__ = {'extend_existing': True}
    #OrderID = db.Column(db.Integer, primary_key=True)
    #OrderDate = db.Column(db.Date,nullable=True)
    #PersonID = db.Column(db.Integer,db.ForeignKey(Person.PersonID), nullable=True)

class OrderLine(db.Model):
    __table__ = db.Model.metadata.tables['OrderLine']
    #__table_args__ = {'extend_existing': True}
    #OrderedQuantity= db.Column(db.Integer)
    #InventoryID = db.Column(db.Integer,db.ForeignKey(inventory.InventoryID), nullable=True)
    #OrderId = db.Column(db.Integer,db.ForeignKey(order1.OrderID), nullable=True)


    

  
