from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.pets.forms import PetForm
from sims.models import Pet, Family, PetType, Plumbob
from flask_login import login_required

pets = Blueprint('pets', __name__)

@pets.route("/pet/new", methods=['GET', 'POST'])
@login_required
def new_pet():
    form = PetForm()
    if form.validate_on_submit():
        try:
            pet_type = PetType(form.type.data)
        except KeyError:
            flash('Invalid pet type', 'danger')
            return redirect(url_for('main.home'))
        pet = Pet(name=form.name.data, type=pet_type, breed=form.breed.data, age=form.age.data,
                      x_coordinate=form.x_coordinate.data, y_coordinate=form.y_coordinate.data)
        db.session.add(pet)
        db.session.commit()
        flash('Pet has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('pets/create_pet.html', title='New Pet',
                           form=form, legend='New Pet')


@pets.route("/pet/<int:pet_id>")
def pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    family = Family.query.get(pet.family_id)
    return render_template('pets/pet.html', pet=pet, family=family)


@pets.route("/pet/<int:pet_id>/update", methods=['GET', 'POST'])
@login_required
def update_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)

    form = PetForm()
    if form.validate_on_submit():
        try:
            pet_type = PetType(form.type.data)
        except KeyError:
            flash('Invalid pet type', 'danger')
            return redirect(url_for('main.home'))
        pet.name = form.name.data
        pet.type = pet_type
        pet.breed = form.breed.data
        pet.age = form.age.data
        pet.x_coordinate = form.x_coordinate.data
        pet.y_coordinate = form.y_coordinate.data
        db.session.commit()
        flash('Your pet has been updated!', 'success')
        return redirect(url_for('pets.pet', pet_id=pet.id))
    elif request.method == 'GET':
        form.name.data = pet.name
        form.type.data = pet.type
        form.breed.data = pet.breed
        form.age.data = pet.age
        form.x_coordinate.data = pet.x_coordinate
        form.y_coordinate.data = pet.y_coordinate
    return render_template('pets/create_pet.html', form=form, legend='Update Pet', title='Update Pet')


@pets.route("/pet/<int:pet_id>/delete", methods=['POST'])
@login_required
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)

    db.session.delete(pet)
    db.session.commit()
    flash('Pet has been deleted!', 'success')
    return redirect(url_for('main.home'))