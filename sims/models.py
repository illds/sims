from datetime import datetime
from sims import db, login_manager
from flask_login import UserMixin


# To create db with models:
# from project import app, db
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
    # posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"





class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False, default=0)
    y_coordinate = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Human('{self.name}', '{self.id}', x={self.x_coordinate}, y={self.y_coordinate})"


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_family = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.Integer, nullable=False, default=1)
    floor_number = db.Column(db.Integer, nullable=False, default=1)
    x_coordinate = db.Column(db.Integer, nullable=False, default=0)
    y_coordinate = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"House('{self.owner_family}', '{self.id}', x={self.x_coordinate}, y={self.y_coordinate})"


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False, default=0)
    y_coordinate = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Human('{self.name}', '{self.id}', x={self.x_coordinate}, y={self.y_coordinate})"
