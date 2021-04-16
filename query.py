import sqlite3
import pandas as pd
import os

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/Bryan/repos/project/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


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


def get_ingredients(recipe_id):
    conn = get_db_connection()
    ingredients = conn.execute(
        f'SELECT ingredient, amount FROM ingredients WHERE recipe_id == ?',
        (recipe_id,)
    ).fetchall()
    
    conn.close()
    
    out = [['Ingredient', "Amount"]]
    out += [[i['ingredient'], i['amount']] for i in ingredients]
    
    return out


def get_instructions(recipe_id):
    conn = get_db_connection()
    instructions = conn.execute(
        f'SELECT  step_number, instruction FROM instructions WHERE recipe_id == ?',
        (recipe_id,)
    ).fetchall()
    
    conn.close()
    
    out = [['Step', "Instruction"]]
    out += [[i['step_number'], i['instruction']] for i in instructions]
    
    return out


def get_reviews(recipe_id):
    #conn = get_db_connection()
    #reviews = conn.execute().fetchall()
    #conn.close()

    out = ["Reviewer", "Score", "Review"]
    return out


def get_recipe_score(reviews):
    return "5.0"
