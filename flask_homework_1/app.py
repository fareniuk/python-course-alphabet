from flask import Flask, render_template, url_for
from main.routes import home
from vegetables.routes import vegetables
from fruits.routes import fruits
from werkzeug.utils import redirect

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(vegetables)
app.register_blueprint(fruits)


@app.route("/redirect")
def one_redirect():
    return redirect(url_for("home.home_page"))


@app.errorhandler(404)
def error_404_handler(error):
    return render_template("error_404.html", error=error)


if __name__ == '__main__':
    app.run()
