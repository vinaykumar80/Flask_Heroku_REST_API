import sqlite3
from db import db

class UserModel(db.Model): # Finding user
    #TABLE_NAME = 'users'

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) #Auto increment column or auto generated
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        #self.id = _id
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (username,)) # always tuples as parameters
        row = result.fetchone()
        if row:
            user = cls(*row) # Positional arguments Equivalent to row[0],row[1],row[2]
        else:
            user = None

        connection.close()
        return user"""
        return cls.query.filter_by(username=username).first() # SELECT * from users

    @classmethod
    def find_by_id(cls, _id):
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row) # Equivalent to row[0],row[1],row[2]
        else:
            user = None

        connection.close()
        return user"""
        return cls.query.filter_by(id=_id).first()