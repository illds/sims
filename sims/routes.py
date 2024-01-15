from flask import render_template, url_for, flash, redirect, request, jsonify
from sims import app, db, bcrypt
from sims.forms import RegistrationForm, LoginForm, HumanForm, UpdateAccountForm
from sims.models import User, Human
from flask_login import login_user, current_user, logout_user, login_required
import matplotlib.pyplot as plt
import os

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


# entities = [
#     {"id": 1, "type": "human", "x": 10, "y": 20},
#     {"id": 2, "type": "building", "x": 30, "y": 40},
#     # Добавьте другие сущности
# ]


@app.route('/')
@app.route('/home')
def home():
    humans = Human.query.all()
    entities = []
    for human in humans:
        entities.append({
            "id": human.id, "type": "human", "x": human.x_coordinate, "y": human.y_coordinate
        })

    return render_template('home.html', entities=entities)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


# @app.route('/api/entities')
# def get_entities():
#     return jsonify(entities)


@app.route("/human/new", methods=['GET', 'POST'])
@login_required
def new_human():
    form = HumanForm()
    if form.validate_on_submit():
        human = Human(name=form.name.data, surname=form.surname.data, age=form.age.data,
                      x_coordinate=form.x_coordinate.data, y_coordinate=form.y_coordinate.data)
        db.session.add(human)
        db.session.commit()
        flash('Human has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_human.html', title='New entity',
                           form=form, legend='New Post')


@app.route("/human/<int:human_id>")
def human(human_id):
    human = Human.query.get_or_404(human_id)
    return render_template('human.html', human=human)
