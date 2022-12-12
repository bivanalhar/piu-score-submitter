from app import web, db
from app.models import User, Score, Chart

@web.shell_context_processor
def make_shell_context():
    return {"db" : db, "user" : User, "score" : Score, "chart" : Chart}