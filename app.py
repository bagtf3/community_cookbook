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


def user_recipe_search(query):
    res = []
    conn = get_db_connection()

    # first search title
    recipes = conn.execute(
        "SELECT * FROM recipes WHERE recipe_name LIKE ?",
        ("%" + query + "%",)
    )
    res += recipes.fetchall()
    found_recipes_ids = [r['id'] for r in res]

    # now ingredients
    hits = conn.execute(
        "SELECT recipe_id FROM ingredients WHERE ingredient LIKE ?",
        ("%" + query + "%",)
    )
    hits = hits.fetchall()
    new_hits = [h for h in hits if h['recipe_id'] not in found_recipes_ids]

    if new_hits:
        # build a string of ? of proper length
        seq = ", ".join(["?"]*len(new_hits))
        recipes = conn.execute(
            f"SELECT * FROM recipes WHERE recipe_id IN ({seq})",
            new_hits
        )

        res += recipes.fetchall()

    conn.close()
    return res


def recipe_search_display(recipes):
    if recipes:
        cols = recipes[0].keys()
        out = []
        for r in recipes:
            l = [
                r['recipe_name'],
                get_recipe_score(r['id']),
                r['username'],
                url_for('recipe', recipe_id=r['id'])
            ]
            
            out.append(l)

        return out
    return recipes


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=('GET', 'POST'))
def search():
    headers = ("Recipe", "Score", "Added By", "Link")

    if request.method == 'POST':
        query = request.form['query']
        recipes = user_recipe_search(query)
    
    else:
        recipes = default_recipe_search()

    recipes = recipe_search_display(recipes)
    return render_template("search.html", headers=headers, data=recipes)

@app.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('upload.html')


@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    conn = get_db_connection()

    recipe = conn.execute(
        "SELECT * FROM recipes WHERE id == ?", (recipe_id,)
    ).fetchone()
    conn.close()

    if not recipe:
        abort(401)

    return render_template('recipe.html', recipe=recipe)