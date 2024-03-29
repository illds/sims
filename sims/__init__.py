from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sims.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from sims.main.routes import main
    from sims.users.routes import users
    from sims.humans.routes import humans
    from sims.pets.routes import pets
    from sims.families.routes import families
    from sims.houses.routes import houses
    from sims.vehicles.routes import vehicles
    from sims.jobs.routes import jobs
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(humans)
    app.register_blueprint(pets)
    app.register_blueprint(families)
    app.register_blueprint(houses)
    app.register_blueprint(vehicles)
    app.register_blueprint(jobs)

    return app
