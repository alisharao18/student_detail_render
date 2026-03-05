from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Get the DATABASE_URL from Render environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    # Always use sslmode='require' on Render
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

@app.route("/", methods=["GET", "POST"])
def home():
    students = []

    if request.method == "POST":
        search_name = request.form.get("name", "").strip()

        if search_name:
            conn = get_db_connection()
            cur = conn.cursor()
            # ILIKE allows case-insensitive search and partial matches
            cur.execute("SELECT * FROM students WHERE name ILIKE %s", (f"%{search_name}%",))
            students = cur.fetchall()
            cur.close()
            conn.close()

    return render_template("app.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)
