from dotenv import load_dotenv
from numpy import apply_along_axis
from flask import Flask, jsonify,request, render_template
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required
from security import authenticate, identity
from flask_sqlalchemy import SQLAlchemy




#Flask config
app = Flask(__name__)
api = Api(app)
#postgresql://<username>:<password>@<server>/<database_name>
#"postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development"
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'postgresql + psycopg2://postgres:postgres@localhost:5000/online_store_main'

#CORS config
cors = CORS(app)

# Environment variables config
app.secret_key = os.environ.get("secret_key")
load_dotenv()


# JWT Config
jwt = JWTManager(app) #JWT create a new endpoint, /auth, 

#Database set up
db = SQLAlchemy(app)

items = []




class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,required=True,  help='This field cannot be left blank')
    data = parser.parse_args()


    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return ('item', item), 200 if item else 404
    
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return ({'message': "An item with name '{}' already exists.".format(name)}), 400

        data = Item.parser.parse_args()

        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        # FIRESTORE
        db.collection('Items').document().set(data)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}
    
    def put(self, name):
        global items
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item



class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(debug=True)
