from app import web, db
from app.models import User, Post

@web.shell_context_processor
def make_shell_context():
    return {"db" : db, "user" : User, "post" : Post}