import os
import re
import json
import time
import requests
import pandas as pd

from datetime import datetime
from lxml import html
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import undetected_chromedriver as uc
from selenium_stealth import stealth


load_dotenv()

# --- CONFIGURATION FROM ENV ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_GPT_API_KEY = os.getenv("CHAT_GPT_API_KEY")
CHAT_GPT_URL = os.getenv("CHAT_GPT_URL")
MODEL_NAME = os.getenv("CHAT_GPT_MODEL")
BASE_URL = "http://86.104.73.3/" 

OUTPUT_FOLDER = "output_files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


GPT_SCHEMA = {
    "Название": None,
    "Цена": None,
    "Валюта": None,
    "Площадь": None,
    "Площадь земли": None,
    "Тип объекта": None,
    "Год постройки": None,
    "Количество комнат": None,
    "Описание": None,
    "Инфраструктура": [],
    "С/у": None,
    "Этаж": None,
    "Локация": None,
    "Координаты": None,
    "Контактное лицо": None,
    "Телефон контактного лица": None,
    "Компания": None
}

def gpt_extract_property(html_content: str, url: str) -> dict:
    truncated_html = html_content[:120000]

    system_prompt = "You are an expert in web scraping and data extraction."

    user_prompt = f"""
Extract real estate data ONLY from the provided HTML.

Rules:
- Return RAW JSON only
- No explanations
- Missing fields must be null

Schema:
{json.dumps(GPT_SCHEMA, ensure_ascii=False, indent=2)}

URL:
{url}

HTML:
{truncated_html}
"""

    headers = {
        "Authorization": f"Bearer {CHAT_GPT_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0
    }

    response = requests.post(CHAT_GPT_URL, headers=headers, json=payload, timeout=120)

    if response.status_code != 200:
        raise Exception(f"LLM Error {response.status_code}: {response.text}")

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned by LLM:\n{content}")

def get_rendered_html(url):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=options)  
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32")  

    try:
        driver.get(url)  
        time.sleep(5)  
        html_content = driver.page_source  
        return html_content
    finally:
        driver.quit()  

def parse_property(url, config):
    html_content = get_rendered_html(url)
    tree = html.fromstring(html_content)

    result = {"Ссылка на объект": url}  
    error_count = 0  

    for field, meta in config["fields"].items():  
        xpath = meta.get("xpath")  
        transform = meta.get("transform")  

        if not xpath:  
            result[field] = "ERROR"  
            error_count += 1  
            continue  

        values = tree.xpath(xpath)  
        if not values:  
            result[field] = "ERROR"  
            error_count += 1  
            continue  

        text = ""  
        for v in values:  
            if hasattr(v, "text_content"):
                text += v.text_content().strip() + " "
            else:
                text += str(v).strip() + " "

        text = text.strip()  

        if transform:  
            try:
                # Use the transform rules from your prompt (normalizing whitespace)
                text = eval(transform, {"re": re}, {"value": text})  
            except:  
                text = "ERROR"  
                error_count += 1  

        result[field] = text if text else "ERROR"  

    # If static XPaths fail, fall back to LLM extraction
    if error_count >= 2: # Lowered threshold to trigger LLM faster if XPaths are brittle
        gpt_data = gpt_extract_property(html_content, url)  
        gpt_data["Ссылка на объект"] = url  
        return gpt_data  

    return result  

def save_to_excel(data):
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".xlsx"
    path = os.path.join(OUTPUT_FOLDER, filename)

    df = pd.DataFrame(data)  
    df.to_excel(path, index=False)  
    return filename  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a property URL to start scraping.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("Please send a valid URL.")
        return

    await update.message.reply_text("🔍 Processing page with Undetected Chromedriver...")

    # Default config used for initial extraction attempt
    config = {  
        "fields": {  
            "Название": {  
                "xpath": "//h1/text() | //h1/span/text()",  
                "transform": "re.sub(r'\\s+', ' ', value).strip()"  
            },  
            "Цена": {  
                "xpath": "//div[contains(@class,'price')]//text()",  
                "transform": "re.sub(r'[^\\d]', '', value)"  
            },  
            "Описание": {  
                "xpath": "//div[contains(@class,'description')]//text()",  
                "transform": "re.sub(r'\\s+', ' ', value).strip()"  
            }  
        }  
    }  

    try:
        property_data = parse_property(url, config)  
        filename = save_to_excel([property_data])  

        await update.message.reply_text(  
            f"✅ Done!\nDownload here: {BASE_URL}output_files/{filename}"  
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found in environment variables.")
    else:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("Bot is running...")
        app.run_polling()