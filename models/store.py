#import sqlite3
#from flask_restful import Resource, reqparse
#from flask_jwt import jwt_required
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    """store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')"""

    items = db.relationship('ItemModel', lazy='dynamic') #

    def __init__(self, name):
        self.name = name
        #self.price = price
        #self.store_id = store_id

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    def delete_from_db(self):
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()"""
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self): # both post and put methods can share this classmethod
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()"""
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_name(cls, name): # So both get and post methods can use this classmethod
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            #return {'item': {'name': row[0], 'price': row[1]}}
            return cls(*row)"""
        return StoreModel.query.filter_by(name=name).first() # SELECT * FROM items where name=name

    