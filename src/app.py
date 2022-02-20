from flask import Flask
from flask_jwt import JWT
from flask_restful import Api


from src.items import Item, ItemList
from src.security import authenticate, identity
from src.user import UserRegister

app = Flask(__name__)
app.secret_key = 'Vienna-Panda'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# api.add_resource(Items,'/test_item/name')


if __name__ == '__main__':
    app.run(port=4000, debug=True)

