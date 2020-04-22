import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from app import create_app
from models import setup_db, Movie, Actor, db_drop_and_create_all

casting_assistant = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1USXdPVFJEUkRneU0wTkVRekpGUTBJelFUaEdSamMzUVRrd01UWXlSRVUzTmtZNU9UVTRPQSJ9.eyJpc3MiOiJodHRwczovL3Z1bmd1eWVuOS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzVlZTEzYTEzNmUwYzVkNDRhYjcxIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODc0MjcxMzcsImV4cCI6MTU4NzUxMzUzNywiYXpwIjoiWUxMRmp4Y0MzbzhLQ0RqYUVxUXlBMGU2OFp2dWQzQTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.lZESKjlu_sDOee1reF6TZoQrBS05Eml_i2DjHuaQrWN5Y-NLTOQAW7iE4-0OiNp2F9RrPeIVF6BPFv4X2FnGqN6h60iWVL5AVF8XrDKHWUQhKSVkhgkKdYfFVfOtRqyNR5X_oiHpTTnEXmj9cdFtxGzW17RBGHeodnsSUTpeL6LDQjEc4GY9WK55ncxC5jAjDLxv2xW2wvFqeWube8LHVr768cnbszoRfdJa1Lnbr_uJsVmytOQAiwp2Hrh0FKO3neqrP-VrRlOS2hnUNv-e9VM0CAUwxXvLHKEHhoh7uY7yjSISKA4OHR60EfCGTJvlCJ9SW5bYFRi5og3ijdQuow"}

casting_director = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1USXdPVFJEUkRneU0wTkVRekpGUTBJelFUaEdSamMzUVRrd01UWXlSRVUzTmtZNU9UVTRPQSJ9.eyJpc3MiOiJodHRwczovL3Z1bmd1eWVuOS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzVmNTYzYTEzNmUwYzVkNDRhY2IyIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODc0MjcyNjUsImV4cCI6MTU4NzUxMzY2NSwiYXpwIjoiWUxMRmp4Y0MzbzhLQ0RqYUVxUXlBMGU2OFp2dWQzQTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwiZWRpdDphY3RvcnMiLCJlZGl0Om1vdmllcyIsInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.lsyupRS3iZyTI9KvqApBjBK7vcGjhSceosXkMVQX8a7lj7GyJ4ZToD8d_xU1D_1YqRqIzfbxVNfy164ZIH1lsiNTn3q0FcITmxzLanP3RwyAY0bnOmGrBstUOHuFWefo1yP2nSGsWVuDIFsLPf2IQJd0O1Rc-cax3SjilfLz6Kq1WaYOnf0IEqKQOFFpPlRatpk7ahp53IZ__09aS5MCWOMvc3x-yDOPcCM0YNmqGtr6gtRn18QxBfEBAP4ZQ24Txy_KUq0zomHBceISGw1LAumYvt0l4uG-x-kg2mMIn4_it8R2JzR_gkqVUGNB7-5j-pb_E90V5IMERC-G_brrYQ"}

executive_producer = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1USXdPVFJEUkRneU0wTkVRekpGUTBJelFUaEdSamMzUVRrd01UWXlSRVUzTmtZNU9UVTRPQSJ9.eyJpc3MiOiJodHRwczovL3Z1bmd1eWVuOS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3YzVmOTRiMzQyMTEwYzU0NzlmNmM0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODc0MjczODksImV4cCI6MTU4NzUxMzc4OSwiYXpwIjoiWUxMRmp4Y0MzbzhLQ0RqYUVxUXlBMGU2OFp2dWQzQTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.wiu44Jk-mUSF-xnclno0C5ShmbvZKq4Ug4qvXPVVuEyUu49aFdupEqSoMGhM8XpN7MvKsmHHSsru-WsQja52cM2R0jAU80-4oOjtWazBR9uaRlzOcckDYg4i185x6Mq3qkjLB2pBflMmgSENusP_Vip5vBX__KZFdjr3fcpfY3fi4NzdNuiJrTdAQ1OrGNVLBMWjTsgH7JkgX8GtP_dE0dmBWyFgnM1N5sgA3acTUrRmmWw1aTEin9UP6q89i01HI_2tMBQFo312hv7tFWzKRyNbXF6Ci1N3toNwtLyIgTJ4DnIe4pqnwKCTB6ImEF7FSUafIbSDsrBCLpCd5RzdPw"}


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the CastingAgency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        db_drop_and_create_all()
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'New Year',
            'release_date': '6/2019'
        }

        self.new_actor = {
            'name': 'Dale',
            'age': '25',
            'gender': 'Male'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# Test POST /movies
    def test_post_movies(self):
        res = self.client().post('/movies', json=self.new_movie, headers=executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_movies'] > 1)

    def test_post_movies_error_401(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    def test_post_movies_error_422(self):
        res = self.client().post('/movies', json={'title': 'Ending'}, headers=executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unprocessable")

# Test GET /movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers=casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_movies_error_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

# Test PATCH /movies
    def test_patch_movies(self):
        res = self.client().patch('/movies/1', json={'title': 'King Kong', 'release_date': '12/2020'}, headers=casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 1)

    def test_patch_movies_error_404(self):
        res = self.client().patch('/movies/99', json={'title': 'King Kong', 'release_date': '12/2020'}, headers=casting_director)
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "resource_not_found")

    def test_patch_movies_error_401(self):
        res = self.client().patch('/movies/1', json={'title': 'King Kong', 'release_date': '12/2020'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

# Test DELETE /movies
    def test_delete_movies_error_401(self):
        res = self.client().delete('/movies/1', headers=casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

    def test_delete_movies(self):
        res = self.client().delete('/movies/1', headers=executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

# Test POST /actors
    def test_post_actors(self):
        res = self.client().post('/actors', json=self.new_actor, headers=executive_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_actors'] > 1)

    def test_post_actors_error_401(self):
        res = self.client().post('/actors', json=self.new_actor, headers=casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

# Test GET /actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers=casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_actors_error_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

# Test PATCH /movies
    def test_patch_actors(self):
        res = self.client().patch('/actors/1', json={'name': 'John', 'age': 45}, headers=casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 1)

    def test_patch_actors_error_404(self):
        res = self.client().patch('/actors/99', json={'name': 'John', 'age': 45}, headers=executive_producer)
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "resource_not_found")

    def test_patch_actors_error_401(self):
        res = self.client().patch('/actors/1', json={'name': 'John', 'age': 45}, headers=casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

# Test DELETE /actors
    def test_delete_actors_error_401(self):
        res = self.client().delete('/actors/1', headers=casting_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

    def test_delete_movies(self):
        res = self.client().delete('/actors/1', headers=casting_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


if __name__ == "__main__":
    unittest.main()
