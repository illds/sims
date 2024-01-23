from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.houses.forms import HouseForm
from sims.models import House, HouseType
from flask_login import login_required

houses = Blueprint('houses', __name__)


@houses.route("/house/new", methods=['GET', 'POST'])
@login_required
def new_house():
    form = HouseForm()
    if form.validate_on_submit():
        try:
            house_type = HouseType(form.type.data)
        except KeyError:
            flash('Invalid house type', 'danger')
            return redirect(url_for('main.home'))
        house = House(type=house_type,
                      room_number=form.room_number.data, floor_number=form.floor_number.data,
                      x_coordinate=form.x_coordinate.data, y_coordinate=form.y_coordinate.data)
        db.session.add(house)
        db.session.commit()
        flash('House has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('houses/create_house.html', title='New house',
                           form=form, legend='New House')


@houses.route("/house/<int:house_id>")
def house(house_id):
    house = House.query.get_or_404(house_id)
    return render_template('houses/house.html', house=house)


@houses.route("/house/<int:house_id>/update", methods=['GET', 'POST'])
@login_required
def update_house(house_id):
    house = House.query.get_or_404(house_id)
    # if house.author != current_user:
    # abort(403)
    form = HouseForm()
    if form.validate_on_submit():
        try:
            house_type = HouseType(form.type.data)
        except KeyError:
            flash('Invalid house type', 'danger')
            return redirect(url_for('main.home'))
        house.type = house_type
        house.room_number = form.room_number.data
        house.floor_number = form.floor_number.data
        house.x_coordinate = form.x_coordinate.data
        house.y_coordinate = form.y_coordinate.data
        db.session.commit()
        flash('Your house has been updated!', 'success')
        return redirect(url_for('houses.house', house_id=house.id))
    elif request.method == 'GET':
        form.type.data = house.type
        form.room_number.data = house.room_number
        form.floor_number.data = house.floor_number
        form.x_coordinate.data = house.x_coordinate
        form.y_coordinate.data = house.y_coordinate
    return render_template('houses/create_house.html', form=form, legend='Update House', title='Update House')


@houses.route("/house/<int:house_id>/delete", methods=['POST'])
@login_required
def delete_house(house_id):
    house = House.query.get_or_404(house_id)

    db.session.delete(house)
    db.session.commit()
    flash('House has been deleted!', 'success')
    return redirect(url_for('main.home'))
