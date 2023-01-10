from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

import sqlite3

app = Flask(__name__)

db_name = "movies.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


def custom_error(message, status_code):
    return make_response(jsonify(message), status_code)


class Movie(db.Model):
    __tablename__ = "movies"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    runtime = db.Column(db.Integer, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    title = db.Column(db.Text, nullable=True)
    budget = db.Column(db.Integer, nullable=True)


class Actor(db.Model):
    __tablename__ = "actor_credits"
    __table_args__ = {"extend_existing": True}
    credit_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    character = db.Column(db.Text)


class Crew(db.Model):
    __tablename__ = "crew_credits"
    __table_args__ = {"extend_existing": True}
    credit_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    department = db.Column(db.Text)
    job = db.Column(db.Text)


@app.route("/")
def index():
    return "Server Works!"


@app.route("/movies", methods=["GET"])
def get_movie_collection():
    movies = Movie.query.limit(50).all()
    movie_list = []
    for movie in movies:
        movie_list += [
            {
                "budget": movie.budget,
                "title": movie.title,
                "release_date": movie.release_date.strftime("%Y-%m-%d"),
                "runtime": movie.runtime,
                "id": movie.id,
            }
        ]
    return jsonify(movie_list)


@app.route("/movies/<int:id>", methods=["GET"])
def get_movie_resource(id):
    movie = Movie.query.filter(Movie.id == id)
    try:
        movie = movie[0]
    except IndexError:
        # TODO: flask might have http code constants.
        return custom_error("Resource not found.", 404)

    # TODO: I'm ignoring the case where movie has >1 entries.
    # This should not happen but we should probably handle it
    # regardless.

    return jsonify(
        {
            "budget": movie.budget,
            "title": movie.title,
            "release_date": movie.release_date.strftime("%Y-%m-%d"),
            "runtime": movie.runtime,
            "id": movie.id,
        }
    )


@app.route("/actors", methods=["GET"])
def get_actor_collection():
    actors = Actor.query.limit(50).all()
    actor_list = []
    for actor in actors:
        actor_list += [
            {
                "character": actor.character,
                "name": actor.name,
                "id": actor.id,
                "movie_id": actor.movie_id,
                "credit_id": actor.credit_id,
            }
        ]
    return jsonify(actor_list)


@app.route("/actors/<int:id>", methods=["GET"])
def get_actor_resource(id):
    actor = Actor.query.filter(Actor.credit_id == id)
    try:
        actor = actor[0]
    except IndexError:
        # TODO: flask might have http code constants.
        return custom_error("Resource not found.", 404)

    # TODO: I'm ignoring the case where actor has >1 entries.
    # This should not happen but we should probably handle it
    # regardless.

    return jsonify(
        {
            "character": actor.character,
            "name": actor.name,
            "id": actor.id,
            "movie_id": actor.movie_id,
            "credit_id": actor.credit_id,
        }
    )


@app.route("/crew", methods=["GET"])
def get_crews():
    crew = Crew.query.limit(50).all()
    crew_list = []
    for c in crew:
        crew_list += [
            {
                "job": c.job,
                "deparment": c.department,
                "name": c.name,
                "movie_id": c.movie_id,
                "credit_id": c.credit_id,
            }
        ]
    return jsonify(crew_list)


@app.route("/crew/<int:id>", methods=["GET"])
def get_crew_resource(id):
    crew = Crew.query.filter(Crew.credit_id == id)
    try:
        crew = crew[0]
    except IndexError:
        # TODO: flask might have http code constants.
        return custom_error("Resource not found.", 404)

    # TODO: I'm ignoring the case where crew has >1 entries.
    # This should not happen but we should probably handle it
    # regardless.

    return jsonify(
        {
            "job": crew.job,
            "deparment": crew.department,
            "name": crew.name,
            "movie_id": crew.movie_id,
            "credit_id": crew.credit_id,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
