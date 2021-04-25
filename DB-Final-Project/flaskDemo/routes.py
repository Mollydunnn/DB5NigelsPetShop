import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, AssignUpdateForm, OrderForm
from flaskDemo.models import Person, Inventory, Order1, OrderLine
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy import select


@app.route("/")
@app.route("/home")
def home():
    results = Inventory.query.all()
    #return render_template('assign_home.html', outString = results)
    #posts = Post.query.all()
    #return render_template('home.html')
    results2 = OrderLine.query.join(Inventory,OrderLine.InventoryID ==Inventory.InventoryID) \
               .add_columns(Inventory.InventoryID, Inventory.ProductName, OrderLine.OrderedQuantity, OrderLine.OrderID) \
               .join(Order1, Order1.OrderID == OrderLine.OrderID).add_columns(Order1.OrderDate)
    results = OrderLine.query.join(Inventory,OrderLine.InventoryID ==Inventory.InventoryID) \
               .add_columns(Inventory.InventoryID, Inventory.ProductName, OrderLine.OrderedQuantity, OrderLine.OrderID)
    return render_template('assign_home.html', title='Join', joined_m_n=results2)

   

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        user = Person(Username=form.Username.data, Name=form.Name.data, Password=form.Password.data)
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
        user = Person.query.filter_by(Username=form.Username.data).first()
        
        if user and bcrypt.check_password_hash(user.Password, form.Password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check Username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/account", methods=['GET', 'POST'])
#@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)




@app.route("/order/new", methods=['GET', 'POST'])
#@login_required
def new_order():
    form = OrderForm()
    if form.validate_on_submit():
        #iid= Inventory.query().filter(Inventory.InventoryID== (Inventory.ProductName==form.ProductName.data)).first()
        #iid= Inventory.query.filter_by(InventoryID==form.ProductName.data).first()
        #iid=(InventoryID==form.ProductName.data)
        order= OrderLine(OrderedQuantity=form.OrderedQuantity.data,InventoryID=(Inventory.query.filter_by(InventoryID=form.ProductName.data).first()),OrderID=form.OrderID.data)
        db.session.add(order)
        db.session.commit()
        flash('You have added a new order!', 'success')
        return redirect(url_for('home'))
    return render_template('create_assign.html', title='New Order',
                           form=form, legend='New Order')


@app.route("/assign")
#@login_required
def assign():
    OrderID=request.args.get('OrderID')
    InventoryID=request.args.get('InventoryID')
    assign = OrderLine.query.get_or_404([OrderID, InventoryID])
    return render_template('assign.html', title=str(assign.OrderID)+"_"+str(assign.InventoryID),assign=assign, now=datetime.utcnow())


#@app.route("/dept/<dnumber>/delete", methods=['POST'])
#@login_required
#def delete_dept(dnumber):
#    dept = Department.query.get_or_404(dnumber)
#    db.session.delete(dept)
#    db.session.commit()
#    flash('The department has been deleted!', 'success')
#    return redirect(url_for('home'))

@app.route("/assign/<OrderID>/<InventoryID>/delete", methods=['POST'])
#@login_required
def delete_assign(OrderID,InventoryID):
    assign = OrderLine.query.get_or_404([OrderID,InventoryID])
    db.session.delete(assign)
    db.session.commit()
    flash('The item has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/assign/<OrderID>/<InventoryID>/update", methods=['GET','POST'])
#@login_required
def update_assign(OrderID,InventoryID):
    #return "update page under construction"
    assign = Inventory.query.get_or_404(InventoryID)
    assign2 = OrderLine.query.get_or_404([OrderID, InventoryID])
    currentAssign = assign.ProductName

    form = AssignUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentAssign!=form.ProductName.data:
            assign.ProductName=form.ProductName.data
        #assign.OrderID=form.OrderID.data
        #assign.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your order has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form

        form.OrderID.data = assign2.OrderID
        form.ProductName.data = assign.ProductName
        #form.mgr_start.data = dept.mgr_start
    return render_template('create_assign.html', title='Update Order',
                           form=form, legend='Update Order')
    
