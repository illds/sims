from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.families.forms import FamilyForm
from sims.models import Human
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


@families.route("/family/<int:family_id>")
def family(family_id):
    family = Family.query.get_or_404(family_id)
    return render_template('families/Family.html', family=family)


@families.route("/family/<int:family_id>/update", methods=['GET', 'POST'])
@login_required
def update_family(family_id):
    family = Family.query.get_or_404(family_id)
    # if family.author != current_user:
        # abort(403)
    form = FamilyForm()
    if form.validate_on_submit():
        family.name = form.name.data
        family.surname = form.surname.data
        family.age = form.age.data
        family.x_coordinate = form.x_coordinate.data
        family.y_coordinate = form.y_coordinate.data
        db.session.commit()
        flash('Your family has been updated!', 'success')
        return redirect(url_for('families.family', family_id=family.id))
    elif request.method == 'GET':
        form.name.data = family.name
        form.surname.data = family.surname
        form.age.data = family.age
        form.x_coordinate.data = family.x_coordinate
        form.y_coordinate.data = family.y_coordinate
    return render_template('families/create_family.html', form=form, legend='Update Family', title='Update Family')


@families.route("/family/<int:family_id>/delete", methods=['POST'])
@login_required
def delete_family(family_id):
    family = Family.query.get_or_404(family_id)

    # if family.author != current_user:
    #     abort(403)

    db.session.delete(family)
    db.session.commit()
    flash('Human has been deleted!', 'success')
    return redirect(url_for('main.home'))