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
        food = (request.form['name'].lower(),
                request.form['calories'],
                request.form['cuisine'].lower(),
                request.form['is_vegetarian'].lower(),
                request.form['is_gluten_free'].lower(), )

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
    fav_food = (food.lower(), )

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
        if foods:
            favs_json = {"favourites":
                         [dict(found_food) for found_food in foods]}
            return jsonify(favs_json)
        else:
            return jsonify("null")


@app.route('/search/')
def search():
    search = (request.args.get('name').lower(), )

    try:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM foods WHERE name=?', search)
        results = cur.fetchall()
        conn.close()
    except:
        pass
    finally:
        if results:
            favs_json = {"favourites":
                         [dict(found_food) for found_food in results]}
            return jsonify(favs_json)
        else:
            return jsonify("null")


@app.route('/drop/')
def drop():
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS foods')
        conn.commit()
        conn.close()
    except:
        pass
    finally:
        return 'dropped'
