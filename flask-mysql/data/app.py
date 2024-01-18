from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import datetime
from datetime import timedelta
from flask import flash 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "thisissecretkeys"
app.permanent_session_lifetime = timedelta(minutes=5)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ajitdubey:ajitdubey@mysql-server:3306/myDB'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ajitdubey:ajitdubey@172.24.0.2:3306/myDB'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# MySQL configuration
app.config['MYSQL_HOST'] = 'mysql-server'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ajitdubey'
app.config['MYSQL_DB'] = 'myDB'
app.config['MYSQL_PORTS'] = '3306'
mysql = MySQL(app)

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password =  form.password.data
        remember_me = form.remember_me.raw_data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        token_string = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        
        token = bcrypt.generate_password_hash(token_string).decode('utf-8')
        #token = dt
        
        # store data in Mysql database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password, token) VALUES (%s,%s,%s, %s)", (name, email, hashed_password, token))
        #cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)", (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password =  form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user[3].encode('utf-8'), password.encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('dashboard.html', user=user)
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('login'))

if __name__ == '__main__':
       
    app.run(host='0.0.0.0', port=5000, debug=True)
