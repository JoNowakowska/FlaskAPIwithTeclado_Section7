from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'There is no store named "{}" in the database'.format(name)}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "A store with that name already exists."}, 400
        else:
            new_store = StoreModel(name)
            try:
                new_store.save_to_db()
                return new_store.json(), 201
            except:
                return {"message": "An error occured while creating the store"}, 500
    
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
                return {"message": "The store named '{}' removed from a database".format(name)}
            except:
                return {"message": "An error occured and the store cannot be removed."}
        return {"message": "No store with the name '{}' found in the database.".format(name)}

class StoreList(Resource):
    def get(self):
        return {"Stores": [store.json() for store in StoreModel.query.all()]}

