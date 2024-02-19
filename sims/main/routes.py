from flask import Blueprint, render_template
from sims.models import Human, House, Pet, Vehicle

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    humans_query = Human.query.all()
    humans = []
    for human in humans_query:
        humans.append({
            "id": human.id, "name": human.name,
            "surname": human.surname, "gender": human.gender, "age": human.age,
            "x": human.x_coordinate, "y": human.y_coordinate
        })

    pets_query = Pet.query.all()
    pets = []
    for pet in pets_query:
        pets.append({
            "id": pet.id, "name": pet.name,
            "type": pet.type, "gender": pet.gender, "age": pet.age,
            "x": pet.x_coordinate, "y": pet.y_coordinate
        })

    houses_query = House.query.all()
    houses = []
    for house in houses_query:
        houses.append({
            "id": house.id,
            "room_number": house.room_number, "floor_number": house.floor_number,
            "x": house.x_coordinate, "y": house.y_coordinate
        })

    vehicles_query = Vehicle.query.all()
    vehicles = []
    for vehicle in vehicles_query:
        vehicles.append({
            "id": vehicle.id, "plate": vehicle.plate,
            "type": vehicle.type, "color": vehicle.color,
            "x": vehicle.x_coordinate, "y": vehicle.y_coordinate
        })

    return render_template('home.html', humans=humans, houses=houses, pets=pets, vehicles=vehicles)