from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from sqlalchemy.exc import IntegrityError
from app.models import db, User, UserSchema


user_routes_bp = Blueprint('user_routes', __name__)
api = Api(user_routes_bp)

user_parser = reqparse.RequestParser()
user_parser.add_argument('firstname', type=str, required=True, help='First name is required')
user_parser.add_argument('lastname', type=str, default='', help='Last name')
user_parser.add_argument('username', type=str, required=True, help='Username is required')
user_parser.add_argument('place', type=str, default='', help='Place')

user_schema = UserSchema()

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return {'users': user_schema.dump(users)}

    def post(self):
        args = user_parser.parse_args()
        new_user = User(
            firstname=args['firstname'],
            lastname=args['lastname'],
            username=args['username'],
            place=args['place']
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Username must be unique'}, 400

class UserResource(Resource):
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        args = user_parser.parse_args()
        user.firstname = args['firstname']
        user.lastname = args['lastname']
        user.username = args['username']
        user.place = args['place']
        try:
            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Username must be unique'}, 400

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200

api.add_resource(UserListResource, '/api/v1/user')
api.add_resource(UserResource, '/api/v1/user/<int:user_id>')
