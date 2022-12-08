from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email
from wtforms.validators import EqualTo, Length
from app.models import User

from sqlalchemy import func

event_choices = [
    "#1 - Let's have a trial competition",
    "#2 - The real UCS will gonna torture you so badly"
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
    username = StringField('PIU Username', validators = [DataRequired()])
    event = SelectField('Select the Event', choices = event_choices, validators = [DataRequired()])
    perfect = IntegerField('Perfect')
    great = IntegerField('Great')
    good = IntegerField('Good')
    bad = IntegerField('Bad')
    miss = IntegerField('Miss')
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(SubmissionForm1, self).__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username(self, username):
        if username.data != self.original_username:
            raise ValidationError("please input the username used during login")
    
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
    username = StringField('Username', validators = [DataRequired()])
    about_me = StringField('About Me', validators = [Length(min = 0, max = 200)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username(self, username):
        #at the moment, we should not accommodate changing the username
        if username.data != self.original_username:
            raise ValidationError("please input the username used during login")