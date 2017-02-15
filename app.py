import sqlite3

from flask import Flask, render_template, request

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
