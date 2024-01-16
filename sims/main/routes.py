from flask import Blueprint, render_template
from sims.models import Human, House

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    humans_query = Human.query.all()
    humans = []
    for human in humans_query:
        humans.append({
            "id": human.id, "name": human.name,
            "surname": human.surname, "age": human.age,
            "x": human.x_coordinate, "y": human.y_coordinate
        })

    houses_query = House.query.all()
    houses = []
    for house in houses_query:
        houses.append({
            "id": house.id, "owner_family": house.owner_family,
            "room_number": house.room_number, "floor_number": house.floor_number,
            "x": house.x_coordinate, "y": house.y_coordinate
        })

    return render_template('home.html', humans=humans, houses=houses)


@main.route("/about")
def about():
    return render_template('about.html', title='About')