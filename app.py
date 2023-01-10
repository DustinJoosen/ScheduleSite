from flask import Flask, render_template, redirect, request, make_response
from flask_caching import Cache
from werkzeug import Response
from datetime import datetime, timedelta
from cookies.settings import Settings
from schedule.schedule import get_schedule
from cookies.cookieencryption import substitution_encryption
from mongo.mongo import Mongo
from mongo.mongoqueue import MongoQueue
from json import dumps

app: Flask = Flask(__name__)
cache: Cache = Cache(app, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp',
    'CACHE_DEFAULT_TIMEOUT': 600
})
cache.init_app(app)


if not Mongo.CONNECTED:
    Mongo.connect()
    MongoQueue.init()


@app.route('/', methods=['GET'])
def schedule() -> Response | str:
    # You need a browser_guid to do anything. Make sure you have one.
    if request.cookies.get("mongo_browser_guid") is None:
        mongo_browser_guid: str = MongoQueue.pop()
        print("popped a uuid out of the queue: " + mongo_browser_guid)

        response: Response = make_response(redirect("/"))
        response.set_cookie("mongo_browser_guid", mongo_browser_guid, expires=datetime.now() + timedelta(days=30))

        return response

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

    print(Mongo.get_mock_document())
    print(schedule)

    return render_template(
        "schedule.html",
        schedule=schedule,
        today=Settings.TODAY,
        json_schedule=dumps(schedule, default=str)
    )


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate() -> Response | str:
    if request.cookies.get("mongo_browser_guid") is None:
        return redirect("/")

    if request.method == "POST":
        email: str = request.form["email"]
        passw: str = request.form["password"]

        encrypted_email: str = substitution_encryption(email)
        encrypted_passw: str = substitution_encryption(passw)

        # The auth cookie is cleared so the new cookie will be used.
        Mongo.set_credentials_document(encrypted_email, encrypted_passw)
        Mongo.clear_auth_document()

        Settings.load()

        print("settings loaded in")
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
        date = Mongo.get_viewingdate_document() + timedelta(weeks=inc)

    Mongo.set_viewingdate_document(date)

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
