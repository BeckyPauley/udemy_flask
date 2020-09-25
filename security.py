from werkzeug.security import safe_str_cmp # safer way of comparing strings and different encodings
from user import User


def authenticate(username, password):
    user = User.find_by_username(username) #.get gives us the value of the key
    if user and safe_str_cmp(user.password, password):  # this means is the user is not none AND their passsword is equal to password
        return user

def identity(payload): # This is unique to flask.JWT
    user_id = payload['identity']
    return User.find_by_id(user_id)