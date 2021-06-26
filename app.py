import os
from flask import Flask, request, abort, jsonify
from flask import render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "super secret key"
    setup_db(app)

    # setup cross origin
    CORS(app)

    AUTH0_CALLBACK_URL = "https://127.0.0.1:8080/login-results"
    AUTH0_AUDIENCE = "http://localhost:5000"
    AUTH0_JWT_API_AUDIENCE = "http://localhost:5000"
   
    @app.after_request
    def after_request(response):

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    database_path = "postgresql://postgres@localhost:5432/cast"


    DATABASE_URL= os.environ['DATABASE_URL']
    AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
    AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
    AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
    AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN

    @app.route("/")
    def index():
        return render_template("index.html")


    @app.route("/auth", methods=["GET"])
    def generate_auth_url():
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={AUTH0_JWT_API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'
        return redirect(url)


    #getting all movies
    @app.route("/movies")
    @requires_auth("get:movies")
    def get_movies(token):
        movies = Movie.query.all()

        return (
            jsonify(
                {
                    "success": True,
                    "movies": [movie.format() for movie in movies],
                }
            ),
            200,
        )

    # get a specific movie of a given id
    @app.route("/movies/<int:id>")
    @requires_auth("get:movies")
    def get_movie_by_id(token, id):
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "movie": movie.format(),
                    }
                ),
                200,
            )
    # create a movie
    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movies")
    def post_movie(token):
        data = request.get_json()
        title = data.get("title", None)
        release_date = data.get("release_date", None)

        if title is None or release_date is None:
            abort(400)

        movie = Movie(title=title, release_date=release_date)

        try:
            movie.insert()
            return jsonify({"success": True, "movie": movie.format()}), 201
        except Exception:
            abort(400)
    
    
    #update a movie of a given id
    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def patch_movie(token, id):

        data = request.get_json()
        title = data.get("title", None)
        release_date = data.get("release_date", None)

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        if title is None or release_date is None:
            abort(400)

        movie.title = title
        movie.release_date = release_date

        try:
            movie.update()
            return jsonify({"success": True, "movie": movie.format()}), 200
        except Exception:
            abort(400)
    
    
    #delete a movie of a given id
    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(token, id):

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        try:
            movie.delete()
            return jsonify(
                {
                    "success": True,
                    "message": f"movie id {movie.id}, titled {movie.title} was deleted",
                }
            )
        except Exception:
            db.session.rollback()
            abort(400)

    #get all actors
    @app.route("/actors")
    @requires_auth("get:actors")
    def get_actors(token):
        actors = Actor.query.all()

        return (
            jsonify(
                {
                    "success": True,
                    "actors": [actor.format() for actor in actors],
                }
            ),
            200,
        )
    
    #get actor of a given id
    @app.route("/actors/<int:id>")
    @requires_auth("get:actors")
    def get_actor_by_id(token, id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        else:
            return (
                jsonify(
                    {
                        "success": True,
                        "actor": actor.format(),
                    }
                ),
                200,
            )

    # create an actor
    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actors")
    def post_actor(token):
        data = request.get_json()
        name1 = data.get("name", None)
        age1 = data.get("age", None)
        gender1 = data.get("gender", None)

        if name1 is None or age1 is None or gender1 is None:
            abort(400)

        actor = Actor(name=name1, age=age1, gender=gender1)

        try:
            actor.insert()
            return jsonify({"success": True, "actor": actor.format()}), 201
        except Exception:
            abort(400)
    
    
    #update an actor of a given id
    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def patch_actor(token, id):

        data = request.get_json()
        name1 = data.get("name", None)
        age1 = data.get("age", None)
        gender1 = data.get("gender", None)

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)

        if name1 is None or age1 is None or gender1 is None:
            abort(400)

        actor.name = name1
        actor.gender = gender1
        actor.age = age1

        try:
            actor.update()
            return jsonify({"success": True, "movie": actor.format()}), 200
        except Exception:
            abort(400)
    
    
    #delete an actor of a given id
    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(token, id):

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        try:
            actor.delete()
            return jsonify(
                {
                    "success": True,
                    "message": f"actor id {actor.id}, titled {actor.name} was deleted",
                }
            )
        except Exception:
            db.session.rollback()
            abort(400)

  
    #Create error handlers for all expected errors 
   
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app

APP = create_app()

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080, debug=True)
