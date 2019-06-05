from flask import Blueprint, render_template, request

fruits = Blueprint('fruits', __name__, template_folder='templates')
fruits_list = ['Orange', 'Banana', 'Apricot']


@fruits.route("/fruits", methods=["GET", "POST", "DELETE", "PATCH"])
def fruits_page():
    if request.method == "POST" and request.form['_method'] == "POST":
        create_fruit()
    elif request.method == "POST" and request.form['_method'] == "DELETE":
        remove_fruit()

    return render_template('fruits.html', title='Fruits', fruits_list=fruits_list)


def create_fruit():
    title = request.form['title']
    fruits_list.append(title)


def remove_fruit():
    fruit = request.form['fruit']
    if fruit in fruits_list:
        fruits_list.remove(fruit)