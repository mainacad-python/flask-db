from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), required=True)
    password = db.Column(db.String(120), required=True)


class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), required=True)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), required=True)

