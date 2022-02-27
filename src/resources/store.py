from models.store import StoreModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class StoreList(Resource):
    def get(self):
        store_qs = StoreModel.query.all()
        return {'data': [store.json() for store in store_qs]}


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str)

    def get(self, name):
        store = StoreModel.query.filter_by(name=name).first()
        if not store:
            return {'error': f'No store found with name {name}'}, 404
        return {'data': store.json()}, 200

    def post(self, name):
        store = StoreModel.query.filter_by(name=name).first()
        if store:
            return {'error': f'A store with name {name} already exists'}, 400

        store = StoreModel(name=name)
        store.save_to_db()
        return {'data': 'Store created successfully'}, 200

    def put(self, name):
        store = StoreModel.query.filter_by(name=name).first()
        if not store:
            store_temp = StoreModel(name=name)
            store_temp.save_to_db()
            return {'data': 'Store created successfully'}, 200
        else:
            data = Store.parser.parse_args()
            new_name = data['name']
            store.name = new_name
            store.save_to_db()
            return {'data': 'Store updated successfully'}, 200

    def delete(self, name):
        store = StoreModel.query.filter_by(name=name).first()
        if store:
            store.delete_from_db()
            return {'data': 'Store deleted'}, 200
        else:
            return {'error': f'Store with name {name} not found'}, 404


