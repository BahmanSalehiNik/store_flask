from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from query_decorator import query_method_decorator

from flask_cors import CORS, cross_origin
from models.item import ItemModel


class ItemList(Resource):
    def get(self, cursor=None):
        item_qs = ItemModel.query.all()
        return {'data': [item.json() for item in item_qs]}


class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='this field is required')

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='this field is required')
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if not item:
            return {'error':f'item with name {name} does not exists.'}, 404
        else:
            return item.json(), 200


    @jwt_required()
    def post(self, name):

        data = Item.parser.parse_args()

        price = data['price']

        item = ItemModel.find_item_by_name(name)
        if item:
            return {'error': f'an item already exists with name: {name}.'}, 400

        new_item = ItemModel(name, price, data['store_id'])
        try:
            new_item.save_to_db()
        except:
            return {'error': 'something went wrong.'}, 500

        return {f'message': f'item with name {name} and price {price} created successfully.'}, 201

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()
        price = data.get('price', None)
        item = ItemModel.find_item_by_name(name)
        if not item:
            item = ItemModel(name=name, price=price, store_id=data['store_id'])
        else:
            item.price = price

        item.save_to_db()
        return item.json(), 200

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if not item:
            return {'error': f'item with name {name} does not exist'}, 404
        else:
            item.delete_from_db()
        return {'data': f'successfully delete item with name: {name}'}, 204
