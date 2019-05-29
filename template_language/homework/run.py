import json

from flask import Flask, render_template

app = Flask(__name__)
start_year = 2010

with open('movies.json') as f:
    MOVIES = json.load(f)


@app.route('/')
def home_page():
    return render_template('home.html', title='Home', author='Andrii Fareniuk')


@app.route('/movies')
def movies_page():
    return render_template('movies.html', title='Movies list', movies=MOVIES, start_year=start_year)


@app.route('/<title>')
def movie_page(title):
    for i, movie in enumerate(MOVIES):
        if MOVIES[i].get('title') == title:
            return render_template('movie.html', title=title, movie=MOVIES[i])
    return render_template('movies.html', title='Movies list', movies=MOVIES, start_year=start_year)


if __name__ == '__main__':
    app.run(debug=True)
