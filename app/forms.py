from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email
from wtforms.validators import EqualTo, Length

from app.models import User
from app.config import current_event, events
from app.ippt_calculator import categories, stations

from sqlalchemy import func

import re

# Get the list of event directly from the current_event config in routes.py
choices = [
    (current_event, events[current_event])
]

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField('PIU Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        #only allow username with all lowercase letters
        if username.data != username.data.lower():
            raise ValidationError("username should contain only lowercase letters")

        #username that has been stored in database cannot be reused
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("please select a different username")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError("please use the different email address")

class SubmissionForm1(FlaskForm):
    event = SelectField('Select the Event', choices = choices, validators = [DataRequired()])
    chart = SelectField('Select the Stepchart', choices = [], validators = [DataRequired()])
    perfect = IntegerField('Perfect')
    great = IntegerField('Great')
    good = IntegerField('Good')
    bad = IntegerField('Bad')
    miss = IntegerField('Miss')
    set_number = IntegerField('Set Number')
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(SubmissionForm1, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_perfect(self, perfect):
        if perfect.data < 0:
            raise ValidationError("the inputted number should be at least 0")

    def validate_great(self, great):
        if great.data < 0:
            raise ValidationError("the inputted number should be at least 0")

    def validate_good(self, good):
        if good.data < 0:
            raise ValidationError("the inputted number should be at least 0")

    def validate_bad(self, bad):
        if bad.data < 0:
            raise ValidationError("the inputted number should be at least 0")

    def validate_miss(self, miss):
        if miss.data < 0:
            raise ValidationError("the inputted number should be at least 0")

class EditProfileForm(FlaskForm):
    cats = [(key, categories[key]) for key in categories]
    cats.insert(0, (0, "Not Specified")) # for backward compatibility, old profile might not have title

    username = StringField('Username', validators = [DataRequired()])
    about_me = StringField('About Me', validators = [Length(min = 0, max = 200)])
    title = SelectField('Title', choices=cats, validators=[DataRequired()])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        #at the moment, we should not accommodate changing the username
        if username.data != self.original_username:
            raise ValidationError("please input the username used during login")

class CommaSeparatedUserInputForm(FlaskForm):
    user_input = StringField('List of comma-separated string')
    submit = SubmitField("Submit")

    def validate_user_input(self, user_input):
        # only allow comma-separated alphanumeric string
        comma_separated_pattern = re.compile("^([a-zA-Z0-9]+,?\s*)+(?<!,)$")
        if re.match(comma_separated_pattern, user_input.data) is None:
            raise ValidationError("input should only be comma-separated alphanumeric string without trailing comma")

class IpptCalculatorForm(FlaskForm):
    stats = [(key, stations[key]) for key in stations]
    cats = [(key, categories[key]) for key in categories]

    ex_score = FloatField('EX-Score, as shown in your Profile Page', validators=[DataRequired()])
    station = SelectField('Select Station', choices=stats, validators=[DataRequired()])
    category = SelectField('Select Category', choices=cats, validators=[DataRequired()])
    submit = SubmitField("Calculate")

