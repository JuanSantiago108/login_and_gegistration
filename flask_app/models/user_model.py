import email
import re
from flask_app import DATABASE
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL   
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# re.compile(r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%#?&])[A-Za-z\d@$!#%?&]{8,18}$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s,);"
        return connectToMySQL(DATABASE).query_db(query, data)



    @classmethod
    def get_by_email (cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result,"===========================================")
        if len(result)<1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result =  connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])




    @classmethod
    def create_one(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) "
        query += "VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"

        return connectToMySQL(DATABASE).query_db(query, data)



    @staticmethod
    def validate_registracion(data):
        is_valid = True
        if len(data['first_name'])<2:
            flash("Must be at least two characters")
            is_valid = False
        if len(data['last_name'])<2:
            flash("Must be at least two characters")
            is_valid = False
        if len(data['password'])<8:
            flash("At least 8 characters,")
            is_valid = False
        if len(data['email']) == 0:
            is_valid = False
        elif User.get_one(data):
            flash("This email is already taken")
            is_valid = False
        if not data['password'] == data['confirm_password']:
            flash("Password does not match")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
        return is_valid


    @staticmethod
    def validate_login(data):
        is_valid = True
        if not User.get_by_email(data):
            is_valid = False
        return is_valid