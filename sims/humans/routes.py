from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.humans.forms import HumanForm
from sims.models import Human, Family, Gender, Job
from flask_login import login_required

humans = Blueprint('humans', __name__)


@humans.route("/human/new", methods=['GET', 'POST'])
@login_required
def new_human():
    form = HumanForm()
    if form.validate_on_submit():
        try:
            job = Job(form.job.data)
            gender = Gender(form.gender.data)
        except KeyError:
            flash('Invalid gender or job type', 'danger')
            return redirect(url_for('main.home'))
        human = Human(name=form.name.data, surname=form.surname.data,
                      gender=gender, age=form.age.data, job=job,
                      x_coordinate=form.x_coordinate.data, y_coordinate=form.y_coordinate.data)
        db.session.add(human)
        db.session.commit()
        flash('Human has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('humans/create_human.html', title='New human',
                           form=form, legend='New Human')


@humans.route("/human/<int:human_id>")
def human(human_id):
    human = Human.query.get_or_404(human_id)
    family = Family.query.get(human.family_id)
    return render_template('humans/human.html', human=human, family=family)


@humans.route("/human/<int:human_id>/update", methods=['GET', 'POST'])
@login_required
def update_human(human_id):
    human = Human.query.get_or_404(human_id)

    form = HumanForm()
    if form.validate_on_submit():
        try:
            job = Job(form.job.data)
            gender = Gender(form.gender.data)
        except KeyError:
            flash('Invalid gender or job type', 'danger')
            return redirect(url_for('main.home'))
        human.name = form.name.data
        human.surname = form.surname.data
        human.gender = gender
        human.job = job
        human.age = form.age.data
        human.x_coordinate = form.x_coordinate.data
        human.y_coordinate = form.y_coordinate.data
        db.session.commit()
        flash('Your human has been updated!', 'success')
        return redirect(url_for('humans.human', human_id=human.id))
    elif request.method == 'GET':
        form.name.data = human.name
        form.surname.data = human.surname
        form.gender.data = human.gender
        form.job.data = human.job
        form.age.data = human.age
        form.x_coordinate.data = human.x_coordinate
        form.y_coordinate.data = human.y_coordinate
    return render_template('humans/create_human.html', form=form, legend='Update Human', title='Update Human')


@humans.route("/human/<int:human_id>/delete", methods=['POST'])
@login_required
def delete_human(human_id):
    human = Human.query.get_or_404(human_id)

    db.session.delete(human)
    db.session.commit()
    flash('Human has been deleted!', 'success')
    return redirect(url_for('main.home'))


@humans.route("/human/<int:human_id>/leave_family", methods=['POST'])
@login_required
def human_leave_family(human_id):
    human = Human.query.get_or_404(human_id)
    human.family_id = None

    db.session.commit()
    flash(f'{human.name} left the family!', 'success')
    return redirect(url_for('humans.human', human_id=human.id))