

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



db = SQLAlchemy()
ma = Marshmallow()





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    place = db.Column(db.String(50), nullable=True)




class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # include_relationships = True  # Include relationships in serialization


