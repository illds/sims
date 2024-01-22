from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.families.forms import FamilyForm
from sims.models import Human, Family
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
    return render_template('families/family.html', family=family)


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


@families.route("/families/<int:human_id>", methods=['GET', 'POST'])
@login_required
def list_families(human_id):
    families = Family.query.all()
    return render_template('families/families_human.html', title='List of Families',
                           families=families, human_id=human_id)


@families.route("/family/join/<int:family_id>/<int:human_id>", methods=['GET', 'POST'])
@login_required
def join_family(family_id, human_id):
    human = Human.query.get_or_404(human_id)
    family = Family.query.get_or_404(family_id)

    human.family_id = family_id
    db.session.commit()

    flash(f'{human.name} has joined {family.name}!', 'success')
    return redirect(url_for('humans.human', human_id=human.id))
