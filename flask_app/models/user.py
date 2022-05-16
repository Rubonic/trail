from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    db = 'trail_finder_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.trail_ids = []

    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (username, email, password, created_at, updated_at) VALUES (%(username)s, %(email)s, %(password)s, NOW(), NOW());"
        user = connectToMySQL(cls.db).query_db(query, data)

        return user


    @classmethod
    def get_by_username(cls, data):
        query = "SELECT * FROM users where username = %(username)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result == ():
            return False
        
        user = cls(result[0])

        return user

    @classmethod
    def add_trail(cls, data):
        query = "INSERT INTO trails (api_trail_id, created_at, updated_at, location_id) VALUES (%(api_trail_id)s, NOW(), NOW(), %(location_id)s)"
        
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def stash_trail(cls, data):
        query = "INSERT INTO saved (trail_id, user_id) VALUES (%(trail_id)s, %(user_id)s)"
        
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def stashed_trails(cls, data):
        query = "SELECT api_trail_id FROM saved JOIN trails ON trails.id = saved.trail_id WHERE user_id = %(user_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)

        stashed_trails = []

        for row in results:
            stashed_trails.append(row['api_trail_id'])

        return stashed_trails




        




# +++++++++++++++++++++++++++++++++++++++++++++
# Static methods

    @staticmethod
    def validate_user_registration(user):
        is_valid = True

        if not len(user['username']) > 2:
            flash('Username must be at least 3 characters long', 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is not valid!", 'reg')
            is_valid = False
        if not len(user['password']) > 4:
            flash('Password must be atleast 5 characters long', 'reg')
            is_valid = False
        if not user['password'] == user['confirm_password']:
            flash('Passwords do not match', 'reg')
            is_valid = False
        return is_valid


    