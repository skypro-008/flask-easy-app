from flask import Flask
from flask_restx import Api

from config import Config
from models import Review, Book
from setup_db import db
from views.books import book_ns
from views.reviews import review_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(book_ns)
    api.add_namespace(review_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.create_all()
        r1 = Review(id=1, user="Oleg", rating=5, book_id=1)
        r2 = Review(id=2, user="Ivan", rating=6, book_id=2)
        r3 = Review(id=3, user="John", rating=4, book_id=3)
        r4 = Review(id=4, user="Diana", rating=3, book_id=4)

        b1 = Book(id=1, name="Гарри Поттер и Тайная Комната", author="Джоан Роулинг", year=1990, pages=400)
        b2 = Book(id=2, name="Граф Монте-Кристо", author="Дюма", year=1510, pages=1344)
        b3 = Book(id=3, name="Гарри Поттер и Орден Феникса", author="Джоан Роулинг", year=1993, pages=500)
        b4 = Book(id=4, name="Гарри Поттер и Кубок Огня", author="Джоан Роулинг", year=1994, pages=600)

        with db.session.begin():
            db.session.add_all([b1, b2, b3, b4])
            db.session.add_all([r1, r2, r3, r4])


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
