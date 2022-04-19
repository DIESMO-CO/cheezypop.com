from flask import Flask, render_template, request, flash, url_for, redirect, session
import mysql.connector

selectMovies = 'SELECT * FROM movies'
selectReviews = 'SELECT * FROM reviews'
app = Flask(__name__);
app.secret_key = "super secret key"

@app.route("/")
def home():
    connection = mysql.connector.connect(host="localhost", port="3306", user="root", database="cheezypop")
    cursor = connection.cursor()
    cursor.execute(selectMovies + ' ORDER BY movies.release_date DESC LIMIT 3;')
    newMovies = cursor.fetchall()
    print(newMovies[0][0])
    cursor.execute('SELECT DISTINCT reviews.moviename FROM reviews ORDER BY reviews.rating DESC LIMIT 5;')
    topRatedMovies = cursor.fetchall()
    print(topRatedMovies)
    cursor.execute(selectMovies)
    movieList = cursor.fetchall()
    print(movieList)
    print(session)
    user = [session['loggedin'], session['username'], session['email']]
    featuredMovies = []
    for movie in topRatedMovies:
        for movieInList in movieList:
            # print(movie[0], end='')
            if movie[0] == movieInList[0]:
                print(movieInList)
                featuredMovies += movieInList
    return render_template("index.html", newMovies=newMovies, featuredMovies=featuredMovies, user=user);

@app.route("/submission/", methods=["POST", "GET"])
def submission():
    user = [session['loggedin'], session['username'], session['email']]
    if request.method == "POST":
        connection = mysql.connector.connect(host="localhost", port="3306", user="root", database="cheezypop")
        cursor = connection.cursor()
        movieName = request.form["movieName"] + '\r\n'
        movieDescription = request.form["movieDescription"]
        movieRating = request.form["movieRating"]
        movieGenre = request.form["movieGenre"]
        movieCompany = request.form["movieCompany"]
        movieDirector = request.form["movieDirector"]
        movieLink = request.form["movieLink"].replace('watch?v=','embed/')
        moviePoster = request.form["moviePoster"]
        movieDurationHours = request.form["movieDurationHours"]
        movieDurationMinutes = request.form["movieDurationMinutes"]
        movieRelease = request.form["movieRelease"]
        insertSyntax = (
            "INSERT INTO `movies` (`idmoviename`, `genre`, `rating`, `description`, `production_company`, `director`, `trailer_link`, `image_link`, `duration_hours`, `duration_minutes`, `release_date`)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        )
        insertData = (
            movieName,
            movieGenre,
            movieRating,
            movieDescription,
            movieCompany,
            movieDirector,
            movieLink,
            moviePoster,
            movieDurationHours,
            movieDurationMinutes,
            movieRelease
        )
        cursor.execute(insertSyntax,insertData)
        cursor.execute("COMMIT;")
        cursor.close()
        connection.close()
        return redirect(url_for("home"))
    else:
        return render_template("submission.html", user=user);

@app.route("/signup",  methods=["GET", "POST"])
def signup():
    connection = mysql.connector.connect(host="localhost", port="3306", user="root", database="cheezypop")
    cursor = connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        insertSyntax = (
            "INSERT INTO `users` (`idusername`, `email`, `password`)"
            " VALUES (%s, %s, %s);"
        )
        insertData = (username, email, password)
        cursor.execute(insertSyntax, insertData)
        print(cursor.statement)
        cursor.execute('COMMIT;')
        cursor.close()

    return render_template("signup.html");

@app.route("/login", methods=["GET", "POST"])
def login():
    connection = mysql.connector.connect(host="localhost", port="3306", user="root", database="cheezypop")
    cursor = connection.cursor()
    user = [session['loggedin'], session['username'], session['email']]
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s', (email, password))
        record = cursor.fetchone()
        #print(record)
        if record:
            session['loggedin']= True
            session['email']= record[1]
            session['username']= record[0]
            return redirect(url_for('home'))
        else:
            print("false")
            return redirect(url_for('signup'))
    return render_template("login.html", user=user);

@app.route("/logout/")
def logout():
    session['username']=''
    session['email']=''
    session['loggedin'] = False
    return redirect(url_for("home"))


@app.route("/movies/")
def movies():
    connection = mysql.connector.connect(host="localhost", port="3306", user="root", database="cheezypop")
    cursor = connection.cursor()
    cursor.execute(selectMovies)
    movieRecords = cursor.fetchall()
    user = [session['loggedin'], session['username'], session['email']]
    return render_template("movies.html", movieRecords=movieRecords, user=user);

@app.route("/<movie>/")
def moviePage(movie):
    connection = mysql.connector.connect(host="localhost", port="3306", user="root", database="cheezypop")
    cursor = connection.cursor()
    cursor.execute(selectMovies)
    movieList = cursor.fetchall()
    user = [session['loggedin'], session['username'], session['email']]
    for movies in movieList:
        if movies[0] == movie:
            return render_template("movie-page.html", movie=movies, user=user);

if __name__ == "__main__":
    app.run(debug=True)
