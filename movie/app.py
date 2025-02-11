from flask import *
from flask_mysqldb import MySQL
app = Flask("mymovieapp")

app.secret_key ='abcd'

# MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root@12'
app.config['MYSQL_DB'] = 'moviedb'

mysql = MySQL(app)

@app.route("/")
def Index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_movie():
    session["uid"] = request.form.get("id")
    session["uname"] = request.form.get("name")
    session["udescription"] = request.form.get("description")

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO movies (id, name, description) VALUES (%s, %s, %s)", 
                (session["uid"], session["uname"], session["udescription"]))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

@app.route('/add', methods=['GET'])
def add_movie_form():
    return render_template('add.html')

@app.route('/search', methods=['GET', 'POST'])
def search_movie():
    session["uid"] = request.form.get("id")
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movies WHERE id = %s", (session["uid"],))
    movie = cur.fetchone()
    cur.close()
    
    return render_template('search.html', movie=movie)

@app.route('/movies')
def show_movies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movies")
    movies = cur.fetchall()
    cur.close()
    
    return render_template('show.html', movies=movies)    
  


app.run(debug=True)