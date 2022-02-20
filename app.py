from flask import Flask, jsonify, request
import json

app = Flask(__name__)
stores = [
    {
       'name': 'diesel',
       'items': [
            {'name': 'jeans',
             'price': 35.2}
        ]
    }
]


def store_error_creator(name):
    return jsonify({'error': f'No store with name {name}'})


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>')
def get_store(name):
    try:
        store = [s for s in stores if s['name'] == name][0]
    except IndexError as krr:
        return store_error_creator(name)
    return jsonify(store)


@app.route('/store')
def get_stores():
    res = {'stores': stores}
    return jsonify(res)


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    request_data = request.get_json()
    for s in stores:
        if s['name'] == name:
            new_item = {
                        'name': request_data['name'],
                        'price': request_data['price']
                        }
            s['items'].append(new_item)
            return jsonify({s['name']: s['items']})
    return store_error_creator(name)


@app.route('/store/<string:name>/item')
def get_items(name):
    for s in stores:
        if s['name'] == name:
            return jsonify({'items': s['items']})
    return store_error_creator(name)

# POST /store date: {name:}
# GET /store/<string:name>
# GET /store
# POST /store/<string:name>/item {name:, price:}
# GET /store/<string:name>/item


if __name__ == '__main__':
    app.run(port=5000)

