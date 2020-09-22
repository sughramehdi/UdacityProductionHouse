import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie, CastDetails


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,DELETE,OPTIONS')
        return response

    return app


APP = create_app()


@APP.route('/actors')
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


if __name__ == '__main__':
    APP.run()
    # APP.run(host='0.0.0.0', port=8080, debug=True)
