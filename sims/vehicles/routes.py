from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.models import VehicleType, Color, Vehicle, Human
from flask_login import login_required

from sims.vehicles.forms import VehicleForm, VehicleColorForm

vehicles = Blueprint('vehicles', __name__)

ADULT_AGE = 18

@vehicles.route("/vehicle/new", methods=['GET', 'POST'])
@login_required
def new_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        try:
            vehicle_type = VehicleType(form.type.data)
            color = Color(form.color.data)
        except KeyError:
            flash('Invalid vehicle or color type', 'danger')
            return redirect(url_for('main.home'))
        vehicle = Vehicle(plate=form.plate.data, type=vehicle_type, color=color,
                          x_coordinate=form.x_coordinate.data, y_coordinate=form.y_coordinate.data)
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('vehicles/create_vehicle.html', title='New vehicle',
                           form=form, legend='New Vehicle')


@vehicles.route("/vehicle/<int:vehicle_id>")
def vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    human = Human.query.get(vehicle.human_id)
    return render_template('vehicles/vehicle.html', vehicle=vehicle, human=human)


@vehicles.route("/vehicle/<int:vehicle_id>/update", methods=['GET', 'POST'])
@login_required
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    form = VehicleForm()
    if form.validate_on_submit():
        try:
            vehicle_type = VehicleType(form.type.data)
            color = Color(form.color.data)
        except KeyError:
            flash('Invalid vehicle type', 'danger')
            return redirect(url_for('main.home'))
        vehicle.plate = form.plate.data
        vehicle.type = vehicle_type
        vehicle.color = color
        vehicle.x_coordinate = form.x_coordinate.data
        vehicle.y_coordinate = form.y_coordinate.data
        db.session.commit()
        flash('Your vehicle has been updated!', 'success')
        return redirect(url_for('vehicles.vehicle', vehicle_id=vehicle.id))
    elif request.method == 'GET':
        form.type.default = vehicle.type.value
        form.color.default = vehicle.color.value
        form.process()

        form.plate.data = vehicle.plate
        form.x_coordinate.data = vehicle.x_coordinate
        form.y_coordinate.data = vehicle.y_coordinate
    return render_template('vehicles/create_vehicle.html', form=form, legend='Update Vehicle', title='Update Vehicle')


@vehicles.route("/vehicle/<int:vehicle_id>/delete", methods=['POST'])
@login_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    db.session.delete(vehicle)
    db.session.commit()
    flash('Vehicle has been deleted!', 'success')
    return redirect(url_for('main.home'))


def is_adult(human):
    return not human.age < ADULT_AGE


@vehicles.route("/vehicle/<int:vehicle_id>/add_human/<int:human_id>", methods=['POST', 'GET'])
@login_required
def vehicle_add_human(vehicle_id, human_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    human = Human.query.get_or_404(human_id)

    if not is_adult(human):
        flash(f'{human.name} is not adult!', 'danger')
        return redirect(url_for('vehicles.vehicle', vehicle_id=vehicle.id))

    vehicle.human_id = human.id
    db.session.commit()
    flash('Owner has been added!', 'success')
    return redirect(url_for('vehicles.vehicle', vehicle_id=vehicle.id))


@vehicles.route("/vehicle/<int:vehicle_id>/leave_human", methods=['POST'])
@login_required
def vehicle_delete_human(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    vehicle.human_id = None

    db.session.commit()
    flash('Human has been deleted!', 'success')
    return redirect(url_for('vehicles.vehicle', vehicle_id=vehicle.id))


@vehicles.route("/vehicle/<int:vehicle_id>/change_color", methods=['GET', 'POST'])
def change_color(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    form = VehicleColorForm(color=2)
    if form.validate_on_submit():
        try:
            color = Color(form.color.data)
        except KeyError:
            flash('Invalid color type', 'danger')
            return redirect(url_for('main.home'))

        vehicle.color = color
        db.session.commit()
        flash('Color has been changed!', 'success')
        return redirect(url_for('vehicles.vehicle', vehicle_id=vehicle.id))
    elif request.method == 'GET':
        form.color.default = vehicle.color.value
        form.process()


    return render_template('vehicles/change_color.html', form=form, legend='Change Color', title='Update Color')
