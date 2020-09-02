from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)

app.secret_key = 'the key should be long and complicated and hidden from others if you share this script'

app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

api = Api(app)

jwt = JWT(app, authenticate, identity) #JWT will automatically create an endpoint /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug = True)