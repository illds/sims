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


class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    ATTACK_HELICOPTER = 'Attack Helicopter'


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)


class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False, default=0)
    y_coordinate = db.Column(db.Integer, nullable=False, default=0)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), default=0)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    plumbob = db.Column(db.Enum(Plumbob), default=Plumbob.GREEN)

    def __repr__(self):
        return f"Human('{self.name}', '{self.id}', x={self.x_coordinate}, y={self.y_coordinate})"


class PetType(Enum):
    CAT = 'Cat'
    DOG = 'Dog'
    HAMSTER = 'Hamster'
    FISH = 'Fish'
    PARROT = 'Parrot'


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(PetType), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False, default=0)
    y_coordinate = db.Column(db.Integer, nullable=False, default=0)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    plumbob = db.Column(db.Enum(Plumbob), default=Plumbob.GREEN)

    def __repr__(self):
        return f"Pet('{self.name}', '{self.id}', x={self.x_coordinate}, y={self.y_coordinate})"


class HouseType(Enum):
    APARTMENT = 'Apartment'
    SINGLE_FAMILY = 'Single-family'
    CONDO = 'Condo'


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(HouseType), nullable=False)
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


class VehicleType(Enum):
    CAR = 'Car'
    TRUCK = 'Truck'
    MOTORCYCLE = 'Motorcycle'
    BUS = 'Bus'


class Color(Enum):
    RED = 'Red'
    GREEN = 'Green'
    BLUE = 'Blue'
    YELLOW = 'Yellow'


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(30), nullable=False)
    type = db.Column(db.Enum(VehicleType), nullable=False)
    color = db.Column(db.Enum(Color), nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False, default=0)
    y_coordinate = db.Column(db.Integer, nullable=False, default=0)
    human_id = db.Column(db.Integer, db.ForeignKey('human.id'))

    def __repr__(self):
        return f"Car('{self.id}', human_id={self.human_id}, x={self.x_coordinate}, y={self.y_coordinate})"
