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
        # self.database_name = 'productionhouse'
        self.database_path = "postgres://oqbvrscqxtauxy:e136500eea05225b7f9c9188950e841a38ff81f73c5702e4b2a8222ad9521e0d@ec2-34-234-185-150.compute-1.amazonaws.com:5432/d54n3tq0r4q5r8"
        #self.database_path = "postgres://postgres:postgres@localhost:5432/productionhouse"
        # .\format('postgres', 'postgres', 'localhost:5432',self.database_name)
        setup_db(self.app, self.database_path)

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
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_404_incorrect_url_categories(self):
        res = self.client().get('/actors/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for GET /movies

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_404_incorrect_get_movies(self):
        res = self.client().get('/movies/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for DELETE /actors
    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

    def test_404_out_of_range_delete_actors(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for DELETE /movies

    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)

    def test_404_out_of_range_delete_movies(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for POST /actors

    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_actor_creation_not_possible(self):
        res = self.client().post('/actor/230', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for POST /movies

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_movie_creation_not_possible(self):
        res = self.client().post('/movies/230', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for PATCH /actors

    def test_update_actor(self):
        res = self.client().patch('/actors/3', json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_actor_updation_not_possible(self):
        res = self.client().patch('/actors/230', json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests for PATCH /movies

    def test_update_movie(self):
        res = self.client().patch('/movies/3', json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_movie_updation_not_possible(self):
        res = self.client().patch('/movies/230', json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
