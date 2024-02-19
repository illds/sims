from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.humans.forms import HumanForm, HumanCoordinatesForm, HumanJobForm
from sims.models import Human, Family, Gender, Jobs
from flask_login import login_required

humans = Blueprint('humans', __name__)


@humans.route("/human/new", methods=['GET', 'POST'])
@login_required
def new_human():
    form = HumanForm()

    # Put all jobs from Job table to the form
    form.job.choices = [(job.id, job.name) for job in Jobs.query.all()]

    if form.validate_on_submit():
        try:
            # job = Job(form.job.data)
            gender = Gender(form.gender.data)
            job_id = int(form.job.data)
        except (KeyError, ValueError):
            flash('Invalid gender or job type', 'danger')
            return redirect(url_for('main.home'))

        human = Human(name=form.name.data, surname=form.surname.data,
                      gender=gender, age=form.age.data, job_id=job_id,
                      x_coordinate=form.x_coordinate.data, y_coordinate=form.y_coordinate.data)
        db.session.add(human)
        db.session.commit()
        flash('Human has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('humans/create_human.html', title='New Human',
                           form=form, legend='New Human')


@humans.route("/human/<int:human_id>")
def human(human_id):
    human = Human.query.get_or_404(human_id)
    family = Family.query.get(human.family_id)
    job = Jobs.query.get(human.job_id)
    return render_template('humans/human.html', human=human, family=family, job=job)


@humans.route("/human/<int:human_id>/update", methods=['GET', 'POST'])
@login_required
def update_human(human_id):
    human = Human.query.get_or_404(human_id)

    form = HumanForm()

    # Think of something smarter
    form.job.choices = [(job.id, job.name) for job in Jobs.query.all()]
    form.x_coordinate.data = human.x_coordinate
    form.y_coordinate.data = human.y_coordinate

    if form.validate_on_submit():
        try:
            gender = Gender(form.gender.data)
        except (KeyError, ValueError):
            flash('Invalid gender type', 'danger')
            return redirect(url_for('main.home'))

        human.name = form.name.data
        human.surname = form.surname.data
        human.gender = gender
        human.job_id = form.job.data
        human.age = form.age.data

        db.session.commit()
        flash('Your human has been updated!', 'success')
        return redirect(url_for('humans.human', human_id=human.id))
    elif request.method == 'GET':
        form.gender.default = human.gender.value
        form.process()

        form.name.data = human.name
        form.surname.data = human.surname
        form.age.data = human.age

    return render_template('humans/create_human.html', form=form, legend='Update Human',
                           title='Update Human', target='EDIT')


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


@humans.route("/humans/vehicle/<int:vehicle_id>", methods=['GET', 'POST'])
@login_required
def humans_vehicle(vehicle_id):
    humans = Human.query.all()
    return render_template('humans/humans_vehicle.html', title='List of Humans',
                           humans=humans, vehicle_id=vehicle_id)


@humans.route("/human/<int:human_id>/change_job", methods=['GET', 'POST'])
def change_job(human_id):
    human = Human.query.get_or_404(human_id)

    form = HumanJobForm()

    # Think of something smarter
    form.job.choices = [(job.id, job.name) for job in Jobs.query.all()]

    if form.validate_on_submit():
        human.job_id = form.job.data

        db.session.commit()
        flash('Job has been changed!', 'success')
        return redirect(url_for('humans.human', human_id=human.id))
    elif request.method == 'GET':
        job = Jobs.query.get(human.job_id)
        if job:
            form.job.default = job.id
            form.process()

    return render_template('humans/change_job.html', form=form, legend='Change Job',
                           title='Change Job', human=human)


@humans.route("/human/<int:human_id>/leave_job", methods=['POST'])
def leave_job(human_id):
    human = Human.query.get_or_404(human_id)
    human.job_id = None

    db.session.commit()
    flash(f'{human.name} left the job!', 'success')
    return redirect(url_for('humans.human', human_id=human.id))


@humans.route("/human/<int:human_id>/change_coordinates", methods=['GET', 'POST'])
def change_coordinates(human_id):
    human = Human.query.get_or_404(human_id)

    form = HumanCoordinatesForm()
    if form.validate_on_submit():
        human.x_coordinate = form.x_coordinate.data
        human.y_coordinate = form.y_coordinate.data

        flash('Coordinates have been changed!', 'success')
        return redirect(url_for('humans.human', human_id=human.id))
    elif request.method == 'GET':
        form.x_coordinate.data = human.x_coordinate
        form.y_coordinate.data = human.y_coordinate
    return render_template('humans/change_coordinates.html', form=form, legend='Change Coordinates',
                           title='Update Coordinates')
