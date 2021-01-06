from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth.auth import AUTH0_DOMAIN, API_AUDIENCE, AuthError, requires_auth
from flask import Flask, request, abort, jsonify, redirect, render_template, abort, jsonify, Response, flash, url_for
import json
import os
# AUTH0 Config
AUTH0_CALLBACK_URL = "https://127.0.0.1:8080/"
AUTH0_CLIENT_ID = "uV2bUfeivPZl2ntqfgGAZG2tRBpYEDl0"

# create and configure the app
app = Flask(__name__)
setup_db(app)
CORS(app)


# Max items per page
MAX_ITEM = 10


# paginate()
def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * MAX_ITEM
    end = start + MAX_ITEM

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items

# --------Root--------
@app.route('/')
def index():
    return "Udacity Casting Agency (Capstone)"


# --------Root_Accept--------
# @app.route('/', methods=['POST'])
# def get_token():
#     token = request.args.get('token')
#     if not token:
#         return jsonify({
#             'message': 'Missing Token'
#         }), 403
#     return jsonify({
#         'token': token
#     }), 200

# --------Authorization--------
@app.route("/auth")
def auth_service():
    url = f'https://{AUTH0_DOMAIN}/authorize' \
        f'?audience={API_AUDIENCE}' \
        f'&response_type=token&client_id=' \
        f'{AUTH0_CLIENT_ID}&redirect_uri=' \
        f'{AUTH0_CALLBACK_URL}'

    return redirect(url)


# --------ACTORS--------
'''
GET /actors
    this endpoint GET paginated actors in JSON,
    endpoint available all roles,
    Actor has the firstname, lastname, age (Number) and gender.
'''
@app.route('/actors')
# @requires_auth('get:actors')
def get_actors():

    selection = Actors.query.order_by(Actors.id).all()
    total = len(selection)
    actors = paginate(request, selection)

    if not len(actors):
        abort(404)

    return jsonify({
        "success": True,
        "actors": actors,
        "total": total
    }), 200


'''
POST /actors
    this endpoint POST a new actor,
    endpoint available to Director and Producer roles only,
    Actor will require the firstname, lastname, age (Number) and gender.
'''


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actor(jwt):

    response = request.get_json()

    try:
        firstname = response.get('firstname')
        lastname = response.get('lastname')
        age = int(response.get('age'))
        gender = response.get('gender')
    except Exception:
        abort(400)
    # Checks if all attributes has value
    if firstname is None:
        abort(400)
    if lastname is None:
        abort(400)
    if age is None:
        abort(400)
    if gender is None:
        abort(400)

    # Create Actor
    actor = Actors(
        firstname=firstname,
        lastname=lastname,
        age=age,
        gender=gender
    )
    # Insert actor into database
    try:
        actor.insert()
    except Exception:
        abort(422)

    return jsonify({
        "success": True,
        "actor": actor.format()
    }), 200


'''
PATCH /actors/<int:id>
    This endpoint updates the actor using id,
    Available to Director and Producer roles
'''


@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actors(jwt, id):

    actor = Actors.query.get(id)
    if actor is None:
        abort(404)

    response = request.get_json()

    if 'firstname' in response:
        actor.firstname = response.get('firstname')

    if 'lastname' in response:
        actor.lastname = response.get('lastname')

    if 'age' in response:
        actor.age = response.get('age')

    if 'gender' in response:
        actor.gender = response.get('gender')

    try:
        actor.update()
    except Exception:
        abort(422)

    return jsonify({
        "success": True,
        "actor": actor.format()
    }), 200


'''
DELETE /actors/<int:id>
    This endpoint is for deleting the actor using id,
    Endpoint is only available to Director and Producer roles

'''


@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(jwt, id):
    actor = Actors.query.get(id)
    if actor is None:
        abort(404)

    id = actor.id

    try:
        actor.delete()
    except Exception:
        abort(422)

    return jsonify({
        "success": True,
        "delete": id
    }), 200


# --------MOVIES--------
'''
GET /movies
    This endpoint available to all three roles,
    Is to get all the movies from the database 
'''


@app.route('/movies')
# @requires_auth('get:movies')
def get_movies():

    selection = Movies.query.order_by(Movies.id).all()
    total_movies = len(selection)
    movies = paginate(request, selection)

    if not len(movies):
        abort(404)

    return jsonify({
        "success": True,
        "movies": movies,
        "total": total_movies
    }), 200


'''
POST /movies
    This endpoint is for adding new movies into the database,
    Only available to Producer roles.
    This endpoint take title, release_date and description parameters
'''


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movie(jwt):
    response = request.get_json()

    title = response.get('title')
    if title is None:
        abort(400)

    release_date = response.get('release_date', None)
    description = response.get('description', None)

    # Create new movie
    movie = Movies(
        title=title,
        release_date=release_date,
        description=description
    )
    # Insert new movie into database
    try:
        movie.insert()
    except Exception:
        abort(422)

    return jsonify({
        "success": True,
        "movie": movie.format()
    }), 200


'''
PATCH /movies/<int:id>
    This endpoint updates the Movie using id,
    Available to Director and Producer roles
    Takes Json body with the key-Value pair 
    of the attributes to update
'''


@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movies(jwt, id):

    movie = Movies.query.get(id)

    # Movie Not found
    if movie is None:
        abort(404)

    response = request.get_json()

    if 'title' in response:
        movie.title = response.get('title')

    if 'release_date' in response:
        movie.release_date = response.get('release_date')

    if 'description' in response:
        movie.description = response.get('description')

    # Update the movie in the database
    try:
        movie.update()
    except Exception:
        abort(422)

    return jsonify({
        "success": True,
        "movie": movie.format()
    }), 200


'''
DELETE /movies/<int:id>
    This endpoint is for deleting the Movie using id,
    Endpoint only available to Producer roles
'''


@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(jwt, id):

    # Get movie from the database
    movie = Movies.query.get(id)
    if movie is None:
        abort(404)

    id = movie.id

    try:
        movie.delete()
    except Exception:
        abort(422)

    return jsonify({
        "success": True,
        "delete": id
    }), 200


# Error Handling
'''
Example error handling for AuthError entity
'''


@app.errorhandler(AuthError)
def auth_error_handler(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


'''
Example error handling for Bad request
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


'''
Example error handling for Unauthorized entity
'''
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401


'''
Example error handling for Forbidden entity
'''
@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Forbidden'
    }), 403


'''
Example error handling for Resource_not_found entity
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource Not Found'
    }), 404


'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


if __name__ == '__main__':
    app.run(port=8080, debug=True)
