from flask_restful import Resource, reqparse

from query_decorator import query_method_decorator
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='this field is required')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='this field is required')

    def post(self):
        data = UserRegister.parser.parse_args()
        username = data.get('username', None)
        user = UserModel.find_by_username(username)
        if user:
            return {'error': f'a user with username {username} already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'user created successfully.'}, 201
