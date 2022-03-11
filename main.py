from flask import Flask, render_template

app = Flask(__name__);

@app.route("/")
def home():
    return render_template("index.html");

@app.route("/submission")
def submission():
    return render_template("submission.html");

@app.route("/signup")
def signup():
    return render_template("signup.html");

@app.route("/login")
def login():
    return render_template("login.html");

@app.route("/movies")
def movies():
    return render_template("movies.html");

@app.route("/movie-page")
def moviePage():
    return render_template("movie-page.html");

if __name__ == "__main__":
    app.run();