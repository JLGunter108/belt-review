from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*?])[A-Za-z\d!@#$%&*?]{8,16}$')

class User:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])  

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters!", "reg-error")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters!", "reg-error")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "reg-error")
            is_valid = False
        if not PW_REGEX.match(user['password']):
            flash("Invalid Password", "reg-error")
            flash("Password must be 8-16 characters", "reg-error")
            flash("Password must contain 1 uppercase letter", "reg-error")
            flash("Password must contain 1 number", "reg-error")
            flash("Password must contain !, @, #, $, %, &, *, or ?", "reg-error")
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash("Passwords must match!", "reg-error")
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        data = {
            'email': user['email']
        }
        user_in_db = User.get_by_email(data)
        if not user_in_db:
            is_valid = False
        return is_valid
