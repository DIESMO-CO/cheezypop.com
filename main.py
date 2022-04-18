from flask import Flask, render_template, request, flash, url_for, redirect
import mysql.connector

selectMovies = 'SELECT * FROM movies'
selectReviews = 'SELECT * FROM reviews'
app = Flask(__name__);

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
    featuredMovies = []
    for movie in topRatedMovies:
        for movieInList in movieList:
            # print(movie[0], end='')
            if movie[0] == movieInList[0]:
                print(movieInList)
                featuredMovies += movieInList
    return render_template("index.html", newMovies=newMovies, featuredMovies=featuredMovies);

@app.route("/submission/", methods=["POST", "GET"])
def submission():
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
        return render_template("submission.html");

@app.route("/signup/")
def signup():
    return render_template("signup.html");

@app.route("/login/")
def login():
    return render_template("login.html");

@app.route("/movies/")
def movies():
    connection = mysql.connector.connect(host="localhost", port="3306", user="root", database="cheezypop")
    cursor = connection.cursor()
    cursor.execute(selectMovies)
    movieRecords = cursor.fetchall()
    return render_template("movies.html", movieRecords=movieRecords);

@app.route("/<movie>/")
def moviePage(movie):
    connection = mysql.connector.connect(host="localhost", port="3306", user="root", database="cheezypop")
    cursor = connection.cursor()
    cursor.execute(selectMovies)
    movieList = cursor.fetchall()
    for movies in movieList:
        if movies[0] == movie:
            return render_template("movie-page.html", movie=movies);

if __name__ == "__main__":
    app.run(debug=True);
