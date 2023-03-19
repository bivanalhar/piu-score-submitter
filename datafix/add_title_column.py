from app import web
import sqlite3

def main():
    # So that we don't need to pass web as an argument to every function
    web.app_context().push()

    db = sqlite3.connect("../app.db")
    cursor = db.cursor()
    add_title = "ALTER TABLE user ADD COLUMN title INTEGER"
    cursor.execute(add_title)
    db.close()

if __name__ == "__main__":
    main()
