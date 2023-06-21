# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL

# db = 'users_schema'

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