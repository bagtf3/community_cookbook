import sqlite3
import pandas as pd
import os

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

import query as qry

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
INVALID = ["", " ", None, False]

def allowed_file(filename):
    if "." not in filename:
        return False

    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def send_to_db(conn, sql, data, where=None):
    try:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        return cur
    
    except Exception as e:
        print(e)
        msg = "Database Error "
        
        if where is not None:
            msg += f"during {where}"

        flash(msg)
        raise Exception("DB Error", e)
    

def upload_image(request):
    # check if the post request has the file part
    try:
        img_file = request.files['img']
        # if user does not select file, browser also
        # submit an empty part without filename
        if img_file.filename == '':
            flash("No image file provided!")
            return ""

        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(UPLOAD_FOLDER, filename))
            return os.path.join("/static/images/", filename)

    except:
        flash("Image upload Failed!")
        return ""


def upload_all(request):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'img' in request.files:
            image_loc = upload_image(request)
        else:
            flash("No image file provided!")
            image_loc = ""

        conn = qry.get_db_connection()
        try:
            recipe_row_id = upload_recipe(request, image_loc, conn)
            upload_ingredients(request, recipe_row_id, conn)
            upload_instructions(request, recipe_row_id, conn)
            return recipe_row_id

        except:
            return -1


def upload_recipe(request, image_url, conn):
    # first create the record

    sql = '''
    INSERT INTO recipes
        (username, recipe_name, image_url)
    VALUES
        (?, ?, ?)
    '''

    user = request.form.get('username', "")
    if user in INVALID:
        user = "anonymous user"

    recipe_name = request.form.get('recipe_name', "")
    if recipe_name in INVALID:
        flash("Please Provide a Recipe Name!")
        raise Exception("No Recipe Name")

    data = (user, recipe_name, image_url)
    cur = send_to_db(conn, sql, data, where="recipe upload")

    return cur.lastrowid


def upload_ingredients(request, recipe_row_id, conn):
    sql = '''
    INSERT INTO ingredients (recipe_name, recipe_id, ingredient, amount)
    VALUES
        (?, ?, ?, ?)
    '''

    data = [request.form['recipe_name'], int(recipe_row_id)]

    ingred_keys = [i for i in request.form.keys() if "ingred" in i]
    ingred_keys = [i for i in ingred_keys if i not in INVALID]

    ingred_keys = [
        i for i in ingred_keys if request.form[i] not in INVALID
    ]

    if not ingred_keys:
        flash("Please Provide Ingredients!")
        raise Exception("No ingredients")

    for i in sorted(ingred_keys):
        amt_val = i.replace("ingred", "amt")
        if request.form.get(amt_val, ""):
            more_data = [request.form[i], request.form[amt_val]] 
            send_to_db(conn, sql, data + more_data, where="ingredient upload")


def upload_instructions(request, recipe_row_id, conn):
    sql = '''
    INSERT INTO instructions (step_number, recipe_name, recipe_id, instruction)
    VALUES
        (?, ?, ?, ?)
    '''

    data = [request.form['recipe_name'], int(recipe_row_id)]
    instr_keys = [i for i in request.form.keys() if "step" in i]
    instr_keys = [i for i in instr_keys if i != ""]

    instr_keys = [
        i for i in instr_keys if request.form[i] not in INVALID
    ]

    if not instr_keys:
        flash("Please Provide Instructions!")
        raise Exception("No Instructions")

    for i in instr_keys:
        step_n = int(i.replace("step", ""))

        if request.form.get(i, "").replace(" ", ""):
            more_data = [step_n] + data + [request.form.get(i, "")]
            send_to_db(conn, sql, more_data, where="instruction upload")


def add_review(request):

    sql = '''
    INSERT INTO reviews (recipe_id, review_text, rating, reviewer)
    VALUES
        (?, ?, ?, ?)
    '''

    user = request.form.get('username', "")
    if user in INVALID:
        user = "anonymous user"

    rate = request.form.get('rate', "")
    if rate in INVALID:
        flash("Reviews must have a rating!")
        raise Exception("No Rating")

    data = [
        request.form['recipe_id'], request.form['review_text'], rate, user
    ]

    conn = qry.get_db_connection()
    send_to_db(conn, sql, data, where="review upload")
