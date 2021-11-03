from flask_restx import Resource, Namespace

from constants import PAGES_PER_MINUTE
from models import Book
from setup_db import db

book_ns = Namespace('books')


@book_ns.route('/')
class BooksView(Resource):
    def get(self):
        bs = db.session.query(Book).all()
        res = []
        for b in bs:
            sm_d = b.__dict__
            # грязный хак чтобы не перебирать поля так как здесь нет сериализации при помощи marshmallow
            del sm_d['_sa_instance_state']
            sm_d["minutes"] = sm_d['pages'] / PAGES_PER_MINUTE
            res.append(sm_d)
        return res, 200


@book_ns.route('/<int:bid>')
class BookView(Resource):
    def get(self, bid):
        b = db.session.query(Book).get(bid)
        sm_d = b.__dict__
        # грязный хак чтобы не перебирать поля так как здесь нет сериализации при помощи marshmallow
        del sm_d['_sa_instance_state']
        sm_d["minutes"] = sm_d['pages'] / PAGES_PER_MINUTE
        return sm_d, 200
