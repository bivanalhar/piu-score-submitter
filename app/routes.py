from flask import render_template, flash, redirect, url_for
from app import web
from app.forms import LoginForm

def base(user1, user2, msg, address):
    user = {'username' : user1}
    posts = [
        {'author' : user2, 'body' : msg},
        {'author' : 'Aubrey', 'body' : 'OMG please no more, Senpai'},
        {'author' : 'EL', 'body' : 'walao cannot anymore lah, my body really hurts now'},
        {'author' : 'Kelvin', 'body' : 'NICEEE finally some display of passion'},
        {'author' : 'Sky', 'body' : 'okay sure.. do all you want!!'},
        {'author' : 'Zhiquan', 'body' : 'Eeeehhh???'}
    ]
    return render_template(
        address, 
        user = user,
        posts = posts
    )

@web.route('/')
def index():
    user = {'username' : "PIUNoobs"}
    return render_template("main.html", user = user)

@web.route('/main')
def main():
    return base(
        user1 = "Ronald",
        user2 = "Bivan",
        msg = 'Aigoo why such nonsense UCS again leh..',
        address = "main1.html"
    )

@web.route('/home')
def home():
    return base(
        user1 = "Bivan",
        user2 = "Ronald",
        msg = 'Teehee lemme torture you all with my UCS',
        address = "main2.html"
    )

@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user = {}, remember_me = {}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('main'))
    return render_template("login.html", title = "Sign In", form = form)