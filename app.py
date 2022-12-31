from flask import Flask, render_template, redirect, request
from flask_caching import Cache
from werkzeug import Response
from datetime import datetime, timedelta
from settings.settings import Settings
from schedule.schedule import get_schedule

app: Flask = Flask(__name__)
cache: Cache = Cache(app, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp',
    'CACHE_DEFAULT_TIMEOUT': 600
})
cache.init_app(app)

Settings.load()


@app.route('/', methods=['GET'])
def schedule() -> Response | str:
    # Handle the 'show_zelfstudie'.
    show_zelfstudie: bool = False
    if request.args.get('show_zelfstudie') in ['true', 'yes']:
        show_zelfstudie = True

    # Get the schedule. Cache is applied.
    schedule = get_schedule(show_zelfstudie=show_zelfstudie, cache=cache)

    # Handle unexpected schedule output.
    if error_msg := schedule.get("error"):
        return redirect(f'/error?e={error_msg}')
    if schedule is None:
        return redirect('/error')

    return render_template(
        "schedule.html",
        class_name=Settings.CLASS_NAME,
        schedule=schedule,
        today=Settings.TODAY
    )


@app.route('/reload', methods=['GET'])
def reload() -> Response:
    Settings.load()
    return redirect('/')


@app.route('/set_week', methods=['GET'])
def set_week() -> Response:
    inc: int = int(request.args.get('inc'))

    # If you pick 'this week', set it to the current week. Otherwise, look at the current viewing date.
    if inc == 0:
        date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        date = Settings.VIEWING_DATE + timedelta(weeks=inc)

    Settings.VIEWING_DATE = date

    Settings.F_DAY_OF_WEEK = date - timedelta(days=date.weekday())
    Settings.L_DAY_OF_WEEK = Settings.F_DAY_OF_WEEK + timedelta(days=4)

    return redirect('/')


@app.route('/error', methods=['GET'])
def error() -> str:
    error: str = request.args.get("e")

    return render_template(
        'error.html',
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
