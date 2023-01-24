from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password = data['password']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s)"
        return connectToMySQL('loginusers').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        users_from_db =  connectToMySQL('loginusers').query_db(query)
        users =[]
        for b in users_from_db:
            users.append(cls(b))
        return users

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        user_from_db = connectToMySQL('loginusers').query_db(query,data)

        return cls(user_from_db[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        user_from_db = connectToMySQL('loginusers').query_db(query,data)
        if len(user_from_db) < 1:
            return False

        return cls(user_from_db[0])



    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('loginusers').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('loginusers').query_db(query,data)

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("Name must be at least 2 characters.", "first_name")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", "last_name")
            is_valid = False
        if len(user['email']) < 3:
            flash("Email must be at least 3 characters.", "email")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "notemail")
            is_valid = False

        if len(user['password']) < 3:
            flash("Password must be at least 3 characters.", "password")
            is_valid = False
        elif not user['password'] == user['confirm_password']:
            is_valid = False
            flash("password doesnt match!", "confirm_password")
        return is_valid