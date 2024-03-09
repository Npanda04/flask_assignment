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

    # Relationship with Balance table
    balance = db.relationship('Balance', back_populates='user', uselist=False)


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)

    # Foreign key relationship with User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship with User table
    user = db.relationship('User', back_populates='balance')


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # include_relationships = True  # Include relationships in serialization


class BalanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Balance
        # include_relationships = True  # Include relationships in serialization
