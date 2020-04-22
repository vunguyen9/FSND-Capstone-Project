import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine, Table


database_name = "capstone"
database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', database_name)
# database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    new_movie = Movie(title='King Kong', release_date='12/2019')
    new_movie.insert()
    new_actor = Actor(name='John', age=25, gender='male')
    new_actor.insert()


Association = db.Table(
                        'Association', db.Model.metadata,
                        Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                        Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
                    )


class Movie(db.Model):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)
    actors = db.relationship("Actor", secondary=Association, backref=db.backref('association', lazy='joined'))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

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
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(db.Model):
    __tablename__ = 'actor'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)

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
