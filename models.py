# where we create database models
# we want database for our users, and also one for our notes (or whatever else you want to store)
# from . == from website (if we were outside directory)
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # date = db.Column(db.DateTime, timezone=True, default=func.now())

    # defining foreign key relationships between notes and users
    # one-many relationship --> one user has many notes
    # user is lowercased here bc sql will have lowercase names for tables by default
    # 'User' class defined below represented by 'user'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# defining all the columns we want stored in the table


class User(db.Model, UserMixin):
    # defining primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    # telling flask/sql, everytime we create note, add into user-note relationship the noteID
    # relationship feild is a list containing all notes
    # Note is capital here //foriegn key --> lowercase, relationship -> class name
    notes = db.relationship('Note')
