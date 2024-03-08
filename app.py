from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://learn.deepanshu:nCJW4YR9DUPV@ep-orange-pine-a5e2k0bs.us-east-2.aws.neon.tech/flask?sslmode=require"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

# Create a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    place = db.Column(db.String(50), nullable=True)

# Parser for request data
user_parser = reqparse.RequestParser()
user_parser.add_argument('firstname', type=str, required=True, help='First name is required')
user_parser.add_argument('lastname', type=str, default='', help='Last name')
user_parser.add_argument('username', type=str, required=True, help='Username is required')
user_parser.add_argument('place', type=str, default='', help='Place')

# Resource for listing and creating users
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        user_list = [{'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username, 'place': user.place} for user in users]
        return {'users': user_list}

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

# Resource for updating and deleting a user by ID
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

# Add resources to the API with the appropriate routes
api.add_resource(UserListResource, '/api/v1/user')
api.add_resource(UserResource, '/api/v1/user/<int:user_id>')

# Home route
@app.route('/')
def home():
    return "Home Page!"

if __name__ == '__main__':
    app.run(debug=True)




# Commit your model (table) to the database
# with app.app_context():
#     db.create_all()
    # db.drop_all()