import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        # init method takes an id, username and password)
        self.id = _id
        self.username = username
        self.password = password

    # Mapping:

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db') # Initialise connection
        cursor = connection.cursor() # Initialise cursor

        query = "SELECT * FROM users WHERE username=?"
        #Select all rows from the database where the username matches a parameter
        result = cursor.execute(query, (username,))
        #Parameters have to be in the form of the tuple, which is why username is passed in as (username,)
        row = result.fetchone()
        #Gets the first row out of that result set, if no rows will reutnr none.
        if row: # if row is not none
            user = cls(*row) # creates user object with the columns defined in the init method (mathcing to parameters in init method i.e. row[0] is id, row [1] is username, row[2] is password)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db') # Initialise connection
        cursor = connection.cursor() # Initialise cursor

        query = "SELECT * FROM users WHERE id=?"
        #Select all rows from the database where the username matches a parameter
        result = cursor.execute(query, (_id,))
        #Parameters have to be in the form of the tuple, which is why username is passed in as (username,)
        row = result.fetchone()
        #Gets the first row out of that result set, if no rows will reutnr none.
        if row: # if row is not none
            user = cls(*row) # creates user object with the columns defined in the init method (mathcing to parameters in init method i.e. row[0] is id, row [1] is username, row[2] is password)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', 
    type=str,
    required=True,
    help="This field cannot be blank."
    )
    parser.add_argument('password', 
    type=str,
    required=True,
    help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES(NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
