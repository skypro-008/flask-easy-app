from setup_db import db


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    author = db.Column(db.String)
    year = db.Column(db.Integer)
    pages = db.Column(db.Integer)


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    rating = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
