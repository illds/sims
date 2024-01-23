from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.houses.forms import HouseForm
from sims.models import House, HouseType, Family, VehicleType, Color, Vehicle
from flask_login import login_required

from sims.vehicles.forms import VehicleForm

vehicles = Blueprint('vehicles', __name__)


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
    return render_template('vehicles/vehicle.html', vehicle=vehicle)


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
        form.plate.data = vehicle.plate
        form.type.data = vehicle.type
        form.color.data = vehicle.color
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


# @vehicles.route("/house/<int:house_id>/add_family/<int:family_id>", methods=['POST', 'GET'])
# @login_required
# def house_add_family(house_id, family_id):
#     house = House.query.get_or_404(house_id)
#     family = Family.query.get_or_404(family_id)
#
#     house.family_id = family.id
#     db.session.commit()
#     flash('Family has been added!', 'success')
#     return redirect(url_for('vehicles.house', house_id=house.id))
#
#
# @vehicles.route("/house/<int:house_id>/leave_family", methods=['POST'])
# @login_required
# def house_leave_family(house_id):
#     house = House.query.get_or_404(house_id)
#     house.family_id = None
#
#     db.session.commit()
#     flash('Family has been deleted!', 'success')
#     return redirect(url_for('vehicles.house', house_id=house.id))
