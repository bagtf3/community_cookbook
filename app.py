import sqlite3
import pandas as pd
import os

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

import upload as upl
import query as qry


UPLOAD_FOLDER = 'C:/Users/Bryan/repos/project/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    if "." not in filename:
        return False

    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_all(request):
    pass


def recipe_search_display(recipes):
    if recipes:
        cols = recipes[0].keys()
        # header
        out = []
        for r in recipes:
            l = [
                r['recipe_name'],
                qry.get_recipe_score(r['id']),
                r['username'],
                url_for('recipe', recipe_id=r['id'])
            ]
            
            out.append(l)

        return out
    return recipes


def get_recipe_score(reviews):
    return "5.0"


################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=('GET', 'POST'))
def search():
    headers = ["Recipe", "Score", "Added By", "Link"]
    if request.method == 'POST':
        query = request.form['query']
        recipes = qry.user_recipe_search(query)
    
    else:
        recipes = qry.default_recipe_search()

    recipes = recipe_search_display(recipes)
    return render_template("search.html", headers=headers, data=recipes)


@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    conn = qry.get_db_connection()

    recipe = conn.execute(
        "SELECT * FROM recipes WHERE id == ?", (recipe_id,)
    ).fetchone()
    conn.close()

    if not recipe:
        abort(401)

    ingredients = qry.get_ingredients(recipe_id)
    instructions = qry.get_instructions(recipe_id)

    reviews = qry.get_reviews(recipe_id)
    meta = {"score": get_recipe_score(reviews)}

    return render_template(
        'recipe.html', recipe=recipe, ing=ingredients, instr=instructions,
        rev=reviews, meta=meta
    )


@app.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        row_id = upl.upload_all(request)
        if row_id:
            return redirect(url_for('recipe', recipe_id=row_id))

    return render_template('upload.html')
    