import sqlite3

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DB = 'database.db'


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/enternew/')
def enter_new():
    return render_template('food.html')


@app.route('/addfood/', methods=['POST'])
def add_food():
    try:
        food = (request.form['name'],
                request.form['calories'],
                request.form['cuisine'],
                request.form['is_vegetarian'],
                request.form['is_gluten_free'], )

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('INSERT INTO foods VALUES(?,?,?,?,?)', food)
        conn.commit()
        conn.close()
    except:
        pass
    finally:
        message = "Added record: {0}".format(food)
        return render_template('result.html', message=message)


@app.route('/favourite/<food>')
def favourite(food):
    fav_food = (food, )

    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM foods WHERE name=?', fav_food)
        foods = cur.fetchall()
        conn.close()
    except:
        pass
    finally:
        favs_json = {"favourites": [dict(found_food) for found_food in foods]}
        return jsonify(favs_json)
