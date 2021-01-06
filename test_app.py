
import unittest
from app import app
from models import setup_db, database_path
import json
from flask_sqlalchemy import SQLAlchemy
from models import Actors, Movies
from flask import Flask


# HEROKU_HOST = 'https://zicsx-fsnd-capstone.herokuapp.com/'

ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNTdWpGeW9LS1FEQkNBLWFVem1HdyJ9.eyJpc3MiOiJodHRwczovL2Rldi04Nm82a2UzYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTUxMjAxMzc3NDQzMjUwODM4NzgiLCJhdWQiOlsiY2FwcyIsImh0dHBzOi8vZGV2LTg2bzZrZTNhLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDk5MTc0OTgsImV4cCI6MTYxMDAwMzg5OCwiYXpwIjoidVYyYlVmZWl2UFpsMm50cWZnR0FaRzJ0UkJwWUVEbDAiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yc1x0IiwiZ2V0Om1vdmllcyJdfQ.Sqb5CQylCxxCPO1sjNm0rHFWssNyRuu0WxXj_FOIRi9A6ROEuYCs-9hDM5sGhPz64lmfGWqY1ktwv0_PBxqsJWfbvkG0w-kxFmv6SxWQkrLFnFfKKWQDVHbxfO9QsCMllAnNpGkRrqhTBH0sUAr9eRZg0_pZ45Oh7nBArFMzdpQf01nBg94qI2HMm-jnxHATlsRsnTxjIRZHGBCQOOGq_V8z50JvEQ6CR3Tm6i8wv0tWnrIl3FqyRoQRdXB5FdiRCEeA851cFMnIvv2XVkSaiVD7WkgOO5GdE_u1MwY2yG7zxV-44H6NYGAOYTt7bqTr-gXZwXTMJaqOOoRo2qodNA'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNTdWpGeW9LS1FEQkNBLWFVem1HdyJ9.eyJpc3MiOiJodHRwczovL2Rldi04Nm82a2UzYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDAzOTgzNzM1NzgyMDA0MDE5NzYiLCJhdWQiOlsiY2FwcyIsImh0dHBzOi8vZGV2LTg2bzZrZTNhLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDk5MTcyNTYsImV4cCI6MTYxMDAwMzY1NiwiYXpwIjoidVYyYlVmZWl2UFpsMm50cWZnR0FaRzJ0UkJwWUVEbDAiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnNcdCIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.trVX_0iL356kNd7XSFs31QdYcvVCYm4AC6rSgOSUDjW39uFguFkaGllB96DIAu5qsBGW_2bnHVDRsW4ZbzAFYBOr-f8Z-XP-Qqo1FxqLHa05PFtHpkSGWTUSMBSAr1_T-jiaigaV98o8l40xZwjDVWnJ3NUpVgv41a_uBOogkNr6E9VMNiQqRjIp7H1smmNE-flF5MEUVy6nYkvpnOlfFcbEuUVhl-1QRsASk_k3NioCiKzwRmImJW8eNgyEyWR1Ugm5WJgVD9D2P_dgpmsWooNSrfwQwgRnzsuO-WWE3ip-ReIIwA0tZXvgN0YvHMe7KhV6jccMx2XqNZ5GwEkJkQ'
PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNTdWpGeW9LS1FEQkNBLWFVem1HdyJ9.eyJpc3MiOiJodHRwczovL2Rldi04Nm82a2UzYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTUyNzQwNDk0NDkzMTA1MTM0NzYiLCJhdWQiOlsiY2FwcyIsImh0dHBzOi8vZGV2LTg2bzZrZTNhLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDk5MjE5NTUsImV4cCI6MTYxMDAwODM1NSwiYXpwIjoidVYyYlVmZWl2UFpsMm50cWZnR0FaRzJ0UkJwWUVEbDAiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzXHQiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.oPvAVUsZXjfakh7MP3mwwEEHTUJLbkhslmEKZZnR8-FFem8rLAd3qTV80uThai-rExvSQmFg575k3s1462ZFCNN4kzr3yrPS6dYgr_oRGq6aE_Ig8SVqYrO9gICG916GP0jmS1tnZLeK0SdtF5IJQ4nM41lwL2euZxo4CjOEvShGCtOONk7wXArR65rhEzoWMWvQ4wWrEDeRTbZlix0wBXfkF6WHYafeW-7iTMqTJ1FwBMlP7nEk8hcqfhv5m8SE4ObE8mYI9IJp2Zr2UmNmWwY5eLpQYs5L7R7OFu5EWCEef2dTgDRbTr_PwJ9WvJWdIqLWZAAYObtB3e0eeKuyUg'


class CapstoneUnittest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.database_path = database_path
        self.token = PRODUCER_TOKEN
        app.config['TESTING'] = True
        self.client = self.app.test_client

        self.actor = {
            "firstname": "Fname",
            "lastname": "Lname",
            "age": 23,
            "gender": "Male"
        }
        self.update_actor = {
            "lastname": "Nolastname"
        }
        self.movie = {
            "title": "My movie",
            "release_date": "2021-01-01"
        }
        self.update_movie = {
            "description": None
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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
