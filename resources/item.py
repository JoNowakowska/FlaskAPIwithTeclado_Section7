from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
    type=float,
    required=True,
    help="This field cannot be left blank!")
    parser.add_argument("store_id",
    type=int,
    required=True,
    help="Every item needs to belong to a store and has a store id.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found."}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        #data = request.get_json() <- instead of this we are going to use reqparse to restrict the parameters in the body
        
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error has occured"}, 500

        return item.json(), 201

    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
                return {"message": "An item '{}' deleted".format(name)}
            return {"message": "An item '{}' does not exist in he db.".format(name)}

        except:
            return {"message": "An error has occured"}, 500
    
    def put(self, name):
        item = ItemModel.find_by_name(name)
                
        data = Item.parser.parse_args()

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        try:
            item.save_to_db()
            return item.json()
        except:
            return {"message": "An error has occured inserting the item"}, 500



class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
        # the same can be achieved by {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}