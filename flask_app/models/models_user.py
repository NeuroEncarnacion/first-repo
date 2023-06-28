# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re       # the regex module 
# create a regular expression object that we'll user later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# model the class after the user table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# instance method to get full name of user
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users_schema').query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append( cls(user) )
        return users


# class method to save a new user to our database
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at ) VALUES ( %(fname)s , %(lname)s, %(email)s, NOW(), NOW() );"
        #data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('users_schema').query_db( query, data )


# class method to edit user information in our database
    @classmethod
    def get_one(cls, data):
        query = """ SELECT * FROM users 
                WHERE id = %(id)s;"""
        results = connectToMySQL('users_schema').query_db(query, data)
        return cls(results[0])


# class method to update a users information
    @classmethod
    def update(cls, data, one_user_id):
        query = f"UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s WHERE id = {one_user_id}; "
        return connectToMySQL('users_schema').query_db(query, data)    

# class method to delete user from database
    @classmethod
    def delete(cls, one_user_id):
        data = {'id' : one_user_id}
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query, data)


# Static methods don't have self or cls passed into the parameters. 
# We do need to take in a parameter represent our user
    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True 
        if len(data['fname']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(data['lname']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address")
            is_valid = False
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL('users_schema').query_db(query, data)
        if len(results) != 0:
            flash('This email is already being used')
            is_valid = False
        return is_valid