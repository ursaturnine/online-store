from dotenv import load_dotenv
from flask import Flask, jsonify,request, render_template
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required
from security import authenticate, identity
from flask_sqlalchemy import SQLAlchemy



#Firebase
import firebase_admin
from firebase_admin import firestore, credentials, initialize_app

#Initialize Firestore DB
# db=firestore.client()
cred = credentials.Certificate("serviceAccountKey.json")
default_app = initialize_app(cred)
# firebase_admin.initialize_app(cred)
db=firestore.client()
items_ref = db.collection('Items')

#Flask config
app = Flask(__name__)
api = Api(app)

#CORS config
cors = CORS(app)

# Environment variables config
app.secret_key = os.environ.get("secret_key")
load_dotenv()


# JWT Config
# jwt = JWTManager(app) #JWT create a new endpoint, /auth, 

# items = []

#add an item to a firestore document
@app.route('/add', methods=['POST'])
def create():
    try:
        id = request.json['id']
        items_ref.document(id).set(request.json)
        return jsonify({'success': True}), 200
    except Exception as e:
        return f'An Error Occurred: {e}'

#get all items from a firestore document
@app.route('/list', methods=['GET'])
def read():
    try:
        #check if ID was passed to URL query
        item_id = request.args.get('id')
        if item_id:
            item = items_ref.document(item_id).get()
            return jsonify(item.to_dict()), 200
        else:
            all_items = [doc.to_dict() for doc in items_ref.stream()]
            return jsonify(all_items), 200  
    except Exception as e:
        return f'An Error Occurred: {e}'

#update items in a firestore document
@app.route('/update', methods=['PUT', 'POST'])
def update():
    try:
        id = request.json['id']
        items_ref.document(id).update(request.json)
        return jsonify({'success': True}), 200
    except Exception as e:
        return f'An Error Occurred: {e}'

#delete a document from a firestore collection
@app.route('/delete', methods=['DELETE'])
def delete():
    try:
        #Check for ID In URL query
        item_id = request.args.get('id')
        items_ref.document(item_id).delete()
        return jsonify({'success': True}), 200
    except Exception as e:
        return f'An Error Occurred: {e}'

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host = '0.0.0.0', port=port)




# class Item(Resource):

#     parser = reqparse.RequestParser()
#     parser.add_argument('price', type=float,required=True,  help='This field cannot be left blank')
#     data = parser.parse_args()


#     @jwt_required()
#     def get(self, name):
#         item = next(filter(lambda x: x['name'] == name, items), None)
#         return ('item', item), 200 if item else 404
    
#     def post(self, name):
#         if next(filter(lambda x: x['name'] == name, items), None) is not None:
#             return ({'message': "An item with name '{}' already exists.".format(name)}), 400

#         data = Item.parser.parse_args()

#         item = {
#             'name': name,
#             'price': data['price']
#         }
#         items.append(item)
#         # FIRESTORE
#         db.collection('Items').document().set(data)
#         return item, 201
    
#     def delete(self, name):
#         global items
#         items = list(filter(lambda x: x['name'] != name, items))
#         return {'message': 'item deleted'}
    
#     def put(self, name):
#         global items
#         data = Item.parser.parse_args()
#         item = next(filter(lambda x: x['name'] == name, items), None)
#         if item is None:
#             item = {'name': name, 'price': data['price']}
#             items.append(item)
#         else:
#             item.update(data)
#         return item



# class ItemList(Resource):
#     def get(self):
#         return {'items': items}


# api.add_resource(Item, '/item/<string:name>')
# api.add_resource(ItemList, '/items')


# app.run(debug=True)
