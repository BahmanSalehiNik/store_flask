from flask_restful import Resource, reqparse

from src.query_decorator import query_method_decorator


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    @query_method_decorator
    def find_by_username(cls, username, cursor=None):
        select_query = f"SELECT * FROM users WHERE username=?"
        user_qs = cursor.execute(select_query, (username,))
        row = user_qs.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        return user

    @classmethod
    @query_method_decorator
    def find_by_id(cls, _id, cursor=None):

        select_query = f"SELECT * FROM users WHERE id=?"
        user_qs = cursor.execute(select_query, (_id,))
        row = user_qs.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        return user


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

    @query_method_decorator
    def post(self, cursor=None):

        data = UserRegister.parser.parse_args()
        username = data.get('username', None)
        user = User.find_by_username(username)
        if user:
            return {'error': f'a user with username {username} already exists'}, 400

        create_user_query = "INSERT INTO users VALUES (Null, ?, ?)"
        cursor.execute(create_user_query, (data['username'], data['password']))

        return {'message': 'user created successfully.'}, 201
