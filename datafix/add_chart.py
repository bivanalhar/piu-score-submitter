from app import web, db
from app.models import Chart

def main():
    # So that we don't need to pass web as an argument to every function
    web.app_context().push()

    # Request user to input event and chart
    event = input("Please input event, e.g. E3: ")
    chart = input("Please input chart, e.g. Follow Me D9 RS: ")
    c = Chart(event = event, chart = chart)

    # Add into the database
    db.session.add(c)
    db.session.commit()

    # Print last element to see if successfully inserted
    print(Chart.query.all()[-1])

if __name__ == "__main__":
    main()
