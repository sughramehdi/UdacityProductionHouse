import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

#database_path = os.environ.get('DATABASE_URL')
database_path = "postgres://oqbvrscqxtauxy:e136500eea05225b7f9c9188950e841a38ff81f73c5702e4b2a8222ad9521e0d@ec2-34-234-185-150.compute-1.amazonaws.com:5432/d54n3tq0r4q5r8"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.drop_all()
    db.create_all()


'''
Cast
'''

CastDetails = db.Table(
    'castdetails', db.Column(
        'id', db.Integer, autoincrement=True, primary_key=True), db.Column(
            'movie_id', db.Integer, db.ForeignKey('movies.id')), db.Column(
                'actor_id', db.Integer, db.ForeignKey('actors.id')))


'''
Actors

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    movies = db.relationship(
        'Movie', secondary=CastDetails,
        backref=db.backref('Actor'))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


'''
Movies

'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    releasedate = Column(String)
    actors = db.relationship(
        'Actor', secondary=CastDetails,
        backref=db.backref('Movie'))

    def __init__(self, name, releasedate):
        self.name = name
        self.releasedate = releasedate

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'releasedate': self.releasedate
        }


# postgresql - adjacent - 66890
