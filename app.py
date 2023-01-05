from flask import Flask, render_template, redirect, request
from flask_caching import Cache
from werkzeug import Response
from datetime import datetime, timedelta
from settings.settings import Settings
from schedule.schedule import get_schedule
from schedule.cookieencryption import substitution_encryption
from schedule.browsercookie import BrowserCookie
from json import dumps

app: Flask = Flask(__name__)
cache: Cache = Cache(app, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp',
    'CACHE_DEFAULT_TIMEOUT': 600
})
cache.init_app(app)


@app.route('/', methods=['GET'])
def schedule() -> Response | str:
    # Make sure the settings are already loaded.
    if not Settings.LOADED:
        try:
            Settings.load()
        except Exception as ex:
            print(ex)
            return redirect("/authenticate")

    # Handle the 'show_zelfstudie'.
    show_zelfstudie: bool = False
    if request.args.get('show_zelfstudie') in ['true', 'yes']:
        show_zelfstudie = True

    # Get the schedule. Cache is applied.
    schedule = get_schedule(show_zelfstudie=show_zelfstudie, cache=cache)

    # Handle unexpected schedule output.
    if (error_msg := schedule.get("error")) and error_msg == "schedule_is_none":
        return redirect('/authenticate')
    if schedule is None:
        return redirect('/error')

    print(BrowserCookie.get_mock_cookie())
    print(schedule)

    #TODO: load the schedule as json inside the javascript. THis can then be used to display the correct info on the schedule details.

    return render_template(
        "schedule.html",
        schedule=schedule,
        today=Settings.TODAY,
        json_schedule=json.dumps(schedule)
    )


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate() -> Response | str:
    if request.method == "POST":
        email: str = request.form["email"]
        passw: str = request.form["password"]

        encrypted_email: str = substitution_encryption(email)
        encrypted_passw: str = substitution_encryption(passw)

        # The auth cookie is cleared so the new cookie will be used.
        BrowserCookie.set_credentials_cookie(encrypted_email, encrypted_passw)
        BrowserCookie.clear_auth_cookie()
        Settings.load()

        return redirect('/')
    return render_template("authenticate.html")


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
