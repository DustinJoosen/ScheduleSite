from typing import Tuple

from flask import Flask, render_template, redirect
from werkzeug import Response
from datetime import datetime

from apiclient.settings import Settings
from apiclient.client import Client

app: Flask = Flask(__name__)

Settings.load()


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/schedule')
@app.route('/rooster')
def schedule() -> Response | str:
    client: Client = Client(min_date="2022-11-21T00:00:00Z", max_date="2022-11-25T00:00:00Z", show_zelfstudie=False)
    schedule: dict = client.request_schedule()

    if schedule is None:
        return redirect('/error')

    # Get the current day, and truncate the time.
    # This is because the api gives the roosterdatum like this.
    today = datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)

    return render_template(
        "schedule.html",
        class_name=Settings.CLASS_NAME,
        schedule=schedule,
        today=today
    )


if __name__ == "__main__":
    app.run(debug=True)
