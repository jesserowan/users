from flask import Flask, render_template, request, redirect, session
from mysqlconnection_copy import connectToMySQL
import datetime
app = Flask(__name__)

@app.route('/')
def index():
    mysql = connectToMySQL('users_assignment')
    users = mysql.query_db('SELECT * FROM users;')
    return render_template('users.html', users=users)

@app.route('/add')
def add():
    mysql = connectToMySQL('users_assignment')
    return render_template('add_user.html')

@app.route('/add_user', methods=["POST"])
def add_user():
    mysql = connectToMySQL('users_assignment')
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(email)s, NOW(), NOW());"

    data = {
        "fn": request.form['first'],
        "ln": request.form['last'],
        "email": request.form['email']
    }

    new_user_id = mysql.query_db(query, data)
    return redirect('/')

@app.route('/user/<id>')
def single_user(id):
    mysql = connectToMySQL('users_assignment')

    query = "SELECT * FROM users WHERE id=%(id)s;"

    data = {
        "id": id
    }

    this_user = mysql.query_db(query, data)
    return render_template('user.html', person=this_user)

@app.route('/delete_user/<id>')
def delete_user(id):
    mysql = connectToMySQL('users_assignment')

    query = "DELETE FROM users WHERE id=%(id)s;"

    data = {
        "id": id
    }

    delete_user = mysql.query_db(query, data)

    return redirect('/')

@app.route('/edit_user/<id>')
def edit_user(id):
    mysql = connectToMySQL('users_assignment')

    query = "SELECT * FROM users WHERE id=%(id)s;"

    data = {
        "id": id
    }

    edit_user = mysql.query_db(query, data)

    return render_template('edit.html', edit=edit_user)

@app.route('/process_edit/<id>', methods=["POST"])
def process_edit(id):
    mysql = connectToMySQL('users_assignment')

    query = "UPDATE users SET first_name=%(fn)s, last_name=%(ln)s, email=%(em)s, updated_at=NOW() WHERE id=%(id)s;"

    data = {
        "id": id,
        "fn": request.form['editfirst'],
        "ln": request.form['editlast'],
        "em": request.form['editemail']
    }
    process_edit = mysql.query_db(query, data)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)