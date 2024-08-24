from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, DB 
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

@app.route("/")
def users():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    if User.validate_register(data):
        user_id = User.register(data)  
        session['user_id'] = user_id  
        session['first_name'] = data['first_name']  
        return redirect('/dashboard')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    if User.validate_login(data):
        user_in_db = User.get_by_email(data)
        session['user_id'] = user_in_db.id 
        session['first_name'] = user_in_db.first_name  
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html', data=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
