from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
#import sqlite3
from models.item import ItemModel


class Item(Resource):
    #TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store ID"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        #item = {'name': name, 'price': data['price']}
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db() 
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json(), 201

    #@jwt_required()
    def delete(self, name):
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}"""
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'Item deleted.'}
        return {'message':'Item not found.'}, 404

    #@jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name, data['price'])
        if item is None:
            """try:
                #Item.insert(updated_item)
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}"""
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            """try:
                #Item.update(updated_item)
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}"""
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'items': items}"""
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}