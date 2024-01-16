from flask import Blueprint, render_template
from sims.models import Human

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    humans = Human.query.all()
    entities = []
    for human in humans:
        entities.append({
            "id": human.id, "name": human.name,
            "surname": human.surname, "age": human.age,
            "x": human.x_coordinate, "y": human.y_coordinate
        })

    return render_template('home.html', entities=entities)


@main.route("/about")
def about():
    return render_template('about.html', title='About')