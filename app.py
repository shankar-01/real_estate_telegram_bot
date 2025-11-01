import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = "supersecretkey"  # change this in production

DB_FILE = "website_configs.db"

# ================= Initialize DB =================
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                config_json TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

init_db()


# ================= Admin Credentials =================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ================= Login Route =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Invalid credentials", "danger")
    return render_template("login.html")


# ================= Dashboard =================
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, website, config_json FROM configs")
    rows = c.fetchall()
    conn.close()
    
    return render_template("dashboard.html", configs=rows)


# ================= Create/Edit Field =================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
@app.route("/edit", defaults={"id": None}, methods=["GET", "POST"])
def edit_field(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    config_data = {"website": "", "config_json": "{}"}
    
    if id:
        c.execute("SELECT website, config_json FROM configs WHERE id=?", (id,))
        row = c.fetchone()
        if row:
            config_data = {"website": row[0], "config_json": row[1]}
    
    if request.method == "POST":
        website = request.form.get("website")
        config_json = request.form.get("config_json")
        
        # Validate JSON
        try:
            json.loads(config_json)
        except:
            flash("❌ Invalid JSON format", "danger")
            return redirect(request.url)
        
        if id:
            c.execute(
                "UPDATE configs SET website=?, config_json=? WHERE id=?",
                (website, config_json, id)
            )
        else:
            c.execute(
                "INSERT INTO configs (website, config_json) VALUES (?, ?)",
                (website, config_json)
            )
        conn.commit()
        conn.close()
        flash("✅ Saved successfully!", "success")
        return redirect(url_for("dashboard"))
    
    conn.close()
    return render_template("edit_field.html", config=config_data)


# ================= Delete =================
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM configs WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("✅ Deleted successfully!", "success")
    return redirect(url_for("dashboard"))

# Serve 'output' folder
@app.route("/output_files/<path:filename>")
def serve_output(filename):
    return send_from_directory("output_files", filename)

# Serve 'images' folder
@app.route("/images/<path:filename>")
def serve_images(filename):
    return send_from_directory("images", filename)

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory("images", filename, as_attachment=True)
@app.route("/image_pages")
def image_pages():
    images = os.listdir("images")
    return render_template("image_pages.html", images=images)

# ================= Logout =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
