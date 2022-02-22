from query_decorator import query_method_decorator


class UserModel:
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