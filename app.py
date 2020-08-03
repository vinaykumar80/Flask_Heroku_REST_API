from flask import Flask #Request contains payload made by client
from flask_restful import Api, reqparse #Flask-restful Handles JSONIFY function # reqparse 
from flask_jwt import jwt_required, current_identity # pip install FLASK-JWT (JSON Web Token - Obfuscation/Encoding of data)
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister # Runs user file and verifies classes/methods etc
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #To turn off Flask SQLAlchemy modifications tracker
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'jose'
api = Api(app)



jwt = JWT(app, authenticate, identity) # Authentication of users, "http://127.0.0.1:5000/auth" endpoint with username and password and if it matches returns JWT token
# JWT token is used in identity function to get user_id and user details 

#items = [] #List of dictionaries 

api.add_resource(Store, '/store/<string:name>') #Instead of @app.route decorator, Tells API to access resource name with route i.e., http://127.0.0.1:5000/Item/Rolf
api.add_resource(Item, '/item/<string:name>') #Instead of @app.route decorator, Tells API to access resource name with route i.e., http://127.0.0.1:5000/Item/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)  # important to mention debug=True, as it displays error message in HTML page
    
