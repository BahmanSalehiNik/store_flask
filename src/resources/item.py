from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from query_decorator import query_method_decorator

from flask_cors import CORS, cross_origin
from models.item import ItemModel

class ItemList(Resource):
    @cross_origin()
    @query_method_decorator
    def get(self, cursor=None):
        item_qs_query = "SELECT * FROM items"
        item_qs = cursor.execute(item_qs_query)
        res = {'items':[]}
        for row in item_qs:
            res['items'].append({'id': row[0], 'name': row[1], 'price': row[2]})
        return res, 200


class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('price',
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
    #@query_method_decorator
    def post(self, name, cursor=None):

        data = Item.parser.parse_args()

        price = data['price']

        item = ItemModel.find_item_by_name(name)
        if item:
            return {'error': f'an item already exists with name: {name}.'}, 400


        # create_item_query = "INSERT INTO items VALUES (NULL , ?, ?)"
        # cursor.execute(create_item_query, (name, price))
        new_item = ItemModel(name, price)
        try:
            new_item.insert()
        except:
            return {'error': 'something went wrong.'}, 500

        return {f'message': f'item with name {name} and price {price} created successfully.'}, 201

    @jwt_required()
    #@query_method_decorator
    def put(self, name, cursor=None):

        data = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)
        if not item:
            new_item = ItemModel(name=name, price=data.get('price', None))
            print(f"no item with name {name}, creating a new one")
            try:
                new_item.insert()
            except Exception:
                return {'error': 'something went wrong while inserting the new item'}, 500

            return new_item.json(), 201
        else:
            # try:
                # update_query = "UPDATE items SET price=? WHERE name=?"
                # cursor.execute(update_query, (data.get('price'), name))
            item.update(data.get('price'))
            return {'data': 'item successfully updated'}, 200
            # except Exception:
            #     return {'error': 'something went wrong while updating the item'}, 500



    @jwt_required()
    @query_method_decorator
    def delete(self, name, cursor=None):
        item = ItemModel.find_item_by_name(name)
        if not item:
            return {'error': f'item with name {name} does not exist'}, 404
        else:
            delete_item_query = "DELETE FROM items WHERE name=?"
            cursor.execute(delete_item_query,(name,))
        return {'data': f'successfully delete item with name: {name}'}, 204
