import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from authTokens import *

class CastTestCase(unittest.TestCase):
    """This class represents the cast test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.assistant_token = assistant
        self.director_token = director
        self.producer_token = producer
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.movie = {
            "title": "Finding Nemo",
            "release_date": "1998-03-22"
        }

        self.invalid_movie = {
            "title": "Finding Nemo",
        }

        self.valid_update_movie = {
            "title": "Finding Nemo 2",
            "release_date": "1999-03-22"
        }

        self.invalid_update_movie = {
            "release_date": "1999-03-22"
        }

        self.actor = {
            "name": "Alan Turing",
            "age": 50,
            "gender": "male"
        }

        self.invalid_actor = {
            "name": "Alan Smith"
        }

        self.valid_update_actor = {
            "name": "Alan Turing",
            "age": 52,
            "gender": "male"
        }

        self.invalid_update_actor = {
            "age": 52,
            "gender": "male"
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

    '''
    def test_get_movies_without_token(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 500)
    '''

    def test_get_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertTrue(len(data["movies"]))

    def test_get_movie_by_id(self):
        res = self.client().get('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["movie"]["title"], "Good Will Hunting")
        
    def test_get_movie_by_id_failded(self):
        res = self.client().get('/movies/111', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
     
    def test_create_movie_with_director_token(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])


    def test_create_movie_with_producer_token(self):
        """Passing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])

    def test_create_movie_with_producer_token_400(self):
        """Passing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.invalid_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
   
    def test_update_movie_with_producer_token(self):
        """Passing Test for POST /movies"""
        res = self.client().patch('/movies/6', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.valid_update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_update_movie_with_producer_token_400(self):
        """Passing Test for update /movies"""
        res = self.client().patch('/movies/6', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.invalid_update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])


    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertTrue(len(data["actors"]))

    def test_get_actor_by_id(self):
        res = self.client().get('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["actor"]["name"], "Tom Hanks")
        
    def test_get_actor_by_id_failded(self):
        res = self.client().get('/actor/199', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_create_actor_with_assistant_token(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        }, json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])


    def test_create_movie_with_director_token(self):
        """Passing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])

    def test_create_actor_with_producer_token_400(self):
        """Passing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.invalid_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
   
    def test_update_actor_with_producer_token(self):
        """Passing Test for POST /actors"""
        res = self.client().patch('/actors/2', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.valid_update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_update_actor_with_producer_token_400(self):
        """Passing Test for update /actors"""
        res = self.client().patch('/actors/2', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        }, json=self.invalid_update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()