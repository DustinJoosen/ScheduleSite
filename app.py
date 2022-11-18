from flask import Flask, render_template

app: Flask = Flask(__name__)


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/schedule')
@app.route('/rooster')
def schedule() -> str:
    return render_template(
        'schedule.html',
        class_name='WFHBOICT22.VG'
    )


if __name__ == "__main__":
    app.run(debug=True)
