from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import web, db
from app.models import User
from app.forms import LoginForm, RegistrationForm

@web.route('/')
@login_required
def entrance():
    return render_template("entrance.html")

@web.route('/home')
@login_required
def home():
    posts = [
        {'author' : 'Ronald', 'body' : 'hmm feels so stressed from work. Let\'s make UCS hihihi'},
        {'author' : 'Bivan', 'body' : 'Aigoo what other nonsense UCS u wanna come up with this time leh..'},
        {'author' : 'Aubrey', 'body' : 'OMG please no more, Senpai'},
        {'author' : 'EL', 'body' : 'walao cannot anymore lah, my body really hurts now'},
        {'author' : 'Kelvin', 'body' : 'NICEEE finally some display of passion'},
        {'author' : 'Sky', 'body' : 'okay sure.. do all you want!!'},
        {'author' : 'Zhiquan', 'body' : 'Eeeehhh???'}
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

@web.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    posts = [
        {"author" : user, "body" : "Testing #1"},
        {"author" : user, "body" : "Testing #2"}
    ]
    return render_template("user.html", user = user, posts = posts)

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

@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))