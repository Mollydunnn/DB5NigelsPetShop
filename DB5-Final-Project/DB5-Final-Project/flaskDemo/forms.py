from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db,app
from flaskDemo.models import User, Inventory, Order1, OrderLine, AnimalImmunization, Animal, Immunization
from wtforms.fields.html5 import DateField

ProductName = Inventory.query.with_entities(Inventory.ProductName,Inventory.InventoryID).distinct()
#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above

#ProductChoices2 = [(row[0],row[0]) for row in pn]  # change
results=list()
for row in ProductName:
    rowDict=row._asdict()
    results.append(rowDict)
    
ProductChoices = [(row['InventoryID'],row['ProductName']) for row in results]

on = Order1.query.with_entities(Order1.OrderID).distinct()
results2=list()
for row in on:
    rowDict=row._asdict()
    results2.append(rowDict)
quantity = [(row['OrderID'],row['OrderID']) for row in results2]


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    options=['Yes','No']  
    employee=SelectField('Employee?', choices=options)                                
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

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
    ProductName= SelectField('Product Name', choices=ProductChoices)
    OrderedQuantity=IntegerField('OrderedQuantity', validators=[DataRequired()])
    submit = SubmitField('Add this order')


class AdoptForm(FlaskForm):
    Months=[1,2,3,4,5,6,7,8,9,10,11,12]
    Days=['Mon','Tue','Wed','Thu','Fri']
    Month=SelectField('Month', choices=Months)
    Day=SelectField('Day', choices=Days)
    submit = SubmitField('Adopt This Animal')


class AddAnimal(FlaskForm):
    AnimalName=StringField('Animal Name', validators=[DataRequired()])
    t=['Dog','Cat']
    Type=SelectField('Animal Type', choices=t)
    g=['M','F']
    Gender=SelectField('Sex', choices=g)
    Breed=StringField('Breed', validators=[DataRequired()])
    y=['Y','N']
    Neutered=SelectField('Neutered?', choices=y)
    Declawed=SelectField('Declawed?',choices=y)
    submit = SubmitField('Add This Animal')

ImmunizationName = Immunization.query.with_entities(Immunization.ImmunizationName,Immunization.ImmunizationID).distinct()

resultsImm=list()
for row in ImmunizationName:
    rowDict=row._asdict()
    resultsImm.append(rowDict)
    
ImmunizationChoices = [(row['ImmunizationID'],row['ImmunizationName']) for row in resultsImm]


class ImmunizationForm(FlaskForm):
    ImmunizationName= SelectField('Immunization Name:', choices=ImmunizationChoices)
    AnimalID = IntegerField("Animal ID", validators=[DataRequired()])  # myChoices defined at top
    submit = SubmitField('Add this Immunization')


