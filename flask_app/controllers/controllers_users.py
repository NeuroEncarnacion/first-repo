from flask_app import app
from flask import request, render_template, redirect
from flask_app.models.models_user import User

@app.route('/')
def index():
    return render_template('/create.html')


@app.route('/users')
def users():
    users = User.get_all()
    return render_template("read.html", users = users)


@app.route('/create')
def create():
    return render_template("create.html")



@app.route('/create_user', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string. 
    data = {
        "fname" : request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"], 
    }
    # We pass the data dictionary into the save method from the User class. 
    User.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/users')


# edit page
@app.route('/edit/<int:one_user_id>')
def edit(one_user_id):
    data = {
        'id' : one_user_id
    }
    user = User.get_one(data)
    return render_template('edit.html', user = user)


# update user page 
@app.route('/update/<one_user_id>', methods=['POST'])
def update_user(one_user_id):
    User.update(request.form, one_user_id) 
    return redirect('/users')


# User Detail Page
@app.route('/view_user/<int:one_user_id>')
def view_user(one_user_id):
    data ={
        "id" : one_user_id
    }
    user =User.get_one(data)
    return render_template("read_one.html", user = user)


# delete user
@app.route('/delete/<int:one_user_id>')
def delete(one_user_id):
    User.delete(one_user_id)
    return redirect('/users')

