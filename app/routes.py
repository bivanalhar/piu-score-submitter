from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import web, db
from app.models import User, Score, Chart
from app.forms import LoginForm, RegistrationForm, EditProfileForm, SubmissionForm1

from datetime import datetime

import git

events = {
    "E1" : "18 Again"
}

charts = {
    "1" : "Papa Gonzales",
    "2" : "First Love",
    "3" : "Blazing",
    "4" : "Jam O'Beat"
}

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
        {'comp_name' : '18 Again', 'code' : "E1"}
    ]
    return render_template(
        "main.html",
        posts = posts
    )

@web.route('/chart/<event>')
def chart(event):
    charts = Chart.query.filter_by(event = event).all()
    chartArray = []

    for chart in charts:
        chartObj = {}
        chartObj["id"] = chart.id
        chartObj["chart"] = chart.chart

        chartArray.append(chartObj)

    return jsonify({'charts' : chartArray})

@web.route('/comp/<event>')
@login_required
def comp(event):
    usernames = [user.username for user in User.query.all()]
    charts = sorted([chart.chart for chart in Chart.query.filter_by(event = event).all()])

    listScore = []
    for user in usernames:
        scores = Score.query.filter_by(event = event, username = user).all()
        if len(scores) == 0:
            continue

        userScores = 0.0
        for chart in charts:
            scores_c = [score for score in scores if score.chart == chart]
            if len(scores_c) > 0:
                maxScore = max(scores_c, key = lambda p: p.finalScore)
                userScores += maxScore.finalScore

        listScore.append(
            {"username" : user, "totalScore" : userScores}
        )
    if len(listScore) == 0:
        final = None
    else:
        final = sorted(listScore, key = lambda p: p["totalScore"], reverse = True)
        for i in range(len(final)):
            final[i]["rank"] = i + 1
    return render_template("comp.html", title = "Competition Details", event = event, final = final)

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

@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))

@web.route('/score', methods=['GET', 'POST'])
@login_required
def score():
    form = SubmissionForm1(current_user.username)

    form.chart.choices = [(chart.id, chart.chart) for chart in Chart.query.filter_by(event = "E1").all()]
    if form.validate_on_submit():
        score = Score(username = current_user.username, perfect = form.perfect.data, great = form.great.data,
            event = form.event.data, good = form.good.data, bad = form.bad.data, miss = form.miss.data,
            chart = charts[form.chart.data])
        score.set_totalScore(form.perfect.data, form.great.data, form.good.data,
            form.bad.data, form.miss.data)
        db.session.add(score)
        db.session.commit()

        flash("Congratulations, {}, for you have successfully uploaded your score".format(current_user.username))
        return redirect(url_for('user', username=current_user.username))
    return render_template("score.html", title = "Score Submission", form = form, username = current_user.username)

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

@web.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    scores = Score.query.filter_by(username = username).all()

    top_scores = []

    if len(scores) > 0:
        all_charts = sorted(set(s.chart for s in scores))
        all_events = sorted(set(s.event for s in scores))
        for event in all_events:
            for chart in all_charts:
                score_events = [s for s in scores if s.event == event and s.chart == chart]
                details = max(score_events, key = lambda p: p.finalScore)
                top_scores.append(details)

    if len(top_scores) == 0:
        top_scores = None

    return render_template("user.html", user = user, top_scores = top_scores, scores = scores, events_map = events)

@web.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('mysite')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

@web.route('/delete_score/<scoreid>')
@login_required
def delete_score(scoreid):
    score = Score.query.filter_by(id = scoreid).first_or_404()
    db.session.delete(score)
    db.session.commit()

    flash("Score with ID {} has been deleted.".format(scoreid))
    return redirect(url_for('user', username=current_user.username))
