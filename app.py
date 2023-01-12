from flask import Flask, jsonify, make_response, request
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

    def to_dict(self):
        return {
            "budget": self.budget,
            "title": self.title,
            "release_date": self.release_date.strftime("%Y-%m-%d"),
            "runtime": self.runtime,
            "id": self.id,
        }


class Actor(db.Model):
    __tablename__ = "actor_credits"
    __table_args__ = {"extend_existing": True}
    credit_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    character = db.Column(db.Text)

    def to_dict(self):
        return {
            "character": self.character,
            "name": self.name,
            "id": self.id,
            "movie_id": self.movie_id,
            "credit_id": self.credit_id,
        }


class Crew(db.Model):
    __tablename__ = "crew_credits"
    __table_args__ = {"extend_existing": True}
    credit_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    department = db.Column(db.Text)
    job = db.Column(db.Text)

    def to_dict(self):
        return {
            "job": self.job,
            "deparment": self.department,
            "name": self.name,
            "movie_id": self.movie_id,
            "credit_id": self.credit_id,
        }


@app.route("/")
def index():
    return "Server Works!"


@app.route("/movies", methods=["GET"])
def get_movie_collection():
    title = request.args.get('title', None)
    budget = request.args.get('title', None)
    release_date = request.args.get('title', None)
    runtime = request.args.get('title', None)
    if title:
        movies: list[Movie] = Movie.query.filter(Movie.title == title).all()
    else:
        movies: list[Movie] = Movie.query.limit(50).all()

    movie_list = []
    for movie in movies:
        movie_list += [movie.to_dict()]
    return jsonify(movie_list)


@app.route("/movies/<int:id>", methods=["GET"])
def get_movie_resource(id):
    movie: list[Movie] = Movie.query.filter(Movie.id == id)
    try:
        movie = movie[0]
    except IndexError:
        # TODO: flask might have http code constants.
        return custom_error("Resource not found.", 404)

    # TODO: I'm ignoring the case where movie has >1 entries.
    # This should not happen but we should probably handle it
    # regardless.

    return jsonify(movie.to_dict())


@app.route("/actors", methods=["GET"])
def get_actor_collection():
    actors: list[Actor] = Actor.query.limit(50).all()
    actor_list = []
    for actor in actors:
        actor_list += [actor.to_dict()]
    return jsonify(actor_list)


@app.route("/actors/<int:id>", methods=["GET"])
def get_actor_resource(id):
    actor: list[Actor] = Actor.query.filter(Actor.credit_id == id)
    try:
        actor = actor[0]
    except IndexError:
        # TODO: flask might have http code constants.
        return custom_error("Resource not found.", 404)

    # TODO: I'm ignoring the case where actor has >1 entries.
    # This should not happen but we should probably handle it
    # regardless.

    return jsonify(actor.to_dict())


@app.route("/crew", methods=["GET"])
def get_crews():
    crew: list[Crew] = Crew.query.limit(50).all()
    crew_list = []
    for c in crew:
        crew_list += [c.to_dict()]
    return jsonify(crew_list)


@app.route("/crew/<int:id>", methods=["GET"])
def get_crew_resource(id):
    crew: list[Crew] = Crew.query.filter(Crew.credit_id == id)
    try:
        crew = crew[0]
    except IndexError:
        # TODO: flask might have http code constants.
        return custom_error("Resource not found.", 404)

    # TODO: I'm ignoring the case where crew has >1 entries.
    # This should not happen but we should probably handle it
    # regardless.

    return jsonify(crew.to_dict())


if __name__ == "__main__":
    app.run(debug=True)
