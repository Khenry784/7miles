from flask_wtf.file import FileRequired,FileField,FileAllowed, DataRequired
from wtforms import  IntegerField, StringField,BooleanField,TextAreaField,validators
from werkzeug.utils import secure_filename
from flask_wtf import Form



class AddItemForm(Form):
    title= StringField('Title',validators=[DataRequired('Name of the item.')])
    description= TextAreaField('Description', validators=[DataRequired('A description is required')])
    price = IntegerField('Price', validators=[DataRequired()])
    quantity= IntegerField('Quantity',validators=[DataRequired('Amount of item in stock')])
    