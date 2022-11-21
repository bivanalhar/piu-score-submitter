from flask import render_template
from app import web

@web.route('/')
@web.route('/home')
def index():
    user = {'username' : 'Bivan'}
    posts = [
        {'author' : 'Ronald', 'body' : 'Teehee lemme torture you all with my UCS'},
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