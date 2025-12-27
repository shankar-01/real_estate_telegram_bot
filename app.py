import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
import requests
from requests.exceptions import RequestException
from flask import send_from_directory
from datetime import datetime
from fetch_using_ai import extract_xpaths
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium_stealth import stealth
import time
import re
import tempfile
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB
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

    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM configs WHERE id=?", (id,))
            conn.commit()
        flash("✅ Deleted successfully!", "success")
    except sqlite3.OperationalError as e:
        flash(f"❌ Database error: {str(e)}", "danger")
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
def create_generator_driver():
    options = build_generator_chrome_options()
    driver = uc.Chrome(options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver
def build_generator_chrome_options():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Realistic User-Agent
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )

    # Unique profile per run
    tempdir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={tempdir}")

    return options

def wait_and_scroll(driver, wait_time=6, lazy_scroll=True, max_scrolls=5, scroll_pause=2):
    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, "//*"))
        )
    except TimeoutException:
        pass

    if not lazy_scroll:
        return

    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def clean_html_for_llm(html_text, max_length=120_000):
    # Remove scripts/styles
    html_text = re.sub(r"<script.*?>.*?</script>", "", html_text, flags=re.S)
    html_text = re.sub(r"<style.*?>.*?</style>", "", html_text, flags=re.S)

    # Collapse whitespace
    html_text = re.sub(r"\s+", " ", html_text).strip()

    # Hard truncate (safety)
    if len(html_text) > max_length:
        html_text = html_text[:max_length]

    return html_text

def fetch_html_for_generator(url):
    """
    Cloudflare-safe HTML fetch for config generator.
    Uses undetected Chrome + stealth.
    """
    driver = None
    try:
        driver = create_generator_driver()
        driver.get(url)

        wait_and_scroll(
            driver,
            wait_time=6,
            lazy_scroll=True,
            max_scrolls=5,
            scroll_pause=2
        )

        html_content = driver.page_source
        return html_content

    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        raise RuntimeError(f"Failed to render URL: {url}\n{e}")

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

def fetch_and_prepare_html(url):
    raw_html = fetch_html_for_generator(url)
    print(f"Fetched HTML length for {url}: {len(raw_html)}")
    return clean_html_for_llm(raw_html)

from urllib.parse import urlparse

def extract_domain_key(url: str) -> str:
    """
    Converts:
    https://www.jamesedition.com/real_estate/united-states
    → jamesedition.com
    """
    parsed = urlparse(url)

    host = parsed.netloc.lower()

    # Remove common subdomains
    for prefix in ["www."]:
        if host.startswith(prefix):
            host = host[len(prefix):]

    return host

@app.route("/generator", methods=["GET", "POST"])
def generator():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    generated_json = None
    domain_url = field1 = field2 = field1_html = field2_html = ""

    if request.method == "POST":
        action = request.form.get("action")
        domain_url = request.form.get("domain_url", "").strip()
        field1 = request.form.get("field1", "").strip()
        field2 = request.form.get("field2", "").strip()
        field1_html = request.form.get("field1_html", "").strip()
        field2_html = request.form.get("field2_html", "").strip()

        if not domain_url:
            flash("❌ Domain URL is mandatory!", "danger")
            return redirect(url_for("generator"))

        # File uploads
        field1_file = request.files.get("field1_file")
        field2_file = request.files.get("field2_file")

        if field1_file:
            field1_html = field1_file.read().decode("utf-8")
        if field2_file:
            field2_html = field2_file.read().decode("utf-8")

        if action == "generate":
            if not ((field1 and field2) or (field1_html and field2_html)):
                flash("❌ Provide URLs, HTML, or uploaded files for both pages", "danger")
                return redirect(url_for("generator"))

            try:
                if not field1_html and field1:
                    field1_html = fetch_and_prepare_html(field1)
                if not field2_html and field2:
                    field2_html = fetch_and_prepare_html(field2)

                extracted = extract_xpaths(list_html=field1_html, detail_html=field2_html)
                generated_json = json.dumps(extracted, indent=2, ensure_ascii=False)

            except Exception as e:
                flash(f"❌ Generation failed: {str(e)}", "danger")
                return redirect(url_for("generator"))

        elif action == "store":
            generated_json = request.form.get("json_data")
            try:
                json.loads(generated_json)
            except:
                flash("❌ Invalid JSON format", "danger")
                return redirect(url_for("generator"))

            # Use mandatory domain_url for DB key
            domain_key = extract_domain_key(domain_url)

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute(
                "INSERT INTO configs (website, config_json) VALUES (?, ?)",
                (domain_key, generated_json)
            )
            conn.commit()
            conn.close()

            flash("✅ Config stored successfully!", "success")
            return redirect(url_for("dashboard"))

        elif action == "reject":
            flash("⚠️ Config rejected", "warning")
            return redirect(url_for("generator"))

    return render_template(
        "generator.html",
        generated_json=generated_json,
        domain_url=domain_url,
        field1=field1,
        field2=field2,
        field1_html=field1_html,
        field2_html=field2_html
    )

import os
import pandas as pd
from datetime import datetime
from main import (
    get_website_config,
    parse_property_with_config,
    parse_list_page,
    save_to_excel,
    send_email_notification,
    BASE_URL
)

def process_user_message(message_text: str):
    """
    Process a user message (URL) using main.py bot functions.
    Returns a tuple of (bot_reply_text, optional_excel_file_link)
    """
    url = message_text.strip()
    bot_messages = []

    bot_messages.append("✅ Принято, собираю…")
    print(f"👀 Input URL: {url}")

    domain, config = get_website_config(url)
    if not config:
        bot_messages.append("❌ Источник не подключён. Добавьте в панели.")
        return bot_messages, None

    # Try single property first
    data, error = parse_property_with_config(url, config)
    download_folder = "images"

    try:
        # Clean old images
        for f in os.listdir(download_folder):
            file_path = os.path.join(download_folder, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"🧹 Old images removed from '{download_folder}'")
    except Exception as e:
        print(f"⚠️ Failed to clear images folder: {e}")

    # Parse properties
    if data and data.get("Название") != "ERROR":
        properties = [data]
    else:
        properties = parse_list_page(url, config)

    if not properties:
        bot_messages.append("❌ Недвижимость не найдена.")
        return bot_messages, None

    # Save to Excel
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_properties.xlsx"
    file_path = save_to_excel(properties, filename)

    # Count errors in Excel
    df = pd.read_excel(file_path, engine="openpyxl")
    error_count = df.apply(lambda x: x.astype(str).str.contains("error", case=False, na=False)).sum().sum()

    download_link = f"{BASE_URL}/output_files/{filename}"
    bot_messages.append(
        f"✅ Готово: {len(properties)} объекта(ов), {error_count} с ошибками. Скачать Excel: \n📂 {download_link}"
    )

    # Optional: send email
    send_email_notification(
        "🚀 Bot Notification",
        f"✅ Готово: {len(properties)} объекта(ов), {error_count} с ошибками. Скачать Excel: \n📂 {download_link}"
    )

    return bot_messages, download_link

@app.route("/chat", methods=["GET", "POST"])
def chat_ui():
    if "chat" not in session:
        session["chat"] = []

    chat = session["chat"]

    if request.method == "POST":
        user_msg = request.form.get("message", "").strip()
        if user_msg:
            # Add user message
            chat.append({"sender": "user", "text": user_msg})

            # ===== Call your main.py bot logic here =====
            # Example placeholder:
            bot_replies, _ = process_user_message(user_msg)
            for reply in bot_replies:
                chat.append({"sender": "bot", "text": reply})

            session["chat"] = chat

    return render_template("chat_ui.html", chat=chat)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
