from sqlite3 import Connection, connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re

class Location:
    db = 'trail_finder_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.state = data['state']
        self.lat = data['lat']
        self.lon = data['lon']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM locations"
        results = connectToMySQL(cls.db).query_db(query)

        locations = []

        for row in results:
            location = cls(row)
            locations.append(location)

        return locations

    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM locations WHERE id = %(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        
        main_location = cls(result[0])

        return main_location


    @classmethod
    def get_location_id_by_name(cls, data):
        query = "SELECT id FROM locations WHERE name = %(location_name)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        location_id = result[0]
        location_id = location_id['id']
        return location_id
