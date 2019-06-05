from flask import Blueprint, render_template, request

vegetables = Blueprint('vegetables', __name__, template_folder='templates')
vegetables_list = ['Potato', 'Cucumber', 'Tomato']


@vegetables.route("/vegetables", methods=["GET", "POST", "DELETE"])
def vegetables_page():
    if request.method == "POST" and request.form['_method'] == "POST":
        create_vegetable()
    elif request.method == "POST" and request.form['_method'] == "DELETE":
        remove_vegetable()

    return render_template('vegetables.html', title='Vegetables', vegetables_list=vegetables_list)


def create_vegetable():
    title = request.form['title']
    vegetables_list.append(title)


def remove_vegetable():
    vegetable = request.form['vegetable']
    if vegetable in vegetables_list:
        vegetables_list.remove(vegetable)
