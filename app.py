from flask import Flask, render_template, redirect
from werkzeug import Response
from datetime import datetime
from settings.settings import Settings
from schedule.schedule import get_schedule

app: Flask = Flask(__name__)

Settings.load()


@app.route('/')
def schedule() -> Response | str:
    schedule: dict = get_schedule(show_zelfstudie=False)

    if schedule is None:
        return redirect('/error')

    return render_template(
        "schedule.html",
        class_name=Settings.CLASS_NAME,
        schedule=schedule,
        today=Settings.TODAY
    )


if __name__ == "__main__":
    app.run(debug=True)
