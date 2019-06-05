from flask import Blueprint, render_template

home = Blueprint('home', __name__, template_folder='templates')


@home.route("/")
@home.route("/home")
@home.route("/main")
def home_page():
    return render_template('home.html', title='Home')
