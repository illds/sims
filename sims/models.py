from datetime import datetime

from enum import Enum

from sims import db, login_manager
from flask_login import UserMixin


# To create db with models:
# from sims import create_app, db
# app = create_app()
# app.app_context().push()
# db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Plumbob(Enum):
    GREEN = 'Green'
    YELLOW = 'Yellow'
    ORANGE = 'Orange'
    RED = 'Red'


class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False, default=0)
    y_coordinate = db.Column(db.Integer, nullable=False, default=0)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    plumbob = db.Column(db.Enum(Plumbob), default=Plumbob.GREEN)

    def __repr__(self):
        return f"Human('{self.name}', '{self.id}', x={self.x_coordinate}, y={self.y_coordinate})"


class PetType(Enum):
    CAT = 'Cat'
    DOG = 'Dog'
    BIRD = 'Bird'
    FISH = 'Fish'
    PARROT = 'Parrot'


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(PetType), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False, default=0)
    y_coordinate = db.Column(db.Integer, nullable=False, default=0)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    plumbob = db.Column(db.Enum(Plumbob), default=Plumbob.GREEN)

    def __repr__(self):
        return f"Human('{self.name}', '{self.id}', x={self.x_coordinate}, y={self.y_coordinate})"


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.Integer, nullable=False, default=1)
    floor_number = db.Column(db.Integer, nullable=False, default=1)
    x_coordinate = db.Column(db.Integer, nullable=False, default=0)
    y_coordinate = db.Column(db.Integer, nullable=False, default=0)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))

    def __repr__(self):
        return f"House('{self.id}', family_id={self.family_id}, x={self.x_coordinate}, y={self.y_coordinate})"


class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Family(id={self.id}, name={self.name}, humans='{self.humans}', pets='{self.pets}')"
