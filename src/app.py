from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from flask_cors import CORS,cross_origin


from resources.item import Item, ItemList
from security import authenticate, identity
from resources.user import UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
app.secret_key = 'Vienna-Panda'
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(UserRegister, '/register')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# api.add_resource(Items,'/test_item/name')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0',port=4000, debug=True)

