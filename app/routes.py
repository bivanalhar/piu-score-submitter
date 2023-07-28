from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import web, db
from app.config import charts, current_event, events
from app.models import User, Score, Chart
from app.forms import LoginForm, RegistrationForm, EditProfileForm, SubmissionForm1, CommaSeparatedUserInputForm, IpptCalculatorForm
from app.ippt_calculator import calculate_ippt_score, categories

from datetime import datetime

import git, random

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
        {'comp_name' : '18 Again', 'code' : "E1", 'status': 0},
        {'comp_name' : 'Oriental Sounds?', 'code' : "E2", 'status': 0},
        {'comp_name' : 'Mini-Tourney 2', 'code' : "MT2", 'status': 0},
        {'comp_name': 'IPPT', 'code': "E3", 'status': 0},
        {'comp_name': 'Mini-Challenge #9', 'code': "E4", 'status': 0},
        {'comp_name': 'Mini-Challenge #10', 'code': "E5", 'status': 1},
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
    users = [user for user in User.query.all()]

    listScore = []
    for user in users:
        scores = Score.query.filter_by(event = event, username = user.username).all()

        if len(scores) == 0:
            continue

        distinct_set_number = set()
        for score in scores:
            distinct_set_number.add(score.setNumber)

        max_total_set_score = 0
        for set_number in distinct_set_number:
            submissions_in_set = [s for s in scores if s.setNumber == set_number]

            top_songs_in_set = []
            all_charts = sorted(set(s.chart for s in submissions_in_set))
            all_events = sorted(set(s.event for s in submissions_in_set))
            for event in all_events:
                for chart in all_charts:
                    score_events = [s for s in submissions_in_set if s.event == event and s.chart == chart]
                    details = max(score_events, key = lambda p: p.finalScore)
                    # Populate IPPT score for the specified event
                    title_enum = getattr(user, "title", 0)
                    if event == "E3" and title_enum is not None and title_enum != 0:
                        stn_enum = 2 if chart == "Baroque Virus Full Song S21" else 1  # ref: config.py
                        details.ippt_points = calculate_ippt_score(details.finalScore, title_enum, stn_enum)
                    top_songs_in_set.append(details)

            total_set_score = 0
            for submission in top_songs_in_set:
                # IPPT score has a greater priority than EX-Score
                # Only populated for IPPT event, so normal event will not have this field
                try:
                    total_set_score += submission.ippt_points
                except:
                    total_set_score += submission.finalScore

            if total_set_score > max_total_set_score:
                max_total_set_score = total_set_score

        listScore.append(
            {"username" : user.username, "totalScore" : max_total_set_score}
        )
    if len(listScore) == 0:
        final = None
    else:
        final = sorted(listScore, key = lambda p: p["totalScore"], reverse = True)
        for i in range(len(final)):
            final[i]["rank"] = i + 1
    return render_template("comp" + event + ".html", title = "Competition Details", event = event, final = final)

@web.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.title = form.title.data
        db.session.commit()

        flash("Your changes has been saved")
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form = EditProfileForm(current_user.username, title=getattr(current_user, "title", 0))
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

    form.chart.choices = [(chart.id, chart.chart) for chart in Chart.query.filter_by(event = current_event).all()]
    if form.validate_on_submit():
        score = Score(username = current_user.username, perfect = form.perfect.data, great = form.great.data,
            event = form.event.data, good = form.good.data, bad = form.bad.data, miss = form.miss.data,
            chart = charts[form.chart.data], setNumber = form.set_number.data)
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
    title = categories[user.title] if user.title else None
    all_scores = Score.query.filter_by(username = username).all()
    event_scores = Score.query.filter_by(username = username, event = current_event).all()

    top_scores = []
    max_total_set_score = 0

    if len(event_scores) > 0:
        distinct_set_number = set()
        for score in event_scores:
            distinct_set_number.add(score.setNumber)

        set_to_submission_dict = {}
        max_set_number = 0

        for set_number in distinct_set_number:
            submissions_in_set = [s for s in event_scores if s.setNumber == set_number]

            top_songs_in_set = []
            all_charts = sorted(set(s.chart for s in submissions_in_set))
            all_events = sorted(set(s.event for s in submissions_in_set))
            for event in all_events:
                for chart in all_charts:
                    score_events = [s for s in submissions_in_set if s.event == event and s.chart == chart]
                    details = max(score_events, key = lambda p: p.finalScore)
                    # Populate IPPT score for the specified event
                    title_enum = getattr(user, "title", 0)
                    if event == "E3" and title_enum is not None and title_enum != 0:
                        stn_enum = 2 if chart == "Baroque Virus Full Song S21" else 1 # ref: config.py
                        details.ippt_points = calculate_ippt_score(details.finalScore, title_enum, stn_enum)
                    top_songs_in_set.append(details)

            set_to_submission_dict[set_number] = top_songs_in_set
            total_set_score = 0
            for submission in top_songs_in_set:
                # IPPT score has a greater priority than EX-Score
                # Only populated for IPPT event, so normal event will not have this field
                try:
                    total_set_score += submission.ippt_points
                except:
                    total_set_score += submission.finalScore

            if total_set_score > max_total_set_score:
                max_total_set_score = total_set_score
                max_set_number = set_number

        top_scores.extend(set_to_submission_dict[max_set_number])

    if len(top_scores) == 0:
        top_scores = None

    return render_template("user.html", title = "Profile", user = user, top_scores = top_scores, max_set_score = max_total_set_score, scores = all_scores, events_map = events, piu_title = title)

@web.route('/pairer', methods=['GET', 'POST'])
def pairer():
    form = CommaSeparatedUserInputForm()
    if form.validate_on_submit():
        splitted = form.user_input.data.split(",")
        indexes = []
        for i in range(len(splitted)):
            indexes.append(i)
        random.shuffle(indexes)

        idx_to_name_map = {}
        for idx in range(len(indexes)):
            ele = indexes[idx]
            idx_to_name_map[ele] = splitted[idx]
        return render_template("pairer.html", form = form, number_of_items = len(indexes), idx_to_name_map = idx_to_name_map)
    return render_template("pairer.html", title = "Pairer", form = form)

@web.route('/randomiser', methods=['GET', 'POST'])
def randomiser():
    form = CommaSeparatedUserInputForm()
    if form.validate_on_submit():
        splitted = form.user_input.data.split(",")
        random_num = random.randint(0, len(splitted)-1)
        output = splitted[random_num]
        return render_template("randomiser.html", form = form, output = output)
    return render_template("randomiser.html", title = "Randomiser", form = form)

@web.route('/ippt_calc', methods=['GET', 'POST'])
def ippt_calc():
    form = IpptCalculatorForm()
    if form.validate_on_submit():
        score = calculate_ippt_score(form.ex_score.data, int(form.category.data), int(form.station.data))
        return render_template("ippt_calculator.html", form = form, score = score)
    return render_template("ippt_calculator.html", title = "IPPT Calculator", form = form)

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
