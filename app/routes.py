from flask_migrate import current
from app import app, db, mail
from app.forms import LoginForm, RegisterForm, OrderForm
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Order
from werkzeug.urls import url_parse
from flask_mail import Message, Mail
from datetime import datetime
import json
import requests
"""
flask imports:
1. Takes in a template and list of variables, returns template with placeholders filled with variables
2. Shows msg to user
3. redirects user to another url
5. contains all info from client (request.args shows it in a dictionary format)

Decorators
@app.route('*link*') 
def function():
    pass
When going to the link in the application, 
the decorator will call the function below it
and pass the return result back to the web browser

GET vs POST
Default = GET 
GET gets info for user
POST submits info to browser

"""

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if current_user.is_authenticated:
        redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # If form submitted (POST & all validators = True)
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc == '': # 2nd checks if next_page is going to page in website
            return redirect(url_for('index'))
        return redirect(url_for(next_page))
        # return render_template('index.html', title='Home', user=user)
    return render_template('login.html', title="Log in", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, birthday=form.birthday.data)
        user.set_password(form.password.data)
        user.set_coupon_count(1)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you are now a registered user, User {}!'.format(user.username))
        flash('By creating an account, you will receive one FREE coupon to purchase items in this website!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/menu')
def menu():
    return render_template('menu.html', title='Menu')

@app.route('/order/<dish>', methods=['GET', 'POST'])
@login_required
def order(dish):
    form = OrderForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first_or_404()
        quantity = form.quantity.data
        date = form.date.data
        today = datetime.today()
        user.set_coupon_count(user.coupons-quantity)
        order = Order(dish=form.dish.data, quantity=quantity, order_date=today, delivery_date=date, user_id=user.id, instructions=form.instructions.data)
        db.session.add(order)
        db.session.commit()
        try:
            try:
                msg = Message('Order confirmed', sender = app.config['ADMINS'][0], recipients = ['lillian.ye06@gmail.com'])
                msg.body = "Your order has been confirmed. It will be delivered on " + date.strftime("%B %d, %Y") + \
                ". Thank you for ordering at Shiawase! \n \nORDER DETAILS \n" + form.dish.data + "\n" + \
                "Date ordered: " + today.strftime("%B %d, %Y") + "\n" + \
                "Delivery Date: " + date.strftime("%B %d, %Y") + "\n" + "Cost: " + str(quantity) + " coupon(s). " +\
                "\nSpecial Instructions: \n" + form.instructions.data + "\n\n\nFor any questions, please email back!"\
                "\nYours truly, \nShiawase"
                mail.send(msg)
            except:
                pass
            msg = Message('Order confirmed', sender = app.config['ADMINS'][0], recipients = [user.email])
            msg.body = "Your order has been confirmed. It will be delivered on " + date.strftime("%B %d, %Y") + \
            ". Thank you for ordering at Shiawase! \n \nORDER DETAILS \n" + form.dish.data + "\n" + \
            "Date ordered: " + today.strftime("%B %d, %Y") + "\n" + \
            "Delivery Date: " + date.strftime("%B %d, %Y") + "\n" + "Cost: " + str(quantity) + " coupon(s). " +\
            "\nSpecial Instructions: \n" + form.instructions.data + "\n\n\nFor any questions, please email back!"\
            "\nYours truly, \nShiawase"
            mail.send(msg)
            flash("Your order has been confirmed. Please check your email for confirmation.")
            
        except:
            flash("Your order has been confirmed. Thank you for ordering at Shiawase!")
        return redirect(url_for('menu'))
    return render_template('order.html', dish=dish, title='Order Dish', form=form)
    
@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='User '+ user.username, user=user)

@app.route('/orders/<filter>/<username>')
@login_required
def orders(username, filter):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        flash("You do not have access to this page.")
        return redirect(url_for("index"))
    user.check_orders()
    if filter != "default":
        current = get_filter(filter, False, user)
    else:
        current = Order.query.filter_by(user_id=user.id, completed=False).order_by(Order.order_date.asc()).all()
    return render_template('orders.html', title='Orders', filter=filter, orders=current, user=user, heading="Orders in Progress", delivered="Delivery Date:")

@app.route('/completed-orders/<filter>/<username>')
@login_required
def completed_orders(username, filter):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        flash("You do not have access to this page.")
        return redirect(url_for("index"))
    user.check_orders()
    if filter != 'default':
        finished = get_filter(filter, True, user)
        return render_template('orders.html', title='Completed Orders', orders=finished, user=user, heading="Completed Orders", delivered="Date Delivered:")
    else: 
        finished = Order.query.filter_by(user_id=user.id, completed=True).order_by(Order.order_date.asc()).all()
    return render_template('orders.html', title='Completed Orders', filter=filter, orders=finished, user=user, heading="Completed Orders", delivered="Date Delivered:")

@app.route('/bday', methods=['POST'])
@login_required
def bday():
    if current_user.is_authenticated:
        u = User.query.filter_by(username = current_user.username).first()
        if u.check_bday() and not u.bday_celebrated:
            u.bday_celebrated = True
            u.set_coupon_count(u.coupons + 5)
            db.session.commit()
    return jsonify({"bday": "complete"})
        
def get_filter(s, complete, user):
    if s == "Dish":
        return Order.query.filter_by(user_id=user.id, completed=complete).order_by(Order.dish.asc()).all()
    elif s == "Date ordered":
        return Order.query.filter_by(user_id=user.id, completed=complete).order_by(Order.order_date.asc()).all()
    elif s == "Delivery Date":
        return Order.query.filter_by(user_id=user.id, completed=complete).order_by(Order.delivery_date.asc()).all()
    return Order.query.filter_by(user_id=user.id, completed=complete).order_by(Order.delivery_date.asc()).all()