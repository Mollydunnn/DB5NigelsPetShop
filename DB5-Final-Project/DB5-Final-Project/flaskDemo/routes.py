import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, AssignUpdateForm, OrderForm, AdoptForm, AddAnimal, ImmunizationForm
from flaskDemo.models import User, Inventory, Order1, OrderLine, Animal, Adoption, Immunization, AnimalImmunization
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy import select, update
import datetime



@app.route("/")
@app.route("/home")
def home():
    results = Inventory.query.all()
    #return render_template('home.html', outString = results)
    #posts = Post.query.all()
    #return render_template('home.html')
    results2 = OrderLine.query.join(Inventory,OrderLine.InventoryID ==Inventory.InventoryID) \
               .add_columns(Inventory.InventoryID, Inventory.ProductName, OrderLine.OrderedQuantity, OrderLine.OrderID) \
               .join(Order1, Order1.OrderID == OrderLine.OrderID).add_columns(Order1.OrderDate)
    results = OrderLine.query.join(Inventory,OrderLine.InventoryID ==Inventory.InventoryID) \
               .add_columns(Inventory.InventoryID, Inventory.ProductName, OrderLine.OrderedQuantity, OrderLine.OrderID)
    return render_template('home.html', title='Join', joined_m_n=results2)



@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,employee=form.employee.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))







@app.route("/order/new", methods=['GET', 'POST'])
@login_required
def new_order():
    form = OrderForm()
    if form.validate_on_submit():
        orderLine= OrderLine(OrderedQuantity=form.OrderedQuantity.data,InventoryID=form.ProductName.data,OrderID=form.OrderID.data)
        order=Order1(OrderID=form.OrderID.data,OrderDate=datetime.datetime.now(),PersonID=current_user.id)
        db.session.add(orderLine)
        db.session.add(order)
        db.session.commit()
        flash('You have added a new order!', 'success')
        return redirect(url_for('home'))
    return render_template('create_order.html', title='New Order',
                           form=form, legend='New Order')


@app.route("/assign")
@login_required
def assign():
    OrderID=request.args.get('OrderID')
    InventoryID=request.args.get('InventoryID')
    assign = OrderLine.query.get_or_404([InventoryID, OrderID])
    return render_template('order.html', title=str(assign.OrderID)+"_"+str(assign.InventoryID),assign=assign, now=datetime.datetime.now())

@app.route("/assign/<OrderID>/<InventoryID>/delete", methods=['POST'])
@login_required
def delete_assign(OrderID,InventoryID):
    assign = OrderLine.query.get_or_404([InventoryID, OrderID])
    db.session.delete(assign)
    db.session.commit()
    flash('The item has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/assign/<OrderID>/<InventoryID>/update", methods=['GET','POST'])
@login_required
def update_assign(OrderID,InventoryID):
    assign = Inventory.query.get_or_404(InventoryID)
    assign2 = OrderLine.query.get_or_404([InventoryID, OrderID])
    currentAssign = assign.ProductName

    form = AssignUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        assign.OrderID=form.OrderID.data
        db.session.query(OrderLine).filter(OrderLine.OrderID== form.OrderID.data).update({OrderLine.OrderedQuantity: form.OrderedQuantity.data}, synchronize_session="fetch")
        db.session.query(OrderLine).filter(OrderLine.OrderID== form.OrderID.data).update({OrderLine.InventoryID: form.ProductName.data}, synchronize_session="fetch")
        db.session.commit()
        flash('Your order has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form
        assign2.OrderID = form.OrderID.data
        assign.ProductName = form.ProductName.data
        #form.mgr_start.data = dept.mgr_start
    return render_template('create_order.html', title='Update Order',
                           form=form, legend='Update Order')


@app.route("/adopt", methods=['GET', 'POST'])
def adopt():
    results = Animal.query.all()
    query = "SELECT COUNT(*) \
    FROM Animal \
    WHERE Animal.Status=1"
    count = list(db.session.execute(query))
    x,=count[0]
    return render_template('adopt.html', title='Adopt now!', count=x, results=results)

@app.route("/adopt/dogsonly", methods=['GET', 'POST'])
def dogsonly():
    query = "SELECT COUNT(*) \
    FROM Animal \
    WHERE Animal.Status=1 AND Animal.Type='Dog'"
    query1 = "SELECT *\
    FROM Animal \
    WHERE Animal.Status=1 AND Animal.Type='Dog'"
    count = list(db.session.execute(query))
    x,=count[0]
    results=db.session.execute(query1)
    return render_template('adopt.html', title='Adopt now!', count=x, results=results)

@app.route("/adopt/catsonly", methods=['GET', 'POST'])
def catsonly():
    query = "SELECT COUNT(*) \
    FROM Animal \
    WHERE Animal.Status=1 AND Animal.Type='Cat'"
    query1 = "SELECT *\
    FROM Animal \
    WHERE Animal.Status=1 AND Animal.Type='Cat'"
    count = list(db.session.execute(query))
    x,=count[0]
    results=db.session.execute(query1)
    return render_template('adopt.html', title='Adopt now!', count=x, results=results)

@app.route("/adopt/<AnimalID>/", methods=['GET','POST'])
@login_required
def adopt_pet(AnimalID):
    results = Animal.query.all()
    row= Animal.query.get_or_404(AnimalID)
    return render_template('adopt_pet.html', title= 'Adopt Me!', results=results, row=row)

@app.route("/adopt/<AnimalID>/assign", methods=['GET','POST'])
@login_required
def assign_adopt(AnimalID):
    form=AdoptForm()
    row= Animal.query.get_or_404(AnimalID)
    user=current_user.id
    Adoption1= Adoption(AnimalID=row.AnimalID, CustomerID=user, DateOfAdoption=datetime.datetime.now())
    if form.validate_on_submit():
        db.session.query(Animal).filter(Animal.AnimalID==row.AnimalID).update({Animal.Status: 0 }, synchronize_session="fetch")
        db.session.add(Adoption1)
        db.session.commit()
        flash('Congrats! You adopted '+ row.AnimalName, 'success')
        redirect(url_for('home'))
    return render_template('assign_adopt.html', title= 'Adopt Me!', row=row, form=form)

@app.route("/add_animal", methods=['GET','POST'])
@login_required
def add_animal():
    form=AddAnimal()
    if form.validate_on_submit():
        Animal1= Animal(AnimalName=form.AnimalName.data,Type=form.Type.data,Gender=form.Gender.data,Breed=form.Breed.data,Neutered=form.Neutered.data,Declawed=form.Declawed.data)
        db.session.add(Animal1)
        db.session.commit()
        flash('You have added a new animal!', 'success')
        return redirect(url_for('home'))
    return render_template('add_animal.html', title='New Animal',
                           form=form, legend='New Animal')


@app.route("/immunization/add_immunization", methods=['GET','POST'])
@login_required
def add_immunization():
    form=ImmunizationForm()
    Imm1= AnimalImmunization(AnimalID=form.AnimalID.data, ImmunizationID=form.ImmunizationName.data, ImmunizationDate=datetime.datetime.now())
    if form.validate_on_submit():
        db.session.add(Imm1)
        db.session.commit()
        flash('You have added a new immunization!', 'success')
        return redirect(url_for('home'))
    return render_template('UpdatePetImmunization.html', title='New Vaccine',
                           form=form, legend='New Vaccine')


@app.route("/immunization", methods=['GET','POST'])
@login_required
def immunization():
    query= "SELECT \
    Animal.AnimalName, \
    Animal.Gender, \
    Immunization.ImmunizationName, \
    AnimalImmunization.ImmunizationDate \
    FROM Animal \
    JOIN AnimalImmunization, Immunization WHERE Animal.AnimalID= AnimalImmunization.AnimalID \
    AND Immunization.ImmunizationID= AnimalImmunization.ImmunizationID "
    results3 = db.session.execute(query)
    subquery="SELECT COUNT(*) \
    FROM AnimalImmunization \
    WHERE  DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) > ImmunizationDate"
    results4 = list(db.session.execute(subquery))
    x,=results4[0]
    return render_template('Immunization.html', title='Join', results4=x, joined_m_n=results3)
