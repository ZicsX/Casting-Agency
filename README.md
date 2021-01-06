# Casting Agency API

## Motivation
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

### Dependencies
#### Python 3.7 | PostgreSQL | Flask | SQLAlchemy

##### Application Dependencies
```
alembic
Flask
Flask-Cors
Flask-Migrate
Flask-Script
Flask-SQLAlchemy
future
gunicorn
Jinja2
jose
Mako
MarkupSafe
psycopg2-binary
pyasn1
pycryptodome
python-dateutil
python-editor
python-jose
python-jose-cryptodome
rsa
SQLAlchemy
```
#### Local development
Running the application locally

###### Virtual Enviornment
Create python virtual environment
```bash
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```bash
env/Scripts/activate
```
##### Install Dependencies

Install application dependencies within the `requirements.txt` file using pip:
```bash
pip install -r requirements.txt
```

##### Database Setup
Create capstone database to store movie-data
In terminal run:
```bash
createdb capstone
```
With Postgres running, restore a database using the capstone.psql file. 
From the project folder in terminal run:
```bash
psql capstone < capstone.psql
```
or
```bash
psql -U username -p port -d capstone -f capstone.psql
```
##### Environment Configuration
Use `setup.sh` bash file to set up local environment variables.
Also set the database URL with correct port
``` 
export DATABASE_URL=postgres://username:password@localhost:port/capstone
```
##### Database Manage & Migrations

```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
#### Running the server locally
To run the server, execute:
```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
or in Windows
```bash
set FLASK_APP=app
set FLASK_ENV=development
flask run
```

## Roles and Permissions
#### Casting Assistant
- Can view actors and movies
#### Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies
#### Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database

## Endpoints
- INDEX `/` returns Casting-Agency
- LOGIN `/login` redirects to the Auth0 login page
- GET `/actors` gets actors from the database
- POST `/actors` post new actors into database
- PATCH `/actors/<int:id>` update actors
- DELETE `/actors/<int:id>` dalete actors using id
- GET `/movies` gets movies from the databse
- POST `/movies` post new movie to database
- PATCH `/movies/<int:id>` update movie
- DELETE `/movies/<int:id>` delete using movie id

### GET `/actors`
- This endpoint GET paginated actors in JSON,
- endpoint available to all three roles, 
- Actor has id, firstname, lastname, age (Number) and gender.
- successful request returns status code of 200 
- and 404 if len(actors) == 0
```
{
  "actors": [
    {
      "age": 1, 
      "firstname": "Fname1", 
      "gender": "Male", 
      "id": 1, 
      "lastname": "Lname1"
    },
    ...
    {
      "age": 11, 
      "firstname": "Fname11", 
      "gender": "Male", 
      "id": 11, 
      "lastname": "Lname11"
    }
  ], 
  "success": true, 
  "total": 28
}
```

### Post `/actors/`
- This endpoint POST a new actor,
- only available to Director and Producer roles,
- It require the firstname, lastname, age (Number) and gender.
```
{
    "firstname": "Noname",
    "lastname": "Nolastname",
    "age": 26,
    "gender": "Female"
}
```
- Successful request returns JSON object (Current actor with the details) and status code of 200
- 400 if value is missing 
- 400 if age is not a number
- 401 if unauthorized
- 422 if Unprocessable Entity

### PATCH ` /actors/<int:id>`
- This endpoint updates the actor using id,
- Only availale to Director and Producer roles
```
{
    "lastname": "Mylastname"
    "age":21
}
```
- Succesful requests returns the current actor with updated details with status code of 200
```
{
    "actor": {
        "age": 21,
        "firstname": "Noname99",
        "gender": "Male",
        "id": 2,
        "lastname": "Mylastname"
    },
    "success": true
}
```
- 400 if age is not a number
- 401 if unauthorized
- 422 if Unprocessable Entity

### DELETE `/actors/<int:id>`
- This endpoint delete the actor using id,
- Endpoint is only available to Director and Producer roles
```
{
    "delete": 2,
    "success": true
}
```
- Succesful requests returns status code of 200
- 401 if Unauthorized
- 404 if actor does not exist
- 422 if Unprocessable Entity

### GET `/movies`
- This endpoint gets paginated list of movies from the database 
- endpoint is available to all three roles,
- Successful request returns Json list of movies with status code of 200
- 404 if len(movies) is zero
```
{
  "movies": [
    {
      "description": "Captain Willard is sent to Cambodia on a dangerous mission to assassinate a renegade colonel who has won the trust of a local tribe.", 
      "id": 1, 
      "release_date": "1979-01-01", 
      "title": "Apocalypse Now"
    }, 
    {
      "description": "Another war movie :-(", 
      "id": 2, 
      "release_date": "1987-01-01", 
      "title": "Full Metal Jacket"
    }, 
    ...
    {
      "description": null, 
      "id": 12, 
      "release_date": "1999-01-02", 
      "title": "American Beauty"
    }
  ], 
  "success": true, 
  "total": 13
}
```


### Post `/movies/`
- This endpoint is for adding new movies into the database,
- Only available to Producer roles.
- This endpoint take title, release_date and description parameters
```
{
    "title": "New Movie",
    "release_date": "2021-01-01",
    "description":"description description description !!!"
}
```
- Successful request returns current movie with datails and status code of 200
- 400 if title is missing
- 401 if Unauthorized
- 422 if Unprocessable Entity

### Patch `/movies/<int:id>`
- This endpoint updates the Movie using id,
- Available to Director and Producer roles
- Takes Json body with the key-Value pair of the attributes to update
```
{
    "description": "Another war movie :("
}
```
- Successful request returns current movie with updated details and status code of 200
- 404 if movie not found
- 401 if Unauthorized
- 422 if invalid object is submitted

### Delete `/movies/<int:id>`
- This endpoint is for deleting the Movie using id,
- Endpoint only available to Producer roles
- Successful request returns status code of 200 with JSON
```
{
    "delete": 11,
    "success": true
}
```
- 404 if movie not found
- 401 if Unauthorized
- 422 if invalid object is submitted


### Error Handling
- 400 - Bad reqest
    ```
        {
          "error": 404, 
          "message": "Resource was not found", 
          "success": false
        }
     ```  
- AuthError
    - 401 - token expired 
    - 401 - invalid claims 
    - 400 - invalid header
    - 403 - unauthorized
- 404 - Resource not found
- 405 - Method not found
- 422 - Unprocessable entity
- 500 - Internal Server error

## Running tests
###### postman test run
Test your endpoints with [Postman](https://getpostman.com).
- Import the postman collection [capstone](capstone.postman_collection.json) to run the tests.
- Change the HOST variable to `localhost:8080` for testing locally

###### Using `test_app.py` script
- Change the HOST variable to `https://zicsx-fsnd-capstone.herokuapp.com` for testing hosted api
```bash
python test_app.py
```

## Hosting
This application is hosted on heroku: ['Casting Agency'](https://zicsx-fsnd-capstone.herokuapp.com/)