import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
    required=True,
    type=str,
    help="This field cannot be left blank")
    parser.add_argument('password',
    required=True,
    type=str,
    help="This field cannot be left blank")

    def post(self):      
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with such a username already exists."}, 400
        else:
            new_user = UserModel(**data) #the same as UserModel(data['username'], data['password'])
            new_user.save_to_db()
            return {"message": "User created successfully!"}, 201