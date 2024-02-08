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

    Human.query.filter_by(job_id=job.id).update({Human.job_id: None})

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
