from flask import render_template, flash, redirect, url_for
from app import web
from app.forms import LoginForm

@web.route('/')
def entrance():
    user = {'username' : "PIUNoobs"}
    return render_template("entrance.html", user = user)

@web.route('/home')
def home():
    user = {'username' : "PIUNoobs"}
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
        user = user,
        posts = posts
    )

@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user = {}, remember_me = {}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home'))
    return render_template("login.html", title = "Sign In", form = form)