import os
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, NoteForm
import datetime
import random

from flask_sqlalchemy import SQLAlchemy


db_path = os.path.abspath('test.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    birth_date = db.Column(db.DateTime)
    rate = db.Column(db.Float, default=0)
    role = db.Column(db.Integer, db.ForeignKey('Roles.id'))

    def __init__(self, username, rate, birthdate=datetime.datetime.utcnow(), role=1):
        self.username = username
        self.birth_date = birthdate
        self.rate = rate
        self.role = role


class Role(db.Model):
    __tablename__ = "Roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

db.create_all()


# def create_roles(list_of_roles):
#     for role_name in list_of_roles:
#         db.session.add(Role(role_name))
#     db.session.commit()
#
#
# def create_users(list_of_users):
#     for user in list_of_users:
#         db.session.add(User(**user))
#     db.session.commit()


roles = ['admin', 'common_user']

users = [{'username': name,
          'rate': random.randrange(0, 100),
          "role": random.randrange(len(roles) - 1 )} for name in ['Alex', "Mannie", 'Gloria', "Mellman"]]

# create_roles(roles)
# create_users(users)



posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/signin", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/create_note", methods=['GET', "POST"])
def create_note():
    form = NoteForm()
    if form.validate_on_submit():
        flash('Success')
        return redirect(url_for('home'))

    return render_template('create_note.html', title='Create note', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True)
