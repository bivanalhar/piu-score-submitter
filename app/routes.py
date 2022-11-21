from app import web

@web.route('/')
@web.route('/index')
def index():
    return "Welcome to the PIU Score Submitter website"