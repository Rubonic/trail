from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 



class Trail:
    db = 'trail_finder_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.global_id = data['global_id']
        self.name = data['name']
        self.length = data['length']
        self.description = data['description']
        self.directions = data['directions']
        self.city = data['city']
        self.region = data['region']
        self.country = data['country']
        self.lat = data['lat']
        self.lon = data['lon']
        self.difficulty = data['difficulty']
        self.rating = data['rating']
        self.thumbnail = data['thumbnail']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.trails = []
