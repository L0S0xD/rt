import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path

# -------------
# CONFIGURATION
# -------------

ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ROOT_DIR / "db.sqlite3"

app = Flask(__name__)


# --------
# DATABASE
# --------


# Database connection
def get_db_connection():
    return sqlite3.connect(DB_PATH)


# Database setup
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            df_reason TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


# Database operations
def get_ratings():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, df_reason FROM ratings ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_rating_by_id(rating_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, df_reason FROM ratings WHERE id = ?", (rating_id,))
    row = cur.fetchone()
    conn.close()
    return row


def add_rating(df_rating: int, df_reason: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO ratings (df_rating, df_reason) VALUES (?,?)", (df_reason,df_rating, ))
    conn.commit()
    conn.close()


def update_rating(rating_id, df_reason: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE ratings SET df_reason = ? WHERE id = ?", (df_reason, rating_id))
    conn.commit()
    conn.close()


def delete_rating(rating_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ratings WHERE id = ?", (rating_id,))
    conn.commit()
    conn.close()


# ------
# ROUTES
# ------


# Home
@app.route("/")
def home():
    ratings = get_ratings()
    return render_template("index.html", ratings=ratings)


# Add
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        df_rating = request.form.get("flow", "").strip()
        df_reason = request.form.get("flow_reason", "").strip()
        if df_rating:
            add_rating(df_reason, df_rating)
        return redirect(url_for("home"))
    return render_template("add.html")


# Edit
@app.route("/edit/<int:rating_id>", methods=["GET", "POST"])
def edit(rating_id):
    if request.method == "POST":
        df_reason = request.form.get("df_reason", "").strip()
        if df_reason:
            update_rating(rating_id, df_reason)
        return redirect(url_for("home"))

    rating = get_rating_by_id(rating_id)
    if not rating:
        return redirect(url_for("home"))
    return render_template("edit.html", rating=rating)


# Delete
@app.route("/delete/<int:rating_id>", methods=["POST"])
def delete(rating_id):
    delete_rating(rating_id)
    return redirect(url_for("home"))


# -------
# STARTUP
# -------

# Starts the database
init_db()

# Runs the app
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
