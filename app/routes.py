from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import web, db
from app.models import User, Score
from app.forms import LoginForm, RegistrationForm, EditProfileForm, SubmissionForm1

from datetime import datetime

@web.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@web.route('/')
@web.route('/home')
@login_required
def home():
    posts = [
        {'comp_name' : 'Let\'s have a trial competition', 'id' : 1},
        {'comp_name' : 'The real UCS will gonna torture you so badly', 'id' : 2}
    ]
    return render_template(
        "main.html", 
        posts = posts
    )

@web.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None:
            flash("Invalid username")
            return redirect(url_for("login"))
        
        if not user.check_password(form.password.data):
            flash("this username has mismatch password")
            return redirect(url_for("login"))
        
        login_user(user, remember = form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")
        return redirect(next_page)
    return render_template("login.html", title = "Sign In", form = form)

@web.route('/score', methods=['GET', 'POST'])
@login_required
def score():
    form = SubmissionForm1(current_user.username)
    if form.validate_on_submit():
        score = Score(username = form.username.data, perfect = form.perfect.data, great = form.great.data,
            event = form.event.data, good = form.good.data, bad = form.bad.data, miss = form.miss.data)
        score.set_totalScore(form.perfect.data, form.great.data, form.good.data, 
            form.bad.data, form.miss.data)
        db.session.add(score)
        db.session.commit()

        flash("Congratulations, {}, for you have successfully uploaded your score".format(form.username.data))
        return redirect(url_for('user', username=current_user.username))
    return render_template("score.html", title = "Score Submission", form = form)

@web.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    scores = Score.query.filter_by(username = username).all()

    all_scores = []

    if len(scores) > 0:
        all_events = sorted(set(s.event for s in scores))
        for event in all_events:
            score_events = [s for s in scores if s.event == event]
            details = max(score_events, key = lambda p: p.finalScore)
            all_scores.append(details)
    
    if len(all_scores) == 0:
        all_scores = None
            
    return render_template("user.html", user = user, all_scores = all_scores)

@web.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Congratulations, {}, for now you have been officially registered".format(form.username.data))
        return redirect(url_for('login'))
    return render_template("signup.html", title = "Sign Up", form = form)

@web.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash("Your changes has been saved")
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title = "Edit Profile", form = form)

@web.route('/comp/<variable>')
@login_required
def comp(variable):
    return render_template("comp.html", title = "Competition Details", var = variable)

@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))