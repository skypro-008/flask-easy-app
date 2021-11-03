from flask import request
from flask_restx import Resource, Namespace

from models import Review
from setup_db import db

review_ns = Namespace('reviews')


@review_ns.route('/')
class ReviewsView(Resource):
    def get(self):
        rs = db.session.query(Review).all()
        res = []
        for b in rs:
            sm_d = b.__dict__
            # грязный хак чтобы не перебирать поля так как здесь нет сериализации при помощи marshmallow
            del sm_d['_sa_instance_state']
            res.append(sm_d)
        return res, 200

    def post(self):
        req_json = request.json
        ent = Review(**req_json)
        
        db.session.add(ent)
        db.session.commit()
        return "", 201, {"location": f"/reviews/{ent.id}"}


@review_ns.route('/<int:rid>')
class ReviewView(Resource):
    def get(self, rid):
        r = db.session.query(Review).get(rid)
        sm_d = r.__dict__
        # грязный хак чтобы не перебирать поля так как здесь нет сериализации при помощи marshmallow
        del sm_d['_sa_instance_state']
        return sm_d, 200

    def put(self, rid):
        review = db.session.query(Review).get(rid)
        req_json = request.json
        review.user = req_json.get("user")
        review.rating = req_json.get("rating")
        review.book_id = req_json.get("book_id")

        db.session.add(review)
        db.session.commit()
        return "", 204

    def delete(self, rid):
        review = db.session.query(Review).delete(rid)
        
        db.session.delete(review)
        db.session.commit()
        return "", 204
