import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS

from models import setup_db, Actor, Movie, CastDetails
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app


APP = create_app()

# CORS Headers


@APP.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,true')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,POST,DELETE,PATCH,OPTIONS')
    return response


@APP.route('/')
def start_page():
    return jsonify({
        "message": "Welcome to Udacity Production House!"
    })


@APP.route('/actors')
@requires_auth('get:actors')
def get_actors():
    try:
        selection = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in selection]

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors
        })
    except Exception:
        abort(422)


@APP.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def create_actors():
    try:

        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    except Exception:
        abort(422)


@APP.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actor')
def update_actors(actor_id):
    try:
        body = request.get_json()

        actor = Actor.query.filter(Actor.id == actor_id).first()

        if actor is None:
            abort(404)

        actor.name = body.get('name', actor.name)
        actor.age = body.get('age', actor.age)
        actor.gender = body.get('gender', actor.gender)

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })
    except Exception:
        abort(422)


@APP.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actors(actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).first()
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'delete': actor_id
        })
    except Exception:
        abort(422)


if __name__ == '__main__':
    APP.run()
    # APP.run(host='0.0.0.0', port=8080, debug=True)
