#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Gift

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"


@app.get('/gifts')
def all_gifts():
    all_gifts = Gift.query.all()
    gift_dicts = [ g.to_dict() for g in all_gifts ]
    return make_response( jsonify( gift_dicts ), 200 )


@app.get('/gifts/<int:id>')
def get_gift(id):
    found_gift = Gift.query.filter(Gift.id == id).first()
    if found_gift:
        return found_gift.to_dict(), 200
    else:
        return { "message": "Not found" }, 404


@app.post('/gifts')
def post_gift():
    data = request.json
    try:
        gift = Gift( name=data["name"], price=data["price"] )
        db.session.add( gift )
        db.session.commit()

        return gift.to_dict(), 201

    except Exception as e:
        print(e)
        return {"message": f"{e}"}, 406
    

@app.delete('/gifts/<int:id>')
def delete_gift(id):
    try:
        # found_gift = Gift.query.filter(Gift.id == id).first()
        found_gift = db.session.get(Gift, id)
        db.session.delete(found_gift)
        db.session.commit()

        return {}, 204
    except:

        return {"message": "Not found"}, 404


if __name__ == '__main__':
    app.run(port=5555, debug=True)
