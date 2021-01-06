
import unittest
from app import app
from models import setup_db, database_path
import json
from flask_sqlalchemy import SQLAlchemy
from models import Actors, Movies
from flask import Flask


# HEROKU_HOST = 'https://zicsx-fsnd-capstone.herokuapp.com/'

ASSISTANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNTdWpGeW9LS1FEQkNBLWFVem1HdyJ9.eyJpc3MiOiJodHRwczovL2Rldi04Nm82a2UzYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTUxMjAxMzc3NDQzMjUwODM4NzgiLCJhdWQiOlsiY2FwcyIsImh0dHBzOi8vZGV2LTg2bzZrZTNhLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDk5MTc0OTgsImV4cCI6MTYxMDAwMzg5OCwiYXpwIjoidVYyYlVmZWl2UFpsMm50cWZnR0FaRzJ0UkJwWUVEbDAiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yc1x0IiwiZ2V0Om1vdmllcyJdfQ.Sqb5CQylCxxCPO1sjNm0rHFWssNyRuu0WxXj_FOIRi9A6ROEuYCs-9hDM5sGhPz64lmfGWqY1ktwv0_PBxqsJWfbvkG0w-kxFmv6SxWQkrLFnFfKKWQDVHbxfO9QsCMllAnNpGkRrqhTBH0sUAr9eRZg0_pZ45Oh7nBArFMzdpQf01nBg94qI2HMm-jnxHATlsRsnTxjIRZHGBCQOOGq_V8z50JvEQ6CR3Tm6i8wv0tWnrIl3FqyRoQRdXB5FdiRCEeA851cFMnIvv2XVkSaiVD7WkgOO5GdE_u1MwY2yG7zxV-44H6NYGAOYTt7bqTr-gXZwXTMJaqOOoRo2qodNA"
DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNTdWpGeW9LS1FEQkNBLWFVem1HdyJ9.eyJpc3MiOiJodHRwczovL2Rldi04Nm82a2UzYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDAzOTgzNzM1NzgyMDA0MDE5NzYiLCJhdWQiOlsiY2FwcyIsImh0dHBzOi8vZGV2LTg2bzZrZTNhLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDk5MjM0NzgsImV4cCI6MTYxMDAwOTg3OCwiYXpwIjoidVYyYlVmZWl2UFpsMm50cWZnR0FaRzJ0UkJwWUVEbDAiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnNcdCIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.bOXAqxEhzWNmnZSV4tFNHUCkctzPwxkU0C45dy_H797NwqasADrnOMdYktnbg1v3i5cO3BkXESaT2UnvjpWeSB5CrNy81hdxeiIEsTCkZlYwBM3A9pyctounjMi01PIe6hoPPNOcOa5RcmCjAZKvDmInkrUpE98hBGTbv8b14_qOZHiPX-TCBosn9OdwzA4R5OXUYy1tLA79W1Uq6cBubu34McueXqT-uOlisHJCbnajNIQxlX-A5_aeV-y-EyMP8ORxl13TpuGvUuYHI21BDM2dh_VEZ8Kq3JAn8tT-R1XA2LfnCsuXJNXUn7IETx4pXh3925eOyzxbwf_fAPX3Iw"
PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNTdWpGeW9LS1FEQkNBLWFVem1HdyJ9.eyJpc3MiOiJodHRwczovL2Rldi04Nm82a2UzYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTUyNzQwNDk0NDkzMTA1MTM0NzYiLCJhdWQiOlsiY2FwcyIsImh0dHBzOi8vZGV2LTg2bzZrZTNhLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDk5MjE5NTUsImV4cCI6MTYxMDAwODM1NSwiYXpwIjoidVYyYlVmZWl2UFpsMm50cWZnR0FaRzJ0UkJwWUVEbDAiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzXHQiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.oPvAVUsZXjfakh7MP3mwwEEHTUJLbkhslmEKZZnR8-FFem8rLAd3qTV80uThai-rExvSQmFg575k3s1462ZFCNN4kzr3yrPS6dYgr_oRGq6aE_Ig8SVqYrO9gICG916GP0jmS1tnZLeK0SdtF5IJQ4nM41lwL2euZxo4CjOEvShGCtOONk7wXArR65rhEzoWMWvQ4wWrEDeRTbZlix0wBXfkF6WHYafeW-7iTMqTJ1FwBMlP7nEk8hcqfhv5m8SE4ObE8mYI9IJp2Zr2UmNmWwY5eLpQYs5L7R7OFu5EWCEef2dTgDRbTr_PwJ9WvJWdIqLWZAAYObtB3e0eeKuyUg"


class CapstoneUnittest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.database_path = database_path
        self.producer = PRODUCER_TOKEN
        self.director = DIRECTOR_TOKEN
        self.assistant = ASSISTANT_TOKEN
        app.config['TESTING'] = True
        self.client = self.app.test_client

        self.actor = {
            "firstname": "Fname",
            "lastname": "Lname",
            "age": 23,
            "gender": "Male"
        }
        self.update_actor = {
            "lastname": "Nolastname",
            "age": 21,
            "gender": "Male"
        }
        self.movie = {
            "title": "My movie",
            "release_date": "2021-01-01"
        }
        self.update_movie = {
            "description": "description description description !!!"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['actors']), 0)

    def test_post_actors_producer(self):
        response = self.client().post('/actors', headers={
            'Authorization': 'Bearer ' + self.producer},
            json=self.actor)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_actors_director(self):
        response = self.client().post('/actors', headers={
            'Authorization': 'Bearer ' + self.director},
            json=self.actor)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_actors_unauthorized(self):
        response = self.client().post('/actors', headers={
            'Authorization': 'Bearer ' + self.assistant},
            json=self.actor)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
