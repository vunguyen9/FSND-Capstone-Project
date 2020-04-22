import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db_drop_and_create_all
import json
from auth import AuthError, requires_auth


def create_app(test_config=None):
    APP = Flask(__name__)
    setup_db(APP)
    CORS(APP)

    @APP.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # GET /movies
    @APP.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def get_movie(token):
        selection = Movie.query.order_by(Movie.id).all()
        movies = [m.format() for m in selection]
        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies': len(movies)
        })

    # DELETE /movies/id
    @APP.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            return abort(404, 'Resource not found')
        movie.delete()
        selection = Movie.query.order_by(Movie.id).all()
        movies = [m.format() for m in selection]
        return jsonify({
            'success': True,
            'movies': movies,
            'deleted': movie.id
        })

    # POST /movies
    @APP.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def post_movie(token):
        if request.data:
            new_movie = json.loads(request.data.decode('utf-8'))
            if 'title' not in new_movie:
                abort(422, "Title Required")
            if 'release_date' not in new_movie:
                abort(422, "Release_date Required")
            title = new_movie['title']
            release_date = new_movie['release_date']
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            selection = Movie.query.order_by(Movie.id).all()
            movies = [m.format() for m in selection]
            return jsonify({
                'success': True,
                'movies': movies,
                'total_movies': len(movies)
            })
        else:
            abort(400, "Bad Request")

    # PATCH /movies/id
    @APP.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def update_movie(token, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            return abort(404, 'Resource not found')
        if request.data:
            body = json.loads(request.data.decode('utf-8'))
            if 'title' in body:
                title = body.get('title')
                movie.title = title
            if 'release_date' in body:
                release_date = body.get('release_date')
                movie.release_date = release_date
            movie.update()
            selection = Movie.query.order_by(Movie.id).all()
            movies = [m.format() for m in selection]
            return jsonify({
                'success': True,
                'movies': movies,
                'total_movies': len(movies),
                'updated': movie.id
            })
        else:
            abort(400, 'Bad Request')

    # GET /actors
    @APP.route('/actors', methods=['GET'])
    @requires_auth('read:actors')
    def get_actor(token):
        selection = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in selection]
        return jsonify({
            'success': True,
            'actors': actors,
            'total_actors': len(actors)
        })

    # DELETE /actors/id
    @APP.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            return abort(404, 'Resource not found')
        actor.delete()
        selection = Actor.query.order_by(Actor.id).all()
        actors = [a.format() for a in selection]
        return jsonify({
            'success': True,
            'actors': actors,
            'deleted': actor.id
        })

    # POST /actors
    @APP.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def post_actor(token):
        if request.data:
            new_actor = json.loads(request.data.decode('utf-8'))
            if 'name' not in new_actor:
                abort(422, "Name Required")
            if 'age' not in new_actor:
                abort(422, "Age Required")
            if 'gender' not in new_actor:
                abort(422, "Gender Required")
            name = new_actor['name']
            age = new_actor['age']
            gender = new_actor['gender']
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            selection = Actor.query.order_by(Actor.id).all()
            actors = [actor.format() for actor in selection]
            return jsonify({
                'success': True,
                'actors': actors,
                'total_actors': len(actors)
            })
        else:
            abort(400, 'Bad Request')

    # PATCH /actors/id
    @APP.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def update_actor(token, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            return abort(404, 'Resource not found')
        if request.data:
            body = json.loads(request.data.decode('utf-8'))
            if 'name' in body:
                name = body.get('name')
                actor.name = name
            if 'age' in body:
                age = body.get('age')
                actor.age = age
            if 'gender' in body:
                gender = body.get('gender')
                actor.gender = gender
            actor.update()
            selection = Actor.query.order_by(Actor.id).all()
            actors = [a.format() for a in selection]
            return jsonify({
                'success': True,
                'actors': actors,
                'total_actors': len(actors),
                'updated': actor.id
            })
        else:
            abort(400, 'Bad Request')

    # Error Handling
    @APP.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource_not_found"
        })

    @APP.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @APP.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        })

    @APP.errorhandler(AuthError)
    def auth_error(error):
        return jsonify(error.error), error.status_code

    return APP


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
