import sqlite3
import pandas as pd

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_recipe_score(recipe_id):
    return "5.0"


def default_recipe_search():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes LIMIT 3').fetchall()
    conn.close()
    return recipes


def recipe_search_display(recipes):
    if recipes:
        cols = recipes[0].keys()
        out = []
        for r in recipes:
            l = [
                r['recipe_name'],
                get_recipe_score(r['recipe_id']),
                r['username']
            ]
            
            out.append(l)

        return out
    return recipes


def user_recipe_search(query):
    return []


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=('GET', 'POST'))
def search():
    headers = ("Recipe", "Score", "Added By", "Link")

    if request.method == 'POST':
        recipes = []
    
    else:
        recipes = default_recipe_search()

    recipe_search_display(recipes)
    return render_template("search.html", headers=headers, data=recipe_search_display)

@app.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        # title = request.form['title']
        # content = request.form['content']

        # if not title:
        #     flash('Title is required!')
        # else:
        #     conn = get_db_connection()
        #     conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
        #                  (title, content))
        #     conn.commit()
        #     conn.close()
        return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))