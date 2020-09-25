import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class ProductionHouseTestCase(unittest.TestCase):
    """This class represents the Udacity Production House test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_URL')
        setup_db(self.app, self.database_path)

        # sample authorization header

        self.auth_header = {'Authorization': os.environ.get('AUTH_HEADER')}

        # sample input for adding a actor
        self.new_actor = {
            'name': 'Bryan',
            'age': 20,
            'gender': 'male'
        }

        # sample input for adding a movie
        self.new_movie = {
            'name': 'Titanic',
            'releasedate': '2020-10-10 00:12:12'
        }

        # sample input for updating a actor
        self.update_actor = {
            'age': 40
        }

        # sample input for updating a movie
        self.update_movie = {
            'releasedate': '2035-10-10 00:12:12'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # tests for GET /actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_405_incorrect_url_get_actors(self):
        res = self.client().get('/actors/23', headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Found')

    # tests for GET /movies

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_405_incorrect_get_movies(self):
        res = self.client().get('/movies/23', headers=self.auth_header)
        print(res.data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Found')

    # tests for DELETE /actors
    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=self.auth_header)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

    def test_422_out_of_range_delete_actors(self):
        res = self.client().delete('/actors/1000', headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

    # tests for DELETE /movies

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.auth_header)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)

    def test_422_out_of_range_delete_movies(self):
        res = self.client().delete('/movies/1000', headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

    # tests for POST /actors

    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_actor_creation_not_possible(self):
        res = self.client().post('/actor/230', json=self.new_actor,
                                 headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for POST /movies

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_405_movie_creation_not_possible(self):
        res = self.client().post('/movies/230', json=self.new_movie,
                                 headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method Not Found')

    # tests for PATCH /actors

    def test_update_actor(self):
        res = self.client().patch('/actors/2', json=self.update_actor,
                                  headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_422_actor_updation_not_possible(self):
        res = self.client().patch('/actors/230', json=self.update_actor,
                                  headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

    # tests for PATCH /movies

    def test_update_movie(self):
        res = self.client().patch(
            '/movies/2',
            json=self.update_movie,
            headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_422_movie_updation_not_possible(self):
        res = self.client().patch(
            '/movies/230',
            json=self.update_movie,
            headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
