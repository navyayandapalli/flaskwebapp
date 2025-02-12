from flask import *
#from flask_mysqldb import MySQL
#from flaskext.mysql import MySQL
from flask import render_template
import pymysql

app = Flask("myMovieapp")

app.secret_key ='abcd'


app_config ={
        "host" : '192.168.0.108',
        "user" : 'root',
        "password" : 'Root@1234',
        "database" : 'moviedb'
}


@app.route("/")
def Index():
    return render_template('index.html')

def get_db_connection():
    connection = pymysql.connect(**app_config)
    return connection

@app.route('/')
def Home():
    connection = get_db_connection()

@app.route('/add', methods=['POST'])
def add_movie():
    session["uid"] = request.form.get("id")
    session["uname"] = request.form.get("name")
    session["udescription"] = request.form.get("description")
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("INSERT INTO movies (id, name, description) VALUES (%s, %s, %s)",
                (session["uid"], session["uname"], session["udescription"]))
    connection.commit()
    cur.close()
    connection.close()
    return redirect('/')

@app.route('/add', methods=['GET'])
def add_movie_form():
    return render_template('add.html')

@app.route('/search', methods=['GET', 'POST'])
def search_movie():
    session["uid"] = request.form.get("id")
    connection = get_db_connection()
    cur = connection.cursor()

    cur.execute("SELECT * FROM movies WHERE id = %s", (session["uid"],))
    movie = cur.fetchone()
    cur.close()
    connection.close()

    return render_template('search.html', movie=movie)

@app.route('/movies')
def show_movies():

    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("SELECT * FROM movies")
    movies = cur.fetchall()
    cur.close()
    connection.close()

    return render_template('show.html', movies=movies)

app.run('0.0.0.0', port=5000, debug=True)
