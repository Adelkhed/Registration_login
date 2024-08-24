from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL, DB
import re
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.sex = data['sex']
        self.birthday = data['birthday']
        self.education_level = data['education_level']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def register(cls,data):
        encrypted_password =bcrypt.generate_password_hash(data['password'])
        data = dict(data)
        data['password'] = encrypted_password
        query = "INSERT INTO users (first_name, last_name,sex,birthday,education_level, email, password) VALUES (%(first_name)s,%(last_name)s,%(sex)s,%(birthday)s,%(education_level)s, %(email)s, %(password)s);"
        return connectToMySQL(DB).query_db(query,data)
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,data)
        if result == ():
            return None
        return cls(result[0])
    @staticmethod
    def validate_register(data):
        is_valid = True
        user_in_db = User.get_by_email(data)

        if len(data['first_name']) <= 3:
            is_valid = False
            flash("Invalid First Name")

        if len(data['last_name']) <= 3:
            is_valid = False
            flash("Invalid Last Name")

        if data.get('sex') not in ['male', 'female']:
            is_valid = False
            flash("Sex not selected")

        if data['education_level'] == 'none':
            is_valid = False
            flash("Education level is required")

        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Invalid Email")

        if user_in_db:
            is_valid = False
            flash("Email already registered")

        if len(data['password']) <= 7:
            is_valid = False
            flash("Invalid Password")

        if data['password'] != data["confirm_password"]:
            is_valid = False
            flash("Passwords Must Match!")

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        user_in_db= User.get_by_email(data)
        if not user_in_db:
            is_valid = False
            flash("Email Not Found !")
        elif not bcrypt.check_password_hash(user_in_db.password,data['password']):
            is_valid = False
            flash("Invalid Password")
        return is_valid
    