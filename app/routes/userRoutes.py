from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from sqlalchemy.exc import IntegrityError
from app.models import db, User, UserSchema, Balance, BalanceSchema
from random import randint
from sqlalchemy.orm import joinedload



user_routes_bp = Blueprint('user_routes', __name__)
api = Api(user_routes_bp)

user_parser = reqparse.RequestParser()
user_parser.add_argument('firstname', type=str, required=True, help='First name is required')
user_parser.add_argument('lastname', type=str, default='', help='Last name')
user_parser.add_argument('username', type=str, required=True, help='Username is required')
user_parser.add_argument('place', type=str, default='', help='Place')

user_schema = UserSchema(many= True)



class HealthCheckResource(Resource):
    def get(self):
        return {'status': 'Server is up and running'}

class UserListResource(Resource):
    def get(self):
        # Assuming you have pagination parameters (page, per_page)
        page = int(request.args.get('page', default=1))
        per_page = int(request.args.get('per_page', default=5))

        offset = (page - 1) * per_page

        # Query users with pagination and include balance details
        users_with_balance = (
            User.query
            .options(joinedload(User.balance))  # Adjust the relationship name based on your implementation
            .order_by(User.username)
            .offset(offset)
            .limit(per_page)
            .all()
        )

        # Extract user and balance data
        result = [
            {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
                'place': user.place,
                'amount': user.balance.amount if user.balance else None  # Use None if no balance is found
            }
            for user in users_with_balance
        ]

        # Build pagination information
        pagination = {
            'page': page,
            'per_page': per_page,
            'total_pages': (User.query.count() + per_page - 1) // per_page,
            'total_items': User.query.count(),
        }

        return jsonify({'users': result, 'pagination': pagination})





    def post(self):
        args = user_parser.parse_args()
        random_balance = randint(1000, 20000)

        new_user = User(
            firstname=args['firstname'],
            lastname=args['lastname'],
            username=args['username'],
            place=args['place']
        )


        # Check if the username already exists
        existing_user = User.query.filter_by(username=args['username']).first()
        if existing_user:
            return {'error': 'Username already exists'}, 400

        # Assuming there is a relationship between User and Balance tables
        new_user_balance = Balance(
            amount=random_balance
        )

        # Set the relationship between User and Balance
        new_user.balance = new_user_balance
        try:
            db.session.add(new_user)
            db.session.add(new_user_balance)
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
api.add_resource(HealthCheckResource, '/health')
