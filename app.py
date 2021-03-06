import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS

from models import setup_db, Actor, Movie
from auth import requires_auth, AuthError


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
def get_actors(payload):
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
def create_actors(payload):
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
def update_actors(payload, actor_id):
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
def delete_actors(payload, actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).first()
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        })
    except Exception:
        abort(422)


@APP.route('/movies')
@requires_auth('get:movies')
def get_movies(payload):
    try:
        selection = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in selection]

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies
        })
    except Exception:
        abort(422)


@APP.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def create_movies(payload):
    try:
        body = request.get_json()

        new_title = body.get('title', None)
        new_releasedate = body.get('releasedate', None)

        movie = Movie(title=new_title, releasedate=new_releasedate)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    except Exception:
        abort(422)


@APP.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movie')
def update_movies(payload, movie_id):
    try:
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).first()

        if movie is None:
            abort(404)

        movie.title = body.get('title', movie.title)
        movie.releasedate = body.get('releasedate', movie.releasedate)
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })
    except Exception:
        abort(422)


@APP.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movies(payload, movie_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie_id
        })
    except Exception:
        abort(422)

    # Error Handling


@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@APP.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@APP.errorhandler(400)
def badrequest(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@APP.errorhandler(500)
def internalservererror(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500


@APP.errorhandler(405)
def methodnotfound(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Found"
    }), 405


@APP.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@APP.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


@APP.errorhandler(AuthError)
def autherror(Exception):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Authorization Error"
    }), 401

# return app


if __name__ == '__main__':
    APP.run()
    # app.run(host='0.0.0.0', port=8080, debug=True)
