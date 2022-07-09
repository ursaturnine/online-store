from user import User

users = [
    User(1, 'aquagirlll', 'hello')
]

# create index on user so we don't have to iterate over list 
# everytime
# find user by username or userid
username_mapping = {u.username: u for u in users }
userid_mapping = {u.id: u for u in users}

# from flask-jwt-extended library
def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == 'password':
        return user
    
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)