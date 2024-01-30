from flask import render_template, url_for, flash, redirect, request, Blueprint
from sims import db
from sims.families.forms import FamilyForm
from sims.jobs.forms import JobForm
from sims.models import Human, Family, Pet, Jobs
from flask_login import login_required

jobs = Blueprint('jobs', __name__)


@jobs.route("/job/new", methods=['GET', 'POST'])
@login_required
def new_job():
    form = JobForm()

    if form.validate_on_submit():
        job = Jobs(name=form.name.data, salary=form.salary.data)

        db.session.add(job)
        db.session.commit()

        flash('Job has been created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('jobs/create_job.html', title='New Job',
                           form=form, legend='New Job')


@jobs.route("/job/<int:job_id>")
def job(job_id):
    job = Jobs.query.get_or_404(job_id)

    return render_template('jobs/job.html', job=job)


@jobs.route("/job/<int:job_id>/update", methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Jobs.query.get_or_404(job_id)

    form = JobForm()
    if form.validate_on_submit():
        job.name = form.name.data
        job.salary = form.salary.data
        db.session.commit()
        flash('Your job has been updated!', 'success')
        return redirect(url_for('jobs.job', job_id=job.id))
    elif request.method == 'GET':
        form.name.data = job.name
        form.salary.data = job.salary

    return render_template('jobs/create_job.html', form=form, legend='Update Job', title='Update Job')


@jobs.route("/job/<int:job_id>/delete", methods=['POST'])
@login_required
def delete_job(job_id):
    job = Jobs.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()
    flash('Job has been deleted!', 'success')
    return redirect(url_for('main.home'))


@jobs.route("/jobs")
@login_required
def all_jobs():
    jobs = Jobs.query.all()
    return render_template('jobs/jobs.html', title='List of jobs',
                           jobs=jobs)
#
#
# @jobs.route("/jobs/human/<int:human_id>", methods=['GET', 'POST'])
# @login_required
# def jobs_human(human_id):
#     jobs = Family.query.all()
#     return render_template('jobs/jobs_human.html', title='List of jobs',
#                            jobs=jobs, human_id=human_id)
#
#
# @jobs.route("/jobs/pet/<int:pet_id>", methods=['GET', 'POST'])
# @login_required
# def jobs_pet(pet_id):
#     jobs = Family.query.all()
#     return render_template('jobs/jobs_pet.html', title='List of jobs',
#                            jobs=jobs, pet_id=pet_id)
#
#
# @jobs.route("/jobs/house/<int:house_id>", methods=['GET', 'POST'])
# @login_required
# def jobs_house(house_id):
#     jobs = Family.query.all()
#     return render_template('jobs/jobs_house.html', title='List of jobs',
#                            jobs=jobs, house_id=house_id)
#
#
# @jobs.route("/family/human_join/<int:family_id>/<int:human_id>", methods=['GET', 'POST'])
# @login_required
# def human_join_family(family_id, human_id):
#     human = Human.query.get_or_404(human_id)
#     family = Family.query.get_or_404(family_id)
#
#     if human.surname != family.name:
#         flash(f'{human.name} doesn\'t have {family.name} surname.', 'danger')
#         return redirect(url_for('humans.human', human_id=human.id))
#
#
#     human.family_id = family_id
#     db.session.commit()
#
#     flash(f'{human.name} has joined {family.name} family!', 'success')
#     return redirect(url_for('humans.human', human_id=human.id))
#
#
# @jobs.route("/family/pet_join/<int:family_id>/<int:pet_id>", methods=['GET', 'POST'])
# @login_required
# def pet_join_family(family_id, pet_id):
#     pet = Pet.query.get_or_404(pet_id)
#     family = Family.query.get_or_404(family_id)
#
#     pet.family_id = family_id
#     db.session.commit()
#
#     flash(f'{pet.name} has joined {family.name} family!', 'success')
#     return redirect(url_for('pets.pet', pet_id=pet.id))
#
#
