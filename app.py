from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret-key-for-project"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    records = conn.execute(
        "SELECT * FROM records WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return render_template("index.html", records=records)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = get_db()
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/add", methods=["POST"])
def add():
    conn = get_db()
    conn.execute(
        "INSERT INTO records (title, description, user_id) VALUES (?, ?, ?)",
        (request.form["title"], request.form["description"], session["user_id"])
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    conn = get_db()
    record = conn.execute(
        "SELECT * FROM records WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":
        conn.execute(
            "UPDATE records SET title=?, description=? WHERE id=?",
            (request.form["title"], request.form["description"], id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("update.html", record=record)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM records WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
