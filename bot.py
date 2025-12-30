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

from openai import OpenAI

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("CHAT_GPT_API_KEY")
BASE_URL = "http://86.104.73.3/" #os.getenv("BASE_URL", "")

OUTPUT_FOLDER = "output_files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

client = OpenAI(api_key=OPENAI_API_KEY)

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

def gpt_extract_property(html_content, url):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Extract real estate data from HTML. Return valid JSON only."},
            {"role": "user", "content":
                "Schema:\n" + json.dumps(GPT_SCHEMA, ensure_ascii=False, indent=2) +
                "\n\nURL: " + url +
                "\n\nHTML:\n" + html_content[:120000]
            }
        ]
    )
    return json.loads(response.choices[0].message.content)

def get_rendered_html(url):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=options)  
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32")  

    driver.get(url)  
    time.sleep(5)  
    html_content = driver.page_source  
    driver.quit()  
    return html_content  


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
                text = eval(transform, {"re": re}, {"value": text})  
            except:  
                text = "ERROR"  
                error_count += 1  

        result[field] = text if text else "ERROR"  

    if error_count >= 5:  
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
    await update.message.reply_text("Send property URL")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("Processing...")

    config = {  
        "fields": {  
            "Название": {  
                "xpath": "//h1",  
                "transform": "re.sub(r'\\s+', ' ', value).strip()"  
            },  
            "Цена": {  
                "xpath": "//span[contains(@class,'price')]",  
                "transform": "re.sub(r'[^\\d.,]', '', value)"  
            },  
            "Описание": {  
                "xpath": "//div[contains(@class,'description')]",  
                "transform": "value.strip()"  
            }  
        }  
    }  

    property_data = parse_property(url, config)  
    filename = save_to_excel([property_data])  

    await update.message.reply_text(  
        "Done\n" + BASE_URL + "/output_files/" + filename  
    )  


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()