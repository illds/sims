from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.families.forms import FamilyForm
from sims.families.procedures import get_family_money, get_family_members
from sims.models import Human, Family, Pet, Jobs
from flask_login import login_required

families = Blueprint('families', __name__)


@families.route("/family/new", methods=['GET', 'POST'])
@login_required
def new_family():
    form = FamilyForm()

    if form.validate_on_submit():
        family = Family(name=form.name.data)

        db.session.add(family)
        db.session.commit()

        flash('Family has been created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('families/create_family.html', title='New Family',
                           form=form, legend='New Family')


def get_pets_in_family(family):
    # Получить всех членов семьи (питомцев)
    return Pet.query.filter_by(family_id=family.id).all()


@families.route("/family/<int:family_id>")
def family(family_id):
    family = Family.query.get_or_404(family_id)
    humans_in_family = get_family_members(family_id)
    pets_in_family = get_pets_in_family(family)
    return render_template('families/family.html', family=family,
                           humans_in_family=humans_in_family, pets_in_family=pets_in_family,
                           total_money=get_family_money(family_id))


@families.route("/family/<int:family_id>/update", methods=['GET', 'POST'])
@login_required
def update_family(family_id):
    family = Family.query.get_or_404(family_id)

    form = FamilyForm()
    if form.validate_on_submit():
        family.name = form.name.data
        db.session.commit()
        flash('Your family has been updated!', 'success')
        return redirect(url_for('families.family', family_id=family.id))
    elif request.method == 'GET':
        form.name.data = family.name

    return render_template('families/create_family.html', form=form, legend='Update Family', title='Update Family')


@families.route("/family/<int:family_id>/delete", methods=['POST'])
@login_required
def delete_family(family_id):
    family = Family.query.get_or_404(family_id)

    Pet.query.filter_by(family_id=family.id).update({Pet.family_id: None})
    Human.query.filter_by(family_id=family.id).update({Human.family_id: None})

    db.session.delete(family)
    db.session.commit()
    flash('Family has been deleted!', 'success')
    return redirect(url_for('main.home'))


@families.route("/families")
@login_required
def all_families():
    families = Family.query.all()
    return render_template('families/families.html', title='List of Families',
                           families=families)


@families.route("/families/human/<int:human_id>", methods=['GET', 'POST'])
@login_required
def families_human(human_id):
    families = Family.query.all()
    return render_template('families/families_human.html', title='List of Families',
                           families=families, human_id=human_id)


@families.route("/families/pet/<int:pet_id>", methods=['GET', 'POST'])
@login_required
def families_pet(pet_id):
    families = Family.query.all()
    return render_template('families/families_pet.html', title='List of Families',
                           families=families, pet_id=pet_id)


@families.route("/families/house/<int:house_id>", methods=['GET', 'POST'])
@login_required
def families_house(house_id):
    families = Family.query.all()
    return render_template('families/families_house.html', title='List of Families',
                           families=families, house_id=house_id)


@families.route("/family/human_join/<int:family_id>/<int:human_id>", methods=['GET', 'POST'])
@login_required
def human_join_family(family_id, human_id):
    human = Human.query.get_or_404(human_id)
    family = Family.query.get_or_404(family_id)

    if human.surname != family.name:
        flash(f'{human.name} doesn\'t have {family.name} surname.', 'danger')
        return redirect(url_for('humans.human', human_id=human.id))

    human.family_id = family_id
    db.session.commit()

    flash(f'{human.name} has joined {family.name} family!', 'success')
    return redirect(url_for('humans.human', human_id=human.id))


@families.route("/family/pet_join/<int:family_id>/<int:pet_id>", methods=['GET', 'POST'])
@login_required
def pet_join_family(family_id, pet_id):
    pet = Pet.query.get_or_404(pet_id)
    family = Family.query.get_or_404(family_id)

    pet.family_id = family_id
    db.session.commit()

    flash(f'{pet.name} has joined {family.name} family!', 'success')
    return redirect(url_for('pets.pet', pet_id=pet.id))
