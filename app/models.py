from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import False_
from wtforms.fields.core import DateField
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash #already downloaded with flask
from flask_login import UserMixin #includes generic functions needed for flask_login
from datetime import datetime

"""
SQl query functions
*Model*.query.filter_by(*columnType*=*item*).first()
^Gets first object in database that matches filter
*Model*.query.all()
^Gets all created models of that model
*Model*.query.get(*id*)
^Gets a model with their id
*Model*.query.order_by(*Model*.*column*.*desc()/asc()*).all()
^Gets all models of that model ordered descending based on column
"""

@login.user_loader #loads user when they're online
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    birthday = db.Column(db.Date())
    password_hash = db.Column(db.String(128))
    coupons = db.Column(db.Integer)
    bday_celebrated = db.Column(db.Boolean(), default=False)
    received_coupons = db.Column(db.Boolean())
    orders = db.relationship("Order", backref="Buyer", lazy="dynamic") #not a part of the table 
    """
    db.relationship(<model that = many in the relationship>, <what the model that = one is referenced as in the 'many' connection>) 
    ^to get access to all orders on other side of connection.
    """

    def __repr__(self): #How objects of this class are printed out
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_coupon_count(self, num):
        self.coupons = num

    def check_bday(self):
        return self.birthday.strftime('%m-%d') == datetime.today().strftime('%m-%d')

    def check_orders(self):
        orders = Order.query.filter_by(user_id=self.id, completed=False).all()
        for order in orders:
            order.complete_order()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish = db.Column(db.String(32), index=True)
    quantity = db.Column(db.Integer)
    order_date = db.Column(db.Date(), default=datetime.today, index=True) # Not adding () after .utcnow means ur passing in the function, not the return result
    delivery_date = db.Column(db.Date(), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Foreignkey will reference the id value from users table
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self): #How objects of this class are printed out
        return '<Order {}>'.format(self.dish)

    def complete_order(self):
        if self.delivery_date.strftime('%Y-%m-%d') == datetime.today().strftime('%Y-%m-%d'):
            self.completed = True

    def format_date(self, date, format):
        return date.strftime(format)