from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Person, Inventory, Order1, OrderLine
from wtforms.fields.html5 import DateField

ProductName = Inventory.query.with_entities(Inventory.ProductName).distinct()
#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above

#ProductChoices2 = [(row[0],row[0]) for row in pn]  # change
results=list()
for row in ProductName:
    rowDict=row._asdict()
    results.append(rowDict)
ProductChoices = [(row['ProductName'],row['ProductName']) for row in results]

on = Order1.query.with_entities(Order1.OrderID).distinct()
results2=list()
for row in on:
    rowDict=row._asdict()
    results2.append(rowDict)
quantity = [(row['OrderID'],row['OrderID']) for row in results2]


class RegistrationForm(FlaskForm):
    Username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    Name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=25)])
    PersonID= IntegerField('ID',
                               validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, Username):
        User = Person.query.filter_by(Username=Username.data).first()
        if User:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    Username = StringField('Username',
                            validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    Username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])
    Name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=25)])
    submit = SubmitField('Update')

    def validate_username(self, Username):
        if Username.data != current_user.username:
            Person = Person.query.filter_by(Username=Username.data).first()
            if Person:
                raise ValidationError('That username is taken. Please choose a different one.')

    
#Adoption page layout?
#class PostForm(FlaskForm):
    #title = StringField('Title', validators=[DataRequired()])
    #content = TextAreaField('Content', validators=[DataRequired()])
    #submit = SubmitField('Post')

    
class AssignUpdateForm(FlaskForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
#  OrderID = HiddenField("")

    ProductName= SelectField('Product Name:', choices=ProductChoices)


#  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
    OrderID = SelectField("Order ID", choices=quantity)  # myChoices defined at top
    OrderedQuantity=IntegerField('OrderedQuantity', validators=[DataRequired()])
    
    submit = SubmitField('Update this order')

#    def validate_ProductName(ProductName):    # apparently in the company DB, dname is specified as unique
 #        order = Inventory.query.filter_by(ProductName=ProductName.data).first()
 #        if order and (str(order.OrderID) != str(self.OrderID.data)):
 #            raise ValidationError('That department name is already being used. Please choose a different name.')

class OrderForm(FlaskForm):

    OrderID=IntegerField('Order ID', validators=[DataRequired()])
    ProductName= SelectField('Product Name:', choices=ProductChoices)
    OrderedQuantity=IntegerField('OrderedQuantity', validators=[DataRequired()])
    submit = SubmitField('Add this order')

 #   def validate_Price(Price):
       # pricecheck=Inventory.query.get(Price)
       # if pricecheck:
       #     ap='Price'
       # else:
       #     ap= "30.00"
       #     return Price


    #def validate_OrderID(self, OrderID):    #because dnumber is primary key and should be unique
    #    order = Order1.query.filter_by(OrderID=OrderID.data).first()
        #order=OrderLine.query.filter_by(OrderID=OrderID.data).first()
      #  if order and (str(order.OrderID) != str(self.OrderID.data)):
         #   raise ValidationError('That order number is taken. Please choose a different one.')




