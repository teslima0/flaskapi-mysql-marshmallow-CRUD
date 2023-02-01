from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, validate
from.import app,db
import uuid
ma = Marshmallow(app)




def hexid():
    return uuid.uuid4().hex

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password=db.Column(db.String(500))
    #password=db.Column(db.String(500))
    def __init__(self,id, username, email,password):
        self.id=id
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '' % self.username

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username":self.username,
            "password":self.password.decode("utf-8")
            # Add any other relevant fields here
        }
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('products', lazy=True))

    def __init__(self, name, description, price, qty, user):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        self.user = user
    def __repr__(self):
        return '' % self.id

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class UserSchema(Schema):
    username = fields.Str(required=True, validate=[validate.Length(min=3, max=20)])
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=[validate.Length(min=6)])




class DriverRating(db.Model):
    __tablename__ = "driver_rating"

    id = db.Column(db.String(100), primary_key=True,index=True,default=hexid)
    rating_count = db.Column(db.Integer)
    rating_comment = db.Column(db.String(250), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #history_id = db.Column(db.String(100), db.ForeignKey('journeyhistory.id'), nullable=False, index=True)
    #driver_id = db.Column(db.String(100), db.ForeignKey('driver.id'), nullable=False, index=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


 


