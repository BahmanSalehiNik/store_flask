from functools import wraps

from db_config import DB_ADDRESS
import sqlite3


def query_method_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect(DB_ADDRESS)
        cursor = connection.cursor()
        res = func(*args, **kwargs, cursor=cursor)
        connection.commit()
        connection.close()
        return res
    return wrapper
