import sqlite3
import pandas as pd
import os

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

import query as qry

UPLOAD_FOLDER = 'C:/Users/Bryan/repos/project/communitycookbook_UI/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    if "." not in filename:
        return False

    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image(request):
    # check if the post request has the file part
    try:
        img_file = request.files['img']
        # if user does not select file, browser also
        # submit an empty part without filename
        if img_file.filename == '':
            return ''

        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(UPLOAD_FOLDER, filename))
            return os.path.join("/static/images/", filename)
    except:
        pass

    return ""


def upload_all(request):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'img' in request.files:
            image_loc = upload_image(request)
        else:
            image_loc = ""

        conn = qry.get_db_connection()
        recipe_row_id = upload_recipe(request, image_loc, conn)
        upload_ingredients(request, recipe_row_id, conn)
        upload_instructions(request, recipe_row_id, conn)

        return recipe_row_id


def upload_recipe(request, image_url, conn):
    # first create the record

    sql = '''
    INSERT INTO recipes
        (username, recipe_name, image_url)
    VALUES
        (?, ?, ?)
    '''

    data = (
        request.form['username'], request.form['recipe_name'], image_url
    )

    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

    return cur.lastrowid


def upload_ingredients(request, recipe_row_id, conn):
    sql = '''
    INSERT INTO ingredients (recipe_name, recipe_id, ingredient, amount)
    VALUES
        (?, ?, ?, ?)
    '''

    data = [request.form['recipe_name'], int(recipe_row_id)]

    ingred_keys = [i for i in request.form.keys() if "ingred" in i]
    ingred_keys = [i for i in ingred_keys if i != ""]

    for i in ingred_keys:
        amt_val = i.replace("ingred", "amt")
        if request.form.get(amt_val, ""):
            more_data = [request.form[i], request.form[amt_val]] 
            cur = conn.cursor()
            cur.execute(sql, data + more_data)
            conn.commit()


def upload_instructions(request, recipe_row_id, conn):
    sql = '''
    INSERT INTO instructions (step_number, recipe_name, recipe_id, instruction)
    VALUES
        (?, ?, ?, ?)
    '''

    data = [request.form['recipe_name'], int(recipe_row_id)]
    instr_keys = [i for i in request.form.keys() if "step" in i]
    instr_keys = [i for i in instr_keys if i != ""]

    for i in instr_keys:
        step_n = int(i.replace("step", ""))

        if request.form.get(i, "").replace(" ", ""):
            more_data = [step_n] + data + [request.form.get(i, "")]
            cur = conn.cursor()
            cur.execute(sql, more_data)
            conn.commit()


def add_review(request):
    conn = qry.get_db_connection()

    sql = '''
    INSERT INTO reviews (step_number, recipe_name, recipe_id, instruction)
    VALUES
        (?, ?, ?, ?)
    '''
    
    # data = [request.form['recipe_name'], int(recipe_row_id)]
    # instr_keys = [i for i in request.form.keys() if "step" in i]
    # instr_keys = [i for i in instr_keys if i != ""]

    # for i in instr_keys:
    #     step_n = int(i.replace("step", ""))

    #     if request.form.get(i, "").replace(" ", ""):
    #         more_data = [step_n] + data + [request.form.get(i, "")]
    #         cur = conn.cursor()
    #         cur.execute(sql, more_data)
    #         conn.commit()
