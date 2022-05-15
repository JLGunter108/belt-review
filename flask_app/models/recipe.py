from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @classmethod
    def get_all(cls):
        query = 'select * from recipes left join users on users.id=recipes.users_id'
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (users_id, name, description, instructions, date_made, under_thirty) VALUES (%(users_id)s, %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_thirty)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name=%(first_name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_thirty=%(under_thirty)s WHERE id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM recipes WHERE id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_from_user(cls, data):
        query = 'SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE user.id=%(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 2:
            flash("Name must be at least 2 characters!", "recipe-error")
            is_valid = False
        if len(recipe['description']) < 2:
            flash("Description must be at least 2 characters!", "recipe-error")
            is_valid = False
        if len(recipe['instructions']) < 10:
            flash("Instructions must be at least 10 characters!", "recipe-error")
            is_valid = False
        if not recipe['date_made']:
            flash("Must include date created!", "recipe-error")
            is_valid = False
        if not recipe['under_thirty']:
            flash("Must include if under 30 minutes!", "recipe-error")
            is_valid = False
        return is_valid
