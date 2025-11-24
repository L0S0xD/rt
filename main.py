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


def add_rating(rating_type: str, rating_name: str, lyrics_rating: int, lyrics_reason: str, beat_rating: int, beat_reason: str, df_rating: int, df_reason: str, melody_rating: int, melody_reason: str, cohesive_rating: int, cohesive_reason: str,  ):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO ratings (rating_type, rating_name, lyrics_rating,lyrics_reason, beat_rating, beat_reason, df_rating, df_reason, melody_rating, melody_reason, cohesive_rating, cohesive_reason) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (rating_type, rating_name,lyrics_rating,lyrics_reason, beat_rating, beat_reason, df_rating, df_reason, melody_rating, melody_reason, cohesive_rating, cohesive_reason))
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
        rating_type = request.form.get("rating_type", "").strip()
        rating_name = request.form.get("rating_name", "").strip()
        lyrics_rating = request.form.get("lyrics", "").strip()
        lyrics_reason = request.form.get("lyrics_reason", "").strip()
        beat_rating = request.form.get("beat", "").strip()
        beat_reason = request.form.get("beat_reason", "").strip()
        df_rating = request.form.get("df", "").strip()
        df_reason = request.form.get("df_reason", "").strip()
        melody_rating = request.form.get("melody", "").strip()
        melody_reason = request.form.get("melody_reason", "").strip()
        cohesive_rating = request.form.get("cohesive", "").strip()
        cohesive_reason = request.form.get("cohesive_reason", "").strip()
        if rating_type:
            add_rating(rating_type, rating_name,lyrics_rating,lyrics_reason, beat_rating, beat_reason, df_rating, df_reason, melody_rating, melody_reason, cohesive_rating, cohesive_reason)
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
