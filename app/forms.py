from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField,validators,TextAreaField,IntegerField,FileField
from wtforms.validators import InputRequired,DataRequired,Optional,Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename


class RegistrationForm(FlaskForm):
    f_name= StringField('Firstname',validators=[DataRequired()])
    l_name= StringField("Surname",validators=[DataRequired()])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
   


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])



