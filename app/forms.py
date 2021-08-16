from flask_migrate import current
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, TextAreaField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email
from wtforms_components import DateRange, read_only
from flask_login import current_user
from app.models import User
import datetime

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    birthday = DateField("Birthday", validators=[DataRequired()], format='%Y-%m-%d')
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])    
    submit = SubmitField("Create account")

    def validate_username(self, username): # By default, functions that follow patten validate_*field_name*() will be automatically called when validating a form
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("This username is taken :(")
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("This email is taken.")

class OrderForm(FlaskForm):
    dish = StringField("Dish Ordered")
    date = DateField("Delivery Date", validators=[DataRequired(), DateRange(min=datetime.date(2021, 9, 9))], format='%Y-%m-%d', default=datetime.datetime(2021, 9, 9))
    quantity = IntegerField("How many?", validators=[DataRequired(), NumberRange(1)], default=1)
    instructions = TextAreaField("Special instructions?")
    submit = SubmitField("Purchase!")

    def validate_quantity(self, quantity):
        if int(quantity.data) > current_user.coupons >= 0:
            raise ValidationError("Not enough coupons!")
