from app import db
from datetime import datetime


class AddItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    price= db.Column(db.Numeric(10,2), nullable=False)

    quantity= db.Column(db.Integer, nullable=False)

    #photo= db.Column(db.String(150), nullable=False,default='image.jpg')

    def __repr__(self):
        return '<AddItem %r>' % self.title

class Brand(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30), nullable=False, unique=True)


class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30), nullable=False, unique=True)


db.create_all()