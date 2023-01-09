from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

import sqlite3

app = Flask(__name__)

db_name = "movies.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = "movies"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    runtime = db.Column(db.Integer, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    title = db.Column(db.Text, nullable=True)
    budget = db.Column(db.Integer, nullable=True)


class Actor(db.Model):
    __tablename__ = "actor_credits"
    __table_args__ = {'extend_existing': True}
    credit_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    character = db.Column(db.Text)


class Crew(db.Model):
    __tablename__ = "crew_credits"
    __table_args__ = {'extend_existing': True}
    credit_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    department = db.Column(db.Text)
    job = db.Column(db.Text)


@app.route("/")
def index():
    return "Server Works!"


@app.route("/movies", methods=["GET", "POST"])
def movies():
    movies = Movie.query.order_by(Movie.title).all()
    movie_text = "<ul>"
    for movie in movies:
        movie_text += "<li>" + movie.title + ", " + movie.release_date + "</li>"
        movie_text += "</ul>"
    return movie_text


@app.route("/actors", methods=["GET", "POST"])
def actors():
    return "actors"


@app.route("/crew", methods=["GET", "POST"])
def crew():
    return "crews"


if __name__ == "__main__":
    app.run(debug=True)
