#classes always start with capital letter
#packages start with lowercase letter
from flask import Flask, jsonify, request, render_template
# This solves a bug in flask_restful 0.3.8
# https://github.com/flask-restful/flask-restful/pull/913
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My item',
                'price': 4.99
            }
        ]
    }
]

class Student(Resource):
    def get(self, name):
        return {'student': name}

api.add_resource(Student, '/student/<string:name>')

@app.route('/')
def home():
    return render_template('index.html')

# Call external api
@app.route('/holidayUS')
def get_us_holiday_list():
    response = requests.get('https://holidayapi.com/v1/holidays',
                            params={'country':'US', 'year':2021, 'pretty': 'true', 'key': '47b0e5cc-8492-496f-8169-8029cf626ef1', 'public': 'true'})
    return jsonify(response.json())

# POST /store date {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over stores
    # If the store name matches, return it
    # If none match, return an error message
    for store in stores:
        if store['name'] == name:
            return jsonify(store)

    return jsonify({'message': 'store not found'})

# GET
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()

    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)

    return jsonify({'message': 'store not found'})

@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})

    return jsonify({'message': 'store not found'})

app.run(port=5000)