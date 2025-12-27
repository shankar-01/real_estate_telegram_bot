import requests
import json
import re
import os
import dotenv
dotenv.load_dotenv()
CHAT_GPT_URL = os.getenv("CHAT_GPT_URL")
CHAT_GPT_API_KEY = os.getenv("CHAT_GPT_API_KEY")
MODEL_NAME = os.getenv("CHAT_GPT_MODEL")  # change to any installed model

SYSTEM_PROMPT = """
You are an expert in web scraping and XPath extraction.
"""


def extract_xpaths(list_html: str, detail_html: str) -> dict:
    """
    Sends both HTML pages to Ollama and returns extracted XPath JSON.
    """

    user_prompt = f"""
You will receive two HTML pages:

- list_page_html
- detail_page_html

Your task:
- Extract XPaths for the detail page only, except where explicitly noted.
- Fill ONLY the values in the provided JSON template.
- Do NOT explain anything and do NOT add any extra text.
- Keep all field names exactly as given.
- Always use Python expression strings for transforms, or null if none.
- Leave values as null if not found.
- list_page_check, page_query, and next_page_xpath must be extracted from list_page_html.
- list_page_check would return the list item links, which are used to route to detail pages.

XPath rules (MANDATORY):
- For fields that return a SINGLE text value, the XPath MUST return text, not an element.
  Use either `/text()` or `string(...)`.
- Do NOT return element nodes for single-value fields.
- For fields that return MULTIPLE values (lists, images, infrastructure), return node sets.
- Attribute values must be selected explicitly using `/@attr`.
- Coordinates must be extracted from attributes, not elements.

Text cleaning rules (MANDATORY):
- All single-text fields MUST use a transform that normalizes whitespace:
  re.sub(r'\\s+', ' ', _v).strip()
- Do NOT attempt to clean whitespace using XPath only.

Inputs:

list_page_html:
{list_html}

detail_page_html:
{detail_html}

Output:
Fill ONLY the following JSON template with correct XPaths and Python transform strings.
Do NOT wrap the output in code blocks. Output RAW JSON only.

{{
  "fields": {{
    "Название": {{"xpath": null, "transform": null}},
    "Цена": {{"xpath": null, "transform": null}},
    "Валюта": {{"xpath": null, "transform": null}},
    "Площадь": {{"xpath": null, "transform": null}},
    "Площадь земли": {{"xpath": null, "transform": null}},
    "Тип объекта": {{"xpath": null, "transform": null}},
    "Год постройки": {{"xpath": null, "transform": null}},
    "Количество комнат": {{"xpath": null, "transform": null}},
    "Описание": {{"xpath": null, "transform": null}},
    "Инфраструктура": {{"xpath": null, "transform": null}},
    "С/у": {{"xpath": null, "transform": null}},
    "Этаж": {{"xpath": null, "transform": null}},
    "Локация": {{"xpath": null, "transform": null}},
    "Координаты": {{"xpath": null, "transform": null}},
    "Фото_ссылки": {{"xpath": null, "transform": null}},
    "Фото_уникальные_названия": {{"xpath": null, "transform": null}},
    "Контактное лицо": {{"xpath": null, "transform": null}},
    "Телефон контактного лица": {{"xpath": null, "transform": null}},
    "Компания": {{"xpath": null, "transform": null}},
    "Телефон компании": {{"xpath": null, "transform": null}}
  }},
  "list_page_check": null,
  "page_query": null,
  "next_page_xpath": null
}}
"""

    headers = {
        "Authorization": f"Bearer {CHAT_GPT_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
    }

    response = requests.post(CHAT_GPT_URL, json=payload, headers=headers)

    if response.status_code != 200:
      raise Exception(f"Error: {response.text}")

    text = response.json()
    content = text["choices"][0]["message"]["content"]
    try:
      return json.loads(content)
    except json.JSONDecodeError as e:
      raise ValueError(f"Model returned invalid JSON:\n{content}") from e


if __name__ == "__main__":
    list_html = """
    
<!DOCTYPE html>
<html lang="en">
  <head prefix="og: http://ogp.me/ns#">
      <link rel="stylesheet" href="https://static-x.jamesedition.com/assets/dist/je2_serp_page.bundle-3146092af2fd63cf8d67f214ccda10ee36d015dcc5f06070c42812fc5a9694c4.css" async="async" />
    <title>Luxury homes for sale in France | JamesEdition</title>

<link rel="manifest" href="data:application/manifest+json,%7B%22name%22%3A%22JamesEdition%3A%20The%20World's%20Luxury%20Marketplace%22%2C%22short_name%22%3A%22James%5Cr%5CnEdition%22%2C%22start_url%22%3A%22https://www.jamesedition.com/?offline=1%22%2C%22icons%22%3A%5B%7B%22src%22%3A%22https%3A%2F%2Fassets.jamesedition.com%2Fandroid-chrome-192x192.png%22%2C%22sizes%22%3A%22192x192%22%2C%22type%22%3A%22image%2Fpng%22%7D%2C%7B%22src%22%3A%22https%3A%2F%2Fassets.jamesedition.com%2Fje3-square-black-icon-500.jpg%22%2C%22sizes%22%3A%22500x500%22%2C%22type%22%3A%22image%2Fjpg%22%2C%22purpose%22%3A%22maskable%22%7D%2C%7B%22src%22%3A%22https%3A%2F%2Fassets.jamesedition.com%2Fandroid-chrome-512x512.png%22%2C%22sizes%22%3A%22512x512%22%2C%22type%22%3A%22image%2Fpng%22%7D%5D%2C%22theme_color%22%3A%22%23ffffff%22%2C%22background_color%22%3A%22%23ffffff%22%2C%22display%22%3A%22standalone%22%7D">

<link href="https://assets.jamesedition.com/favicon.ico?v=2" rel="shortcut icon" type="image/ico">
<link rel="apple-touch-icon" sizes="180x180" href="https://assets.jamesedition.com/android-chrome-192x192.png?v=2">
<link rel="icon" type="image/png" sizes="32x32" href="https://assets.jamesedition.com/favicon-32x32.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="https://assets.jamesedition.com/favicon-16x16.png?v=2">
<meta name="theme-color" content="#ffffff">
<meta content="en" name="language">
<meta content="en_US" property="og:locale">
  <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport">
<meta name="csrf-param" content="authenticity_token" />
<meta name="csrf-token" content="5_fReppGjfuLst7ey-L55jovmHD1j8rbokNmtEsD9tm_Xk8HoVPhuKJlDDPQchpA_rZVuv4WhVUvSw_GKq85hQ" />
  <meta content="https://assets.jamesedition.com/ShareBranding.jpg" property="og:image">
  <link href="https://www.jamesedition.com/real_estate/france" rel="canonical">
  <meta content="https://www.jamesedition.com/real_estate/france" property="og:url">
  <link href="https://www.jamesedition.com/real_estate/france?real_estate_type%5B%5D=house&amp;real_estate_type%5B%5D=villa&amp;real_estate_type%5B%5D=estate&amp;real_estate_type%5B%5D=country_house&amp;real_estate_type%5B%5D=finca&amp;real_estate_type%5B%5D=chalet&amp;real_estate_type%5B%5D=townhouse&amp;real_estate_type%5B%5D=bungalow&amp;bedrooms_from=3&amp;eur_price_cents_to=247208500&amp;page=2" rel="next">
  <meta content="Your destination for buying luxury property in France. Discover your dream home among our modern houses, penthouses and villas for sale" name="description">
  <meta content="Your destination for buying luxury property in France. Discover your dream home among our modern houses, penthouses and villas for sale" property="og:description">
  <meta content="Luxury homes for sale in France | JamesEdition" property="og:title">
  <meta content="643afb2028860a1f9d0a4750d1b1158c" name="p:domain_verify">
  <meta content="DzNmkvUwkQRm9GzYMJC8PUC3jupgh_K1InmvNQOYS7c" name="google-site-verification">
  <meta property="og:type" content="website">

<link href="https://static.jamesedition.com" rel="preconnect">
<link href="https://static-x.jamesedition.com" rel="preconnect">
<link href="https://assets.jamesedition.com" rel="preconnect">
<link href="https://img.jamesedition.com" rel="preconnect">


      <meta content="searchresultpage" name="atdlayout">
          <link rel="preload" as="image" href="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/a434c3e3-29d1-4b52-8318-fadffb52a835/je/556x342xcxm.jpg">
  <link rel="preload" as="image" href="https://api.mapbox.com/styles/v1/jamesedition/ckcd8kyfr0ofa1io8eo4zwxa3/static/[-5.5591, 41.31433, 9.6624999, 51.1241999]/500x550@2x?access_token=pk.eyJ1IjoiamFtZXNlZGl0aW9uIiwiYSI6ImNrc2hjZnY2bzFiM20yd3RiZnd6dTJ3dHYifQ.FZcx6OUbx12Y_icPdxMeBg&amp;attribution=false&amp;padding=50&amp;addlayer=%7B%22id%22%3A%22all%22%2C%22type%22%3A%22circle%22%2C%22source%22%3A%7B%22type%22%3A%22vector%22%2C%22url%22%3A%22mapbox%3A%2F%2Fjamesedition.difstjhl%22%7D%2C%22source-layer%22%3A%22all%22%2C%22paint%22%3A%7B%22circle-color%22%3A%22%23000000%22%2C%22circle-stroke-width%22%3A2%2C%22circle-stroke-color%22%3A%22%23fff%22%2C%22circle-radius%22%3A4%7D%2C%22filter%22%3A%5B%22all%22%2C%5B%22in%22%2C%5B%22get%22%2C%22n%22%5D%2C%5B%22literal%22%2C%5B%22france%22%5D%5D%5D%5D%7D">


    <style type="text/css">
    @font-face {
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url('https://static-x.jamesedition.com/assets/inter/inter-regular-15d70055271f3f6df4ffb4287233fc9ebb3770779661c0bee4c8ebf3718627dc.eot');
        src: local(''),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-15d70055271f3f6df4ffb4287233fc9ebb3770779661c0bee4c8ebf3718627dc.eot?#iefix') format('embedded-opentype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-7a1e50a41e236283cc554591d92ca62508132c9cbda31d15ea3e8bfb70a5b50b.woff2') format('woff2'),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-2f9e1bec49baf9ccf9794cdf41e7a9b50a246ce12548cf581e594a24a17e7d40.woff') format('woff'),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-79664a362216fd6a6e7f4dc6f057a6602dab3527605f0fa66ad1f08a4df8f376.ttf') format('truetype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-caacbbac3eafe3961b3b007da19e856b1ad7d3108261110a9e2132b7f00fe06d.svg#Inter') format('svg');
    }

    @font-face {
        font-family: 'Inter';
        font-style: normal;
        font-weight: 500;
        font-display: swap;
        src: url('https://static-x.jamesedition.com/assets/inter/inter-500-93f4acecb976a2df41b26f647c75eb317e912127e31349f23ee8f25f9cc25946.eot');
        src: local(''),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-93f4acecb976a2df41b26f647c75eb317e912127e31349f23ee8f25f9cc25946.eot?#iefix') format('embedded-opentype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-bcf82294eedd8e4011e95d67f12d6a3de1d98c2d6a5fd1196073870cc633f7dd.woff2') format('woff2'),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-4a21a390c618ec545fb2451f60f951a79f9a7df9e6adf61f43a6d1e47842efae.woff') format('woff'),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-2d86d524048555d308128c2ef54f5803a01551d717c190c8385c2000cb587019.ttf') format('truetype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-633fc6b1432a6c3eb62583a91585f362ca61409af5242e137bbe4506aaf5f140.svg#Inter') format('svg');
    }

    @font-face {
        font-family: 'Inter';
        font-style: normal;
        font-weight: 600;
        font-display: swap;
        src: url('https://static-x.jamesedition.com/assets/inter/inter-600-8b2f7582931802de7cd6d3dcc20f0fe5d81d1fe2f5a889e8c4678cd78c2cc201.eot');
        src: local(''),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-8b2f7582931802de7cd6d3dcc20f0fe5d81d1fe2f5a889e8c4678cd78c2cc201.eot?#iefix') format('embedded-opentype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-45731a4b0962ee79642ec4bd38650379c588973f9ec57140386ada0f6b8316db.woff2') format('woff2'),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-cbbb70dec22dafdd00716b179ea45f54947dab043b1daa0796dd101ccc0b67ff.woff') format('woff'),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-7aa2268dabb0037837f3afe96957aeb0f43bb44573812cdaeaee046f907635be.ttf') format('truetype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-0d4f387df6a81f8c83f6d68366995b383f0b2c62447bd6b27bb40bff43a22589.svg#Inter') format('svg');
    }

    @font-face {
        font-family: heldane;
        src: url('https://static-x.jamesedition.com/assets/heldane/Regular-f974ddb7f76e56d78861adcc3c37eda4217d32b3d4f400eac018ef5ccfc947f7.woff2') format('woff2'),
            url('https://static-x.jamesedition.com/assets/heldane/Regular-16de9bcc4536394668bb93690b1b14e151045f0e27d811fd6c5f9d45c2116903.woff') format('woff');
        font-weight: normal;
        font-style: normal;
        font-display: swap;
    }

    @font-face {
        font-family: prata;
        src: url('https://static-x.jamesedition.com/assets/Prata-Regular-574345a3423feeb31f801fef6a127cd4a1e38f744212c73b83f0ab881d34b14a.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
        font-display: swap;
    }
</style>

  </head>
  <body class="EUR serp">
    <svg width="0" height="0" style="display:none" xmlns="http://www.w3.org/2000/svg" id="je-shared-icons">
  <symbol viewBox="0 0 8 12" id="arrow-left" fill="none">
      <path d="M7 1L2 6L7 11" stroke-width="2" fill="none" />
  </symbol>
  <symbol viewBox="0 0 8 12" id="arrow-right" fill="none">
      <path d="M1 1L6 6L1 11" stroke-width="2" fill="none" />
  </symbol>
  <svg viewBox="0 0 24 43" id="arrow-left-thin">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M20.8953 0.939331L23 3.05454L4.20933 21.9393L23 40.8241L20.8953 42.9393L9.17939e-07 21.9393L20.8953 0.939331Z" />
  </svg>
  <svg viewBox="0 0 24 43" id="arrow-right-thin">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M3.04412 0.939331L0.939453 3.05454L19.7301 21.9393L0.939451 40.8241L3.04412 42.9393L23.9395 21.9393L3.04412 0.939331Z" />
  </svg>
  <symbol viewBox="0 0 10 16" id="arrow-right-v2">
    <path d="m1.5 1 7 7-7 7" stroke="#151515" stroke-width="1.6" />
  </symbol>
  <symbol viewBox="0 0 10 16" id="arrow-left-v2">
    <path d="m8.5 1-7 7 7 7" stroke="#151515" stroke-width="1.6" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="cars">
      <path d="M16.125 8a2.625 2.625 0 0 1 2.625 2.625v2.188a.437.437 0 0 1-.438.437H17a2.625 2.625 0 0 1-5.25 0h-3.5a2.625 2.625 0 0 1-5.25 0H1.687a.437.437 0 0 1-.437-.438V9.75c0-.815.559-1.493 1.313-1.688l1.31-3.337a1.75 1.75 0 0 1 1.624-1.1h5.85c.464 0 1.076.294 1.366.657L15.688 8h.437zm-10.5 6.563a1.314 1.314 0 0 0 0-2.625 1.314 1.314 0 0 0 0 2.625zM7.594 8V5.375H5.497L4.447 8h3.147zm1.312 0h4.54l-2.1-2.625h-2.44V8zm5.469 6.563a1.314 1.314 0 0 0 0-2.625 1.314 1.314 0 0 0 0 2.625z" />
  </symbol>
  <symbol viewBox="0 0 32 32" id="heart">
      <path d="M14.0929 7.00711L14.1083 7.02247L14.1243 7.03715L15.3243 8.13715L16.0301 8.78414L16.7071 8.10711L17.8071 7.00711C20.3166 4.49763 24.3834 4.49763 26.8929 7.00711C29.4024 9.51658 29.4024 13.5834 26.8929 16.0929L15.997 26.9888L5.00711 16.0929C5.0066 16.0924 5.00609 16.0919 5.00558 16.0914C2.49763 13.5818 2.49814 9.51607 5.00711 7.00711C7.51658 4.49763 11.5834 4.49763 14.0929 7.00711Z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="white-heart">
      <path d="M8.82574 4.36176L8.83495 4.37098L8.84457 4.37979L9.59457 5.06729L10.018 5.45548L10.4243 5.04926L11.1118 4.36176C12.6899 2.78358 15.2476 2.78358 16.8257 4.36176C18.4039 5.93995 18.4039 8.49755 16.8257 10.0757L9.99818 16.9033L3.11176 10.0757C3.11146 10.0754 3.11116 10.0751 3.11085 10.0748C1.53358 8.49656 1.53388 5.93965 3.11176 4.36176C4.68995 2.78358 7.24755 2.78358 8.82574 4.36176Z" stroke="#151515" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="helicopters">
      <path d="M9.562 13.25a.985.985 0 0 1-.7-.35L6.5 9.75 2.125 8l-.862-2.956a.437.437 0 0 1 .425-.544H2.78c.138 0 .268.065.35.175L4.312 6.25H10V4.5H5.187a.437.437 0 0 1-.437-.438v-.875c0-.241.196-.437.437-.437h11.375c.242 0 .438.196.438.438v.874a.437.437 0 0 1-.438.438H11.75v1.75a6.125 6.125 0 0 1 6.125 6.125.875.875 0 0 1-.875.875H9.562zm3.063-5.154V11.5h3.412a4.384 4.384 0 0 0-3.412-3.404zm5.998 7.2c.18.18.165.479-.027.647-.906.794-1.464.807-1.871.807H7.812a.438.438 0 0 1-.437-.439v-.876c0-.242.196-.439.437-.439h8.913c.295 0 .48-.122.674-.307a.441.441 0 0 1 .619 0l.605.607z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="jets">
      <path d="M15.25 8c.967 0 2.625.783 2.625 1.75s-1.658 1.75-2.625 1.75h-3.125L9.25 16.53a.438.438 0 0 1-.38.22H7.08c-.29 0-.5-.278-.42-.558L8 11.5H5.187l-1.18 1.575a.437.437 0 0 1-.35.175H2.562a.437.437 0 0 1-.425-.544L3 9.75l-.862-2.956a.437.437 0 0 1 .425-.544h1.093c.138 0 .268.065.35.175L5.187 8H8L6.66 3.308a.437.437 0 0 1 .42-.558h1.791c.14 0 .31.099.38.22L12.125 8h3.125z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="jewelery">
      <path d="M15.4 2.75l2.475 4.375h-2.764L13.217 2.75H15.4zm-3.5 0l1.893 4.375H6.207L8.1 2.75h3.8zm-7.3 0h2.182L4.889 7.125H2.125L4.6 2.75zM2.125 8h2.754l3.363 6.882c.04.085-.074.162-.137.09L2.125 8zm4.052 0h7.646l-3.747 8.7c-.027.066-.123.066-.15 0L6.177 8zm5.581 6.882L15.121 8h2.754l-5.98 6.97c-.063.074-.178-.003-.137-.088z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="lifestyle">
      <path d="M5.625 8.875c0-.965-.785-1.75-1.75-1.75H3A2.626 2.626 0 0 1 5.625 4.5h8.75A2.626 2.626 0 0 1 17 7.125h-.875c-.965 0-1.75.785-1.75 1.75v1.75h-8.75v-1.75zM17 8c.965 0 1.75.785 1.75 1.75 0 .645-.355 1.203-.875 1.507v3.306c0 .24-.197.437-.438.437h-1.75a.439.439 0 0 1-.437-.438v-.437H4.75v.438c0 .24-.197.437-.438.437h-1.75a.439.439 0 0 1-.437-.438v-3.305A1.746 1.746 0 0 1 1.25 9.75C1.25 8.785 2.035 8 3 8h.875c.484 0 .875.391.875.875V11.5h10.5V8.875c0-.484.391-.875.875-.875H17z" />
  </symbol>
  <symbol viewBox="0 0 135 18" id="logo">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M.209 1.632l3.52-.65v11.74c0 2.371-1.43 3.996-3.644 4.14L0 16.867v.91h.09c1.578 0 3.003-.501 4.012-1.413 1.013-.914 1.57-2.206 1.57-3.638V.235H.21v1.397zm133.309 1.497l.433 10.462-10.462-10.48-.027-.026h-.646v13.396h1.482l-.495-10.355 10.391 10.355h.753V3.129h-1.429zm-16.022 2.803c-1.15-1.141-2.762-1.77-4.54-1.77-3.341 0-3.84 3.28-3.84 5.236 0 1.794.467 3.19 1.387 4.15 1.072 1.119 2.795 1.686 5.12 1.686 1.314 0 2.24-.461 2.831-1.411.518-.833.77-2.03.77-3.66 0-1.622-.613-3.125-1.728-4.231zm3.761 3.603a7.042 7.042 0 0 1-2.148 5.1c-1.375 1.333-3.216 2.067-5.184 2.067-3.884 0-6.814-2.87-6.814-6.675 0-1.947.764-3.758 2.151-5.1 1.378-1.333 3.228-2.067 5.208-2.067 3.869 0 6.787 2.87 6.787 6.675zm-17.562 6.858l.001.088h1.612l.185-13.352h-1.981l.183 13.264zm-14.1-11.86l5.282-.52.188 12.468h1.604l.186-12.468 5.281.52V3.13h-12.54v1.404zm-3.233 11.86v.088h1.613l.184-13.352h-1.98l.183 13.264zM78.617 4.356h-4.439v11.172c.553-.043 2.593-.202 3.348-.267 1.48-.129 2.715-.655 3.574-1.524.873-.884 1.335-2.104 1.335-3.529 0-1.872-.25-3.24-.762-4.178-.614-1.127-1.614-1.674-3.056-1.674zm3.985.634c1.203 1.17 1.865 2.803 1.865 4.6 0 2.127-.586 3.781-1.743 4.916-1.338 1.311-3.48 1.976-6.37 1.976h-.132L72.2 16.48V3.129h5.426c2.003 0 3.724.644 4.976 1.86zM54.28 8.827c-2.302-1.03-3.41-1.577-3.41-2.73 0-1.19.407-1.982 1.853-1.982 3.173 0 4.981 1.621 4.999 1.638l.153.14.123-1.763-.033-.029c-.014-.013-.356-.317-1.04-.62-.63-.28-1.683-.614-3.128-.614-2.985 0-4.767 1.33-4.767 3.558 0 1.953 1.362 2.903 4.225 4.177 2.368 1.06 3.557 1.593 3.557 2.811 0 1.633-.991 1.976-1.822 1.976-1.906 0-3.38-.49-4.283-.9-.976-.444-1.507-.893-1.513-.897l-.152-.13-.117 1.848.036.029c.004.003.437.348 1.224.683.725.308 1.916.676 3.465.676 1.564 0 2.851-.368 3.724-1.066.817-.653 1.25-1.562 1.25-2.628 0-1.918-1.527-2.948-4.344-4.177zm-13.388 1.247l5.498.227V8.986l-5.498.227V4.06l6.342.41V3.13h-8.32v13.35h8.402v-1.34l-6.424.434v-5.5zm-11.5 2.53l-5.866-9.432-.027-.043h-1.642v13.352h1.61L23.032 5.65l6.149 9.734 5.862-10.299-.4 11.396h2.097V3.129h-1.858l-5.492 9.476zM13.123 5.808l-3.036 6.06 5.922-.255-2.886-5.805zm7.553 10.674h-2.219l-1.816-3.6-6.94-.238-1.91 3.838H6.309l.065-.13L13.081 3.13h.714l6.882 13.352zm41.826-1.012l7.909-.494v1.498h-10V.047h9.899v1.4L62.503.986v6.625l6.77-.28v1.46l-6.77-.28v6.958z" />
  </symbol>
  <symbol viewBox="0 0 140 18" id="logo-new">
      <path d="M8.54 0v.321298c-.595.249898-.805.571196-.805 1.320892V12.7091c0 3.1416-1.225 4.1055-3.465 4.641-1.61.357-3.99-.0357-3.99-.0357L0 14.9582l.385-.1428c.665 1.1067 1.54 2.4276 2.835 2.1063 1.4-.3213 1.295-4.2483 1.295-4.2483V1.60649c0-.785395-.175-1.106693-.77-1.320892V0H8.54zm2.905 12.8162h4.34l.84 2.7132c.07.2142.105.3927.105.5712 0 .3927-.175.6069-.63.7854v.2499h4.83v-.2499c-.525-.2142-.84-.5712-1.085-1.3566L16.1 3.53428h-2.555L9.695 15.5294c-.105.3927-.385.7854-.665.9996-.21.1785-.385.2499-.805.357v.2499h3.43v-.2499c-.84-.1785-1.155-.4284-1.155-.8925 0-.1428.035-.2856.07-.4284l.875-2.7489zm.28-.8211l1.89-5.96184 1.89 5.96184h-3.78zm36.435 3.6414c-.7.714-1.505.9996-2.695.9996H44.45c-.875 0-1.4-.1785-1.575-.4998-.07-.1785-.105-.4284-.105-.7854V9.92454h1.82c1.4 0 1.995.42836 2.065 1.46366h.42V7.92535h-.42c-.14.96389-.77 1.39229-2.065 1.39229h-1.82V5.28357c0-.8211.385-1.1424 1.295-1.1424h1.085c1.54 0 2.45.6426 3.045 2.07059h.455l-.21-2.60608h-9.73v.2856c.595.24989.805.57119.805 1.32089V15.458c0 .7497-.21 1.071-.805 1.3209v.357h9.94l.7-2.7846-.42-.1785c-.245.7497-.42 1.071-.77 1.4637zm10.64-5.4621c-.56-.28556-1.26-.60686-2.03-.92816-1.785-.71399-2.45-1.10669-2.94-1.74929-.28-.3927-.42-.85679-.42-1.39229 0-1.28519.945-2.17768 2.31-2.17768 1.715 0 3.01 1.28519 3.185 3.21297h.49l.49-2.64178c-1.365-.60689-1.89-.82109-2.555-.96389-.595-.1428-1.225-.2142-1.89-.2142-2.905 0-4.725 1.53509-4.725 3.96267 0 1.57079.7 2.64179 2.24 3.42715.455.2499.98.4998 1.61.7854 2.38 1.0353 3.185 1.785 3.185 3.0702 0 1.3209-1.015 2.2491-2.485 2.2491-2.275 0-3.745-1.4637-3.745-3.7128l-.49-.0714-.595 2.8917c1.26.7497 1.82.9639 3.01 1.2852.77.2142 1.54.2856 2.31.2856 2.835 0 4.9-1.785 4.9-4.2126.035-1.428-.56-2.3919-1.855-3.1059zm12.425 5.4621c-.7.714-1.505.9996-2.695.9996h-.98c-.875 0-1.4-.1785-1.575-.4998-.07-.1785-.105-.4284-.105-.7854V8.31805h1.82c1.4 0 1.995.42839 2.065 1.46369h.42V6.31886h-.42c-.14.96389-.77 1.39229-2.065 1.39229h-1.82V1.64219c0-.821095.385-1.142393 1.295-1.142393h1.085c1.54 0 2.45.642593 3.045 2.070583h.455L71.54 0h-9.73v.285598c.595.249899.805.571197.805 1.320892V15.4937c0 .7497-.21 1.071-.805 1.3209v.3213h9.94l.7-2.7846-.42-.1785c-.245.7497-.42 1.071-.805 1.4637zm15.505-4.8909c0 4.0698-2.45 6.426-6.65 6.426h-6.335v-.2856c.595-.2499.805-.5712.805-1.3209V5.28357c0-.7854-.21-1.1067-.805-1.3209v-.28559H75.6c.28 0 .84-.0357 1.575-.0714.805-.0714 1.505-.0714 2.065-.0714 4.585-.0357 7.49 2.74888 7.49 7.21132zm-3.255-.2142c0-4.06974-1.68-6.49733-4.41-6.49733-.98 0-1.435.3927-1.435 1.2852V15.5294c0 .714.56 1.071 1.68 1.071 2.73 0 4.165-2.0706 4.165-6.069zm4.655-6.56873c.595.2499.805.5712.805 1.3209V15.5294c0 .7497-.21 1.071-.805 1.3209v.2856h4.865v-.2856c-.63-.2499-.805-.5712-.805-1.3209V5.28357c0-.7854.175-1.1067.805-1.3209v-.28559H88.13v.28559zm6.335-.32129l-.735 2.96308.455.0714c.385-.7497.56-1.0353 1.05-1.42799.63-.5355 1.365-.8211 2.205-.8211.84 0 1.19.2856 1.19.9996V15.4937c0 .7497-.21 1.071-.805 1.3209v.3213h4.83v-.2856c-.595-.2499-.805-.5712-.805-1.3209V5.56916c0-.78539.315-1.10669 1.155-1.10669.84 0 1.47.2499 2.135.8568.455.39269.665.67829 1.05 1.39229l.49-.0714-.735-2.96308h-11.48v-.0357zm12.95.32129c.595.2499.805.5712.805 1.3209V15.5294c0 .7497-.21 1.071-.805 1.3209v.2856h4.865v-.2856c-.63-.2499-.805-.5712-.805-1.3209V5.28357c0-.7854.175-1.1067.805-1.3209v-.28559h-4.865v.28559zm19.25 6.46163c0 4.0341-2.87 7.0686-6.72 7.0686-3.815 0-6.685-3.0345-6.685-7.0686 0-4.03404 2.87-7.06852 6.685-7.06852 3.85-.0357 6.72 2.99878 6.72 7.06852zm-3.255 0c0-4.06974-1.295-6.53302-3.465-6.53302-2.1 0-3.36 2.53468-3.36 6.56872 0 4.0698 1.295 6.4974 3.465 6.4974 2.065-.0357 3.36-2.499 3.36-6.5331zm13.51-6.78292v.2856c.84.17849 1.12.49979 1.12 1.39229v8.81783l-6.825-10.49572h-4.025v.2856c.84.17849 1.12.49979 1.12 1.39229V15.458c0 .8568-.28 1.2138-1.12 1.3923v.2856h3.045v-.2856c-.84-.1785-1.12-.5355-1.12-1.3923V6.35456l7 10.81704h2.765V5.31927c0-.8568.245-1.1781 1.12-1.39229v-.2856h-3.08zm-100.065.32129v-.28559h-3.99l-3.5 11.20972L25.69 3.64138h-4.025v.2856c.315.07139.525.14279.7.28559 0 0 .035 0 .035.0357l.035.0357.14.1428c.14.2142.21.4998.21.8925V15.458c0 .8568-.28 1.2138-1.12 1.3923v.2856h3.045v-.2856c-.84-.1785-1.12-.5355-1.12-1.3923V7.17565l3.29 9.96025h2.52l3.36-10.70994v9.06774c0 .7497-.21 1.071-.805 1.3209v.3213h4.865v-.2856c-.63-.2499-.805-.5712-.805-1.3209V5.28357c.035-.7497.21-1.071.84-1.3209z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="motorcycles">
      <path d="M15.275 8a3.516 3.516 0 0 1 3.478 3.47A3.5 3.5 0 0 1 15.22 15a3.51 3.51 0 0 1-3.467-3.475 3.495 3.495 0 0 1 1.225-2.686l-.342-.568a4.142 4.142 0 0 0-1.537 3.418.657.657 0 0 1-.656.686H8.141a3.5 3.5 0 0 1-6.89-.957 3.51 3.51 0 0 1 4.497-3.273l.309-.56c-.249-.38-.637-.679-1.307-.679H3.219a.655.655 0 0 1-.656-.642c-.009-.37.3-.67.67-.67H4.75c1.504 0 2.248.462 2.732 1.093h4.202l-.525-.875H9.344a.439.439 0 0 1-.438-.437v-.438c0-.24.197-.437.438-.437h2.187c.23 0 .443.12.563.317l.624 1.04 1.025-1.141a.657.657 0 0 1 .487-.216h1.239c.363 0 .656.293.656.656v.875a.655.655 0 0 1-.656.657h-2.253l.9 1.5A3.46 3.46 0 0 1 15.274 8zM4.75 13.688c.894 0 1.665-.542 2.004-1.313H4.531a.657.657 0 0 1-.574-.973L5.092 9.34a2.19 2.19 0 0 0-2.53 2.16 2.19 2.19 0 0 0 2.188 2.188zm12.685-2.068a2.187 2.187 0 0 0-2.62-2.261l1.33 2.212a.44.44 0 0 1-.151.602l-.375.224a.44.44 0 0 1-.601-.15l-1.351-2.254a2.17 2.17 0 0 0-.604 1.507 2.19 2.19 0 0 0 2.307 2.185 2.192 2.192 0 0 0 2.065-2.065z" />
  </symbol>
  <symbol viewBox="0 0 32 32" id="real-estate">
      <path d="M28 12L16 4L4 12V28H13V20H19V28H28V12Z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="recent">
      <path d="M10 2.969a6.78 6.78 0 0 1 6.781 6.781A6.78 6.78 0 0 1 10 16.531 6.78 6.78 0 0 1 3.219 9.75 6.78 6.78 0 0 1 10 2.969zm1.561 9.573a.33.33 0 0 0 .46-.071l.77-1.061a.328.328 0 0 0-.07-.46l-1.737-1.263V5.922a.33.33 0 0 0-.328-.328H9.344a.33.33 0 0 0-.328.328v4.602a.33.33 0 0 0 .134.265l2.411 1.753z" />
  </symbol>
  <symbol viewBox="0 0 18 18" id="recent-search">
    <path d="M9 16.428A7.429 7.429 0 1 0 9 1.571a7.429 7.429 0 0 0 0 14.857Z" stroke-width="1.6" />
    <path d="M9 6.143V9l2.903 3.383" stroke-width="1.6" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="search">
      <path d="M14.2499 1.5C9.67493 1.5 5.99994 5.175 5.99994 9.75C5.99994 11.775 6.74994 13.575 7.94994 15L2.62495 20.325L3.67495 21.375L8.99994 16.05C10.4249 17.25 12.2999 18 14.2499 18C18.8249 18 22.4999 14.325 22.4999 9.75C22.4999 5.175 18.8249 1.5 14.2499 1.5ZM14.2499 16.5C10.4999 16.5 7.49994 13.5 7.49994 9.75C7.49994 6 10.4999 3 14.2499 3C17.9999 3 20.9999 6 20.9999 9.75C20.9999 13.5 17.9999 16.5 14.2499 16.5Z" />
  </symbol>
  <symbol viewBox="0 0 17 17" id="search-icon">
    <path d="M6.8 12.8a6 6 0 1 0 0-12 6 6 0 0 0 0 12ZM15.47 15.47l-4.8-4.8" stroke-width="1.6" />
  </symbol>
  <symbol width="16" height="17" viewBox="0 0 16 17" id="nearby" fill="none">
    <path d="M14 2.5L8.95833 13.5L8.04167 8.22917L3 7.08333L14 2.5Z" stroke="#404040" stroke-width="1.6" />
    </symbol>
  <symbol viewBox="0 0 20 20" id="yachts">
      <path d="M2.48 12.38a.33.33 0 01-.23-.57l1.83-1.83a.33.33 0 01.47 0l1.83 1.83c.2.21.06.56-.24.56h-.96c.56 1.5 2.33 2.37 3.94 2.58v-5.2H7.7a.33.33 0 01-.32-.33v-1.1c0-.17.14-.32.32-.32h1.43v-.15a2.63 2.63 0 01.9-5.1 2.63 2.63 0 012.6 2.62c0 1.15-.74 2.12-1.76 2.48V8h1.43c.18 0 .32.15.32.33v1.1a.33.33 0 01-.32.32h-1.43v5.2c1.62-.2 3.4-1.09 3.95-2.58h-.97a.33.33 0 01-.23-.56l1.84-1.83a.33.33 0 01.46 0l1.83 1.83c.2.21.06.56-.23.56h-.89c-.6 2.81-3.73 4.38-6.63 4.38s-6.04-1.57-6.63-4.38h-.89zM10 4.5a.88.88 0 000 1.75.88.88 0 000-1.75z" />
  </symbol>
  <symbol viewBox="0 0 12 8" id="arrow-down">
      <path d="M0 1.53033L1.06066 0.469666L5.53033 4.93934L10 0.469666L11.0607 1.53033L5.53033 7.06066L0 1.53033Z" />
  </symbol>
  <symbol viewBox="0 0 18 14" id="check">
    <path fill-rule="evenodd" d="M17.533 2.587 6.416 13.15.885 7.003l2.23-2.006L6.584 8.85 15.467.412l2.066 2.175Z" clip-rule="evenodd" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="cross">
      <path d="M21.6 1.8L20.2.4 11 9.6 1.8.4.4 1.8 9.6 11 .4 20.2l1.4 1.4 9.2-9.2 9.2 9.2 1.4-1.4-9.2-9.2 9.2-9.2z" />
  </symbol>
  <symbol viewBox="0 0 19 16" id="message-bubble">
      <path d="M0.75 0.125V12H4.5V15.8125L9.6875 12H18.25V0.125H0.75Z" />
  </symbol>
  <symbol viewBox="0 0 32 32" id="small-cross">
      <path d="M24 9.4L22.6 8L16 14.6L9.4 8L8 9.4L14.6 16L8 22.6L9.4 24L16 17.4L22.6 24L24 22.6L17.4 16L24 9.4Z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="globe">
      <path d="M10 0C4.47581 0 0 4.47581 0 10C0 15.5242 4.47581 20 10 20C15.5242 20 20 15.5242 20 10C20 4.47581 15.5242 0 10 0ZM17.2177 6.45161H14.5161C14.2339 5 13.7903 3.70968 13.2258 2.66129C14.9597 3.42742 16.371 4.75806 17.2177 6.45161ZM10 1.93548C10.7258 1.93548 11.9355 3.62903 12.5403 6.45161H7.41935C8.02419 3.62903 9.23387 1.93548 10 1.93548ZM1.93548 10C1.93548 9.47581 1.97581 8.91129 2.09677 8.3871H5.20161C5.16129 8.95161 5.16129 9.47581 5.16129 10C5.16129 10.5645 5.16129 11.0887 5.20161 11.6129H2.09677C1.97581 11.129 1.93548 10.5645 1.93548 10ZM2.74194 13.5484H5.44355C5.72581 15.0403 6.16935 16.3306 6.73387 17.379C5 16.6129 3.58871 15.2419 2.74194 13.5484ZM5.44355 6.45161H2.74194C3.58871 4.75806 5 3.42742 6.73387 2.66129C6.16935 3.70968 5.72581 5 5.44355 6.45161ZM10 18.0645C9.23387 18.0645 8.02419 16.4113 7.41935 13.5484H12.5403C11.9355 16.4113 10.7258 18.0645 10 18.0645ZM12.8226 11.6129H7.1371C7.09677 11.129 7.09677 10.5645 7.09677 10C7.09677 9.43548 7.09677 8.91129 7.1371 8.3871H12.8226C12.8629 8.91129 12.9032 9.43548 12.9032 10C12.9032 10.5645 12.8629 11.129 12.8226 11.6129ZM13.2258 17.379C13.7903 16.3306 14.2339 15.0403 14.5161 13.5484H17.2177C16.371 15.2419 14.9597 16.6129 13.2258 17.379ZM14.7581 11.6129C14.7984 11.0887 14.8387 10.5645 14.8387 10C14.8387 9.47581 14.7984 8.95161 14.7581 8.3871H17.9032C17.9839 8.91129 18.0645 9.47581 18.0645 10C18.0645 10.5645 17.9839 11.129 17.9032 11.6129H14.7581Z" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="arrow-left-alt">
      <path d="M8.625 4.57495L9.675 5.62495L4.05 11.25H22.5V12.75H4.05L9.675 18.3749L8.625 19.4249L1.2 12L8.625 4.57495Z" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="arrow-right-alt">
      <path d="M15.375 4.57495L14.325 5.62495L19.95 11.25H1.5V12.75H19.95L14.325 18.375L15.375 19.425L22.8 12L15.375 4.57495Z" />
  </symbol>
  <symbol viewBox="0 0 18 18" id="globe-alt">
      <path d="M17.25 12.4375C17.6625 11.4062 17.9375 10.2375 17.9375 9C17.9375 7.7625 17.6625 6.59375 17.25 5.5625C15.875 2.33125 12.7125 0.0625 9 0.0625C5.2875 0.0625 2.125 2.33125 0.75 5.5625C0.3375 6.59375 0.0625 7.7625 0.0625 9C0.0625 10.2375 0.3375 11.4062 0.75 12.4375C2.125 15.6687 5.2875 17.9375 9 17.9375C12.7125 17.9375 15.875 15.6687 17.25 12.4375ZM9 16.5625C7.83125 16.5625 6.59375 14.9812 5.975 12.4375H12.025C11.4062 14.9812 10.1687 16.5625 9 16.5625ZM5.7 11.0625C5.63125 10.4438 5.5625 9.75625 5.5625 9C5.5625 8.24375 5.63125 7.55625 5.7 6.9375H12.3C12.3687 7.55625 12.4375 8.24375 12.4375 9C12.4375 9.75625 12.3687 10.4438 12.3 11.0625H5.7ZM1.4375 9C1.4375 8.3125 1.575 7.625 1.7125 6.9375H4.325C4.25625 7.625 4.1875 8.3125 4.1875 9C4.1875 9.6875 4.25625 10.375 4.325 11.0625H1.7125C1.575 10.375 1.4375 9.6875 1.4375 9ZM9 1.4375C10.1687 1.4375 11.4062 3.01875 12.025 5.5625H5.975C6.59375 3.01875 7.83125 1.4375 9 1.4375ZM13.675 6.9375H16.2875C16.4937 7.625 16.5625 8.3125 16.5625 9C16.5625 9.6875 16.425 10.375 16.2875 11.0625H13.675C13.7437 10.375 13.8125 9.6875 13.8125 9C13.8125 8.3125 13.7437 7.625 13.675 6.9375ZM15.7375 5.5625H13.4688C13.1938 4.1875 12.7125 3.01875 12.0938 2.125C13.675 2.8125 14.9125 4.05 15.7375 5.5625ZM5.90625 2.125C5.2875 3.01875 4.875 4.25625 4.53125 5.5625H2.2625C3.0875 4.05 4.325 2.8125 5.90625 2.125ZM2.2625 12.4375H4.53125C4.80625 13.8125 5.2875 14.9812 5.90625 15.875C4.325 15.1875 3.0875 13.95 2.2625 12.4375ZM12.0938 15.875C12.7125 14.9812 13.125 13.7437 13.4688 12.4375H15.7375C14.9125 13.95 13.675 15.1875 12.0938 15.875Z" />
  </symbol>
  <symbol viewBox="0 0 16 16" id="short-arrow">
      <path d="M8.00005 10.85L3.05005 5.85002L3.75005 5.15002L8.00005 9.40002L12.25 5.15002L12.95 5.85002L8.00005 10.85Z" />
  </symbol>
  <symbol viewBox="0 0 6 10" id="breadcrumb-arrow">
    <path d="M1 1L5 5L1 9" stroke="#ADADAD" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="phone-solid-icon">
    <path d="M0.0559626 3.09404C1.93013 12.8082 10.9261 21.775 20.6718 23.8922C21.4214 24.1413 21.6713 24.0167 22.296 22.8959C24.545 18.0388 23.9203 16.7934 23.9203 16.7934C23.9203 16.7934 19.2974 13.6799 18.2978 13.6799C17.2983 13.5554 14.6744 17.0425 14.6744 17.0425C12.5504 16.1707 8.42723 12.0609 6.9279 9.44558C6.9279 9.44558 10.4263 6.83024 10.4263 5.83392C10.4263 4.8376 7.17778 0.105081 7.17778 0.105081C7.17778 0.105081 5.92834 -0.642159 1.18046 1.84864C0.430795 2.22226 -0.193926 2.3468 0.0559626 3.09404Z" />
  </symbol>
  <symbol viewBox="0 0 16 16" id="contact">
    <path stroke="currentColor" fill="none" d="M1.33398 4.66663C2.86052 5.63713 8.00065 8.66663 8.00065 8.66663C8.00065 8.66663 13.1408 5.63713 14.6673 4.66663" />
    <path stroke="currentColor" fill="none" d="M3.15217 2.66663C2.14801 2.66663 1.33398 3.46257 1.33398 4.4444V11.5555C1.33398 12.5374 2.14801 13.3333 3.15217 13.3333H12.8491C13.8533 13.3333 14.6673 12.5374 14.6673 11.5555V4.4444C14.6673 3.46256 13.8533 2.66663 12.8491 2.66663H3.15217Z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="pointing-hand">
    <path d="M7.99212 18.1318C5.83024 16.8482 3.66886 12.9974 2.48939 10.6635C1.30992 8.32965 3.79146 6.14167 5.24079 7.86288C6.69012 9.5841 6.81307 9.72996 6.81307 9.72996V2.49503C6.81307 1.59276 7.42901 0.861328 8.18881 0.861328C8.94862 0.861328 9.56456 1.59276 9.56456 2.49503V6.46257C9.56456 5.5603 10.1805 4.82888 10.9403 4.82888C11.7001 4.82888 12.316 5.5603 12.316 6.46257V7.16273C12.316 6.26046 12.932 5.52903 13.6918 5.52903C14.4516 5.52903 15.0675 6.25976 15.0675 7.16203V9.49667C15.0675 8.59441 15.6835 7.86288 16.4433 7.86288C17.2031 7.86288 17.819 8.59431 17.819 9.49658V13.578C17.819 14.117 17.7157 14.6516 17.46 15.097C17.0005 15.897 16.0903 17.2147 14.6743 18.1318C12.5124 19.5321 10.154 19.4154 7.99212 18.1318Z" stroke="#151515" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" />
  </symbol>
  <symbol viewBox="0 0 17 16" id="list">
    <g stroke="#151515" stroke-width="1.6" clip-path="url(#a)"><path d="M4.66 3.52h12M4.66 8h12M4.66 12.48h12M2.66 3.52h-2M2.66 8h-2M2.66 12.48h-2" /></g><defs><clipPath id="a"><path fill="#fff" d="M.66 0h16v16h-16z" /></clipPath></defs>
  </symbol>
  <symbol viewBox="0 0 17 16" id="list-white">
    <g stroke="#EEE" stroke-width="1.6" clip-path="url(#a)"><path d="M4.66 3.52h12M4.66 8h12M4.66 12.48h12M2.66 3.52h-2M2.66 8h-2M2.66 12.48h-2" /></g><defs><clipPath id="a"><path fill="#fff" d="M.66 0h16v16h-16z" /></clipPath></defs>
  </symbol>
  <symbol viewBox="0 0 18 18" id="layer">
    <g stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path d="m9.7 3.56 4.04 2.71c1.16.52 1.16 1.37 0 1.88l-4.05 2.71c-.46.2-1.21.2-1.67 0l-4.04-2.7c-1.17-.52-1.17-1.37 0-1.89l4.04-2.7c.46-.21 1.21-.21 1.67 0Z" /><path d="M2.83 10.02c0 .57.43 1.24.96 1.47l4.66 2.98c.35.16.76.16 1.1 0l4.66-2.98c.53-.23.96-.9.96-1.47" /></g>
  </symbol>
</svg>

    <div class="real_estate index" id="view">
      

<div class="je3-header js-header _with-search _w-questionnaire _feed-v2">
  <header>
    <button class="je2-button js-hamburger-menu _noborder" aria-label="Menu">

    <svg width="20" height="14" viewBox="0 0 20 14" xmlns="http://www.w3.org/2000/svg">
  <path d="M0 13.0444H20" stroke-width="1.6" />
  <path d="M0 7.04443H20" stroke-width="1.6" />
  <path d="M0 1.04443H20" stroke-width="1.6" />
</svg>







  
  


</button>

    <a href="/" class="je2-button _noborder" aria-label="JamesEdition">

    <svg class="je2-icon"><use xlink:href="#logo-new" /></svg>







    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M16 0C7.36932 0 2 0.737706 2 0.737706C2 0.737706 2 9.66955 2 16.1362C2 21.6573 4.07286 24.8065 8.19987 27.022L16 31L23.8001 27.022C27.9295 24.8065 30 21.6573 30 16.1362C30 9.66955 30 0.737706 30 0.737706C30 0.737706 24.633 0 16 0ZM14.7015 6.01604C14.2243 6.20747 14.0652 6.46193 14.0652 7.06424V16.0778C14.0652 18.5407 13.0896 19.3018 11.2717 19.7126C9.9756 20.0068 8.05481 19.5539 8.05481 19.5539L7.84191 17.8497L8.16009 17.7423C8.71223 18.7975 9.38135 19.6403 10.4248 19.4068C11.5478 19.1523 11.4542 16.0801 11.4542 16.0801C11.4542 16.0801 11.4542 7.56382 11.4542 7.06657C11.4542 6.46193 11.3115 6.20747 10.8342 6.01838V5.78025H10.8506H14.6898H14.7062V6.01604H14.7015ZM23.5872 19.2387H15.6093V19.0169C16.0866 18.8115 16.2457 18.557 16.2457 17.9687V7.06657C16.2457 6.46193 16.0866 6.20747 15.6093 6.01838V5.78025H23.4141L23.5896 7.81362H23.2246C22.7473 6.6697 22.0127 6.17712 20.7704 6.17712H19.8954C19.1467 6.17712 18.8449 6.43158 18.8449 7.06657V11.8336H20.2931C21.3272 11.8336 21.8372 11.4998 21.9495 10.7364H22.2841V13.4538H21.9495C21.9027 12.6437 21.4231 12.2935 20.2931 12.2935H18.8449V17.824C18.8449 18.1112 18.8777 18.3166 18.9408 18.445C19.0836 18.7158 19.4977 18.8419 20.1995 18.8419H20.995C21.9495 18.8419 22.6046 18.6037 23.1614 18.0481C23.4632 17.747 23.6083 17.5089 23.8305 16.9206L24.1651 17.063L23.5872 19.2387Z" fill="#151515" />
</svg>


  


</a>

      <div class="je3-search-field js-search-field _with-value">
  <div class="je3-search-field__input">
    <div class="je3-search-field__placeholder js-placeholder">
        <svg><use xlink:href="#search-icon"></use></svg>

      <p>France</p>
    </div>

    <label>
        <button class="je2-button _noborder js-back" aria-label="Back">

    <svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <path d="M19.1666 10L1.66663 10" stroke="#151515" stroke-width="1.6" />
  <path d="M10 18.3332L1.66667 9.99984L10 1.6665" stroke="#151515" stroke-width="1.6" fill="none">
</svg>







    <svg><use xlink:href="#search-icon"></use></svg>

  


</button>
      <input type="text" autocomplete="off" class="js-search-text" name="search"
             placeholder="City, Region, Country" enterkeyhint="search" data-url=""
             data-hj-allow value="France" aria-label="City, Region, Country"
             data-location-slug="">
    </label>

    <button class="je2-button _noborder js-clear" aria-label="Clear">

    <svg viewBox="0 0 32 32">
  <path d="M26.6 6.80002L25.2 5.40002L16 14.6L6.80002 5.40002L5.40002 6.80002L14.6 16L5.40002 25.2L6.80002 26.6L16 17.4L25.2 26.6L26.6 25.2L17.4 16L26.6 6.80002Z"/>
</svg>







  
  


</button>
  </div>

  <div class="je3-search-field__suggestions js-search-suggestions"></div>

  <div
    class="js-search-field-translations"
    style="display:none;"
    data-search-near-me="Search near me"
    data-recent-searches="Recent searches"
    data-permision-popup-title="Browser Can’t Detect Your Location"
    data-permision-popup-description="To search near you, enable location access for JamesEdition in your browser settings, and avoid using a VPN or incognito mode."
    data-permision-popup-button="Got it"></div>
</div>



    
<div class="je2-user-block _compact">

      <ul>
        <li>
          <a href="/buyer/feed" class="je2-button _noborder je2-feed-entrypoint">

  

    <span>
          Just for You
    </span>




  
  


</a>
        </li>
      </ul>

        <ul>
          <li>
  <button class="je2-button js-sell-with-us _noborder _light"
          aria-expanded="false" aria-haspopup="true">
    <div>
      <span>Sell</span>
      <svg viewBox="0 0 12 8">
  <path fill="none" d="M11 1.49997L6 6.49997L1 1.49997" stroke="currentColor" stroke-width="1.6" />
</svg>

    </div>
  </button>
</li>

<nav class="je2-sell-with-us js-seller-dropdown _hidden _light">
  <ul>
    <li>
      <a href="/professional_seller/real_estate">
        Sell as a Business / Agent
      </a>
    </li>
    <li>
      <a href="https://join.jamesedition.com/sell-your-home">
        Sell as a Private Owner
      </a>
    </li>
  </ul>
</nav>

        </ul>

    <ul>
        <li>
          <a href="/offices/real_estate" class="je2-button _noborder">

  

    <span>
          Find Agencies
    </span>




  
  


</a>
        </li>
    </ul>

  <ul class="je2-user-controls js-user-controls">

    <li>
        <div class="je2-user-controls__login">
          <button class="je2-button js-login" aria-haspopup="true">

    <svg viewBox="0 0 14 15" stroke-width="1.2">
  <path fill="none" d="M7 8C8.79493 8 10.25 6.54493 10.25 4.75C10.25 2.95507 8.79493 1.5 7 1.5C5.20507 1.5 3.75 2.95507 3.75 4.75C3.75 6.54493 5.20507 8 7 8Z" stroke="currentColor" />
  <path fill="none" d="M13.1801 14.5C12.7602 13.1908 11.9355 12.0488 10.8249 11.2386C9.71416 10.4284 8.37487 9.99182 7.00007 9.99182C5.62526 9.99182 4.28597 10.4284 3.17528 11.2386C2.0646 12.0488 1.23989 13.1908 0.820068 14.5" stroke="currentColor" />
</svg>



    <span>
          Log in
    </span>




  
  


</button>
        </div>
    </li>

  </ul>
</div>

  </header>

    <div class="je3-header__questionnaire js-questionnaire">
      <div class="js-click-here">
        <span>Personalize your property search</span>
        <button class="je2-button _noborder" aria-label="Get started">

  

    <span>
          Get started
    </span>




    <svg viewBox="0 0 13 12">
  <path d="M0.5 6L11 6" stroke-width="1.6" />
  <path d="M6 11L11 6L6 1" stroke-width="1.6" />
</svg>


  


</button>
      </div>
    </div>


  <div class="je3-filter-bar js-je3-filterbar   _filters_v2">
    <button class="je2-button je2-saved-search-mobile _cyan _rounded" data-disabled-text="Search saved" data-active-text="Save search">

    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 16"><path fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="M1 7.042a6.041 6.041 0 1 0 12.083 0A6.041 6.041 0 0 0 1 7.041v0Z" /><path stroke-linejoin="round" stroke-width="1.6" d="m11 11 4 4" /><path d="M9.62 5.063a1.267 1.267 0 0 0-1.835 0L7 5.876l-.786-.813a1.267 1.267 0 0 0-1.834 0 1.373 1.373 0 0 0 0 1.897l2.34 2.42a.386.386 0 0 0 .56 0l2.34-2.42a1.373 1.373 0 0 0 0-1.897Z" /></svg>



    <span>
          Save search
    </span>




  
  


</button>
    <button class="je2-button js-filter-button _black" aria-label="Filters">

    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="11.6" cy="4.8" r="2.4" stroke="white" stroke-width="1.2" />
  <path d="M1.59998 4.8L9.59998 4.8" stroke="white" stroke-width="1.2" />
  <ellipse cx="4.4" cy="11.2" rx="2.4" ry="2.4" stroke="white" stroke-width="1.2" />
  <path d="M6.40002 11.2L14.4 11.2" stroke="white" stroke-width="1.2" />
</svg>



    <span>
          Filters
    </span>

    <div class="je2-button__badge"></div>



  
  


</button>
    <button class="je2-button js-filter-button" data-type="home-type">

  

    <span>
          Type
    </span>

    <div class="je2-button__badge"></div>



    <svg><use xlink:href='#arrow-down'></use></svg>

  


</button>
    <button class="je2-button js-filter-button" data-type="price">
    <div class="je2-button__temporary"></div>

  

    <span>
          Price
    </span>




    <svg><use xlink:href='#arrow-down'></use></svg>

  


</button>
    <button class="je2-button js-filter-button" data-type="beds">

  

    <span>
          Beds
    </span>

    <div class="je2-button__badge"></div>



    <svg><use xlink:href='#arrow-down'></use></svg>

  


</button>

      <button class="je2-button js-filter-button" data-type="amenities">

  

    <span>
          Amenities
    </span>

    <div class="je2-button__badge"></div>



    <svg><use xlink:href='#arrow-down'></use></svg>

  


</button>

      <button class="je2-button js-filter-button" data-property-feature="24">

  

    <span>
          New Builds
    </span>




  
  


</button>







    <div class="je2-tooltip _hidden">

  <div class="je2-tooltip__bell">
    <svg viewBox="0 0 18 17">
  <path stroke="currentColor" d="M7.3999 15.4287H10.5999" stroke-width="1.6" />
  <path stroke="currentColor" fill="none" d="M13.5715 6.57143C13.5715 5.35901 13.0899 4.19625 12.2326 3.33894C11.3752 2.48163 10.2125 2 9.00007 2C7.78765 2 6.62489 2.48163 5.76758 3.33894C4.91027 4.19625 4.42864 5.35901 4.42864 6.57143V10.5714C4.42864 11.0261 4.24803 11.4621 3.92654 11.7836C3.60505 12.1051 3.16901 12.2857 2.71436 12.2857H15.2858C14.8311 12.2857 14.3951 12.1051 14.0736 11.7836C13.7521 11.4621 13.5715 11.0261 13.5715 10.5714V6.57143Z" stroke-width="1.6" />
  <path stroke="currentColor" d="M1.57129 6.42314C1.57191 5.3353 1.83133 4.26322 2.32813 3.29545C2.82493 2.32768 3.54485 1.49199 4.42843 0.857422" stroke-width="1.6" />
  <path stroke="currentColor" d="M16.4284 6.42314C16.4278 5.3353 16.1684 4.26322 15.6716 3.29545C15.1748 2.32768 14.4549 1.49199 13.5713 0.857422" stroke-width="1.6" />
</svg>

  </div>
  <div class="je2-tooltip__title">Create Search Alert?</div>
  <div class="je2-tooltip__subtitle">
    Be notified of new similar listings 
    as they arrive
  </div>
  <div class="je2-tooltip__buttons">
    <button class="je2-button _black _uppercase js-yes">

  

    <span>
          Yes
    </span>




  
  


</button>
    <button class="je2-button _uppercase js-later">

  

    <span>
          Later
    </span>




  
  


</button>
  </div>

</div>

    <button class="je2-button je2-button je2-saved-search" data-disabled-text="Search saved" data-active-text="Save search">

    <svg viewBox="0 0 16 16">
  <path d="M1 7.04158C1 8.64384 1.6365 10.1805 2.76947 11.3134C3.90244 12.4464 5.43907 13.0829 7.04133 13.0829C8.64359 13.0829 10.1802 12.4464 11.3132 11.3134C12.4462 10.1805 13.0827 8.64384 13.0827 7.04158C13.0827 5.43932 12.4462 3.90268 11.3132 2.76971C10.1802 1.63674 8.64359 1.00024 7.04133 1.00024C5.43907 1.00024 3.90244 1.63674 2.76947 2.76971C1.6365 3.90268 1 5.43932 1 7.04158V7.04158Z" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none" />
  <path d="M11 11.0002L15 15.0002" stroke-width="1.6" stroke-linejoin="round" />
  <path d="M9.61939 5.06302C9.50109 4.93887 9.35882 4.84004 9.20119 4.77251C9.04357 4.70499 8.87387 4.67017 8.70239 4.67017C8.53091 4.67017 8.36121 4.70499 8.20359 4.77251C8.04596 4.84004 7.90369 4.93887 7.78539 5.06302L6.99939 5.87568L6.21339 5.06302C6.09509 4.93887 5.95282 4.84004 5.79519 4.77251C5.63757 4.70499 5.46787 4.67017 5.29639 4.67017C5.12491 4.67017 4.95521 4.70499 4.79759 4.77251C4.63996 4.84004 4.49769 4.93887 4.37939 5.06302C4.13548 5.3185 3.99939 5.65813 3.99939 6.01135C3.99939 6.36457 4.13548 6.7042 4.37939 6.95968L6.72006 9.38035C6.7561 9.41815 6.79945 9.44823 6.84746 9.46879C6.89547 9.48935 6.94716 9.49995 6.99939 9.49995C7.05162 9.49995 7.10331 9.48935 7.15132 9.46879C7.19934 9.44823 7.24268 9.41815 7.27872 9.38035L9.61939 6.95968C9.8633 6.7042 9.99939 6.36457 9.99939 6.01135C9.99939 5.65813 9.8633 5.3185 9.61939 5.06302V5.06302Z" stroke="none" />
</svg>



    <span>
          Save search
    </span>




  
  


    <div class="je2-button__tooltip_v2 js-button-tooltip-v2 _hidden">
      <div><span> This search is already saved <a class='je2-link' href='/buyer/saved-searches'>Saved searches</a> </span></div>
    </div>
</button>
</div>


  
    <aside class="je3-hamburger js-hamburger _loading _mobile-right" aria-hidden="true">
    <nav>
      <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>

    </nav>
  </aside>

</div>


  <script type="application/ld+json">
      {
        "@context": "http://schema.org",
        "@type": "BreadcrumbList",
        "name": "JamesEdition",
        "itemListElement": [
          {"@type":"ListItem","position":1,"item":{"@id":"https://www.jamesedition.com/","name":"JamesEdition"}}, {"@type":"ListItem","position":2,"item":{"@id":"https://www.jamesedition.com/real_estate","name":"🏡 Real Estate"}}, {"@type":"ListItem","position":3,"item":{"@id":"https://www.jamesedition.com/real_estate/france","name":"🏡 France"}}
        ]
      }
  </script>


      <div id="page_content" class="" role="main">
          

  <div class="JE-offcanvas__overlay js-toggle-offcanvas"></div>


  <section class="je2-search-page js-search-page _v2 _questionnaire-enabled">
    <div class="je2-search-page__right-side js-right-side _short">
      
<div class="je2-map js-map-root _loading _serp
  
  ">
    <div class="je2-map__close">
      <button class="je2-button js-close-map _onlyicon _noborder" aria-label="Close">

    <svg viewBox="0 0 32 32">
  <path d="M26.6 6.80002L25.2 5.40002L16 14.6L6.80002 5.40002L5.40002 6.80002L14.6 16L5.40002 25.2L6.80002 26.6L16 17.4L25.2 26.6L26.6 25.2L17.4 16L26.6 6.80002Z"/>
</svg>







  
  


</button>
    </div>

    <div class="je2-map__filter">
      <button class="je2-button js-filter-map _onlyicon _noborder" aria-label="Filters">

    <svg viewBox="0 0 32 32">
  <path d="M15 4C14.3542 4 13.7708 4.1875 13.25 4.5625C12.75 4.9375 12.3958 5.41667 12.1875 6H4V8H12.1875C12.3958 8.58333 12.75 9.0625 13.25 9.4375C13.7708 9.8125 14.3542 10 15 10C15.6458 10 16.2188 9.8125 16.7188 9.4375C17.2396 9.0625 17.6042 8.58333 17.8125 8H28V6H17.8125C17.6042 5.41667 17.2396 4.9375 16.7188 4.5625C16.2188 4.1875 15.6458 4 15 4ZM15 6C15.2917 6 15.5312 6.09375 15.7188 6.28125C15.9062 6.46875 16 6.70833 16 7C16 7.27083 15.9062 7.51042 15.7188 7.71875C15.5312 7.90625 15.2917 8 15 8C14.7292 8 14.4896 7.90625 14.2812 7.71875C14.0938 7.51042 14 7.27083 14 7C14 6.70833 14.0938 6.46875 14.2812 6.28125C14.4896 6.09375 14.7292 6 15 6ZM22 12C21.3542 12 20.7708 12.1875 20.25 12.5625C19.75 12.9375 19.3958 13.4167 19.1875 14H4V16H19.1875C19.3958 16.5833 19.75 17.0625 20.25 17.4375C20.7708 17.8125 21.3542 18 22 18C22.6458 18 23.2188 17.8125 23.7188 17.4375C24.2396 17.0625 24.6042 16.5833 24.8125 16H28V14H24.8125C24.6042 13.4167 24.2396 12.9375 23.7188 12.5625C23.2188 12.1875 22.6458 12 22 12ZM22 14C22.2917 14 22.5312 14.0938 22.7188 14.2812C22.9062 14.4688 23 14.7083 23 15C23 15.2708 22.9062 15.5104 22.7188 15.7188C22.5312 15.9062 22.2917 16 22 16C21.7292 16 21.4896 15.9062 21.2812 15.7188C21.0938 15.5104 21 15.2708 21 15C21 14.7083 21.0938 14.4688 21.2812 14.2812C21.4896 14.0938 21.7292 14 22 14ZM11 20C10.3542 20 9.77083 20.1875 9.25 20.5625C8.75 20.9375 8.39583 21.4167 8.1875 22H4V24H8.1875C8.39583 24.5833 8.75 25.0625 9.25 25.4375C9.77083 25.8125 10.3542 26 11 26C11.6458 26 12.2188 25.8125 12.7188 25.4375C13.2396 25.0625 13.6042 24.5833 13.8125 24H28V22H13.8125C13.6042 21.4167 13.2396 20.9375 12.7188 20.5625C12.2188 20.1875 11.6458 20 11 20ZM11 22C11.2917 22 11.5312 22.0938 11.7188 22.2812C11.9062 22.4688 12 22.7083 12 23C12 23.2708 11.9062 23.5104 11.7188 23.7188C11.5312 23.9062 11.2917 24 11 24C10.7292 24 10.4896 23.9062 10.2812 23.7188C10.0938 23.5104 10 23.2708 10 23C10 22.7083 10.0938 22.4688 10.2812 22.2812C10.4896 22.0938 10.7292 22 11 22Z"/>
</svg>




    <div class="je2-button__badge"></div>



  
  


</button>
    </div>

    <div class="je2-map__bell">
      <button class="je2-button js-bell-map _onlyicon _noborder" aria-label="Notify me via email when similar listings appear">

    <svg viewBox="0 0 32 32">
  <path d="M16 3C15.4375 3 14.9583 3.19792 14.5625 3.59375C14.1875 3.96875 14 4.4375 14 5L14.0312 5.25C12.8854 5.54167 11.8542 6.0625 10.9375 6.8125C10.0208 7.5625 9.30208 8.47917 8.78125 9.5625C8.26042 10.625 8 11.7708 8 13V22C8 22.2917 7.90625 22.5312 7.71875 22.7188C7.53125 22.9062 7.29167 23 7 23H6V25H13.1875C13.0625 25.3542 13 25.6875 13 26C13 26.8125 13.2917 27.5104 13.875 28.0938C14.4792 28.6979 15.1875 29 16 29C16.8125 29 17.5104 28.6979 18.0938 28.0938C18.6979 27.5104 19 26.8125 19 26C19 25.6875 18.9375 25.3542 18.8125 25H26V23H25C24.7083 23 24.4688 22.9062 24.2812 22.7188C24.0938 22.5312 24 22.2917 24 22V13.2812C24 12.0521 23.7396 10.8854 23.2188 9.78125C22.7188 8.65625 22.0104 7.69792 21.0938 6.90625C20.1771 6.11458 19.1354 5.5625 17.9688 5.25L18 5C18 4.4375 17.8021 3.96875 17.4062 3.59375C17.0312 3.19792 16.5625 3 16 3ZM15.5625 7C15.625 7 15.7188 7 15.8438 7H16.1875C17.25 7.04167 18.2292 7.35417 19.125 7.9375C20.0208 8.5 20.7188 9.26042 21.2188 10.2188C21.7396 11.1771 22 12.1979 22 13.2812V22C22 22.3125 22.0625 22.6458 22.1875 23H9.8125C9.9375 22.6458 10 22.3125 10 22V13C10 11.9583 10.2396 11 10.7188 10.125C11.2188 9.22917 11.8958 8.51042 12.75 7.96875C13.6042 7.40625 14.5417 7.08333 15.5625 7ZM16 25C16.2917 25 16.5312 25.0938 16.7188 25.2812C16.9062 25.4688 17 25.7083 17 26C17 26.2708 16.9062 26.5104 16.7188 26.7188C16.5312 26.9062 16.2917 27 16 27C15.7292 27 15.4896 26.9062 15.2812 26.7188C15.0938 26.5104 15 26.2708 15 26C15 25.7083 15.0938 25.4688 15.2812 25.2812C15.4896 25.0938 15.7292 25 16 25Z"/>
</svg>







  
  


</button>
    </div>

    <div class="je2-map__autosearch js-map-autosearch _loading">
      <label class="je2-checkbox
        js-checkbox
        _black 
        ">
  <input type="checkbox" name="" checked="checked" />
    <span class="je2-checkbox__icon">
      <svg><use xlink:href="#check"></use></svg>
    </span>
  <span class="je2-checkbox__text"
    
    >
    Search as I move the map
  </span>
</label>

      <button class="je2-button _noborder" aria-label="Search this area">

    <svg viewBox="0 0 18 17" stroke-width="0">
  <path d="M9 0.375C7.52865 0.375 6.16146 0.746094 4.89844 1.48828C3.67448 2.20443 2.70443 3.17448 1.98828 4.39844C1.24609 5.66146 0.875 7.02865 0.875 8.5C0.875 9.97135 1.24609 11.3385 1.98828 12.6016C2.70443 13.8255 3.67448 14.7956 4.89844 15.5117C6.16146 16.2539 7.52865 16.625 9 16.625C10.4714 16.625 11.8385 16.2539 13.1016 15.5117C14.3255 14.7956 15.2956 13.8255 16.0117 12.6016C16.7539 11.3385 17.125 9.97135 17.125 8.5H15.875C15.875 9.75 15.5625 10.9089 14.9375 11.9766C14.3255 13.0052 13.5052 13.8255 12.4766 14.4375C11.4089 15.0625 10.25 15.375 9 15.375C7.75 15.375 6.59115 15.0625 5.52344 14.4375C4.49479 13.8255 3.67448 13.0052 3.0625 11.9766C2.4375 10.9089 2.125 9.75 2.125 8.5C2.125 7.25 2.4375 6.09115 3.0625 5.02344C3.67448 3.99479 4.49479 3.17448 5.52344 2.5625C6.59115 1.9375 7.75 1.625 9 1.625C10.1849 1.625 11.2982 1.91146 12.3398 2.48438C13.3294 3.03125 14.1367 3.78646 14.7617 4.75H11.5V6H16.5V1H15.25V3.32422C14.4948 2.41276 13.5833 1.69661 12.5156 1.17578C11.4089 0.641927 10.237 0.375 9 0.375Z"/>
</svg>



    <span>
          Search this area
    </span>




  
  


</button>
      <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>

    </div>
    <div class="je2-map__count">
      <button class="je2-button js-count-map _noborder" data-value="Showing &lt;span&gt;&lt;/span&gt; of &lt;span&gt;&lt;/span&gt; results in this area" aria-label="Loading...">

    <svg viewBox="0 0 32 32">
  <path d="M7 9H3V11H7V9Z" />
  <path d="M7 15H3V17H7V15Z" />
  <path d="M7 21H3V23H7V21Z" />
  <path d="M29 9H9V11H29V9Z" />
  <path d="M29 15H9V17H29V15Z" />
  <path d="M29 21H9V23H29V21Z" />
</svg>



    <span>
          Loading...
    </span>




  
  


</button>
    </div>


  <div class="je2-map__heatmap__scale js-heatmap-scale _hidden">
    <div>Price per sqm</div>
    <div></div>
    <div>
      <div>Low</div>
      <div>
          <div style="background: rgba(253, 243, 216, 1)"></div>
          <div style="background: rgba(252, 216, 118, 1)"></div>
          <div style="background: rgba(243, 181, 101, 1)"></div>
          <div style="background: rgba(242, 147, 100, 1)"></div>
          <div style="background: rgba(229, 105, 91, 1)"></div>
      </div>
      <div>High</div>
    </div>
  </div>

  <div class="je2-map__zoom">
    <button class="je2-button js-plus-map _onlyicon _noborder" aria-label="Zoom in">

    <svg viewBox="0 0 32 32">
  <path d="M15 5V15H5V17H15V27H17V17H27V15H17V5H15Z"/>
</svg>







  
  


</button>
    <button class="je2-button js-minus-map _onlyicon _noborder" aria-label="Zoom out">

    <svg viewBox="0 0 32 32">
  <path d="M5 15V17H27V15H5Z"/>
</svg>







  
  


</button>
  </div>
  <div class="je2-map__map js-mapbox-map"></div>







    <button class="je2-button je2-map__draw-tip js-draw-tip _noborder _hidden">

  

    <span>
          Click on map to define your area
    </span>




  
  


</button>

    <button class="je2-button je2-map__area-too-big js-area-too-big _error _noborder _hidden">

  

    <span>
          A little too big! Draw smaller area
    </span>




  
  


</button>

    <button class="je2-button je2-map__filter-mobile js-filter-button _noborder">

    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 21 20"><g fill="none" stroke="#151515" stroke-width="1.6" clip-path="url(#a)"><circle cx="13.5" cy="6" r="3" /><path d="M.5 6h10M16.5 6h4" /><circle cx="7.5" cy="14" r="3" /><path d="M.5 14h4M10.5 14h10" /></g><defs><clipPath id="a"><path fill="#fff" d="M.5 0h20v20H.5z" /></clipPath></defs></svg>







  
  


</button>

    <button class="je2-button je2-map__back-to-list js-map-back-to-list _black _noborder _center">

    <svg><use xlink:href="#list-white"></use></svg>


    <span>
          Show list
    </span>




  
  


</button>

    <button class="je2-button je2-map__layer js-layer-control _noborder _show-tooltip-v2-on-hover _tooltip-on-the-left
            _tooltip-desktop-only" aria-label="Layers toggle">

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 21 21"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" fill="none" d="M11.267 1.53c.162.05.31.136.45.23l5.42 3.632c.146.098.302.18.457.26 1.369.712 1.369 1.779 0 2.49-.155.08-.31.163-.456.26l-5.421 3.633c-.14.094-.288.18-.45.23a3.582 3.582 0 0 1-1.943 0 1.742 1.742 0 0 1-.45-.23l-5.42-3.633a4.744 4.744 0 0 0-.457-.26c-1.368-.711-1.368-1.778 0-2.49.155-.08.311-.162.456-.26L8.874 1.76c.141-.094.288-.18.45-.23a3.581 3.581 0 0 1 1.943 0Z" /><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="M1.58 11.054c0 .757.516 1.62 1.183 2.025.133.08.271.15.401.233l6.344 4.067c.13.083.264.16.41.206.389.12.803.12 1.185-.003.14-.044.268-.118.391-.197l6.353-4.073c.13-.084.268-.153.4-.233.668-.404 1.183-1.268 1.183-2.025" fill="none" /></svg>







  
  


    <div class="je2-button__tooltip_v2 js-button-tooltip-v2 _hidden">
      <div>Map layers</div>
    </div>
</button>

    <button class="je2-button je2-map__draw-your-area js-draw-your-area _noborder _show-tooltip-v2-on-hover _tooltip-on-the-left
            _tooltip-desktop-only">

    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 21"><path stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" fill="none" d="m13.823 3.26-10.76 9.462 13.787 4.863-.588-5.866" /><circle cx="14.034" cy="3.294" r="2.084" fill="#fff" stroke="#000" stroke-width="1.6" /><circle cx="3.384" cy="12.816" r="2.084" fill="#fff" stroke="#000" stroke-width="1.6" /><circle cx="16.918" cy="17.525" r="2.084" fill="#fff" stroke="#000" stroke-width="1.6" fill="none" /></svg>







  
  


    <div class="je2-button__tooltip_v2 js-button-tooltip-v2 _hidden">
      <div>Draw custom area</div>
    </div>
</button>

    <button class="je2-button je2-map__remove-draw js-remove-draw _cyan _noborder">

    <svg viewBox="0 0 32 32">
  <path d="M26.6 6.80002L25.2 5.40002L16 14.6L6.80002 5.40002L5.40002 6.80002L14.6 16L5.40002 25.2L6.80002 26.6L16 17.4L25.2 26.6L26.6 25.2L17.4 16L26.6 6.80002Z"/>
</svg>







  
  


    <div class="je2-button__tooltip_v2 js-button-tooltip-v2 _hidden">
      <div>Remove selected area by clicking here</div>
    </div>
</button>

    <button class="je2-button je2-map__draw-tip-mobile js-draw-tip-mobile _noborder _center">

  

    <span>
          Tap on map to draw area
    </span>




  
  


</button>

    <button class="je2-button je2-map__heatmap-tip-mobile js-heatmap-tip-mobile _noborder">

  

    <span>
          Based on price per sqm
    </span>




  
  


</button>

    <button class="je2-button je2-map__area-too-big-mobile js-area-too-big-mobile _error _noborder _center">

  

    <span>
          Draw smaller area
    </span>




  
  


</button>

</div>

    </div>

<div class="je2-search-page__left-side">
  <div class="je2-search-page__above-header">
    <div class="je2-breadcrumbs">
  <ol>
        <li>
              <a href="/real_estate">Real Estate</a>
        </li>
        <li>
            <span>
                <div class="js-breadcrumb-overlay _loading" data-place-id=""
                     aria-label="Choose location">
                  <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>


                  <p>Most popular</p>
                  <ol class="js-most-popular"></ol>

                  <p>All</p>
                  <ol class="js-all"></ol>
                </div>
                <button class="je2-button js-breadcrumb-choose _noborder" data-value="France">

  

    <span>
          France
    </span>




    <svg><use xlink:href="#short-arrow"></use></svg>

  


</button>
            </span>
        </li>

      <li class="je2-breadcrumbs__next">
        <span>
          <div class="js-breadcrumb-overlay _loading" data-place-id="79652"
               aria-label="Choose location">
            <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>


            <p>Most popular</p>
            <ol class="js-most-popular"></ol>

            <p>All</p>
            <ol class="js-all"></ol>
          </div>
          <button class="je2-button js-breadcrumb-choose _noborder _gray">

  

    <span>
          Choose location
    </span>




    <svg><use xlink:href="#short-arrow"></use></svg>

  


</button>
        </span>
      </li>

  </ol>
</div>

  </div>
  <div class="je2-search-page__header">
    <div class="je2-search-page__header__left">
      <h1>Luxury Homes for Sale in France</h1>
    </div>
    <div class="je2-search-page__header__right
      
      _w-questionnaire">
      <span>
          54,100+ listings
          
      </span>
      <div>
        <span>Sort:</span>
        <div class="je2-select _with-placeholder">
  <svg class="je2-select__right-icon"><use xlink:href="#arrow-down"></use></svg>
  <select name="order" id="order" aria-label="order"><option value="premium">Premium</option>
<option value="popular">Popular</option>
<option value="recent">Recent</option>
<option value="price_asc">Price lowest first</option>
<option value="price_desc">Price highest first</option>
<option value="living_area_asc">Smallest living area</option>
<option value="living_area_desc">Biggest living area</option>
<option value="price_per_sqm_asc">Price per ㎡ lowest first</option>
<option value="price_per_sqm_desc">Price per ㎡ highest first</option></select>
    <span>Premium</span>
</div>
      </div>
    </div>
  </div>


    <div class="je2-search-page__hits js-je-listings-hits _search-result">
          <article class="ListingCard _v3 _promoted" data-id="15870025" data-price-usd="1079629" data-price-euro="927000" data-price="927000" data-currency="EUR" data-country-code="FR" data-country="France" data-country-subdivision="Provence-Alpes-Côte d&#39;Azur" data-city="Tanneron" data-office-id="390855" data-agent-id="1799655" data-group-id="395" data-category="RealEstate" data-lat="43.58946" data-lng="6.87163" data-position="Promoted" data-serp-position="0" data-type="Listing card">
  <a href="/real_estate/tanneron-france/for-sale-exceptional-sea-view-villa-in-tanneron-french-riviera-15870025" title="For Sale – Exceptional Sea View Villa in Tanneron, French Riviera" target="_blank" class="js-link">
    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Virtual tour
    </div>
    <div class="ListingCard__badges__text">
        Promoted
    </div>
</div>


    <div class="ListingCard__save js-heart "
         data-listing-id="15870025"
         role="button" tabindex="0" aria-label="Save listing">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
      <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 29
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 29 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <picture>
          <source media="(max-width: 500px)"
                  srcset="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/a434c3e3-29d1-4b52-8318-fadffb52a835/je/380xxsxm.jpg,
                          https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/a434c3e3-29d1-4b52-8318-fadffb52a835/je/760x470xc.jpg 2x">
          <source media="(max-width: 700px)"
                  srcset="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/a434c3e3-29d1-4b52-8318-fadffb52a835/je/1000x620xc.jpg">
          <source media="(min-width: 701px)"
                  srcset="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/a434c3e3-29d1-4b52-8318-fadffb52a835/je/556x342xcxm.jpg,
                          https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/a434c3e3-29d1-4b52-8318-fadffb52a835/je/1112x684xcxm.jpg 2x">
          <img src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/a434c3e3-29d1-4b52-8318-fadffb52a835/je/507x312xc.jpg" fetchpriority="high" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 1">
        </picture>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/c1a88107-0d9a-45a6-b763-03c60f4dfb47/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/ee8b51c7-3027-4743-a878-d3afb0901fe9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/eea5eca8-824e-4620-9c73-dfb91fda32d1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/b9f86be1-dbcb-4675-a87d-422a058251de/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/9f65ea40-3391-4627-a809-bff4eb3c8744/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/57a86c4f-6088-45af-8719-3422d472e765/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/cc7666de-b283-4d54-830d-1a3f8b04eb44/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/24684cb7-0ac4-477d-8f4c-05813a5735c8/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/5ee8d451-ab19-4b9f-b4ec-4478fa3c69f1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

      <div class="ListingCard__side-photos">
          <div class="ListingCard__side-photo je-background-pixel">
              <img alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 1" class="je2-lazy-load" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/c1a88107-0d9a-45a6-b763-03c60f4dfb47/je/355x210xc.jpg" src="" />
          </div>
          <div class="ListingCard__side-photo je-background-pixel">
              <img alt="House in Tanneron, Provence-Alpes-Côte d&#39;Azur, France 2" class="je2-lazy-load" data-src="https://img.jamesedition.com/listing_images/2025/07/01/12/41/51/ee8b51c7-3027-4743-a878-d3afb0901fe9/je/355x210xc.jpg" src="" />
          </div>
      </div>

</a>
  <div class="ListingCard__right">

    <a href="/real_estate/tanneron-france/for-sale-exceptional-sea-view-villa-in-tanneron-french-riviera-15870025" title="For Sale – Exceptional Sea View Villa in Tanneron, French Riviera" target="_blank" class="js-link">
      <div class="ListingCard__description">
        <div class="ListingCard__price">
            €927,000
        </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">3 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">180 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "3",
        "address": "Tanneron, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


        <div class="ListingCard__title">
          House<span> in </span>Tanneron, Provence-Alpes-Côte d&#39;Azur, France
        </div>

        <div class="ListingCard__actions">
            <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
        </div>
      </div>

      <div class="ListingCard__right__container">
        <div class="ListingCard__right__features">
          <ul>
              <li><svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M18.75 9.37499c-.0017-.83357-.2419-1.64925-.6923-2.35068-.4504-.70142-1.0921-1.25928-1.8494-1.60766.0676-.35885.0544-.72823-.0385-1.08137-.0928-.35315-.2631-.68121-.4984-.96041-.2353-.27921-.5298-.50256-.8622-.65388-.3323-.15132-.6941-.22681-1.0592-.221-.0525 0-.1017.0125-.1542.01583-.4011-.58318-.938-1.06006-1.5644-1.38952-.6265-.329455-1.3236-.501605-2.03142-.501605-.70779 0-1.40496.17215-2.0314.501605-.62644.32946-1.16335.80634-1.56443 1.38952-.0525-.00333-.10167-.01583-.15417-.01583-.3651-.00581-.72693.06968-1.05925.221-.33232.15132-.62682.37467-.86215.65388-.23533.2792-.40559.60726-.49846.96041-.09287.35314-.10601.72252-.03847 1.08137-.83373.38362-1.52536 1.02022-1.97664 1.81936-.45128.79913-.63925 1.72016-.5372 2.63222.10205.91207.48892 1.76877 1.10565 2.44837.61673.6797 1.43196 1.1477 2.32986 1.3376.22029.4754.54743.8935.95591 1.2217.40848.3281.88725.5575 1.39897.6702.51173.1127 1.04256.1056 1.55111-.0206.50855-.1262.98106-.3683 1.38067-.7072.39982.3389.87242.5807 1.38112.7068.5087.1261 1.0396.1329 1.5513.02.5118-.113.9905-.3426 1.3989-.671.4083-.3285.7353-.7468.9553-1.2224.9798-.2085 1.8583-.7469 2.4887-1.5254.6304-.7784.9745-1.7496.9747-2.75131v0ZM10 6.875v12.5" /><path d="M10 12.5c2.5 0 3.75-1.25 3.75-3.75M9.99999 10c-.41694.0252-.83448-.03843-1.22502-.18657-.39055-.14815-.74521-.37748-1.04057-.67284-.29536-.29535-.52469-.65002-.67283-1.04057-.14815-.39054-.21174-.80808-.18658-1.22502" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>
<span>Garden</span></li>
              <li><svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M2.29167 2.39999H17.7083c.1105 0 .2165.0439.2947.12204.0781.07814.122.18412.122.29463v2.5H1.875v-2.5c0-.11051.0439-.21649.12204-.29463.07814-.07814.18412-.12204.29463-.12204v0Z" /><path d="M1.875 5.31665h16.25v2.5c0 .11051-.0439.21649-.122.29463-.0782.07814-.1842.12204-.2947.12204H2.29167c-.11051 0-.21649-.0439-.29463-.12204-.07814-.07814-.12204-.18412-.12204-.29463v-2.5 0ZM19.375 13.4333c0 .4421-.1756.866-.4882 1.1785-.3125.3126-.7364.4882-1.1785.4882H2.29167c-.44203 0-.86595-.1756-1.17851-.4882C.800595 14.2993.625 13.8754.625 13.4333c0-.442.175595-.8659.48816-1.1785.31256-.3125.73648-.4881 1.17851-.4881H17.7083c.4421 0 .866.1756 1.1785.4881.3126.3126.4882.7365.4882 1.1785ZM4.375 8.23334v3.53336M15.625 8.23334v3.53336M4.375 1.14999v1.25M15.625 1.14999v1.25M2.91675 15.1l-1.25 3.75M17.0833 15.1l1.25 3.75" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>
<span>Terrace</span></li>
              <li><svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M.625 19.0117c.8889.3584 1.86199.4541 2.8037.2758.94171-.1783 1.81245-.6231 2.5088-1.2817.92861.8792 2.15875 1.3691 3.4375 1.3691 1.2787 0 2.5089-.4899 3.4375-1.3691.8768.8299 2.0242 1.3146 3.2304 1.3645 1.2062.05 2.3898-.3382 3.3321-1.0928M14.375 15.625v-12.5c0-.66304.2634-1.29893.7322-1.76777C15.5761.888392 16.212.625 16.875.625s1.2989.263392 1.7678.73223c.4688.46884.7322 1.10473.7322 1.76777M6.875 15.625v-12.5c0-.66304.26339-1.29893.73223-1.76777C8.07607.888392 8.71196.625 9.375.625c.663 0 1.2989.263392 1.7678.73223.4688.46884.7322 1.10473.7322 1.76777M6.875 9.375h7.5M6.875 13.125h7.5M6.875 5.625h7.5" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>
<span>Pool</span></li>
              <li><svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M.623291 13.125v6.25M9.99829 13.125v6.25M19.3733 13.125v6.25M19.3733 15H.623291M19.3733 17.5H.623291M1.24829 10.625l5.625-3.75 5.62501 3.75M11.2483 4.375c1.0355 0 1.875-.83947 1.875-1.875S12.2838.625 11.2483.625c-1.0355 0-1.87501.83947-1.87501 1.875s.83951 1.875 1.87501 1.875Z" /><path d="M9.99829 8.95833 14.9983 5.625l4.3767 2.9175" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>
<span>Mountain View</span></li>
              <li><svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M7.5 19.375h5M10 19.375v-7.2408M15.7391 5.43083c.155 1.00881.0415 2.04066-.3292 2.9916-.3708.95094-.9856 1.78737-1.7825 2.42507-1.0296.8237-2.3089 1.2725-3.62748 1.2725-1.31857 0-2.59788-.4488-3.6275-1.2725v0C5.5755 10.2098 4.96072 9.37337 4.59 8.42243c-.37073-.95094-.48429-1.98279-.32924-2.9916L4.91659 1.155c.02273-.1478.0977-.28256.21131-.379806s.25831-.150534.40786-.150192h8.92834c.1492.000056.2936.053525.4068.150735.1133.09721.188.231743.2107.379263l.6575 4.27583ZM4.23413 5.625H15.7658" /></svg>
<span>Wine Cellar</span></li>
              <li><svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M19.3758 14.1667c-.9621.3899-2.0223.4684-3.0313.2242-1.0091-.2441-1.9162-.7984-2.5937-1.5851-.4637.5409-1.039.975-1.6863 1.2726-.6472.2976-1.3512.4517-2.0637.4517-.71239 0-1.41639-.1541-2.06367-.4517-.64728-.2976-1.22253-.7317-1.6863-1.2726-.67802.7862-1.58554 1.3398-2.59478 1.5831-1.00924.2432-2.06935.1637-3.03105-.2272M.625 17.7608c.96201.3903 2.02222.469 3.03131.225 1.0091-.2439 1.91624-.7983 2.59369-1.585.46376.5408 1.03901.9749 1.68629 1.2725.64729.2977 1.35128.4518 2.06371.4518.7124 0 1.4164-.1541 2.0637-.4518.6473-.2976 1.2225-.7317 1.6863-1.2725.6775.7866 1.5846 1.341 2.5936 1.5851 1.0091.2441 2.0693.1657 3.0314-.2242M5 10.625c0-1.32608.52678-2.59785 1.46447-3.53553C7.40215 6.15178 8.67392 5.625 10 5.625c1.3261 0 2.5979.52678 3.5355 1.46447C14.4732 8.02715 15 9.29892 15 10.625M2.50073 10.625H.625732M19.3757 10.625h-1.875M10.0007 1.875V3.75M15.0007 5.625l1.25-1.25M5.00073 5.625l-1.25-1.25" /></svg>
<span>Sea View</span></li>
              <li><svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M19.3758 14.1667c-.9621.3899-2.0223.4684-3.0313.2242-1.0091-.2441-1.9162-.7984-2.5937-1.5851-.4637.5409-1.039.975-1.6863 1.2726-.6472.2976-1.3512.4517-2.0637.4517-.71239 0-1.41639-.1541-2.06367-.4517-.64728-.2976-1.22253-.7317-1.6863-1.2726-.67802.7862-1.58554 1.3398-2.59478 1.5831-1.00924.2432-2.06935.1637-3.03105-.2272M.625 17.7608c.96201.3903 2.02222.469 3.03131.225 1.0091-.2439 1.91624-.7983 2.59369-1.585.46376.5408 1.03901.9749 1.68629 1.2725.64729.2977 1.35128.4518 2.06371.4518.7124 0 1.4164-.1541 2.0637-.4518.6473-.2976 1.2225-.7317 1.6863-1.2725.6775.7866 1.5846 1.341 2.5936 1.5851 1.0091.2441 2.0693.1657 3.0314-.2242M5 10.625c0-1.32608.52678-2.59785 1.46447-3.53553C7.40215 6.15178 8.67392 5.625 10 5.625c1.3261 0 2.5979.52678 3.5355 1.46447C14.4732 8.02715 15 9.29892 15 10.625M2.50073 10.625H.625732M19.3757 10.625h-1.875M10.0007 1.875V3.75M15.0007 5.625l1.25-1.25M5.00073 5.625l-1.25-1.25" /></svg>
<span>Water View</span></li>
              <li><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M.605 18.641h18.75M1.855 7.391h16.25v11.25H1.855V7.392ZM19.355 5.891a.627.627 0 0 0-.333-.551L10.272.673a.629.629 0 0 0-.589 0L.933 5.34A.627.627 0 0 0 .6 5.89v.875a.625.625 0 0 0 .625.625h17.5a.625.625 0 0 0 .625-.625l.005-.875Z" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /><path d="M4.355 9.891h11.25v8.75H4.355v-8.75ZM6.855 13.641h6.25M6.855 16.141h6.25" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /></svg>
<span>Garage</span></li>
              <li><svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M.6 16.9H10A6.9 6.9 0 1 0 10 3H.6M2 19.4A1.3 1.3 0 0 1 .6 18V2A1.3 1.3 0 0 1 2 .6H10a9.4 9.4 0 1 1 0 18.8H1.9Z" /><path d="M4 7.3v9.6H.6V6.5h2.5a.8.8 0 0 1 .9.8v0Z" /><path d="M7.3 10.6V17H4V9.8h2.5a.8.8 0 0 1 .8.8v0ZM7.3 16.9V13h2.5a.8.8 0 0 1 .8.9v2.8" /></g><defs><clipPath id="a"><path fill="#fff" d="M20 0v20H0V0z" /></clipPath></defs></svg>
<span>Basement</span></li>
          </ul>
        </div>

        <div class="ListingCard__right__description">Nestled in the sought-after commune of Tanneron, just 4 km from all amenities, this stunning 180 m² villa offers absolute peace and quiet in a beautiful countryside setting — with breathtaking views o</div>
      </div>

</a>
    <a href="/offices/real_estate/veronique-costaz-immobilier-390855" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/10/13/32/8bdfa1d8-ed6e-4cd6-b8ef-6d335c8f6663/je/320x160xs.jpg" data-type="office_logo" data-watermark="true" alt="Véronique Costaz Immobilier" src="" />

      <div class="ListingCard__footer__agent">Alexandre Dubrana</div>
  </div>
</a>
  </div>
</article>
            
<div class="je2-static-map js-static-map">
  <div class="je2-static-map__block-entry" style='background-image: url("https://api.mapbox.com/styles/v1/jamesedition/ckcd8kyfr0ofa1io8eo4zwxa3/static/[-5.5591, 41.31433, 9.6624999, 51.1241999]/500x550@2x?access_token=pk.eyJ1IjoiamFtZXNlZGl0aW9uIiwiYSI6ImNrc2hjZnY2bzFiM20yd3RiZnd6dTJ3dHYifQ.FZcx6OUbx12Y_icPdxMeBg&amp;attribution=false&amp;padding=50&amp;addlayer=%7B%22id%22%3A%22all%22%2C%22type%22%3A%22circle%22%2C%22source%22%3A%7B%22type%22%3A%22vector%22%2C%22url%22%3A%22mapbox%3A%2F%2Fjamesedition.difstjhl%22%7D%2C%22source-layer%22%3A%22all%22%2C%22paint%22%3A%7B%22circle-color%22%3A%22%23000000%22%2C%22circle-stroke-width%22%3A2%2C%22circle-stroke-color%22%3A%22%23fff%22%2C%22circle-radius%22%3A4%7D%2C%22filter%22%3A%5B%22all%22%2C%5B%22in%22%2C%5B%22get%22%2C%22n%22%5D%2C%5B%22literal%22%2C%5B%22france%22%5D%5D%5D%5D%7D")'>
      <button class="je2-button js-show-map-view">

    <svg viewBox="0 0 16 18" fill="none">
  <path fill="none" d="M5.5998 15.2856L2.15779 16.1051C1.46311 16.2705 0.799805 15.7266 0.799805 14.9915V3.62315C0.799805 3.09104 1.15601 2.62933 1.6589 2.5096L5.5998 1.57129V15.2856Z" stroke-width="1.6" stroke-linejoin="round" />
  <path fill="none" d="M5.59961 15.2856L10.3996 16.4284V2.71415L5.59961 1.57129V15.2856Z" stroke-width="1.6" stroke-linejoin="round" />
  <path fill="none" d="M15.1999 14.377C15.1999 14.9091 14.8437 15.3708 14.3408 15.4906L10.3999 16.4288V2.71456L13.8419 1.89504C14.5365 1.72964 15.1999 2.27355 15.1999 3.00859V14.377Z" stroke-width="1.6" stroke-linejoin="round" />
</svg>



    <span>
          Show all results on map
    </span>




  
  


</button>
  </div>
</div>

        <div class="ListingCard _ar-70" data-id="16460690" data-price-usd="777752" data-price-euro="667800" data-price="667800" data-currency="EUR" data-country-code="FR" data-country="France" data-country-subdivision="Nouvelle-Aquitaine" data-city="Angoulême" data-office-id="359439" data-agent-id="1728859" data-category="RealEstate" data-lat="45.6488766" data-lng="0.1567288" data-position="Search" data-serp-position="1" data-type="Listing card">
  <a href="/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690" title="LUXURY FAMILY ESTATE WITH HEATED POOL AND OUTBUILDINGS IN VARS, NEAR ANGOULEME" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Video
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16460690">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 37
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 37 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/e4dfd4f4-c406-4c2c-a387-093cb23acf78/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/5148de7a-c860-4180-8099-f16a9674c408/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/f043a991-eabb-43fa-a780-64245bbf8e69/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/53dd69df-1893-4425-a491-47a797201769/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/fcdc1bd6-310d-4346-945b-17e89d0b5caf/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €667,800
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">2 Baths</span>
    <span class="ListingCard__tag">256 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "2",
        "numberOfBedrooms": "4",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/elite-group-real-estate-359439" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/05/05/12/16/09/b5c8a2bb-244b-4c69-86ed-f507f830785f/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="ELITE GROUP Real Estate" src="" />

      <div class="ListingCard__footer__agent">Antoine BEAUDOU</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/05/05/09/56/36/b49713c4-1257-4f62-918b-053cc5df1dc9/je/80x80xc.jpg" alt="Antoine BEAUDOU photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16247522" data-price-usd="920072" data-price-euro="790000" data-price="790000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Cannes" data-office-id="436908" data-agent-id="1913227" data-group-id="2771" data-category="RealEstate" data-lat="49.859704549" data-lng="0.707123093" data-position="Search" data-serp-position="2" data-type="Listing card">
  <a href="/real_estate/saint-valery-en-caux-france/rare-beachfront-villa-with-2-converted-dependencies-near-marina-beach-and-restaurants-16247522" title="RARE BEACHFRONT VILLA WITH 2 CONVERTED DEPENDENCIES NEAR MARINA, BEACH, AND RESTAURANTS" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16247522">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 20
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 20 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/d6eee1e8-eb23-4f0f-93a7-889218c2e307/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/13462b31-e5ea-43ca-85cd-94d479e34394/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/3e23e79f-9226-42b7-a872-45c31efcf952/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/e925d04f-f3c6-479d-a675-0e4ebcf9527e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/2ff764be-3c9c-4437-a5a6-4415cf5d7466/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/fd2022db-e96f-4d94-8b94-0c8407d9de82/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/5bef92a0-231f-4d91-8467-1174325515a4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/46d30023-abe7-4e94-b559-be304c7df61c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/dc9c92c0-e1e7-4e35-bc1a-984e804a1aa4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Cannes, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/58/40c2b8be-2bb9-4271-a310-5389173c2758/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €790,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">10 Beds</span>
    <span class="ListingCard__tag">6 Baths</span>
    <span class="ListingCard__tag">330 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "6",
        "numberOfBedrooms": "10",
        "address": "Cannes, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Cannes, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  
</div>
        <div class="ListingCard _ar-70" data-id="16368872" data-price-usd="2771863" data-price-euro="2380000" data-price="2380000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Nice" data-office-id="450218" data-agent-id="1934464" data-group-id="2771" data-category="RealEstate" data-lat="43.712363989" data-lng="7.237937874" data-position="Search" data-serp-position="3" data-type="Listing card">
  <a href="/real_estate/nice-france/house-for-sale-in-nice-west-360m-9-rooms-2-380-000-16368872" title="House for Sale in Nice West, 360m² 9 Rooms 2,380,000€" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16368872">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 10
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 10 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/2206eb67-a028-483a-b6f9-521d56b72468/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/f55049a3-10bb-40ec-8111-68f23c9599a1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/e84b18be-f72d-4868-9449-5bf522e18ae4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/85582c08-5837-42e7-9d06-993b0a6fb658/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/57d43beb-d374-4df7-9598-5078204a2d17/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/2d5f35ca-676f-4ac4-a5a0-6a4081462d2b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/cde200f4-78c1-4a9f-9807-2ca095e2e97c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/ee075935-1a57-4365-bafd-0f8e1c2d6ba9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/183921ca-c2ce-48c5-9fbf-3581a73b32b4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/10/13/34/30/f250446e-4649-4ef3-bd48-181fc95d83d7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €2,380,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">7 Beds</span>
    <span class="ListingCard__tag">360 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "",
        "numberOfBedrooms": "7",
        "address": "Nice, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Nice, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  
</div>
        <div class="ListingCard _ar-70" data-id="16293592" data-price-usd="1007421" data-price-euro="865000" data-price="865000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Grasse" data-office-id="105684" data-agent-id="1596933" data-group-id="395" data-category="RealEstate" data-lat="43.63665" data-lng="6.91244" data-position="Search" data-serp-position="4" data-type="Listing card">
  <a href="/real_estate/grasse-france/grasse-saint-jacques-charming-family-villa-4-bedrooms-16293592" title="Grasse – Saint-Jacques – Charming Family Villa – 4 Bedrooms" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Video
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16293592">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 23
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 23 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/01/14/19/07/047de42b-2348-4522-b5dc-cf1b4496a331/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/01/14/19/07/7573bc17-5b88-48e0-aa5a-4bc1a38889e2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/01/14/19/07/0ab83e5d-28da-47e4-a000-7c7efdf706bc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/01/14/19/07/a31586cb-261c-47a8-b001-3441c48e748f/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/01/14/19/07/b0dd3121-e28f-43fa-8497-3f96be2cc619/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/01/14/19/07/befd80ac-4985-4d2c-af81-4ed0baddc346/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/14/16/27/36/b5d4b0f0-ab9e-452d-a569-59f7c1558b25/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/01/14/19/07/a54bfd74-bed1-4706-b669-e8ce690d8a18/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/01/14/19/07/f92cc77f-17fb-481c-9a85-cf5990650a44/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/01/14/19/07/79b76987-f7d8-48e5-9741-1ab3ccc1b72a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €865,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">2 Baths</span>
    <span class="ListingCard__tag">200 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "2",
        "numberOfBedrooms": "4",
        "address": "Grasse, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Grasse, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/barnes-valbonne-105684" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/10/11/34/8995f51e-79fe-4e49-8741-bcd5072033d7/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="BARNES Valbonne" src="" />

      <div class="ListingCard__footer__agent">Camille Charles</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/10/20/898727db-17b1-4d58-b282-6328982acd9d/je/80x80xc.jpg" alt="Camille Charles photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16400177" data-price-usd="1106416" data-price-euro="950000" data-price="950000" data-currency="EUR" data-country-code="FR" data-country="France" data-country-subdivision="" data-city="Besançon" data-office-id="407890" data-agent-id="1938749" data-group-id="3728" data-category="RealEstate" data-lat="47.2551269927" data-lng="6.0192810348" data-position="Search" data-serp-position="5" data-type="Listing card">
  <a href="/real_estate/besancon-france/prestigious-villa-overlooking-vesoul-the-villa-saint-martin-opens-its-doors-to-you-16400177" title="PRESTIGIOUS VILLA OVERLOOKING VESOUL : THE VILLA SAINT MARTIN OPENS ITS DOORS TO YOU...        " target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16400177">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 27
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 27 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 1" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/10/99bc59c3-3ff0-4df4-b87e-f36038320f9b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 2" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/10/c1ec900f-5e64-40e2-9a91-bb04f67ed7b7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 3" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/39/b5e04576-55b0-4437-89cc-4e37e1fb9999/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 4" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/10/ef672c6a-81d7-453b-b6ec-200b276bc276/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 5" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/39/28d45609-aa9b-4b19-a8ab-a4c1d0f64547/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 6" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/09/5b51b292-8ce0-4327-bcec-bbb20ea412fe/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 7" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/09/4c7c0736-c5c4-4e69-889f-1b71b83fc511/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 8" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/10/fbe63b68-3afe-4c88-bbb3-9616f4460299/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 9" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/10/12d8c7c3-0f02-47cc-84e2-a12c66184639/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Estate in Besançon, Bourgogne-Franche-Comté, France 10" data-src="https://img.jamesedition.com/listing_images/2025/11/05/14/04/39/87f5175e-ec21-4e6f-aa6a-eaa9b6020c8f/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €950,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">5 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">330 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Estate",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "5",
        "address": "Besançon, Bourgogne-Franche-Comté, France"
    }
</script>


      <div class="ListingCard__title">
          Estate<span> in </span>Besançon, Bourgogne-Franche-Comté, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/arriere-cour-immobilier-407890" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/10/06/16/23/40/d202435c-ce66-47f5-8fec-47986e53077d/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Arrière-Cour Immobilier" src="" />

      <div class="ListingCard__footer__agent">Julie ROWLETT</div>
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16138374" data-price-usd="1687459" data-price-euro="1448900" data-price="1448900" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Landéda" data-office-id="10637" data-group-id="2" data-category="RealEstate" data-lat="48.5870399" data-lng="-4.5721318" data-position="Search" data-serp-position="6" data-type="Listing card">
  <a href="/real_estate/landeda-france/landeda-sainte-marguerite-peninsula-full-sea-view-in-a-peaceful-location-16138374" title="Landéda Sainte Marguerite Peninsula, Full Sea View In A Peaceful Location" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16138374">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 14
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 14 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 1" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/559af405-0b43-4ab2-adb3-a622a4d261f9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 2" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/88621205-f6b1-479d-b7db-4e97b0b2029a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 3" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/857fdf0a-8b39-44d2-9275-3106fa7a739e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 4" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/54f52ee8-9db4-4af8-a36b-086eb8b75584/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 5" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/6291350f-5081-4d2f-acb9-40e37df7f72e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 6" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/796f7d5a-12c6-4ab6-adb9-b8d5c6435375/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 7" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/dc271d31-ac34-430f-8653-327e18f20b53/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 8" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/bfc02b70-c2eb-4b1d-9cf5-246d917c9dff/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 9" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/5c12001f-092b-4611-9215-3539b32d754c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Landéda, Brittany, France 10" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/7cf2d76e-59fe-4c71-a1ed-74671a7fc67d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,448,900
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">6 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">180 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "6",
        "address": "Landéda, Brittany, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Landéda, Brittany, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/bretagne-sud-sotheby-s-international-realty-10637" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/08/36/26/daf7d24f-eccc-4ede-8f10-f28c678b6d7f/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Bretagne Sud Sotheby&#39;s International Realty" src="" />

  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16397640" data-price-usd="1741149" data-price-euro="1495000" data-price="1495000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Lyon" data-office-id="141245" data-agent-id="1670925" data-category="RealEstate" data-lat="45.7591534" data-lng="4.7777898" data-position="Search" data-serp-position="7" data-type="Listing card">
  <a href="/real_estate/tassin-la-demi-lune-france/house-tassin-la-demi-lune-16397640" title="House, Tassin La Demi Lune" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16397640">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 14
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 14 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 1" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/08b6dce3-70c6-468f-a3a0-f89f95715b5a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 2" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/36a480ee-83b6-4c86-81dc-9b5a8f1a24a9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 3" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/e9e7b1f2-2cde-4ee3-9e09-a7835f01ef77/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 4" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/34804565-5858-4452-8879-7e0b5804ead2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 5" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/453dfeea-2880-473b-8942-9466f92c9b2d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 6" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/0562e921-68b5-473e-b3fa-ea4464b47f36/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 7" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/89e13bfa-cc6f-419d-bb06-7d8d3c987683/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 8" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/6c903fa7-8fe6-4cfd-9f50-a70aac62d3dc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 9" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/2320d7c0-c1f1-46b8-9b3a-edadb0ca7d5e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Lyon, Auvergne-Rhône-Alpes, France 10" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/b53d29bc-d302-4120-8b94-57942312cf7f/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,495,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">5 Beds</span>
    <span class="ListingCard__tag">190 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "",
        "numberOfBedrooms": "5",
        "address": "Lyon, Auvergne-Rhône-Alpes, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Lyon, Auvergne-Rhône-Alpes, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/kretz-real-estate-141245" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2023/11/30/14/20/45/92ffd19f-cd56-4705-a156-7b4f05c2c44b/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Kretz Real Estate" src="" />

      <div class="ListingCard__footer__agent">Romain Djerraf</div>
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="15998576" data-price-usd="2853389" data-price-euro="2450000" data-price="2450000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Cassis" data-office-id="230906" data-agent-id="1752554" data-group-id="2" data-category="RealEstate" data-lat="43.2186071" data-lng="5.537959499999999" data-position="Search" data-serp-position="8" data-type="Listing card">
  <a href="/real_estate/cassis-france/cassis-contemporary-villa-with-panoramic-sea-view-15998576" title="Cassis – Contemporary Villa With Panoramic Sea View" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="15998576">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 15
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 15 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/09/01/16/10/55/c4567ec9-8c7c-4eca-9fd6-dca19d36b989/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/07/31/15/18/38/c088b903-d436-4c01-a336-06e60f05aed3/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/07/31/15/18/38/b3c9e81e-850a-4ee0-b74e-e0cb209de105/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/09/01/16/10/55/6fc76dc8-96de-4f0e-9fc8-e2567f203522/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/09/01/16/10/55/c7533c79-5006-4421-88f5-1ca148b5f148/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/09/01/16/10/55/6dfb1823-acc0-4ed7-a2e8-e5f4509f0bd8/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/09/01/16/10/55/f99513a1-f7a6-4fe0-b121-55399fa81997/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/09/01/16/10/55/1c71ebd1-7a78-40d0-a64d-fc08f094b532/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/09/01/16/10/55/eab204a4-92d2-4215-9961-dc05d315f2ee/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Cassis, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/09/01/16/10/55/c52e44d8-07e7-4dbe-aca9-74b36b914a16/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €2,450,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">7 Beds</span>
    <span class="ListingCard__tag">9 Baths</span>
    <span class="ListingCard__tag">232 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "9",
        "numberOfBedrooms": "7",
        "address": "Cassis, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Cassis, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/cassis-sotheby-s-international-realty-230906" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/08/31/41/94d0bf5f-bba7-448f-8582-7465e79438d1/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Cassis Sotheby&#39;s International Realty" src="" />

  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16276704" data-price-usd="2550580" data-price-euro="2190000" data-price="2190000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Gordes" data-office-id="136129" data-agent-id="1524064" data-category="RealEstate" data-lat="43.91131499999999" data-lng="5.200176" data-position="Search" data-serp-position="9" data-type="Listing card">
  <a href="/real_estate/gordes-france/exceptional-gordes-retreat-with-landscaped-grounds-and-refined-i-16276704" title="Exceptional Gordes retreat with landscaped grounds and refined i" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Virtual tour
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16276704">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 24
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 24 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/f2f17d3c-4fcd-4c77-a317-154909888c63/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/51920174-dc15-4062-9923-b0a57b2e1b2d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/eb730af3-2592-433a-b745-19d32f948c9e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/f6833293-66c6-4866-bce7-d5ce615c8b23/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/cfc1b223-55b0-4232-8456-351b31144104/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/36d1b377-9d1f-409f-8a86-f6a1799ff09a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/52c777ac-0a5a-48ba-b377-51f2351fd199/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/12b451b3-b618-42c4-95f0-62de0f0b8b57/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/ef439d05-8eac-4a0e-a933-6e01ca449e94/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Gordes, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/09/27/04/06/22/dd860855-94bd-4131-b676-a21bdfca6d14/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €2,190,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">5 Beds</span>
    <span class="ListingCard__tag">3 Baths</span>
    <span class="ListingCard__tag">296 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "3",
        "numberOfBedrooms": "5",
        "address": "Gordes, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Gordes, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/maison-victoire-immobilier-136129" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2022/07/25/11/00/11/53182c06-b832-43de-925c-65d796d3ca62/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Maison Victoire Immobilier" src="" />

      <div class="ListingCard__footer__agent">MAISON VICTOIRE Immobilier</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2024/11/21/10/21/39/fa052d3a-a5c9-47f3-a785-5b6551168885/je/80x80xc.jpg" alt="MAISON VICTOIRE Immobilier photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16225846" data-price-usd="1123886" data-price-euro="965000" data-price="965000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Nice" data-office-id="128177" data-group-id="197" data-category="RealEstate" data-lat="43.71755" data-lng="7.23023" data-position="Search" data-serp-position="10" data-type="Listing card">
  <a href="/real_estate/nice-france/villa-in-nice-saint-pierre-de-feric-sea-view-16225846" title="VILLA IN NICE SAINT-PIERRE DE FÉRIC - SEA VIEW" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        New price
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16225846">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 14
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 14 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/09/23/14/08/29/1cb3b079-686f-4ba5-92d8-9f37c5d7aedc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/09/23/14/08/29/646ce4f8-b8a1-4ce9-818b-7127332c8d9a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/56/2c2944eb-7255-4b58-bc7d-0767d2a5d7ee/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/09/23/14/08/29/327faf9a-ad68-42f0-aa31-505afdeb70a4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/09/23/14/08/29/036a8509-a9df-4f89-afd8-4b1c4dc9f5eb/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/09/23/14/08/29/17dfd84e-3150-4762-b0ad-ac33b1bdf49f/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/09/23/14/08/29/39404ab0-7219-40dd-a7a7-93cefcb7fa6d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/09/23/14/08/29/50eddc6e-d4d4-43de-8653-3494101b8dee/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/09/23/14/08/29/f4ccf2dd-caae-46d5-a4bf-8dbd5ba6f2b2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Nice, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/09/23/14/08/29/4e020732-ea58-4620-9bb6-8bd3823492cb/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €965,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">143 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "4",
        "address": "Nice, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Nice, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/michael-zingraf-nice-128177" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2022/05/04/07/36/04/7a2410e3-a77a-41a8-ae28-ca90bd6cfa70/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Michaël Zingraf Nice" src="" />

  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16358017" data-price-usd="2427127" data-price-euro="2084000" data-price="2084000" data-currency="EUR" data-country-code="FR" data-country="France" data-country-subdivision="Nouvelle-Aquitaine" data-city="Vaux-sur-Mer" data-office-id="359439" data-agent-id="1944252" data-category="RealEstate" data-lat="45.6452013" data-lng="-1.0600972" data-position="Search" data-serp-position="11" data-type="Listing card">
  <a href="/real_estate/vaux-sur-mer-france/exceptional-267-m-villa-with-pool-jacuzzi-and-sea-view-in-vaux-sur-mer-16358017" title="EXCEPTIONAL 267 M² VILLA WITH POOL, JACUZZI, AND SEA VIEW IN VAUX-SUR-MER" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Video
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16358017">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 22
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 22 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/09/14/25/22/7bf3b2b7-092a-406f-8b12-c4be9e2dd56f/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/09/14/38/03/91c0bc97-c8e3-4e3a-a446-0a3bd6eeb429/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/09/15/05/53/64c8b32e-16bc-4e86-ba0f-31ae38cca1d4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/09/14/25/22/4f4aa6ee-1c4a-478a-887c-86f9026cef79/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/09/14/25/22/67091b6b-9214-41a5-96ad-f46f5e0435ad/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/09/14/38/03/ef253b60-42cf-40bb-bffd-a40cb846106e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/09/14/25/22/c2cee919-bdaf-41cf-9d2d-4688ac26dbf7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/09/14/38/03/41600715-0574-4e17-9fb8-73ead596ef94/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/09/15/16/41/ff37419a-819e-4ced-940d-b50f3082aa0d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vaux-sur-Mer, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/09/14/38/03/cba3dac2-fa62-420e-9bcb-7e3255c8391b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €2,084,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">3 Baths</span>
    <span class="ListingCard__tag">267 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "3",
        "numberOfBedrooms": "4",
        "address": "Vaux-sur-Mer, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Vaux-sur-Mer, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/elite-group-real-estate-359439" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/05/05/12/16/09/b5c8a2bb-244b-4c69-86ed-f507f830785f/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="ELITE GROUP Real Estate" src="" />

      <div class="ListingCard__footer__agent">Elodie CHEVALIER</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/10/15/11/33/21/b9a8e45d-ded5-4b2e-a2da-fd1283372927/je/80x80xc.jpg" alt="Elodie CHEVALIER photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16496560" data-price-usd="2667045" data-price-euro="2290000" data-price="2290000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Grimaud" data-office-id="102131" data-agent-id="1596633" data-group-id="395" data-category="RealEstate" data-lat="43.28102" data-lng="6.52074" data-position="Search" data-serp-position="12" data-type="Listing card">
  <a href="/real_estate/grimaud-france/grimaud-close-to-the-village-5-bedroom-house-16496560" title="GRIMAUD – CLOSE TO THE VILLAGE – 5-BEDROOM HOUSE" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16496560">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 16
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 16 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/99e1f211-2347-453a-8d1c-8e2ef449405e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/1f1f4938-6d5d-4417-af5c-fa7d92f4fb78/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/8128367b-1e71-4e38-9ea6-8e1928fb156a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/8f4a1a2f-18b9-4ff0-8678-74c5bf59ac1e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/7358bf67-d256-4043-addb-fe9df69c7c29/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/3c237e85-da34-410f-91be-b1945461a533/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/bd557831-5a25-43b8-8cf1-3562fe42d1d1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/0e30b7c3-4f19-4123-94a4-892ceafcd192/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/897399f4-f7df-4163-b7ef-ca273ef26d09/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Grimaud, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/69f9aea3-4447-4879-b03b-b7be1d5f4e5b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €2,290,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">5 Beds</span>
    <span class="ListingCard__tag">5 Baths</span>
    <span class="ListingCard__tag">215 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "5",
        "numberOfBedrooms": "5",
        "address": "Grimaud, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Grimaud, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/barnes-saint-tropez-102131" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/10/14/06/eb29b3f2-e2d5-4fb9-b2ab-a304462fda44/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="BARNES Saint-Tropez" src="" />

      <div class="ListingCard__footer__agent">Vincent Martel</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/10/01/1e2ee2c2-a01c-4a77-8566-5bf876a4dd77/je/80x80xc.jpg" alt="Vincent Martel photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16129746" data-price-usd="2550580" data-price-euro="2190000" data-price="2190000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Grasse" data-office-id="105684" data-agent-id="1596933" data-group-id="395" data-category="RealEstate" data-lat="43.61591" data-lng="6.93211" data-position="Search" data-serp-position="13" data-type="Listing card">
  <a href="/real_estate/grasse-france/on-the-outskirts-of-mougins-gated-domain-tennis-court-6-bedrooms-16129746" title="On the outskirts of Mougins – Gated Domain – Tennis Court - 6 Bedrooms" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Video
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16129746">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 20
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 20 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/09/10/15/31/47/eecebff0-4ce6-44e6-bd11-1f42b83ce1ba/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/09/04/13/36/41/1e457fff-b62e-4ceb-92fc-c116c42a439e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/09/04/13/36/41/7ce52b5f-5a3e-4668-b446-9cdf88c15611/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/09/04/13/36/41/7970daba-8127-4913-8967-6a2954a2ea05/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/09/04/13/36/41/7d966e48-eda7-4218-bf97-f279a416ca88/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/09/04/13/36/41/c7d4adf2-a50d-48a3-a1c6-1e72e21568e1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/09/04/13/36/41/2a3a3c89-93d5-40bc-bca1-87d78b8c910b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/09/04/13/36/41/d488b995-fa82-4c70-bc24-65b1a40b9148/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/09/04/13/36/41/7a6c6642-c1ee-4f64-af62-f292f5adc654/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/09/04/13/36/41/898a5070-cbdd-42cf-b73f-85c446924c3b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €2,190,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">7 Beds</span>
    <span class="ListingCard__tag">8 Baths</span>
    <span class="ListingCard__tag">237 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "8",
        "numberOfBedrooms": "7",
        "address": "Grasse, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Grasse, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/barnes-valbonne-105684" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/10/11/34/8995f51e-79fe-4e49-8741-bcd5072033d7/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="BARNES Valbonne" src="" />

      <div class="ListingCard__footer__agent">Camille Charles</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/10/20/898727db-17b1-4d58-b282-6328982acd9d/je/80x80xc.jpg" alt="Camille Charles photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16178817" data-price-usd="2038135" data-price-euro="1750000" data-price="1750000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Ajaccio" data-office-id="102594" data-agent-id="1596960" data-group-id="395" data-category="RealEstate" data-lat="41.91916" data-lng="8.739" data-position="Search" data-serp-position="14" data-type="Listing card">
  <a href="/real_estate/ajaccio-france/exclusive-north-of-ajaccio-tiuccia-calcatoggio-stone-built-villa-5-bedrooms-pool-gym-sea-vi-16178817" title="Exclusive, North of Ajaccio, Tiuccia, Calcatoggio,  stone-built villa, 5 bedrooms, pool, gym, sea vi" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16178817">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 13
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 13 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 1" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/b699ae64-a7ec-4152-a1c7-58c79bdd1492/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 2" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/dbc2a87b-36f1-4508-9d99-f2f29537838b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 3" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/df804b7b-f802-4997-a60f-ccc1a3bb61e1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 4" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/b103587f-bfd4-4f13-9af3-8c25546d8bd3/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 5" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/d7718a64-8a09-4726-8a05-8722714015e6/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 6" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/e9635e9c-b4ab-4b4b-8c54-1e99e58ca789/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 7" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/f6ff51b3-06eb-46ce-8365-0e70edb5f787/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 8" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/3bf659b2-bef8-4ad9-b84d-473cf0b09892/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 9" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/4470f8f8-7e91-4a70-82b4-4e032ea19421/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Ajaccio, Corsica, France 10" data-src="https://img.jamesedition.com/listing_images/2025/09/12/08/50/04/db63c813-fc85-414d-b981-b8fb12b506a9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,750,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">5 Beds</span>
    <span class="ListingCard__tag">5 Baths</span>
    <span class="ListingCard__tag">197 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "5",
        "numberOfBedrooms": "5",
        "address": "Ajaccio, Corsica, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Ajaccio, Corsica, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/barnes-corse-102594" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/10/11/27/28159521-3fe1-4f17-a7f1-7b5623f85d68/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="BARNES Corse" src="" />

      <div class="ListingCard__footer__agent">Marie Pietri</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/10/23/118043d8-049d-4d8f-8f32-36799194de39/je/80x80xc.jpg" alt="Marie Pietri photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16122150" data-price-usd="953847" data-price-euro="819000" data-price="819000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Toulouse" data-office-id="141245" data-agent-id="1670928" data-category="RealEstate" data-lat="43.6046256" data-lng="1.444205" data-position="Search" data-serp-position="15" data-type="Listing card">
  <a href="/real_estate/toulouse-france/villa-toulouse-16122150" title="Villa, Toulouse" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16122150">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 18
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 18 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 1" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/f4345274-0d88-42e7-af2a-652d168a9ca6/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 2" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/73392c03-a68f-403d-81a4-709bf2d9e5f2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 3" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/74988e4c-ce6c-435b-aa8a-3064db7568af/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 4" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/4d076023-6aa0-489c-a207-d1c9ac2430eb/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 5" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/1e5c42a8-ee80-46eb-a492-e8ef3d73c6d8/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 6" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/d3c7473c-9686-454d-ae98-e7f17be70363/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 7" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/a0e5e7ce-77e3-4dfe-8298-c17b5ecdd0ad/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 8" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/74ff8e8a-c676-40c7-b8f4-cb9913a9a974/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 9" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/1cd06f51-9f17-4871-b777-e72f5a242b52/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Toulouse, Occitanie, France 10" data-src="https://img.jamesedition.com/listing_images/2025/12/04/09/54/30/752c9dc3-7d3c-428c-98e1-f936f082dc7e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €819,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">3 Baths</span>
    <span class="ListingCard__tag">250 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "3",
        "numberOfBedrooms": "4",
        "address": "Toulouse, Occitanie, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Toulouse, Occitanie, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/kretz-real-estate-141245" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2023/11/30/14/20/45/92ffd19f-cd56-4705-a156-7b4f05c2c44b/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Kretz Real Estate" src="" />

      <div class="ListingCard__footer__agent">DELLUS Caroline</div>
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16137264" data-price-usd="2201186" data-price-euro="1890000" data-price="1890000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Nice" data-office-id="133059" data-group-id="2" data-category="RealEstate" data-lat="43.70008379999999" data-lng="7.2620933" data-position="Search" data-serp-position="16" data-type="Listing card">
  <a href="/real_estate/nice-france/renovated-contemporary-villa-with-pool-and-sea-view-in-nice-saint-pierre-de-fer-16137264" title="Renovated Contemporary Villa With Pool And Sea View In Nice Saint Pierre De Fér…" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16137264">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 20
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 20 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/038f80fe-affa-4cee-853f-c16f69da2cc2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/3ad07459-f358-4379-ad11-75339f1a3187/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/bd6d814f-8fa7-4734-afdf-33aae8e131fa/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/4d239980-eda5-489f-b58b-25484102f998/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/2d5dd8a3-5db2-4058-b8d7-67230e00bec3/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/07bd1f9b-c70e-42b1-b4ed-e3d3baf27a7d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/ab387af4-c73d-4d25-99ff-453d3f28c0b4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/68774288-95be-442c-9881-e189f4f4235a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/25069d45-72b7-492c-861d-d4159711dead/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Nice, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/09/05/15/50/24/9cf7f11b-119e-4c18-988a-74709919231b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,890,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">5 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">276 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "5",
        "address": "Nice, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Nice, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/cote-d-azur-sotheby-s-international-realty-133059" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/08/31/59/115cb8ca-6694-448d-9194-a906fb9ebe3d/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Côte d&#39;Azur Sotheby&#39;s International Realty" src="" />

  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16098982" data-price-usd="2201186" data-price-euro="1890000" data-price="1890000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Sant&#39;Andréa-d&#39;Orcino" data-office-id="102594" data-agent-id="1597126" data-group-id="395" data-category="RealEstate" data-lat="42.05939" data-lng="8.75064" data-position="Search" data-serp-position="17" data-type="Listing card">
  <a href="/real_estate/ajaccio-france/north-of-ajaccio-san-andrea-d-orcino-4-bedroom-villa-infinity-pool-panoramic-sea-view-walk-to-b-16098982" title="North of Ajaccio, San Andréa d’Orcino, 4 Bedroom Villa, Infinity Pool, Panoramic Sea View, Walk to B" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16098982">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 22
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 22 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 1" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/e45a6f4d-cd2b-4df5-85bc-e5dc0634e512/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 2" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/cb2cc812-d935-4a16-a88b-09efa5b5a3f9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 3" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/bc1b9eea-a97a-41ec-bf13-958d1cfec5bc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 4" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/22baa263-2286-40a2-afab-bb90b1b4a1e2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 5" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/88ec2dfc-ecf5-4855-8141-fe7a27d9cd1b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 6" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/77df61ca-f7de-4d45-9f93-25b2210e3dab/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 7" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/459ad73f-a940-45db-a721-2c86cfa0d6e5/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 8" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/487ab4a3-9c80-4209-a736-f06b8ca428d8/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 9" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/3854caa5-575e-42fa-90f1-79da11c562f1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Sant&#39;Andréa-d&#39;Orcino, Corsica, France 10" data-src="https://img.jamesedition.com/listing_images/2025/08/27/12/21/42/3f70de55-be6b-4d19-93a0-d54d153969a7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,890,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">3 Beds</span>
    <span class="ListingCard__tag">5 Baths</span>
    <span class="ListingCard__tag">172 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "5",
        "numberOfBedrooms": "3",
        "address": "Sant&#39;Andréa-d&#39;Orcino, Corsica, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Sant&#39;Andréa-d&#39;Orcino, Corsica, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/barnes-corse-102594" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/10/11/27/28159521-3fe1-4f17-a7f1-7b5623f85d68/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="BARNES Corse" src="" />

      <div class="ListingCard__footer__agent">Jocelyne Jeulin</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/10/41/2ddff4a3-a5d7-4e88-ba59-3076ac226940/je/80x80xc.jpg" alt="Jocelyne Jeulin photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="15945756" data-price-usd="755857" data-price-euro="649000" data-price="649000" data-currency="EUR" data-country-code="FR" data-country="France" data-country-subdivision="Occitanie" data-city="Narbonne" data-office-id="157881" data-category="RealEstate" data-lat="43.184277" data-lng="3.003078" data-position="Search" data-serp-position="18" data-type="Listing card">
  <a href="/real_estate/narbonne-france/architect-villa-15945756" title="🏡 ARCHITECT VILLA " target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Video
    </div>
    <div class="ListingCard__badges__text">
        Virtual tour
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="15945756">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 30
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 30 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 1" data-src="https://img.jamesedition.com/listing_images/2025/07/17/15/49/15/676ef70d-b9fe-4630-9354-6b7d364ac0e4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 2" data-src="https://img.jamesedition.com/listing_images/2025/07/17/15/49/15/4192e790-d495-4f2f-8828-aa4b85ae6c0d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 3" data-src="https://img.jamesedition.com/listing_images/2025/07/17/16/29/32/b78cf689-cb48-4182-9afe-ca1c2207631c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 4" data-src="https://img.jamesedition.com/listing_images/2025/07/17/16/29/32/5766bf1c-ca39-4c7e-a511-7a22287927fd/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 5" data-src="https://img.jamesedition.com/listing_images/2025/07/17/14/27/46/762c7f54-c4d8-4d08-811d-0220d548670b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 6" data-src="https://img.jamesedition.com/listing_images/2025/07/18/10/44/14/5c1c5397-5706-46a0-8474-0a5e3e249b35/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 7" data-src="https://img.jamesedition.com/listing_images/2025/07/17/16/29/32/1ea184a0-1d6c-455b-a624-b003dd2e9fdd/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 8" data-src="https://img.jamesedition.com/listing_images/2025/07/17/14/27/46/ec2264ef-6f6a-4485-87fc-8d07dbe4cb7f/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 9" data-src="https://img.jamesedition.com/listing_images/2025/07/17/16/29/32/ac837bcd-633d-4bf9-9d92-9fa96f85fee3/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Narbonne, Occitanie, France 10" data-src="https://img.jamesedition.com/listing_images/2025/07/17/14/27/46/61767711-5de0-4717-89e6-1c1443a6c12e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €649,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">5 Beds</span>
    <span class="ListingCard__tag">190 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "0",
        "numberOfBedrooms": "5",
        "address": "Narbonne, Occitanie, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Narbonne, Occitanie, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/proprietes-privees-bruno-vuillemin-157881" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2023/02/28/17/34/54/9c95df9a-e7d7-4bd9-8a6b-2f1c83d208aa/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="PROPRIETES PRIVEES - Bruno VUILLEMIN" src="" />

  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16296175" data-price-usd="1892554" data-price-euro="1625000" data-price="1625000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Grasse" data-office-id="105684" data-agent-id="1596816" data-group-id="395" data-category="RealEstate" data-lat="43.6621" data-lng="6.95503" data-position="Search" data-serp-position="19" data-type="Listing card">
  <a href="/real_estate/grasse-france/grasse-bastide-sector-peyloubet-quiet-4-bedrooms-pool-16296175" title="Grasse Bastide, sector Peyloubet, quiet, 4 bedrooms, pool" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Video
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16296175">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 24
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 24 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/6a7aa65f-19e6-4a87-bc77-7c3736cbe40b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/da999078-8e51-4cad-aa75-2fdd80ddc497/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/8663a298-e890-42f0-9c99-230a18d1efba/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/16e6c298-2724-4ebe-89af-bbcc603b824a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/fd035371-9940-4b70-84d8-0048eb4d4ba1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/2bc0122f-091f-43fd-bc9c-e9c28c6f0f76/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/312a571f-86ba-43d5-9df3-612a28ab9a41/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/6d10836a-1af8-44dd-b513-fc3c178c7dde/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/726a4252-be08-451e-b456-1b35721a9c8e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Grasse, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/02/15/11/22/6f8f2d31-4dbb-4c8d-946b-c45afc183066/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,625,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">252 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "4",
        "address": "Grasse, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Grasse, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/barnes-valbonne-105684" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/10/11/34/8995f51e-79fe-4e49-8741-bcd5072033d7/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="BARNES Valbonne" src="" />

      <div class="ListingCard__footer__agent">Catherine Macfadyen</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/10/11/9926e2da-e17d-49c3-9742-16c45a32e213/je/80x80xc.jpg" alt="Catherine Macfadyen photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="15919668" data-price-usd="1385931" data-price-euro="1190000" data-price="1190000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Vence" data-office-id="103860" data-agent-id="1595873" data-group-id="395" data-category="RealEstate" data-lat="43.72237" data-lng="7.07686" data-position="Search" data-serp-position="20" data-type="Listing card">
  <a href="/real_estate/vence-france/vence-charming-provencal-villa-with-sea-glimpse-15919668" title="Vence: Charming Provençal Villa with Sea Glimpse" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="15919668">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 10
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 10 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/2421450c-c4b0-4bc7-9c80-a04239a21d49/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/021bbf49-179d-4471-9d9e-0f380957ba99/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/0029ed5f-aee9-4559-b5de-5bda780f301e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/a1536ce1-13e3-48d2-963a-50ede047293b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/5ab3d7b1-2eb9-4504-9d68-9402b1751ab2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/f0ad472e-a404-443f-9eb3-b11fe382109f/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/dc3903cc-5edc-4f57-8437-ae9cb6b2724c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/e60ae677-8f7c-409b-99ea-34ac09418e05/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/ca017a26-5ff3-460b-ac6a-c35a5abacc7b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Vence, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/07/11/12/35/22/18cd0af3-acdb-48b2-a6b4-5794e4d7a6cd/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,190,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">188 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "4",
        "address": "Vence, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Vence, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/michael-zingraf-saint-paul-de-vence-103860" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_logos/2025/12/06/10/11/30/bbc1c24b-fea0-499d-948a-053927c338d3/je/320x160xs.jpg" data-type="office_logo" data-watermark="true" alt="Michaël Zingraf Saint-Paul de Vence" src="" />

      <div class="ListingCard__footer__agent">Sven Ingwersen</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/09/13/09/00/30/9c1f10be-915f-4f69-922b-cbd1dbb18260/je/80x80xc.jpg" alt="Sven Ingwersen photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16315771" data-price-usd="2445762" data-price-euro="2100000" data-price="2100000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Chamonix" data-office-id="269613" data-agent-id="1561057" data-group-id="395" data-category="RealEstate" data-lat="45.95342" data-lng="6.90161" data-position="Search" data-serp-position="21" data-type="Listing card">
  <a href="/real_estate/chamonix-mont-blanc-france/chamonix-classic-alpine-chalet-with-6-bedrooms-in-les-tines-16315771" title="CHAMONIX - Classic alpine chalet with 6 bedrooms in Les Tines" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Virtual tour
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16315771">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 21
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 21 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 1" data-src="https://img.jamesedition.com/listing_images/2025/12/02/16/32/41/fea08f8a-b2a4-4608-87f3-f08f45bc45e1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 2" data-src="https://img.jamesedition.com/listing_images/2025/12/02/16/32/41/f362c21f-7b11-4ef7-a869-20461ea2c96b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 3" data-src="https://img.jamesedition.com/listing_images/2025/12/02/16/32/41/7356ce7c-e905-40e0-b880-11c1dfe18f89/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 4" data-src="https://img.jamesedition.com/listing_images/2025/11/26/17/19/35/e8cbe3ed-de0a-4f91-9fd1-e410665be8b9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 5" data-src="https://img.jamesedition.com/listing_images/2025/11/26/17/19/35/63adc6c9-2154-40c1-bb11-a9d64cef6839/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 6" data-src="https://img.jamesedition.com/listing_images/2025/11/26/17/19/35/6bbaa1c8-30f6-461f-a989-387ae46b8c3a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 7" data-src="https://img.jamesedition.com/listing_images/2025/11/26/17/19/35/fd2f44b0-49a0-4d94-8998-8766285037ff/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 8" data-src="https://img.jamesedition.com/listing_images/2025/11/26/17/19/35/b962a30a-dd76-4cb2-a1a6-862d33e12dbf/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 9" data-src="https://img.jamesedition.com/listing_images/2025/11/26/17/19/35/678d31de-5354-4272-af50-0389d9b4aafa/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Chalet in Chamonix, Auvergne-Rhône-Alpes, France 10" data-src="https://img.jamesedition.com/listing_images/2025/11/26/17/19/35/c5ccd69d-4e56-4fc2-9cbf-d1f835b31936/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €2,100,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">6 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">236 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Chalet",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "6",
        "address": "Chamonix, Auvergne-Rhône-Alpes, France"
    }
</script>


      <div class="ListingCard__title">
          Chalet<span> in </span>Chamonix, Auvergne-Rhône-Alpes, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/mountain-base-269613" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/10/13/09/18647af6-9180-4b9d-98a2-3cfb9161b921/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Mountain Base" src="" />

      <div class="ListingCard__footer__agent">Amanda GOTTHOLD</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2024/08/17/15/02/11/7de62468-2146-4191-9438-071a50be6f86/je/80x80xc.jpg" alt="Amanda GOTTHOLD photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16402616" data-price-usd="2084721" data-price-euro="1790000" data-price="1790000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Paris" data-office-id="339116" data-agent-id="1686625" data-group-id="395" data-category="RealEstate" data-lat="48.82982" data-lng="2.30184" data-position="Search" data-serp-position="22" data-type="Listing card">
  <a href="/real_estate/paris-15eme-france/townhouse-paris-15th-138-97-sqm-4-bedrooms-16402616" title="Townhouse - Paris 15th - 138.97 sqm - 4 bedrooms" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Video
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16402616">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 28
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 28 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/37b048e0-a829-408f-96e0-43e7c34da9d7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/36a087a4-c5ad-4d03-9c0d-f5465b65f3cb/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/0d0e946c-7cfe-4faa-b248-9958a41a2aef/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/8f1d829a-566c-4618-be00-e767208f2ac8/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/b3cbeca2-2066-4fa6-b09f-b681f3c66bc2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/be03b768-de66-447d-b62c-7879782577a0/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/2fbb3344-3de4-4740-9023-0fd48c343c7a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/511c502a-b0c4-4b84-b623-b0ad891b8f85/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/523a63e8-773d-4759-86f5-b563368676f2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Paris, Île-de-France, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/15/15/48/35/3cb03b6a-fa68-4c83-8c5d-55d516d28bf2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,790,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">6 Baths</span>
    <span class="ListingCard__tag">139 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "6",
        "numberOfBedrooms": "4",
        "address": "Paris, Île-de-France, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Paris, Île-de-France, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/junot-breteuil-339116" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/11/14/14/11/44/eae1394e-28cc-4763-89f0-b110fcdba7bc/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Junot Breteuil" src="" />

      <div class="ListingCard__footer__agent">Leslie Vilain</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/15/05/e5b0da14-fa64-43b9-a4aa-f330de04fd35/je/80x80xc.jpg" alt="Leslie Vilain photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="15583924" data-price-usd="1741149" data-price-euro="1495000" data-price="1495000" data-currency="EUR" data-country-code="FR" data-country="France" data-country-subdivision="Nouvelle-Aquitaine" data-city="Angoulême" data-office-id="359439" data-agent-id="1728859" data-category="RealEstate" data-lat="45.6488766" data-lng="0.1567288" data-position="Search" data-serp-position="23" data-type="Listing card">
  <a href="/real_estate/angouleme-france/luxurious-15th-century-mill-on-the-charente-river-15583924" title="LUXURIOUS 15TH-CENTURY MILL ON THE CHARENTE RIVER" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Video
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="15583924">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 24
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 24 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/05/05/11/40/34/e8545890-5d51-47f6-ad6d-d10fab0d10d2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/05/05/13/11/02/0f379e32-c665-455c-95c4-cbbe533230d7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/05/05/11/40/34/538375f2-5cec-4742-b0ea-92f63bb262b9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/05/05/13/11/02/8e8bc508-7c56-4749-ad26-07401958f742/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/05/05/13/11/02/3d02d17b-e142-43ae-b6f8-4caea27c907b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/05/05/11/40/34/b236fb61-fb1a-4565-b735-7eb739e0ea3a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/05/05/11/40/34/432738ce-fe5c-4503-bb88-9b95bfc3d25d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/05/05/11/40/34/ef3b00f9-d725-44b5-b23c-401dff49bcb5/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/05/05/11/40/34/102942ec-7ad0-42f0-bc6f-e397a964cdc1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/05/05/11/40/34/a9383072-b527-4003-9034-2e000ae6775a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,495,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">10 Beds</span>
    <span class="ListingCard__tag">7 Baths</span>
    <span class="ListingCard__tag">540 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "7",
        "numberOfBedrooms": "10",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/elite-group-real-estate-359439" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/05/05/12/16/09/b5c8a2bb-244b-4c69-86ed-f507f830785f/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="ELITE GROUP Real Estate" src="" />

      <div class="ListingCard__footer__agent">Antoine BEAUDOU</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/05/05/09/56/36/b49713c4-1257-4f62-918b-053cc5df1dc9/je/80x80xc.jpg" alt="Antoine BEAUDOU photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16078872" data-price-usd="1589745" data-price-euro="1365000" data-price="1365000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Figanières" data-office-id="402139" data-agent-id="1855847" data-category="RealEstate" data-lat="43.569404" data-lng="6.496756" data-position="Search" data-serp-position="24" data-type="Listing card">
  <a href="/real_estate/figanieres-france/france-french-riviera-figanieres-83830-elegant-maison-de-maitre-456-m-5-6-bedrooms-terraced-16078872" title="FRANCE – FRENCH RIVIERA – FIGANIÈRES 83830 ELEGANT MAISON DE MAÎTRE  456 m² 5/6 BEDROOMS   TERRACED" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16078872">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 23
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 23 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/3562252c-e8a6-488d-a202-0ac63fb5b3fc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/101f6d7e-df58-4ec9-b8c4-d8a7d1c0ed98/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/cf2cc881-205a-4705-b173-93f29707f0d3/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/40a89155-ff11-49a8-8bf7-28e5923dfa09/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/278b762f-16af-4122-b69c-4f3df2d13d65/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/ce3ca3ab-639c-4e52-bd78-e5fa16ccac51/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/f7e1c5a2-02dc-4936-a055-a9ee30adf388/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/dff315ae-5ad3-4cc1-b427-0b68365c26bf/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/9e26e1d7-2e25-4a80-be96-de934a01b540/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Figanières, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/08/21/14/24/35/7ce49616-af86-47e7-811d-7bd6e9c399f7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,365,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">8 Beds</span>
    <span class="ListingCard__tag">1 Baths</span>
    <span class="ListingCard__tag">456 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "1",
        "numberOfBedrooms": "8",
        "address": "Figanières, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Figanières, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/beguet-associes-402139" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/08/14/09/28/46/b7104411-5439-423a-b6c0-aa2891e425cc/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Béguet Associés" src="" />

      <div class="ListingCard__footer__agent"></div>
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16474198" data-price-usd="570677" data-price-euro="490000" data-price="490000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Hyères" data-office-id="462279" data-agent-id="1955235" data-group-id="2771" data-category="RealEstate" data-lat="43.116948473" data-lng="6.158103808" data-position="Search" data-serp-position="25" data-type="Listing card">
  <a href="/real_estate/ile-du-levant-france/seafront-house-on-the-isle-of-levant-16474198" title="Seafront House on the Isle of Levant" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16474198">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 29
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 29 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/0335b1c0-b425-4350-b5f6-0f8080a99f15/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/9df40cb5-e124-459c-9327-4a52c5c47512/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/fa5fc9b0-4d29-4f92-a772-8cbd10f4a97c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/dc4ca81e-7248-4516-a715-5d8c63371ca7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/16fdb8d6-ba39-44ff-bc81-ce79c92aa8ce/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/af9138c6-fdc2-41dc-af2c-5f1225906cfd/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/2ddcaf3b-2fc5-4214-96e7-c3cb657d5d58/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/9865a0d2-7254-4f15-acd8-21a61c239cd4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/f886fa0d-6821-453d-9405-8bf98cc01bd3/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Hyères, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/22/15/23/34/4b9638d9-6cb5-4394-92e1-4a0ee81c86f2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €490,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">3 Beds</span>
    <span class="ListingCard__tag">77 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "",
        "numberOfBedrooms": "3",
        "address": "Hyères, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Hyères, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  
</div>
        <div class="ListingCard _ar-70" data-id="15885380" data-price-usd="791961" data-price-euro="680000" data-price="680000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Lacoste" data-office-id="136129" data-agent-id="1524064" data-category="RealEstate" data-lat="43.832624" data-lng="5.273197" data-position="Search" data-serp-position="26" data-type="Listing card">
  <a href="/real_estate/lacoste-france/17th-century-stone-cottage-with-swimming-pool-in-the-heart-of-15885380" title="17th-century stone cottage, with swimming pool, in the heart of" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Virtual tour
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="15885380">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 20
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 20 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/5a4e0746-5528-41f5-ad0f-c2a1892042a4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/091c13a0-34c2-47e2-a082-380477c22210/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/811d3c71-fd02-4690-88bf-00f508c97cc0/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/19476c8d-e857-4de4-9f07-7f011f0629d1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/59b66f3c-cc89-48f3-8fe0-4a7be3450077/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/1f0a5de7-8717-47ee-93b2-610ff36bc3e2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/7d5a8c60-8abe-46cf-953b-71d02fed3353/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/f69a729a-5227-42bd-b2bd-97da6f64bdab/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/5fe0a62b-6435-4dff-b70f-0a4ffd8fa903/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Lacoste, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/07/04/07/35/08/16594bb2-eb91-4ebc-aafc-6ed13c8e6637/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €680,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">3 Baths</span>
    <span class="ListingCard__tag">144 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "3",
        "numberOfBedrooms": "4",
        "address": "Lacoste, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Lacoste, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/maison-victoire-immobilier-136129" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2022/07/25/11/00/11/53182c06-b832-43de-925c-65d796d3ca62/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Maison Victoire Immobilier" src="" />

      <div class="ListingCard__footer__agent">MAISON VICTOIRE Immobilier</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2024/11/21/10/21/39/fa052d3a-a5c9-47f3-a785-5b6551168885/je/80x80xc.jpg" alt="MAISON VICTOIRE Immobilier photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="15949407" data-price-usd="2306004" data-price-euro="1980000" data-price="1980000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Taillades" data-office-id="136129" data-agent-id="1524064" data-category="RealEstate" data-lat="43.834485" data-lng="5.093096" data-position="Search" data-serp-position="27" data-type="Listing card">
  <a href="/real_estate/taillades-france/elegant-proven-al-property-with-guest-houses-two-pools-tennis-15949407" title="Elegant Proven?al property with guest houses, two pools, tennis" target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Virtual tour
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="15949407">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 24
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 24 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/c755a5a3-8de0-4528-bb6e-c038baef9111/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/22bea121-cd5a-4138-8038-b2469757377c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/ac0852b7-8af9-4fce-a3db-c8ad36e63ab7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/85e05930-4e87-4f7e-849e-3c9a8b877232/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/05bdb9ee-10e8-4ddf-858a-0da566208c5b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/7f01fc69-f4a1-4528-9cc8-6eba191c70b4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/36c0359a-2e10-4f4a-a11a-d2c73e76bbe2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/6054d4b7-e938-42ea-b902-1c2340f17b6d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/c7cf9bda-9bbe-4893-a68d-8b878023003a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Taillades, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/07/18/15/07/24/b4e8c329-0885-4501-a528-b861ef592f46/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,980,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">13 Beds</span>
    <span class="ListingCard__tag">12 Baths</span>
    <span class="ListingCard__tag">500 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "12",
        "numberOfBedrooms": "13",
        "address": "Taillades, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Taillades, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/maison-victoire-immobilier-136129" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2022/07/25/11/00/11/53182c06-b832-43de-925c-65d796d3ca62/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Maison Victoire Immobilier" src="" />

      <div class="ListingCard__footer__agent">MAISON VICTOIRE Immobilier</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2024/11/21/10/21/39/fa052d3a-a5c9-47f3-a785-5b6551168885/je/80x80xc.jpg" alt="MAISON VICTOIRE Immobilier photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="15989347" data-price-usd="2667045" data-price-euro="2290000" data-price="2290000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Fréjus" data-office-id="102290" data-group-id="395" data-category="RealEstate" data-lat="43.37851" data-lng="6.71986" data-position="Search" data-serp-position="28" data-type="Listing card">
  <a href="/real_estate/saint-aygulf-france/waterfont-villa-to-renovate-15989347" title="Waterfont villa to renovate" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="15989347">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 13
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 13 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/99ff8b33-d0e1-4477-9e73-bc276feee7ae/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/90ec8ca0-b456-492b-91c0-be02a9c1121a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/ccc0e5c7-5185-4a77-b709-66bc94b6fc17/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/4193c6e2-2b08-465c-9cc3-5642409749ff/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/2231f1a4-9b4e-4fb9-8151-3c32910e4d78/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/2d84406c-8e80-46a1-b414-7ace0be9e41e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/f22c8e1b-7e7a-4bc0-bf44-28376707a1d4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/322e4609-3f90-49eb-b5af-6d9e8e73be0c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/bc7d6ef2-d56b-4362-8fb8-92bf338db752/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Fréjus, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/07/29/14/29/48/f1d412d7-29bd-4781-89ef-5be516e2c23d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €2,290,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">7 Beds</span>
    <span class="ListingCard__tag">2 Baths</span>
    <span class="ListingCard__tag">171 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "2",
        "numberOfBedrooms": "7",
        "address": "Fréjus, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Fréjus, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/magrey-sons-saint-tropez-102290" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/12/06/10/11/27/100e9978-575f-451a-b5dc-4af0c2b3bb87/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Magrey &amp; Sons Saint Tropez" src="" />

  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16006574" data-price-usd="2038135" data-price-euro="1750000" data-price="1750000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Roussillon" data-office-id="136129" data-agent-id="1524064" data-category="RealEstate" data-lat="43.902285" data-lng="5.2937715" data-position="Search" data-serp-position="29" data-type="Listing card">
  <a href="/real_estate/roussillon-france/superb-stone-bastide-with-heated-pool-and-breathtaking-views-16006574" title="Superb stone bastide with heated pool and breathtaking views." target="_blank" class="js-link">

    <div class="ListingCard__badges">
    <div class="ListingCard__badges__text">
        Virtual tour
    </div>
</div>


    <div class="ListingCard__save js-heart " data-listing-id="16006574">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 24
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 24 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 1" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/d0345f25-179b-41a7-ae49-7b638b2b99f5/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 2" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/32fad540-22d9-4588-9d94-42caeebfeba6/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 3" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/c01d3402-4386-44e3-8a0d-afc8cd9d7f72/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 4" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/7a85cc67-f1aa-49f9-ab85-245ebca76612/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 5" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/db4371f0-daf6-4bea-83e2-17ff66f36abd/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 6" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/48cc1001-8105-4dc5-a3fa-b2dcbf0e1b2c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 7" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/79921360-b561-4b49-bd7e-6dfc1b06cd3b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 8" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/d68b6269-8678-4aa4-9982-df421dba569c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 9" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/0b53cec3-0aa8-459f-b0b9-e925c1c0d22b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Roussillon, Provence-Alpes-Côte d&#39;Azur, France 10" data-src="https://img.jamesedition.com/listing_images/2025/08/01/15/56/36/76035784-d043-44bb-b54f-3d31df5365dd/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,750,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">6 Beds</span>
    <span class="ListingCard__tag">2 Baths</span>
    <span class="ListingCard__tag">256 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "2",
        "numberOfBedrooms": "6",
        "address": "Roussillon, Provence-Alpes-Côte d&#39;Azur, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Roussillon, Provence-Alpes-Côte d&#39;Azur, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  <a href="/offices/real_estate/maison-victoire-immobilier-136129" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2022/07/25/11/00/11/53182c06-b832-43de-925c-65d796d3ca62/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Maison Victoire Immobilier" src="" />

      <div class="ListingCard__footer__agent">MAISON VICTOIRE Immobilier</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2024/11/21/10/21/39/fa052d3a-a5c9-47f3-a785-5b6551168885/je/80x80xc.jpg" alt="MAISON VICTOIRE Immobilier photo" src="" />
  </div>
</a>
</div>
        <div class="ListingCard _ar-70" data-id="16247710" data-price-usd="1688740" data-price-euro="1450000" data-price="1450000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Bazoches-sur-Hoëne" data-office-id="436894" data-agent-id="1913213" data-group-id="2771" data-category="RealEstate" data-lat="48.4893" data-lng="0.4514" data-position="Search" data-serp-position="30" data-type="Listing card">
  <a href="/real_estate/la-perriere-france/futuristic-villa-16247710" title="Futuristic Villa" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16247710">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 33
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 33 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 1" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/2b30b775-14e8-4c0f-b02e-73b887efdc1e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 2" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/3d0564aa-4e74-4605-8867-cd202daa5ada/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 3" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/16bc98b0-852e-47bf-92ba-3a97b3e6eafa/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 4" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/48d27243-19fa-4379-a933-b7f09f1ffa0b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 5" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/af7ab173-159f-4d36-8569-2e13590534dc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 6" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/66da6df4-760e-4576-9913-6d3009076898/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 7" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/1b900521-b919-44f3-a724-30a2ab1f0fcc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 8" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/a6795aad-496d-4ab7-9573-ab54fc27b627/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 9" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/46fc7375-53bc-40ca-baab-6a5b0a9572b5/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Villa in Bazoches-sur-Hoëne, Normandy, France 10" data-src="https://img.jamesedition.com/listing_images/2025/09/24/15/26/57/d8d4b391-6e2f-419d-9d84-7de5f23877e8/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,450,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">320 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Villa",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "4",
        "address": "Bazoches-sur-Hoëne, Normandy, France"
    }
</script>


      <div class="ListingCard__title">
          Villa<span> in </span>Bazoches-sur-Hoëne, Normandy, France
      </div>


      <div class="ListingCard__actions">
          <div class="js-contact-button">Contact<svg><use xlink:href="#contact"></use></svg></div>
      </div>

    </div>

</a>
  
</div>
    </div>




    <div class="je2-search-page__pagination js-pagination-serp">
        <a href="https://www.jamesedition.com/real_estate/france?real_estate_type%5B%5D=house&amp;real_estate_type%5B%5D=villa&amp;real_estate_type%5B%5D=estate&amp;real_estate_type%5B%5D=country_house&amp;real_estate_type%5B%5D=finca&amp;real_estate_type%5B%5D=chalet&amp;real_estate_type%5B%5D=townhouse&amp;real_estate_type%5B%5D=bungalow&amp;bedrooms_from=3&amp;eur_price_cents_to=247208500&amp;page=2" class="je2-button " data-next="true">

  

    <span>
          Next
    </span>




  
  


</a>

      
  <div class="Pagination js-pagination">
    <div class="Pagination__pages">
      
        <span class="_active" data-page="1">
    1
  </span>

              <a aria-label="2" href="/real_estate/house%2Fvilla%2Festate%2Fcountry_house%2Ffinca%2Fchalet%2Ftownhouse%2Fbungalow-france?bedrooms_from=3&amp;eur_price_cents_to=247208500&amp;page=2">
    <span data-page="2">2</span>
</a>
              <a aria-label="3" href="/real_estate/house%2Fvilla%2Festate%2Fcountry_house%2Ffinca%2Fchalet%2Ftownhouse%2Fbungalow-france?bedrooms_from=3&amp;eur_price_cents_to=247208500&amp;page=3">
    <span data-page="3">3</span>
</a>
          <span>…</span>

        <a class="_last" aria-label="50" href="/real_estate/house%2Fvilla%2Festate%2Fcountry_house%2Ffinca%2Fchalet%2Ftownhouse%2Fbungalow-france?bedrooms_from=3&amp;eur_price_cents_to=247208500&amp;page=50">
    <span data-page="50">50</span>
</a>
        <a aria-label="2" href="/real_estate/house%2Fvilla%2Festate%2Fcountry_house%2Ffinca%2Fchalet%2Ftownhouse%2Fbungalow-france?bedrooms_from=3&amp;eur_price_cents_to=247208500&amp;page=2">
    <span class="_next" data-page="2">
      <svg><use xlink:href="#short-arrow"></use></svg>
    </span>
</a>
    </div>
    <div class="Pagination__stats">
      1-30 of 54,100 homes for sale
    </div>
  </div>

    </div>


  <script type="131723e888cc8f98efbd5b21-text/javascript">
      window.JEParams = window.JEParams || {};
      window.JEParams.withSeoContent = false;
      window.JEParams.serpPage = {"propertyFeature":null,"realEstateType":null,"currentPlaceBounds":[-5.5591,41.31433,9.6624999,51.1241999],"noResults":false,"nearbyCount":null,"personalizedSearch":false,"listingsCoords":[[0.1567288,45.6488766],[0.707123093,49.859704549],[7.237937874,43.712363989],[6.91244,43.63665],[6.0192810348,47.2551269927],[-4.5721318,48.5870399],[4.7777898,45.7591534],[5.537959499999999,43.2186071],[5.200176,43.91131499999999],[7.23023,43.71755],[-1.0600972,45.6452013],[6.52074,43.28102],[6.93211,43.61591],[8.739,41.91916],[1.444205,43.6046256],[7.2620933,43.70008379999999],[8.75064,42.05939],[3.003078,43.184277],[6.95503,43.6621],[7.07686,43.72237],[6.90161,45.95342],[2.30184,48.82982],[0.1567288,45.6488766],[6.496756,43.569404],[6.158103808,43.116948473],[5.273197,43.832624],[5.093096,43.834485],[6.71986,43.37851],[5.2937715,43.902285],[0.4514,48.4893]]};
  </script>
      <div class="je2-map-entry js-sticky-map-entry _hidden">
      <button class="je2-button js-show-map-view _noborder _black _rounded">

    <svg viewBox="0 0 16 18" fill="none">
  <path fill="none" d="M5.5998 15.2856L2.15779 16.1051C1.46311 16.2705 0.799805 15.7266 0.799805 14.9915V3.62315C0.799805 3.09104 1.15601 2.62933 1.6589 2.5096L5.5998 1.57129V15.2856Z" stroke-width="1.6" stroke-linejoin="round" />
  <path fill="none" d="M5.59961 15.2856L10.3996 16.4284V2.71415L5.59961 1.57129V15.2856Z" stroke-width="1.6" stroke-linejoin="round" />
  <path fill="none" d="M15.1999 14.377C15.1999 14.9091 14.8437 15.3708 14.3408 15.4906L10.3999 16.4288V2.71456L13.8419 1.89504C14.5365 1.72964 15.1999 2.27355 15.1999 3.00859V14.377Z" stroke-width="1.6" stroke-linejoin="round" />
</svg>



    <span>
          Show map
    </span>




  
  


</button>
  </div>

<script type="131723e888cc8f98efbd5b21-text/javascript">
  window.JEParams = window.JEParams || {};
  window.JEParams.staticMapLink = window.decodeURIComponent("/real_estate/map?bedrooms_from=3&amp;eur_price_cents_to=247208500&amp;map_coordinates=-5.5591,41.31433,9.6624999,51.1241999&amp;location=france&amp;country=france&amp;real_estate_type[]=house&amp;real_estate_type[]=villa&amp;real_estate_type[]=estate&amp;real_estate_type[]=country_house&amp;real_estate_type[]=finca&amp;real_estate_type[]=chalet&amp;real_estate_type[]=townhouse&amp;real_estate_type[]=bungalow".replaceAll("&amp;", "&"));
</script>

    

</div>

  <script type="131723e888cc8f98efbd5b21-text/javascript">
      window.JEParams = window.JEParams || {};
      window.JEParams.pageType = 'serp';
  </script>
  </section>
  <div class="je2-search-filters js-je2-search-filters _on-re _v2">
    <div class="je2-search-filters__container"><div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>
</div>
  </div>

<div class="je2-search-page__seo-container js-seo-container ">
    
<div class="je2-seo-parts__header">
  <div class="je2-texts__heading-34">Dream Locations in France</div>
  <h2 class="je2-texts__regular-14">Castles and luxury mansions for sale in France</h2>
</div>
<div class="je2-seo-parts__slider">
  
<div class="je2-slider js-je2-slider _alt fit-parent grid-align collapsed no-title"
     data-slider-config="{&quot;showDots&quot;:false,&quot;paged&quot;:true,&quot;mobilePaged&quot;:null}"
     data-items-count="4">

  <div class="je2-slider__wrapper">
    <div class="je2-slider__content">
              <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/paris-france">
  <div class="je2-popular-location__title">Paris</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>
      <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/nice-france">
  <div class="je2-popular-location__title">Nice</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>
      <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/cannes-france">
  <div class="je2-popular-location__title">Cannes</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>
      <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/french-riviera-france">
  <div class="je2-popular-location__title">French Riviera</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>
      <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/brittany-france">
  <div class="je2-popular-location__title">Brittany</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>
      <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/nouvelle-aquitaine-france">
  <div class="je2-popular-location__title">Nouvelle-Aquitaine, France</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>
      <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/normandy-france">
  <div class="je2-popular-location__title">Normandy</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>
      <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/centre-val-de-loire-france">
  <div class="je2-popular-location__title">Loire Valley</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>
      <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/provence-alpes-cote-d-azur-france">
  <div class="je2-popular-location__title">Provence-Alpes-Cote d&#39;Azur, France</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>
      <div class="je2-slider__item-4">
        
<a class="je2-popular-location " href="/real_estate/auvergne-rhone-alpes-france">
  <div class="je2-popular-location__title">Auvergne-Rhone-Alpes, France</div>
  <div class="je2-popular-location__count">view homes</div>
  <svg><use xlink:href="#arrow-right-alt"></use></svg>
</a>

      </div>

    </div>
  </div>

    <div class="je2-slider__navigation">

        <div class="je2-slider__scroll left">
          <svg><use xlink:href="#short-arrow"></use></svg>
        </div>
        <div class="je2-slider__scroll right">
          <svg><use xlink:href="#short-arrow"></use></svg>
        </div>
    </div>
</div>

</div>


    
<div class="je2-popular-links">

  <div class="je2-popular-links__grid _4">

      <div class="je2-popular-links__section">
        <input id="group-0" class="je2-popular-links__toggle" type="checkbox" />

          <h2 class="je2-popular-links__label">
            <span>
                France cities
            </span>
</h2>
        <ul class="je2-popular-links__list" id="je-group-0">
          <li>
                <a target="_blank" href="/real_estate/paris-france">Homes for sale in <strong>Paris, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/cannes-france">Homes for sale in <strong>Cannes, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/nice-france">Homes for sale in <strong>Nice, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/antibes-france">Homes for sale in <strong>Antibes, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/bordeaux-france">Homes for sale in <strong>Bordeaux, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/marseille-france">Homes for sale in <strong>Marseille, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/mougins-france">Homes for sale in <strong>Mougins, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/saint-raphael-france">Homes for sale in <strong>Saint-Raphaël, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/aix-en-provence-france">Homes for sale in <strong>Aix-en-Provence, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/roquebrune-cap-martin-france">Homes for sale in <strong>Roquebrune-Cap-Martin, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/sainte-maxime-france">Homes for sale in <strong>Sainte-Maxime, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/neuilly-sur-seine-france">Homes for sale in <strong>Neuilly-sur-Seine, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/montpellier-france">Homes for sale in <strong>Montpellier, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/grimaud-france">Homes for sale in <strong>Grimaud, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/toulouse-france">Homes for sale in <strong>Toulouse, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/lyon-france">Homes for sale in <strong>Lyon, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/roquebrune-sur-argens-france">Homes for sale in <strong>Roquebrune-sur-Argens, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/le-cannet-france">Homes for sale in <strong>Le Cannet, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/nantes-france">Homes for sale in <strong>Nantes, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/menton-france">Homes for sale in <strong>Menton, France</strong></a>
          </li>
        </ul>

        <label class="je2-popular-links__more _active" for="group-0">
          <div class="je2-popular-links__more-open">Show all</div>
          <div class="je2-popular-links__more-close">Show less</div>
          <svg><use xlink:href="#short-arrow"></use></svg>
</label>      </div>

      <div class="je2-popular-links__section">
        <input id="group-1" class="je2-popular-links__toggle" type="checkbox" />

          <h2 class="je2-popular-links__label">
            <span>
                France regions
            </span>
</h2>
        <ul class="je2-popular-links__list" id="je-group-1">
          <li>
                <a target="_blank" href="/real_estate/provence-alpes-cote-d-azur-france">Homes for sale in <strong>Provence-Alpes-Côte d'Azur, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/ile-de-france-france">Homes for sale in <strong>Ile-de-France, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/nouvelle-aquitaine-france">Homes for sale in <strong>Nouvelle-Aquitaine, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/auvergne-rhone-alpes-france">Homes for sale in <strong>Auvergne-Rhône-Alpes, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/occitanie-france">Homes for sale in <strong>Occitanie, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/brittany-france">Homes for sale in <strong>Brittany, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/pays-de-la-loire-france">Homes for sale in <strong>Pays de la Loire, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/hauts-de-france-france">Homes for sale in <strong>Hauts-de-France, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/normandy-france">Homes for sale in <strong>Normandy, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/grand-est-france">Homes for sale in <strong>Grand Est, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/corsica-france">Homes for sale in <strong>Corsica, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/centre-val-de-loire-france">Homes for sale in <strong>Centre-Val de Loire, France</strong></a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/bourgogne-franche-comte-france">Homes for sale in <strong>Bourgogne-Franche-Comté, France</strong></a>
          </li>
        </ul>

        <label class="je2-popular-links__more _active" for="group-1">
          <div class="je2-popular-links__more-open">Show all</div>
          <div class="je2-popular-links__more-close">Show less</div>
          <svg><use xlink:href="#short-arrow"></use></svg>
</label>      </div>

      <div class="je2-popular-links__section">
        <input id="group-2" class="je2-popular-links__toggle" type="checkbox" />

          <h2 class="je2-popular-links__label">
            <span>
                <a href="/real_estate/france" target="_blank">France property types</a>
            </span>
</h2>
        <ul class="je2-popular-links__list" id="je-group-2">
          <li>
                <a target="_blank" href="/real_estate/house-france"><strong>Houses</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/apartment-france"><strong>Apartments</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/villa-france"><strong>Villas</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/estate-france"><strong>Estates</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/chalet-france"><strong>Chalets</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/castle-france"><strong>Castles</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/land-france"><strong>Land</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/penthouse-france"><strong>Penthouses</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/farm_ranch-france"><strong>Farm Ranches</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/chateau-france"><strong>Chateaus</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/condo-france"><strong>Condos</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/country_house-france"><strong>Country Homes</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/townhouse-france"><strong>Townhouses</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/finca-france"><strong>Fincas</strong> for sale in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/private_island-france"><strong>Private Islands</strong> for sale in France</a>
          </li>
        </ul>

        <label class="je2-popular-links__more _active" for="group-2">
          <div class="je2-popular-links__more-open">Show all</div>
          <div class="je2-popular-links__more-close">Show less</div>
          <svg><use xlink:href="#short-arrow"></use></svg>
</label>      </div>

      <div class="je2-popular-links__section">
        <input id="group-3" class="je2-popular-links__toggle" type="checkbox" />

          <h2 class="je2-popular-links__label">
            <span>
                France popular searches
            </span>
</h2>
        <ul class="je2-popular-links__list" id="je-group-3">
          <li>
                <button class="je2-button je2-button _noborder js-popular-link-button" data-url="/real_estate/france?order=recent">

  

    <span>
          Newest homes for sale in France
    </span>




  
  


</button>
          </li>
          <li>
                <a target="_blank" href="/real_estate/garden--france"><strong>Properties with Garden</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/terrace--france"><strong>Properties with Terrace</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/garage--france"><strong>Properties with Garage</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/pool--france"><strong>Properties with Pool</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/balcony--france"><strong>Properties with Balcony</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/mountain-view--france"><strong>Mountain View properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/water-view--france"><strong>Water View properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/elevator--france"><strong>Properties with Elevator</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/renovated--france"><strong>Renovated properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/modern--france"><strong>Modern properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/sea-view--france"><strong>Sea View properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/scenic-view--france"><strong>Panoramic / Scenic View properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/fitness-center--france"><strong>Properties with Fitness Center / Gym</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/wine-cellar--france"><strong>Properties with Wine Cellar</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/duplex--france"><strong>Duplex properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/sauna--france"><strong>Properties with Sauna</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/investment-property--france"><strong>Investment Property properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/cinema--france"><strong>Properties with Cinema</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/equestrian--france"><strong>Equestrian properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/tennis-court--france"><strong>Properties with Tennis Court</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/library--france"><strong>Properties with Library</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/waterfront--france"><strong>Waterfront properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/mansion--france"><strong>Mansion properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/new-built--france"><strong>New Builds properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/indoor-pool--france"><strong>Properties with Indoor Pool</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/oceanfront--france"><strong>Oceanfront properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/coastal--france"><strong>Coastal properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/seafront--france"><strong>Seafront properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/vineyard--france"><strong>Properties with Vineyard / Winery</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/high-altitude--france"><strong>High Altitude properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/lake-view--france"><strong>Lake View properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/ski-in-ski-out--france"><strong>Ski-In / Ski-Out properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/hilltop--france"><strong>Hilltop properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/beachfront--france"><strong>Beachfront properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/ocean-view--france"><strong>Ocean View properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/gated-community--france"><strong>Gated Community properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/helipad--france"><strong>Properties with Helipad</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/private-beach--france"><strong>Properties with Private Beach</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/river-view--france"><strong>River View properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/riverfront--france"><strong>Riverfront properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/private-airport--france"><strong>Properties with Private Airport</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/golf-view--france"><strong>Golf View properties</strong> in France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/lakefront--france"><strong>Lakefront properties</strong> in France</a>
          </li>
        </ul>

        <label class="je2-popular-links__more _active" for="group-3">
          <div class="je2-popular-links__more-open">Show all</div>
          <div class="je2-popular-links__more-close">Show less</div>
          <svg><use xlink:href="#short-arrow"></use></svg>
</label>      </div>
  </div>
</div>


  

      <div class="je2-seo-parts__texts">
        <div class="je2-texts__regular-14">
          <h2 class='je2-texts__medium-16'> Find your dream home for sale in France</h2> <div class='je2-texts__regular-14'> There are currently 110,533 luxury homes for sale in France on JamesEdition. JamesEdition can help you find the home that match all the preferences for your dream home. Use filters and narrow your search by price, number of bedrooms, bathrooms, and amenities to find homes that fit your criteria. Click on listings to see photos, amenities, price and much more. <br/><br/>
The average price of a home in France is 900,094 USD, and range in price between 489,688 USD and 139,911,016 USD. The most popular property types are House (50,627 listings) and Apartment (34,942 listings). Common amenities in France are Garden, Terrace, Garage and Pool. <br/><br/>
On JamesEdition you can find luxury homes in France of any size between 1 and 100 bedrooms with an average of 160 ㎡ in size. <br/><br/>
Popular locations in France that also could be worth exploring are Paris, Cannes, Nice, Antibes and Bordeaux.<br/><br/>
Remember to save your search to receive email alerts when new listings that fit your criteria hit the market, and as you find homes that you love, you can save them to receive status change alerts. </div>
        </div>
      </div>
      <div class="je2-seo-parts__texts">

    <h2 class="je2-texts__medium-16"><p>Looking for your dream home in France?
<br />Discover our definitive selection of luxury real estate in France: castles and mansions, modern luxury homes, and other French properties for sale</p></h2>
    <div class="je2-texts__regular-14"><p>The laid-back French lifestyle, pleasant climate, unparalleled haute cuisine, some of the best wine-producing regions in the world, and a thrilling real estate market are only a small sampling of the compelling reasons to search for second homes and luxury real estate in France.</p>

<p><br>Each region varies in terms of weather, culture, landscape, and prices, offering a wide range of luxury mansions, homes, and medieval castles for sale in France. And even though the "country of love" is perfect from almost every angle, when considering buying a property in France, potential residents need to know exactly where to look for the best luxury French properties.</p></div>

      <h3 class="je2-texts__medium-14"><p>From Paris to Burgundy: the best castles available for sale in France</p></h3>
      <div class="je2-texts__regular-14"><p>When thinking about buying an authentic chateau, the first thought that comes to mind usually is a gorgeous, dreamlike French castle. The country indeed offers an innumerable quantity of the best castles in the world with historical associations with medieval knights and templar castles as well as small ancient castles, castles with vineyards, moats and watchtowers, and even abandoned castles and ruins for sale.</p>

<p><br>The central part of France, including Île-de-France, Burgundy, and the famous Châteaux Area of the <a href="https://whc.unesco.org/en/list/933/">Loire Valley</a>, especially stands out. The area offers the best historical or modern luxury castles available for sale in France. Here, a buyer can find over 300 manors and palaces of the Loire Valley (alongside some of the most fantastic castles in France for sale), the majestic Palace of Versailles, Paris, and the Châteaux &amp; Abbeys of Burgundy.</p>

<p><br>Speaking of how many castles are listed for sale in France in 2020-2021 overall, JamesEdition offers <a href="/real_estate/france?real_estate_type%5B%5D=Castle%26real_estate_type%5B%5D%3DChateau&amp;order=price_desc">412 chateaus</a> with prices up to US$141M. But, of course, more affordable and cheaper castles on the luxury real estate market of France also appear with prices under US$500K.</p></div>
      <h3 class="je2-texts__medium-14"><p>From Brittany and Normandy to Alsace: top, luxury mansions available for sale in France</p></h3>
      <div class="je2-texts__regular-14"><p>The North of France (both the eastern and the western parts) offers a long list of benefits for those investing in luxury French properties. With Brittany and Normandy to the west and Alsace and Lorraine to the east, the northern part of the country is a historically rich and colorful region, boasting a spectacular 2,700-kilometer coastline and numerous, charming villages.</p>

<p><br>Brittany and Normandy, with their picturesque granite cliffs, dramatic coastlines, and authentic culture, have always been a popular choice for those seeking perfect luxury mansions, expensive classic houses, or more affordable coastal homes available for sale in France.</p>

<p><br>Within Alsace, we highly recommend taking a closer look at Strasbourg and Lorraine at Nancy; both cities enjoy an expansive real estate market with some of the best luxury mansions and homes for sale in France.</p></div>
      <h3 class="je2-texts__medium-14"><p>From southern Bordeaux to Toulouse: top, classic-style, luxury homes for sale in France</p></h3>
      <div class="je2-texts__regular-14"><p>Moving on to the southern parts of France, our first recommendation is the west coast with its long expanses of sandy beaches and stunning views over the Atlantic coastline.</p>

<p><br>The fascinating Bordeaux region is nestled just a few miles from the ocean, so the climate is very pleasant with warm summers and mild winters. It is a historic region, and Bordeaux City boasts nearly <a href="https://whc.unesco.org/en/list/1256/">350 UNESCO</a> protected buildings, setting the tone for the luxury French properties listed for sale nearby.</p>

<p><br>In the southwest of France there is plenty of luxury authentic real estate for every taste: from large castles like the famous Château de Montbrun in Limousin to rural cottages and luxury mansions listed for sale in this wine region of France. JamesEdition offers <a href="/real_estate/bordeaux-france?order=price_desc">139 luxury French properties in Bordeaux</a> with prices ranging from US$513K to US$18M.</p>

<p><br>Toulouse, slightly further to the south, also offers numerous benefits. It is strategically located on the road from France to Spain. Named La Ville Rose (the pink city) due to the pink, clay bricks used for many of the city’s buildings, <a href="/real_estate/toulouse-france?order=price_desc">Toulouse</a> is a beautiful place to search for perfect, luxury homes for sale in the South of France.</p></div>
      <h3 class="je2-texts__medium-14"><p>From Nice to Cannes: the best, luxury real estate in France</p></h3>
      <div class="je2-texts__regular-14"><p>Headed by the most famous cities of Nice, Cannes, and Marseilles, the <a href="/stories/real-estate/top-places-to-live-and-stay-on-french-riviera-best-beaches-views-towns-villages/">Provence-Alpes-Côte d'Azur</a> region has a well-deserved reputation for being one of the most popular attractions in the world.</p>

<p><br>Located near Auvergne-Rhône-Alpes, it is a unique geographical area of France. And, if you’re searching for a hotspot to enjoy a relaxed, coastal lifestyle, you’ll be satisfied with an enormous variety of stunning locations, providing the best of French living, including gorgeous views, high-end amenities, and unparalleled entertainment opportunities, as well as the most luxury mansions, homes, and castles listed for sale in France.</p>

<p><br>The real estate market here is guaranteed to thrill: you can easily find some of the best castles and chateaus for sale in the south of France with prices ranging from US$760K up to a record US$141M. The palette of architectural styles also is fascinating: from solid, 10th century medieval buildings to sophisticated, neo-gothic castles and chateaus available for sale today in France.</p>

<p><br>Whether you decide to buy luxury, French properties in <a href="/real_estate/cannes-france">Cannes</a>, <a href="/real_estate/nice-france">Nice</a>, or <a href="/real_estate/marseille-france">Marseille</a>, JamesEdition offers the best luxury real estate in France for even the most selective buyer.</p></div>

</div>


</div>


          

<div class="je2-newsletter js-newsletter" id="newsletter" style="min-height: 250px">
</div>


          

          
<div class="je2-footer ">
  <div class="je2-footer__top">
    <div class="je2-footer__menu">
      <div class="je2-footer__menu-section">
        <div class="je2-footer__label">JAMESEDITION</div>
        <ul class="js-foooter-submenu">
          <li><a href="https://www.jamesedition.com/about">About</a></li>
          <li><a href="https://help.jamesedition.com/en/" class="js-intercom-show-message">Contact</a></li>
          <li><a href="https://careers.jamesedition.com">Careers</a></li>
          <li><a href="https://help.jamesedition.com/en/">Help &amp; FAQ</a></li>
          <li><a href="https://www.jamesedition.com/about/terms-of-use">Terms</a></li>
          <li><a href="https://www.jamesedition.com/about/privacy-policy">Privacy</a></li>
        </ul>
      </div>
      <div class="je2-footer__menu-section">
        <div class="je2-footer__label">CATEGORIES</div>
        <ul class="js-foooter-submenu">
          <li><a href="https://www.jamesedition.com/real_estate">Real Estate</a></li>
          <li><a href="https://www.jamesedition.com/cars">Cars</a></li>
          <li><a href="https://www.jamesedition.com/yachts">Yachts</a></li>
          <li><a href="https://www.jamesedition.com/jets">Jets</a></li>
          <li><a href="https://www.jamesedition.com/helicopters">Helicopters</a></li>
          <li><a href="https://www.jamesedition.com/watches">Watches</a></li>
          <li><a href="https://www.jamesedition.com/jewelry">Jewelry</a></li>
          <li><a href="https://www.jamesedition.com/extraordinaire">Extraordinaire</a></li>
          <li><a href="https://www.jamesedition.com/lifestyle-collectibles">Lifestyle</a></li>
        </ul>
      </div>
      <div class="je2-footer__menu-section">
        <div class="je2-footer__label">CATALOG</div>
        <ul class="js-foooter-submenu">
          <li><a href="https://www.jamesedition.com/brands">All Brands</a></li>
          <li><a href="https://www.jamesedition.com/offices">All Businesses</a></li>
        </ul>
      </div>
      <div class="je2-footer__menu-section">
        <div class="je2-footer__label">FOR BUSINESS</div>
        <ul class="js-foooter-submenu">
          <li><a href="/professional_seller">
            Sell With Us
          </a></li>
          <li><a href="mailto:marketing@jamesedition.com">Partner</a></li>
          <li><a href="/widgets">Linking</a></li>
        </ul>
      </div>
        <div class="je2-footer__qr">
          <div class="je2-footer__label">MOBILE APP</div>
          <div class="je2-footer__qr__content">
            <svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" fill="none">
    <path fill="#fff" d="M96 0H0v96h96V0Z" />
    <path fill="#000" d="M5.1885 5.1891H7.783v2.5946H5.1885V5.1892Zm2.5946 0h2.5946v2.5946H7.7831V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5945v2.5946h-2.5945V5.1892Zm2.5945 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946H20.756V5.1892Zm7.7838 0h2.5946v2.5946h-2.5946V5.1892Zm10.3784 0h2.5946v2.5946h-2.5946V5.1892Zm10.3784 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946H59.675V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5945v2.5946h-2.5945V5.1892Zm7.7837 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892ZM5.1885 7.7837H7.783v2.5946H5.1885V7.7837Zm15.5675 0h2.5946v2.5946H20.756V7.7837Zm5.1892 0h2.5946v2.5946h-2.5946V7.7837Zm2.5946 0h2.5946v2.5946h-2.5946V7.7837Zm5.1892 0h2.5946v2.5946H33.729V7.7837Zm2.5946 0h2.5946v2.5946h-2.5946V7.7837Zm2.5946 0h2.5946v2.5946h-2.5946V7.7837Zm5.1892 0h2.5946v2.5946h-2.5946V7.7837Zm12.973 0h2.5946v2.5946h-2.5946V7.7837Zm2.5946 0h2.5946v2.5946H59.675V7.7837Zm12.9729 0h2.5946v2.5946h-2.5946V7.7837Zm15.5676 0h2.5946v2.5946h-2.5946V7.7837Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H33.729v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm15.5675 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946Zm15.5676 0h2.5946v2.5946H59.675v-2.5946Zm12.9729 0h2.5946v2.5946h-2.5946v-2.5946Zm15.5676 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H46.702v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm-51.8919 2.5946h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946ZM5.1885 25.9459H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 28.5405H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm18.1622 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 31.1351h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3783 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H33.729v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 33.7297h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm15.5675 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 36.3243h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H33.729v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm-67.4594 2.5946h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H46.702v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 41.5135h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm12.9729 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 44.1081h2.5946v2.5946H7.7831v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H46.702v-2.5946Zm12.973 0h2.5946v2.5946H59.675v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946Zm10.3783 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 46.7027H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm15.5676 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm-75.2432 2.5946h2.5946v2.5945h-2.5946v-2.5945Zm15.5675 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm7.7838 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm12.973 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945H59.675v-2.5945Zm5.1892 0h2.5945v2.5945h-2.5945v-2.5945Zm7.7837 0h2.5946v2.5945h-2.5946v-2.5945Zm7.7838 0h2.5946v2.5945h-2.5946v-2.5945Zm5.1892 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm-83.027 2.5945H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7837 0h2.5946v2.5946H20.756v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H33.729v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H59.675v-2.5946Zm10.3783 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-75.2432 2.5946h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm18.1622 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 57.081H7.783v2.5946H5.1885V57.081Zm2.5946 0h2.5946v2.5946H7.7831V57.081Zm7.7838 0h2.5945v2.5946h-2.5945V57.081Zm5.1891 0h2.5946v2.5946H20.756V57.081Zm10.3784 0h2.5946v2.5946h-2.5946V57.081Zm2.5946 0h2.5946v2.5946H33.729V57.081Zm10.3784 0h2.5946v2.5946h-2.5946V57.081Zm2.5946 0h2.5946v2.5946H46.702V57.081Zm2.5946 0h2.5946v2.5946h-2.5946V57.081Zm7.7838 0h2.5946v2.5946h-2.5946V57.081Zm5.1892 0h2.5946v2.5946h-2.5946V57.081Zm2.5946 0h2.5945v2.5946h-2.5945V57.081Zm2.5945 0h2.5946v2.5946h-2.5946V57.081Zm7.7838 0h2.5946v2.5946h-2.5946V57.081Zm2.5946 0h2.5946v2.5946h-2.5946V57.081Zm7.7838 0h2.5946v2.5946h-2.5946V57.081ZM5.1885 59.6756H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 64.8648H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm18.1621 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm12.973 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3783 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 67.4594H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7837 0h2.5946v2.5946H20.756v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946ZM25.9452 70.054h2.5946v2.5946h-2.5946V70.054Zm20.7568 0h2.5946v2.5946H46.702V70.054Zm2.5946 0h2.5946v2.5946h-2.5946V70.054Zm2.5946 0h2.5946v2.5946h-2.5946V70.054Zm2.5946 0h2.5946v2.5946h-2.5946V70.054Zm2.5946 0h2.5946v2.5946h-2.5946V70.054Zm2.5946 0h2.5946v2.5946H59.675V70.054Zm7.7837 0h2.5946v2.5946h-2.5946V70.054Zm10.3784 0h2.5946v2.5946h-2.5946V70.054Zm5.1892 0h2.5946v2.5946h-2.5946V70.054Zm5.1892 0h2.5946v2.5946h-2.5946V70.054Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm12.973 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 75.2432H7.783v2.5946H5.1885v-2.5946Zm15.5675 0h2.5946v2.5946H20.756v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H33.729v-2.5946Zm15.5676 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 83.027H7.783v2.5946H5.1885V83.027Zm5.1892 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5945v2.5946h-2.5945V83.027Zm5.1891 0h2.5946v2.5946H20.756V83.027Zm5.1892 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm7.7838 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946H46.702V83.027Zm5.1892 0h2.5946v2.5946h-2.5946V83.027Zm5.1892 0h2.5946v2.5946h-2.5946V83.027Zm7.7838 0h2.5945v2.5946h-2.5945V83.027Zm7.7837 0h2.5946v2.5946h-2.5946V83.027Zm10.3784 0h2.5946v2.5946h-2.5946V83.027ZM5.1885 85.6216H7.783v2.5946H5.1885v-2.5946Zm15.5675 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H46.702v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm12.9729 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 88.2162H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Z" />
</svg>

            <a href="https://apps.apple.com/us/app/jamesedition-luxury-homes/id6737836918" class="je2-button js-app-download" target="_blank" rel="noreferrer" aria-label="Download the app on the App Store">

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 138 40" fill="none"><path fill="#000" d="M137.234 35.387c0 2.132-1.755 3.858-3.927 3.858H4.803c-2.17 0-3.931-1.726-3.931-3.858V4.618c0-2.13 1.761-3.863 3.931-3.863h128.503c2.173 0 3.927 1.732 3.927 3.863l.001 30.769Z" /><path fill="#A6A6A6" d="M132.893.801c2.365 0 4.289 1.884 4.289 4.199v30c0 2.315-1.924 4.199-4.289 4.199H5.213c-2.365 0-4.29-1.884-4.29-4.199V5c0-2.315 1.925-4.199 4.29-4.199h127.68Zm0-.801H5.213C2.405 0 .105 2.251.105 5v30c0 2.749 2.3 5 5.108 5h127.68c2.808 0 5.107-2.251 5.107-5V5c0-2.749-2.299-5-5.107-5Z" /><path fill="#fff" d="M30.88 19.784c-.03-3.223 2.695-4.791 2.82-4.864-1.544-2.203-3.936-2.504-4.776-2.528-2.01-.207-3.959 1.177-4.982 1.177-1.044 0-2.62-1.157-4.319-1.123-2.186.033-4.23 1.272-5.352 3.196-2.315 3.923-.588 9.688 1.63 12.859 1.108 1.553 2.405 3.287 4.101 3.226 1.66-.067 2.28-1.036 4.283-1.036 1.985 0 2.567 1.036 4.297.997 1.782-.028 2.903-1.56 3.974-3.127 1.282-1.78 1.797-3.533 1.817-3.623-.042-.014-3.46-1.291-3.493-5.154ZM27.611 10.306c.893-1.093 1.504-2.58 1.334-4.089-1.292.056-2.908.875-3.838 1.944-.824.942-1.56 2.486-1.37 3.938 1.452.106 2.943-.717 3.874-1.793ZM50.207 10.009c0 1.177-.36 2.063-1.08 2.658-.668.549-1.616.824-2.843.824-.61 0-1.13-.026-1.566-.078V6.982c.569-.09 1.182-.136 1.843-.136 1.17 0 2.051.249 2.646.747.666.563 1 1.368 1 2.416Zm-1.129.029c0-.763-.206-1.348-.619-1.756-.412-.407-1.015-.611-1.809-.611-.337 0-.624.022-.862.068v4.889c.132.02.373.029.723.029.82 0 1.452-.223 1.897-.669.446-.446.67-1.096.67-1.95ZM56.192 11.037c0 .725-.211 1.319-.634 1.785-.444.479-1.03.718-1.764.718-.707 0-1.27-.229-1.69-.689-.419-.459-.628-1.038-.628-1.736 0-.73.216-1.329.649-1.794.433-.465 1.015-.698 1.748-.698.707 0 1.275.229 1.705.688.409.446.614 1.022.614 1.726Zm-1.11.034c0-.435-.096-.808-.287-1.119-.225-.376-.545-.564-.96-.564-.43 0-.757.188-.982.564-.192.311-.287.69-.287 1.138 0 .435.096.808.287 1.119.232.376.555.564.971.564.409 0 .73-.191.96-.574.199-.317.298-.693.298-1.128ZM64.216 8.719l-1.506 4.714h-.981l-.624-2.047a15.061 15.061 0 0 1-.387-1.523h-.02a10.947 10.947 0 0 1-.387 1.523l-.663 2.047h-.992L57.24 8.719h1.1l.544 2.241c.132.53.24 1.035.327 1.513h.02c.08-.394.211-.896.397-1.503l.683-2.25h.873l.654 2.202c.159.537.287 1.054.386 1.552h.03c.073-.485.182-1.002.327-1.552l.584-2.202h1.051v-.001ZM69.766 13.433h-1.07v-2.7c0-.832-.323-1.248-.97-1.248a.975.975 0 0 0-.774.343 1.202 1.202 0 0 0-.297.808v2.796h-1.07v-3.366c0-.414-.014-.863-.04-1.349h.941l.05.737h.03c.124-.229.31-.418.555-.569.29-.176.614-.265.97-.265.45 0 .823.142 1.12.427.37.349.555.87.555 1.562v2.824ZM72.718 13.433h-1.07V6.556h1.07v6.877ZM79.02 11.037c0 .725-.211 1.319-.634 1.785-.443.479-1.032.718-1.764.718-.708 0-1.27-.229-1.69-.689-.418-.459-.628-1.038-.628-1.736 0-.73.216-1.329.649-1.794.433-.465 1.015-.698 1.748-.698.707 0 1.274.229 1.705.688.409.446.614 1.022.614 1.726Zm-1.111.034c0-.435-.096-.808-.287-1.119-.224-.376-.545-.564-.96-.564-.43 0-.757.188-.98.564-.193.311-.288.69-.288 1.138 0 .435.096.808.287 1.119.232.376.555.564.972.564.408 0 .728-.191.959-.574.199-.317.297-.693.297-1.128ZM84.201 13.433h-.961l-.08-.543h-.03c-.328.433-.797.65-1.406.65-.455 0-.822-.143-1.099-.427a1.323 1.323 0 0 1-.377-.96c0-.576.245-1.015.739-1.319.492-.304 1.184-.453 2.076-.446V10.3c0-.621-.333-.931-1-.931-.475 0-.894.117-1.255.349l-.218-.688c.448-.271 1-.407 1.652-.407 1.258 0 1.89.65 1.89 1.95v1.736c0 .471.023.846.069 1.124Zm-1.111-1.62v-.727c-1.181-.02-1.772.297-1.772.95 0 .246.068.43.206.553a.758.758 0 0 0 .523.184c.235 0 .454-.073.654-.218a.89.89 0 0 0 .389-.742ZM90.284 13.433h-.95l-.05-.757h-.03c-.303.576-.82.864-1.547.864-.58 0-1.063-.223-1.446-.669-.383-.446-.574-1.025-.574-1.736 0-.763.207-1.381.624-1.853.404-.44.898-.66 1.486-.66.647 0 1.1.213 1.357.64h.02V6.556h1.072v5.607c0 .459.012.882.038 1.27Zm-1.11-1.988v-.786a1.19 1.19 0 0 0-.417-.965c-.199-.171-.439-.257-.716-.257-.399 0-.712.155-.941.466-.228.311-.343.708-.343 1.193 0 .466.109.844.328 1.135.232.31.545.465.936.465.351 0 .632-.129.846-.388.206-.239.307-.527.307-.863ZM99.439 11.037c0 .725-.212 1.319-.635 1.785-.443.479-1.03.718-1.764.718-.706 0-1.268-.229-1.69-.689-.418-.459-.627-1.038-.627-1.736 0-.73.215-1.329.648-1.794.433-.465 1.016-.698 1.75-.698.706 0 1.275.229 1.704.688.408.446.614 1.022.614 1.726Zm-1.11.034c0-.435-.096-.808-.287-1.119-.225-.376-.544-.564-.96-.564-.43 0-.757.188-.982.564-.192.311-.287.69-.287 1.138 0 .435.096.808.287 1.119.231.376.554.564.971.564.409 0 .73-.191.961-.574.197-.317.297-.693.297-1.128ZM105.195 13.433h-1.07v-2.7c0-.832-.323-1.248-.971-1.248a.97.97 0 0 0-.772.343 1.193 1.193 0 0 0-.298.808v2.796h-1.071v-3.366c0-.414-.012-.863-.038-1.349h.94l.05.737h.029c.126-.229.312-.418.555-.569.291-.176.615-.265.972-.265.448 0 .822.142 1.119.427.371.349.555.87.555 1.562v2.824ZM112.399 9.504h-1.179v2.29c0 .582.21.873.624.873.192 0 .352-.016.477-.049l.028.795c-.212.078-.489.117-.832.117-.423 0-.751-.126-.989-.378-.239-.252-.358-.676-.358-1.271V9.504h-.704v-.785h.704v-.864l1.049-.31v1.173h1.179v.786h.001ZM118.066 13.433h-1.072v-2.68c0-.845-.323-1.268-.969-1.268-.497 0-.836.245-1.022.735-.031.103-.05.229-.05.377v2.835h-1.069V6.556h1.069v2.841h.021c.337-.517.82-.775 1.446-.775.443 0 .81.142 1.101.427.363.355.545.883.545 1.581v2.803ZM123.911 10.853c0 .188-.014.346-.04.475h-3.21c.014.466.168.821.465 1.067.271.22.622.33 1.051.33.475 0 .908-.074 1.298-.223l.168.728c-.457.194-.994.291-1.616.291-.746 0-1.333-.215-1.758-.645-.427-.43-.639-1.007-.639-1.731 0-.711.198-1.303.595-1.775.415-.504.975-.756 1.683-.756.693 0 1.219.252 1.574.756.287.4.429.895.429 1.483Zm-1.021-.271a1.39 1.39 0 0 0-.208-.805c-.185-.291-.468-.437-.851-.437-.35 0-.635.142-.852.427a1.567 1.567 0 0 0-.318.815h2.229ZM54.9 31.504h-2.319l-1.27-3.909h-4.417l-1.21 3.909h-2.26l4.377-13.308h2.702l4.398 13.308Zm-3.973-5.549-1.149-3.475c-.121-.355-.35-1.191-.685-2.507h-.041c-.134.566-.35 1.402-.646 2.507l-1.128 3.475h3.65ZM66.154 26.588c0 1.632-.45 2.922-1.351 3.869-.807.843-1.81 1.264-3.005 1.264-1.292 0-2.219-.454-2.784-1.362h-.04v5.055h-2.178V25.067c0-1.026-.028-2.079-.081-3.159h1.915l.122 1.521h.04c.727-1.146 1.829-1.718 3.308-1.718 1.156 0 2.121.447 2.894 1.342.774.896 1.16 2.074 1.16 3.535Zm-2.219.078c0-.934-.214-1.704-.645-2.31-.471-.632-1.103-.948-1.896-.948-.537 0-1.026.176-1.462.523-.437.35-.723.807-.857 1.373-.067.264-.1.48-.1.65v1.6c0 .698.218 1.287.655 1.768.437.481 1.005.721 1.704.721.82 0 1.458-.31 1.915-.928.458-.619.686-1.435.686-2.449ZM77.428 26.588c0 1.632-.45 2.922-1.352 3.869-.806.843-1.808 1.264-3.005 1.264-1.29 0-2.218-.454-2.782-1.362h-.04v5.055H68.07V25.067c0-1.026-.027-2.079-.08-3.159h1.915l.121 1.521h.041c.726-1.146 1.828-1.718 3.308-1.718 1.155 0 2.12.447 2.895 1.342.77.896 1.158 2.074 1.158 3.535Zm-2.219.078c0-.934-.215-1.704-.646-2.31-.471-.632-1.101-.948-1.895-.948-.538 0-1.026.176-1.463.523-.437.35-.722.807-.856 1.373a2.79 2.79 0 0 0-.1.65v1.6c0 .698.218 1.287.653 1.768.437.48 1.005.721 1.706.721.82 0 1.458-.31 1.915-.928.458-.619.686-1.435.686-2.449ZM90.032 27.772c0 1.132-.401 2.053-1.207 2.764-.886.777-2.119 1.165-3.703 1.165-1.463 0-2.635-.276-3.523-.829l.505-1.777c.956.566 2.005.85 3.148.85.82 0 1.458-.182 1.917-.544.457-.362.684-.848.684-1.454 0-.54-.188-.995-.564-1.364-.375-.369-1.002-.712-1.876-1.029-2.38-.869-3.569-2.142-3.569-3.816 0-1.094.417-1.991 1.252-2.689.831-.699 1.94-1.048 3.327-1.048 1.237 0 2.265.211 3.085.632l-.544 1.738c-.766-.408-1.632-.612-2.602-.612-.766 0-1.364.185-1.793.553-.363.329-.545.73-.545 1.205 0 .526.207.961.624 1.303.363.316 1.022.658 1.978 1.027 1.17.461 2.028 1 2.58 1.618.551.616.826 1.387.826 2.307ZM97.233 23.508h-2.4v4.659c0 1.185.422 1.777 1.27 1.777.389 0 .712-.033.967-.099l.06 1.619c-.429.157-.993.236-1.693.236-.86 0-1.532-.257-2.018-.77-.483-.514-.726-1.376-.726-2.587v-4.837h-1.43v-1.6h1.43v-1.757l2.14-.632v2.389h2.4v1.602ZM108.062 26.627c0 1.475-.431 2.686-1.291 3.633-.902.975-2.099 1.461-3.591 1.461-1.438 0-2.583-.467-3.437-1.401-.854-.934-1.281-2.113-1.281-3.534 0-1.487.44-2.705 1.32-3.652.88-.948 2.067-1.422 3.559-1.422 1.439 0 2.596.467 3.469 1.402.836.907 1.252 2.078 1.252 3.513Zm-2.259.069c0-.885-.193-1.644-.584-2.277-.457-.766-1.11-1.148-1.955-1.148-.876 0-1.541.383-1.997 1.148-.391.634-.584 1.405-.584 2.317 0 .885.193 1.644.584 2.276.471.766 1.128 1.148 1.977 1.148.832 0 1.484-.39 1.955-1.168.402-.645.604-1.412.604-2.296ZM115.142 23.783a3.871 3.871 0 0 0-.687-.059c-.766 0-1.358.283-1.775.85-.363.5-.545 1.132-.545 1.895v5.035h-2.176l.02-6.574c0-1.106-.027-2.113-.082-3.021h1.897l.08 1.836h.06c.23-.631.593-1.139 1.089-1.52a2.67 2.67 0 0 1 1.574-.514c.201 0 .383.014.545.039v2.033ZM124.881 26.252c0 .382-.026.704-.08.967h-6.533c.025.948.341 1.673.948 2.173.55.447 1.262.671 2.137.671.967 0 1.85-.151 2.643-.454l.341 1.48c-.927.396-2.022.593-3.286.593-1.52 0-2.713-.438-3.581-1.313-.866-.875-1.3-2.05-1.3-3.524 0-1.447.403-2.652 1.211-3.613.846-1.026 1.989-1.539 3.427-1.539 1.413 0 2.482.513 3.209 1.539.575.815.864 1.823.864 3.02Zm-2.077-.553c.014-.632-.127-1.178-.423-1.639-.377-.593-.956-.889-1.735-.889-.712 0-1.291.289-1.734.869-.362.461-.578 1.014-.644 1.658h4.536v.001Z" /></svg>







  
  


</a>
          </div>
        </div>
    </div>
    <div class="je2-footer__settings">
      <div class="je2-footer__label">SETTINGS</div>

      <form class="js-form">
        <div class="je2-select">
  <svg class="je2-select__right-icon"><use xlink:href="#arrow-down"></use></svg>
  <select name="je_language" id="je_language" aria-label="je_language"><option selected="selected" value="en">English</option>
<option value="de">German</option>
<option value="fr">French</option>
<option value="es">Spanish</option>
<option value="it">Italian</option></select>
</div>
        <div class="je2-select">
  <svg class="je2-select__right-icon"><use xlink:href="#arrow-down"></use></svg>
  <select name="je_currency" id="je_currency" aria-label="je_currency"><option value="AUD">Australian dollar - AUD $</option>
<option value="BRL">Brazilian real - BRL R$</option>
<option value="CAD">Canadian dollar - CAD $</option>
<option value="CZK">Czech korun - CZK Kč</option>
<option value="DKK">Danish krone - DKK kr.</option>
<option value="AED">Emirati dirham - AED AED</option>
<option selected="selected" value="EUR">Euro - EUR €</option>
<option value="HKD">Hong Kong dollar - HKD HK$</option>
<option value="HUF">Hungarian forint - HUF Ft</option>
<option value="INR">Indian rupee - INR ₹</option>
<option value="JPY">Japanese yen - JPY ¥</option>
<option value="MYR">Malaysian ringgit - MYR RM</option>
<option value="MXN">Mexican peso - MXN $</option>
<option value="NZD">New Zealand dollar - NZD $</option>
<option value="NOK">Norwegian krone - NOK kr</option>
<option value="PLN">Polish zloty - PLN zł</option>
<option value="GBP">Pound sterling - GBP £</option>
<option value="RUB">Russian ruble - RUB RUB</option>
<option value="SAR">Saudi Arabian riyal - SAR ر.س</option>
<option value="SGD">Singapore dollar - SGD $</option>
<option value="ZAR">South African rand - ZAR R</option>
<option value="KRW">South Korean won - KRW ₩</option>
<option value="SEK">Swedish krona - SEK kr</option>
<option value="CHF">Swiss franc - CHF CHF</option>
<option value="TRY">Turkish lira - TRY ₺</option>
<option value="USD">United States dollar - USD $</option></select>
</div>
        <div class="je2-select">
  <svg class="je2-select__right-icon"><use xlink:href="#arrow-down"></use></svg>
  <select name="je_measurement_units" id="je_measurement_units" aria-label="je_measurement_units"><option value="sqft">Square Feet — ft² / Acre - Ac</option>
<option selected="selected" value="sqm">Square Meter — m² / Hectare - Ha</option></select>
</div>
      </form>
    </div>
  </div>
  <div class="je2-footer__bottom">
    <div class="je2-footer__copyright">
      <div class="je2-footer__logo">
        <svg width="26" height="28" viewBox="0 0 26 28" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12.7263 0C4.88083 0 0 0.666315 0 0.666315C0 0.666315 0 8.73379 0 14.5746C0 19.5614 1.88428 22.4059 5.63582 24.407L12.7263 28L19.8168 24.407C23.5705 22.4059 25.4526 19.5614 25.4526 14.5746C25.4526 8.73379 25.4526 0.666315 25.4526 0.666315C25.4526 0.666315 20.5739 0 12.7263 0ZM11.546 5.43384C11.1121 5.60675 10.9675 5.83658 10.9675 6.3806V14.5219C10.9675 16.7464 10.0807 17.4338 8.42821 17.805C7.25 18.0706 5.50396 17.6616 5.50396 17.6616L5.31043 16.1223L5.59966 16.0253C6.10157 16.9784 6.70981 17.7396 7.65833 17.5287C8.67916 17.2989 8.59409 14.524 8.59409 14.524C8.59409 14.524 8.59409 6.83184 8.59409 6.38271C8.59409 5.83658 8.46436 5.60675 8.03051 5.43595V5.22088H8.0454H11.5354H11.5502V5.43384H11.546ZM19.6233 17.3769H12.3712V17.1766C12.805 16.991 12.9496 16.7612 12.9496 16.2298V6.38271C12.9496 5.83658 12.805 5.60675 12.3712 5.43595V5.22088H19.4659L19.6254 7.05746H19.2936C18.8598 6.02425 18.192 5.57934 17.0627 5.57934H16.2673C15.5868 5.57934 15.3124 5.80917 15.3124 6.38271V10.6885H16.6289C17.5689 10.6885 18.0325 10.3869 18.1346 9.69742H18.4387V12.1518H18.1346C18.092 11.4201 17.6561 11.1038 16.6289 11.1038H15.3124V16.0991C15.3124 16.3585 15.3422 16.544 15.3996 16.66C15.5293 16.9046 15.9058 17.0185 16.5438 17.0185H17.2669C18.1346 17.0185 18.7301 16.8034 19.2362 16.3015C19.5106 16.0295 19.6424 15.8144 19.8445 15.2831L20.1486 15.4117L19.6233 17.3769Z" fill="#606060"/>
</svg>

      </div>
      Copyright © 2025 JamesEdition B.V.®
    </div>
    <div class="je2-footer__social">
      <a alt="Instagram" aria-label="Instagram" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://www.instagram.com/jameseditioncom/">
        <svg viewBox="0 0 30 30">
  <path d="M11.2559 6C10.3079 6 9.42773 6.23698 8.61523 6.71094C7.81966 7.1849 7.1849 7.82812 6.71094 8.64062C6.23698 9.4362 6 10.3079 6 11.2559V18.6191C6 19.5671 6.23698 20.4473 6.71094 21.2598C7.1849 22.0553 7.81966 22.6901 8.61523 23.1641C9.42773 23.638 10.3079 23.875 11.2559 23.875H18.6191C19.5671 23.875 20.4388 23.638 21.2344 23.1641C22.0469 22.6901 22.6901 22.0553 23.1641 21.2598C23.638 20.4473 23.875 19.5671 23.875 18.6191V11.2559C23.875 10.3079 23.638 9.4362 23.1641 8.64062C22.6901 7.82812 22.0469 7.1849 21.2344 6.71094C20.4388 6.23698 19.5671 6 18.6191 6H11.2559ZM11.2559 7.625H18.6191C19.2793 7.625 19.8887 7.78581 20.4473 8.10742C21.0059 8.42904 21.446 8.86914 21.7676 9.42773C22.0892 9.98633 22.25 10.5957 22.25 11.2559V18.6191C22.25 19.2793 22.0892 19.8887 21.7676 20.4473C21.446 21.0059 21.0059 21.446 20.4473 21.7676C19.8887 22.0892 19.2793 22.25 18.6191 22.25H11.2559C10.5957 22.25 9.98633 22.0892 9.42773 21.7676C8.86914 21.446 8.42904 21.0059 8.10742 20.4473C7.78581 19.8887 7.625 19.2793 7.625 18.6191V11.2559C7.625 10.5957 7.78581 9.98633 8.10742 9.42773C8.42904 8.86914 8.86914 8.42904 9.42773 8.10742C9.98633 7.78581 10.5957 7.625 11.2559 7.625ZM19.7363 9.40234C19.5332 9.40234 19.3555 9.47852 19.2031 9.63086C19.0677 9.76628 19 9.93555 19 10.1387C19 10.3418 19.0677 10.5195 19.2031 10.6719C19.3555 10.8073 19.5332 10.875 19.7363 10.875C19.9395 10.875 20.1087 10.8073 20.2441 10.6719C20.3965 10.5195 20.4727 10.3418 20.4727 10.1387C20.4727 9.93555 20.3965 9.76628 20.2441 9.63086C20.1087 9.47852 19.9395 9.40234 19.7363 9.40234ZM14.9375 10.0625C14.0573 10.0625 13.2448 10.2826 12.5 10.7227C11.7552 11.1628 11.1628 11.7552 10.7227 12.5C10.2826 13.2448 10.0625 14.0573 10.0625 14.9375C10.0625 15.8177 10.2826 16.6302 10.7227 17.375C11.1628 18.1198 11.7552 18.7122 12.5 19.1523C13.2448 19.5924 14.0573 19.8125 14.9375 19.8125C15.8177 19.8125 16.6302 19.5924 17.375 19.1523C18.1198 18.7122 18.7122 18.1198 19.1523 17.375C19.5924 16.6302 19.8125 15.8177 19.8125 14.9375C19.8125 14.0573 19.5924 13.2448 19.1523 12.5C18.7122 11.7552 18.1198 11.1628 17.375 10.7227C16.6302 10.2826 15.8177 10.0625 14.9375 10.0625ZM14.9375 11.6875C15.5299 11.6875 16.0716 11.8314 16.5625 12.1191C17.0703 12.4069 17.4681 12.8047 17.7559 13.3125C18.0436 13.8034 18.1875 14.3451 18.1875 14.9375C18.1875 15.5299 18.0436 16.0801 17.7559 16.5879C17.4681 17.0788 17.0703 17.4681 16.5625 17.7559C16.0716 18.0436 15.5299 18.1875 14.9375 18.1875C14.3451 18.1875 13.7949 18.0436 13.2871 17.7559C12.7962 17.4681 12.4069 17.0788 12.1191 16.5879C11.8314 16.0801 11.6875 15.5299 11.6875 14.9375C11.6875 14.3451 11.8314 13.8034 12.1191 13.3125C12.4069 12.8047 12.7962 12.4069 13.2871 12.1191C13.7949 11.8314 14.3451 11.6875 14.9375 11.6875Z"/>
</svg>

</a>      <a alt="Facebook" aria-label="Facebook" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://www.facebook.com/thejamesedition">
        <svg viewBox="0 0 30 30">
  <path d="M7.625 6C7.1849 6 6.80404 6.16081 6.48242 6.48242C6.16081 6.80404 6 7.1849 6 7.625V22.25C6 22.6901 6.16081 23.071 6.48242 23.3926C6.80404 23.7142 7.1849 23.875 7.625 23.875H22.25C22.6901 23.875 23.071 23.7142 23.3926 23.3926C23.7142 23.071 23.875 22.6901 23.875 22.25V7.625C23.875 7.1849 23.7142 6.80404 23.3926 6.48242C23.071 6.16081 22.6901 6 22.25 6H7.625ZM7.625 7.625H22.25V22.25H18.0352V16.7656H20.1426L20.4473 14.3281H18.0352V12.7539C18.0352 12.3477 18.1029 12.0599 18.2383 11.8906C18.4245 11.6706 18.7546 11.5605 19.2285 11.5605H20.5488V9.35156C20.1426 9.30078 19.5078 9.27539 18.6445 9.27539C17.6797 9.27539 16.9095 9.55469 16.334 10.1133C15.7754 10.6719 15.4961 11.4674 15.4961 12.5V14.3281H13.3633V16.7656H15.4961V22.25H7.625V7.625Z"/>
</svg>

</a>      <a alt="Youtube" aria-label="Youtube" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://www.youtube.com/channel/UC0ilNPVLpRHDMFgfLVr3v4Q">
      <svg viewBox="0 0 32 32">
  <path d="M26.7809 11.4524C26.7809 11.4524 26.566 9.88392 25.9043 9.19522C25.0664 8.28881 24.1297 8.28437 23.7 8.23105C20.6234 8 16.0043 8 16.0043 8H15.9957C15.9957 8 11.3766 8 8.3 8.23105C7.87031 8.28437 6.93359 8.28881 6.0957 9.19522C5.43398 9.88392 5.22344 11.4524 5.22344 11.4524C5.22344 11.4524 5 13.2963 5 15.1358V16.8598C5 18.6992 5.21914 20.5432 5.21914 20.5432C5.21914 20.5432 5.43398 22.1116 6.09141 22.8003C6.9293 23.7067 8.0293 23.6756 8.51914 23.7734C10.2809 23.9467 16 24 16 24C16 24 20.6234 23.9911 23.7 23.7645C24.1297 23.7112 25.0664 23.7067 25.9043 22.8003C26.566 22.1116 26.7809 20.5432 26.7809 20.5432C26.7809 20.5432 27 18.7037 27 16.8598V15.1358C27 13.2963 26.7809 11.4524 26.7809 11.4524ZM13.727 18.9525V12.5587L19.6695 15.7667L13.727 18.9525Z"/>
</svg>

</a>      <a alt="Twitter" aria-label="Twitter" target="_blank" rel="noreferrer" class="je2-footer__social-link _twitter" href="https://twitter.com/JamesEdition">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1227"><path d="M714.16 519.28 1160.9 0h-105.86l-387.9 450.89L357.34 0H0l468.5 681.82L0 1226.37h105.87l409.62-476.15 327.18 476.15H1200L714.14 519.28h.02Zm-145 168.55-47.46-67.9L144 79.7h162.6l304.8 436 47.47 67.89 396.2 566.72h-162.6L569.16 687.85v-.02Z" /></svg>

</a>      <a alt="linkedin" aria-label="linkedin" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://www.linkedin.com/company/jamesedition/">
        <svg viewBox="0 0 32 32">
  <path d="M9.63546 5.3335C9.00351 5.3335 8.46185 5.55919 8.01046 6.01058C7.55907 6.44391 7.33337 6.98558 7.33337 7.63558C7.33337 8.26752 7.55907 8.80919 8.01046 9.26058C8.46185 9.71197 8.99449 9.93766 9.60837 9.93766C10.2403 9.93766 10.782 9.71197 11.2334 9.26058C11.6848 8.80919 11.9105 8.26752 11.9105 7.63558C11.9105 7.00363 11.6848 6.46197 11.2334 6.01058C10.8 5.55919 10.2674 5.3335 9.63546 5.3335ZM20.7938 11.4002C19.9091 11.4002 19.1417 11.6078 18.4917 12.0231C17.9681 12.3661 17.5528 12.8266 17.2459 13.4043H17.1917V11.671H13.4V24.4002H17.3542V18.0897C17.3542 17.4036 17.3903 16.88 17.4625 16.5189C17.5709 15.9772 17.7695 15.571 18.0584 15.3002C18.4014 14.9932 18.8889 14.8397 19.5209 14.8397C20.1528 14.8397 20.6313 15.0203 20.9563 15.3814C21.2271 15.6703 21.4077 16.1036 21.498 16.6814C21.5521 17.0245 21.5792 17.53 21.5792 18.1981V24.4002H25.5334V17.4127C25.5334 16.1307 25.416 15.1016 25.1813 14.3252C24.9105 13.3863 24.45 12.6731 23.8 12.1856C23.0778 11.662 22.0757 11.4002 20.7938 11.4002ZM7.65837 11.671V24.4002H11.6125V11.671H7.65837Z"/>
</svg>

</a>      <a alt="pinterest" aria-label="pinterest" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://pinterest.com/jamesedition/">
        <svg viewBox="0 0 32 32">
  <path d="M15.4667 6.6665C13.8056 6.6665 12.2563 7.08178 10.8188 7.91234C9.42922 8.72692 8.32714 9.829 7.51256 11.2186C6.682 12.6561 6.26672 14.2054 6.26672 15.8665C6.26672 17.1443 6.52228 18.3662 7.03339 19.5321C7.51256 20.6502 8.19138 21.6405 9.06985 22.503C9.96429 23.3495 10.9785 23.9964 12.1126 24.4436C11.9848 23.3096 11.9928 22.4231 12.1365 21.7842L13.2146 17.2321L13.1428 17.0405C13.0948 16.8967 13.0549 16.737 13.023 16.5613C12.9751 16.3377 12.9511 16.0981 12.9511 15.8425C12.9511 15.2196 13.1108 14.6925 13.4303 14.2613C13.7497 13.83 14.141 13.6144 14.6042 13.6144C14.9876 13.6144 15.2751 13.7422 15.4667 13.9978C15.6744 14.2373 15.7782 14.5408 15.7782 14.9082C15.7782 15.1318 15.7383 15.4193 15.6584 15.7707C15.5945 15.9943 15.4907 16.3297 15.3469 16.7769C15.1872 17.32 15.0754 17.7193 15.0115 17.9748C14.8997 18.438 14.9796 18.8373 15.2511 19.1728C15.5386 19.4922 15.9139 19.6519 16.3771 19.6519C16.9202 19.6519 17.4073 19.4762 17.8386 19.1248C18.2858 18.7575 18.6372 18.2544 18.8928 17.6155C19.1483 16.9766 19.2761 16.2498 19.2761 15.4353C19.2761 14.7005 19.1084 14.0537 18.773 13.4946C18.4535 12.9196 17.9983 12.4804 17.4073 12.1769C16.8323 11.8575 16.1695 11.6978 15.4188 11.6978C14.5883 11.6978 13.8455 11.8894 13.1907 12.2728C12.5837 12.6241 12.1126 13.1113 11.7771 13.7342C11.4417 14.3412 11.274 14.988 11.274 15.6748C11.274 16.0582 11.3379 16.4495 11.4657 16.8488C11.5935 17.2321 11.7612 17.5436 11.9688 17.7832C12.0327 17.863 12.0487 17.9509 12.0167 18.0467L11.7771 19.0769C11.7292 19.2526 11.6254 19.2925 11.4657 19.1967C10.9067 18.9571 10.4514 18.47 10.1001 17.7353C9.76464 17.0484 9.59693 16.3537 9.59693 15.6509C9.59693 14.6606 9.82853 13.7502 10.2917 12.9196C10.7709 12.0412 11.4497 11.3623 12.3282 10.8832C13.2865 10.3401 14.4046 10.0686 15.6823 10.0686C16.7205 10.0686 17.6709 10.3002 18.5334 10.7634C19.4119 11.2266 20.0987 11.8655 20.5938 12.68C21.0889 13.4946 21.3365 14.3971 21.3365 15.3873C21.3365 16.4415 21.1289 17.4078 20.7136 18.2863C20.3143 19.1488 19.7473 19.8356 19.0126 20.3467C18.2938 20.8578 17.4792 21.1134 16.5688 21.1134C16.1056 21.1134 15.6744 21.0096 15.2751 20.8019C14.8917 20.5943 14.6202 20.3467 14.4605 20.0592L13.8855 22.2394C13.7258 22.8783 13.3424 23.6849 12.7355 24.6592C13.6299 24.9307 14.5403 25.0665 15.4667 25.0665C17.1278 25.0665 18.6771 24.6512 20.1146 23.8207C21.5042 23.0061 22.6063 21.904 23.4209 20.5144C24.2514 19.0769 24.6667 17.5276 24.6667 15.8665C24.6667 14.2054 24.2514 12.6561 23.4209 11.2186C22.6063 9.829 21.5042 8.72692 20.1146 7.91234C18.6771 7.08178 17.1278 6.6665 15.4667 6.6665Z"/>
</svg>

</a>    </div>
  </div>
</div>

      </div>
    </div>
      <script data-turbolinks-track="reload" type="131723e888cc8f98efbd5b21-text/javascript">
  (function () {
      window.dataLayer = window.dataLayer || [];

      const dimensions = {"dimension1":null,"dimension2":null,"dimension3":null,"dimension4":null,"dimension5":null,"dimension6":"FR","dimension7":"","dimension8":"real_estate","dimension9":"SearchResult","dimension10":"No","dimension11":null,"dimension12":"For sale","dimension13":"RealEstate","dimension14":null,"dimension15":null,"dimension16":null,"dimension17":"92484","dimension18":null};
      const events = [];

      window.dataLayer.push({
        office_id: dimensions.dimension1,
        agent_id: dimensions.dimension2,
        listing_id: dimensions.dimension3,
        group_id: dimensions.dimension4,
        country: dimensions.dimension6,
        city: dimensions.dimension7,
        category: dimensions.dimension8,
        page_type: dimensions.dimension9,
        is_authenticated: dimensions.dimension10,
        listing_price: dimensions.dimension11,
        section: dimensions.dimension12,
        sub_section: dimensions.dimension13,
        current_experiment: dimensions.dimension16,
        place_id: dimensions.dimension17,
        subscription: dimensions.dimension18,
      });

      for (let event of events) {
        window.dataLayer.push({ event: event });
      }

        window.dataLayer.push({ userAuth: 0});

  })();
</script>

  <script type="131723e888cc8f98efbd5b21-text/javascript" data-turbolinks-track="reload">
  window.addEventListener("load", () => {
    setTimeout(() => {
      (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
      new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
      j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
      'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
      })(window,document,'script','dataLayer','GTM-N8N6RLK');
    },1);
  });

  window.dataLayer = window.dataLayer || []
</script>


  <noscript>
  <iframe height="0" src="https://www.googletagmanager.com/ns.html?id=GTM-N8N6RLK" style="display:none;visibility:hidden" width="0"></iframe>
</noscript>


    <script id="Cookiebot" src="https://consent.cookiebot.com/uc.js" data-cbid="a5081197-ee35-4671-954e-50cefb375242" type="131723e888cc8f98efbd5b21-text/javascript"></script>

<script type="131723e888cc8f98efbd5b21-text/javascript">
    SIGNUP_PATH = "/signup";
    RECENT_LISTINGS_PATH = "/buyer/recent-listings/create";
    SAVE_LISTING_PATH = "/buyer/saved-listings/create";
    UNSAVE_LISTING_PATH = "/buyer/saved-listings/remove";

    window.mixpanelToken = "bfe35bec091a7744f92d5d75ca232054";

    window.DATA = window.DATA || {};
    window.DATA.currenciesConvertTable = {"USD":1.1651956072125609,"EUR":"1.0","AED":"4.27918086748812956975152203676194521610142125412","AUD":"1.7549022692184450464621748376009","CAD":"1.6184916542864633400332080748055545545540767365","CHF":"0.936135628768679542078126365463565335999322877065","CNY":"8.2393311777214599900958373386932","GBP":"0.872724518628564770310815928223986673302475234288","HKD":"9.0714847505024906056104168487285","HRK":"7.5340312855020536572577121384252","MXN":"21.202124151591948498354161204812","NOK":"11.75828832765300474817209939118528707310503202438","RUB":"89.432259605581286958548166273413","SEK":"10.958912872498470680765533513939","THB":"37.11148008972006175536718226572229175287462456488","ZAR":"19.73451600687465408255410877101","TWD":"36.439744822162020449182906580442","PHP":"68.734891199860176527134492702963","CZK":"24.201811879169215532057444143436","MUR":"53.68056395467389087943138454367963900967381397581","SGD":"1.5089236505578373969530134871392","KYD":"0.97070465204346179614902851816249","CLP":"1071.44396865623816598211424742928540157142677116807","PAB":"1.1651956072125608086457514055172","BBD":"2.3303912144251216172915028110344","INR":"104.79695301348713915348539136007","JPY":"180.83486265256779981939468088205336562656860022823","XCD":"3.1489993882723062134055754609805","NZD":"2.01591307640770194296367502694513859108602724549","GIP":"0.87272451862856477031081592822395","BRL":"6.2210958664685834134405313291969","ILS":"3.762614698942584986454601066154","OMR":"0.44799790264790701739054443764747","PLN":"4.2316583646479652771709050656879","FJD":"2.63386641032363307990328876460137335781720586353","COP":"4424.82603046986512860846514608632846624800013598938","XPF":"119.3318045966966704535523901074898662131785789749","BSD":"1.1651956072125608086457514055172","QAR":"4.2455766261761193160301785662268","CRC":"568.96400477730198957149931544758","HUF":"381.99319059687144979463427422879313804759208607514","MAD":"10.756197966733665414081388913164","DKK":"7.4683328963849806286230300911766","BMD":"1.1651956072125608086457514055172","LKR":"359.27035334556788720906522182411","TRY":"49.536047073902531387456669288357661634880214305","MYR":"4.7901191412508374843426840280812","SAR":"4.3731760319263596376241661568936","KRW":"1715.8745736840572111043141367356910150575917158209","BZD":"2.3425523609775991144513385184538","PYG":"8098.7334626700457339275830930117","IDR":"19437.71685164146931166069503918","DOP":"74.207299950479186693466165632556","JMD":"186.43091380465495645081418043054","EGP":"55.431268024119549069300008738967","XOF":"655.95734218881994814879547904104","NGN":"1690.5590025925602260479477992368","TND":"3.4167834775262897258877334032451","RSD":"117.39345742666550147105945410586","CVE":"110.25987008068979579946983599872","NAD":"19.74051326866497713303620845349410016168766090801","VES":"289.65117422587316845815491275598","MZN":"74.455991144513385184537854292289","KES":"150.65979201258411255789565673337","CLF":"0.027300533076990299746569955431268","ANG":"2.0857001369104838474758950158758","ARS":"1677.2847446765125695476128054997","AWG":"2.0988085874916251565731597191879","VND":"30719.66525328439511783040577937"}

    window.GTM_DATA = window.GTM_DATA || {};
    window.GTM_DATA.country_code = 'DE';
</script>





<script data-cfasync="false" type="text/javascript" id="exposed-vars">
  window.JEParams = window.JEParams || {};
  Object.assign(JEParams, {"listingsCount":"54,100+ homes","searchPageParams":{"city":null,"cityGroup":null,"country":"France","countrySubdivision":null,"numberOfListings":54100,"listingIds":[16460690,16247522,16368872,16293592,16400177,16138374,16397640,15998576,16276704,16225846,16358017,16496560,16129746,16178817,16122150,16137264,16098982,15945756,16296175,15919668,16315771,16402616,15583924,16078872,16474198,15885380,15949407,15989347,16006574,16247710],"promotedListingId":15870025,"order":"premium","pageNumber":1},"isProduction":true,"isStaging":false,"isTest":false,"locale":"en","category":"RealEstate","pageType":"serp_page","rental":false,"recaptchaSiteKey":"6LeNK2caAAAAABqNVS2GtBowWgxSInPKc9XdX4PE","googlePlacesApiKey":"AIzaSyCk0QTmI7K69eXqOgdFf9ty82mOsYcCIME","withBottomBar":false,"isUsOrEmployee":null,"currentCurrency":"EUR","showSellerEntryPoints":true,"preventInquirySendingWithOtp":true,"singleAgentFlow":false,"showQuestionnaireAfterInquiry":true,"previewFeaturedAgent":false});
</script>

   <script src="https://static-x.jamesedition.com/assets/dist/je2_serp_page.bundle-33040d0ea175302fe046210c007d23902981c2da2fe95509d838adff310066b9.js" async="async" type="131723e888cc8f98efbd5b21-text/javascript"></script>


  <script type="131723e888cc8f98efbd5b21-text/javascript">
  window.addEventListener("load", () => {
      setTimeout(() => {
          const loader = document.createElement("script");
          loader.src = "https://accounts.google.com/gsi/client";
          loader.async = true;
          loader.defer = true;
          document.body.appendChild(loader);
      },2000);
  });
</script>

  <div id="g_id_onload" data-client_id="193019720404-9qm8r0ovhh67sdh5hent9vc9akiskg2l.apps.googleusercontent.com" data-auto_select="true" data-use_fedcm_for_prompt="true" data-login_uri="https://www.jamesedition.com/auth/google/using_one_tap" data-after_auth_redirect_url="https://www.jamesedition.com/real_estate/france?real_estate_type[]=house&amp;real_estate_type[]=villa&amp;real_estate_type[]=estate&amp;real_estate_type[]=country_house&amp;real_estate_type[]=finca&amp;real_estate_type[]=chalet&amp;real_estate_type[]=townhouse&amp;real_estate_type[]=bungalow&amp;bedrooms_from=3&amp;eur_price_cents_to=247208500"></div>



<script type="131723e888cc8f98efbd5b21-text/javascript">
    const connection = window.navigator.connection || window.navigator.mozConnection || window.navigator.webkitConnection || {};

    if (!connection) window.navigator.connection = {};

    if (!connection.effectiveType) {
        window.navigator.connection = { effectiveType: '4g' };
        const trigger = setTimeout(() => window.navigator.connection.effectiveType =  '2g', 5000); // set to 2g if there is no "load" event in 5 sec
        window.addEventListener("load", () => clearTimeout(trigger) );
    }
</script>

<script type="131723e888cc8f98efbd5b21-text/javascript">
    JEParams.canLoadImmediately = false;
    if (document.readyState !== "complete") window.addEventListener("load", () => setTimeout(() => (JEParams.canLoadImmediately = true), 2000));
    else setTimeout(() => (JEParams.canLoadImmediately = true), 2000)
</script>

<script type="application/ld+json">
  {
    "@context" : "http://schema.org",
    "@type" : "Organization",
    "name" : "JamesEdition",
    "alternateName": ["JE", "James Edition"],
    "url" : "https://www.jamesedition.com/",
    "logo" : "https://assets.jamesedition.com/android-chrome-512x512.png",
    "sameAs": [
      "https://www.facebook.com/thejamesedition",
      "https://twitter.com/JamesEdition",
      "https://www.instagram.com/jameseditioncom/",
      "https://pinterest.com/jamesedition/"
    ],
    "address": {
      "@type": "PostalAddress",
      "postalCode": "1043NX",
      "addressCountry": "The Netherlands",
      "addressLocality": "Amsterdam",
      "streetAddress": "Radarweg 29"
    },
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+31 85 888 5346",
      "contactType": "Customer Service",
      "areaServed": "Worldwide"
    },
    "foundingDate": "2008",
    "foundingLocation": "Stockholm, Sweden",
    "email": "support@jamesedition.com"
  }
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "JamesEdition: Luxury Homes",
  "operatingSystem": "iOS",
  "applicationCategory": "LifestyleApplication",
  "applicationSubCategory": "RealEstateListing",
  "url": "https://www.jamesedition.com/",
  "downloadUrl": "https://apps.apple.com/app/jamesedition-luxury-homes/id6737836918",
  "installUrl": "ios-app://6737836918",
  "identifier": "ios:6737836918",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "10"
  },
  "publisher": {
    "@type": "Organization",
    "name": "JamesEdition B.V.",
    "url": "https://www.jamesedition.com"
  },
  "screenshot": [
    "https://assets.jamesedition.com/app/app_screenshot_1.webp",
    "https://assets.jamesedition.com/app/app_screenshot_2.webp",
    "https://assets.jamesedition.com/app/app_screenshot_3.webp",
    "https://assets.jamesedition.com/app/app_screenshot_4.webp"
  ],
  "description": "Discover the world’s finest luxury properties with JamesEdition. Browse exclusive listings, save searches, and connect with top agents — all in one seamless experience."
}
</script>

  <script src="/cdn-cgi/scripts/7d0fa10a/cloudflare-static/rocket-loader.min.js" data-cf-settings="131723e888cc8f98efbd5b21-|49" defer></script></body>
</html>
"""
    detail_html = """
    
<!DOCTYPE html>
<html lang="en">
  <head prefix="og: http://ogp.me/ns#">
      <link rel="stylesheet" href="https://static-x.jamesedition.com/assets/dist/je2_listing_page_v2.bundle-ae0d39acfb4364837daf1d0d15e607bc58692d3430a31e320bdb4e0223aed84f.css" async="async" />
    <title>Luxury Family Estate With Heated Pool In Angoulême, Nouvelle Aquitaine, France For Sale (16460690)</title>

<link rel="manifest" href="data:application/manifest+json,%7B%22name%22%3A%22JamesEdition%3A%20The%20World's%20Luxury%20Marketplace%22%2C%22short_name%22%3A%22James%5Cr%5CnEdition%22%2C%22start_url%22%3A%22https://www.jamesedition.com/?offline=1%22%2C%22icons%22%3A%5B%7B%22src%22%3A%22https%3A%2F%2Fassets.jamesedition.com%2Fandroid-chrome-192x192.png%22%2C%22sizes%22%3A%22192x192%22%2C%22type%22%3A%22image%2Fpng%22%7D%2C%7B%22src%22%3A%22https%3A%2F%2Fassets.jamesedition.com%2Fje3-square-black-icon-500.jpg%22%2C%22sizes%22%3A%22500x500%22%2C%22type%22%3A%22image%2Fjpg%22%2C%22purpose%22%3A%22maskable%22%7D%2C%7B%22src%22%3A%22https%3A%2F%2Fassets.jamesedition.com%2Fandroid-chrome-512x512.png%22%2C%22sizes%22%3A%22512x512%22%2C%22type%22%3A%22image%2Fpng%22%7D%5D%2C%22theme_color%22%3A%22%23ffffff%22%2C%22background_color%22%3A%22%23ffffff%22%2C%22display%22%3A%22standalone%22%7D">

<link href="https://assets.jamesedition.com/favicon.ico?v=2" rel="shortcut icon" type="image/ico">
<link rel="apple-touch-icon" sizes="180x180" href="https://assets.jamesedition.com/android-chrome-192x192.png?v=2">
<link rel="icon" type="image/png" sizes="32x32" href="https://assets.jamesedition.com/favicon-32x32.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="https://assets.jamesedition.com/favicon-16x16.png?v=2">
<meta name="theme-color" content="#ffffff">
<meta content="en" name="language">
<meta content="en_US" property="og:locale">
  <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport">
<meta name="csrf-param" content="authenticity_token" />
<meta name="csrf-token" content="t8Xe1d8vmm3IAJE-n6j29FE4EHU4JF2U11WKoKpx0o7vbECo5Dr2LuHXQ9OEOBVSlaHdvzO9EhpaXePSy90d0g" />
  <meta content="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/1040x620xc.jpg" property="og:image">
  <link href="https://www.jamesedition.com/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690" rel="canonical">
  <meta content="https://www.jamesedition.com/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690" property="og:url">
  <meta content="Angoulême, Nouvelle-Aquitaine, France | 4 Bed, 2 Bath House For Sale | €667,800 - ELITE GROUP Real Estate is delighted to present this magnificent family..." name="description">
  <meta content="Angoulême, Nouvelle-Aquitaine, France | 4 Bed, 2 Bath House For Sale | €667,800 - ELITE GROUP Real Estate is delighted to present this magnificent family..." property="og:description">
  <meta content="Luxury Family Estate With Heated Pool In Angoulême, Nouvelle Aquitaine, France For Sale (16460690)" property="og:title">
  <meta content="643afb2028860a1f9d0a4750d1b1158c" name="p:domain_verify">
  <meta content="DzNmkvUwkQRm9GzYMJC8PUC3jupgh_K1InmvNQOYS7c" name="google-site-verification">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">

<link href="https://static.jamesedition.com" rel="preconnect">
<link href="https://static-x.jamesedition.com" rel="preconnect">
<link href="https://assets.jamesedition.com" rel="preconnect">
<link href="https://img.jamesedition.com" rel="preconnect">

  <link rel="alternate" hreflang="x-default" href="https://www.jamesedition.com/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690">
  <link rel="alternate" hreflang="en" href="https://www.jamesedition.com/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690">
    <link rel="alternate" hreflang="de" href="https://www.jamesedition.com/de/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690">
    <link rel="alternate" hreflang="fr" href="https://www.jamesedition.com/fr/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690">
    <link rel="alternate" hreflang="es" href="https://www.jamesedition.com/es/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690">
    <link rel="alternate" hreflang="it" href="https://www.jamesedition.com/it/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690">

    <meta content="product" property="og:type">


    <style type="text/css">
    @font-face {
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url('https://static-x.jamesedition.com/assets/inter/inter-regular-15d70055271f3f6df4ffb4287233fc9ebb3770779661c0bee4c8ebf3718627dc.eot');
        src: local(''),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-15d70055271f3f6df4ffb4287233fc9ebb3770779661c0bee4c8ebf3718627dc.eot?#iefix') format('embedded-opentype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-7a1e50a41e236283cc554591d92ca62508132c9cbda31d15ea3e8bfb70a5b50b.woff2') format('woff2'),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-2f9e1bec49baf9ccf9794cdf41e7a9b50a246ce12548cf581e594a24a17e7d40.woff') format('woff'),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-79664a362216fd6a6e7f4dc6f057a6602dab3527605f0fa66ad1f08a4df8f376.ttf') format('truetype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-regular-caacbbac3eafe3961b3b007da19e856b1ad7d3108261110a9e2132b7f00fe06d.svg#Inter') format('svg');
    }

    @font-face {
        font-family: 'Inter';
        font-style: normal;
        font-weight: 500;
        font-display: swap;
        src: url('https://static-x.jamesedition.com/assets/inter/inter-500-93f4acecb976a2df41b26f647c75eb317e912127e31349f23ee8f25f9cc25946.eot');
        src: local(''),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-93f4acecb976a2df41b26f647c75eb317e912127e31349f23ee8f25f9cc25946.eot?#iefix') format('embedded-opentype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-bcf82294eedd8e4011e95d67f12d6a3de1d98c2d6a5fd1196073870cc633f7dd.woff2') format('woff2'),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-4a21a390c618ec545fb2451f60f951a79f9a7df9e6adf61f43a6d1e47842efae.woff') format('woff'),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-2d86d524048555d308128c2ef54f5803a01551d717c190c8385c2000cb587019.ttf') format('truetype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-500-633fc6b1432a6c3eb62583a91585f362ca61409af5242e137bbe4506aaf5f140.svg#Inter') format('svg');
    }

    @font-face {
        font-family: 'Inter';
        font-style: normal;
        font-weight: 600;
        font-display: swap;
        src: url('https://static-x.jamesedition.com/assets/inter/inter-600-8b2f7582931802de7cd6d3dcc20f0fe5d81d1fe2f5a889e8c4678cd78c2cc201.eot');
        src: local(''),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-8b2f7582931802de7cd6d3dcc20f0fe5d81d1fe2f5a889e8c4678cd78c2cc201.eot?#iefix') format('embedded-opentype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-45731a4b0962ee79642ec4bd38650379c588973f9ec57140386ada0f6b8316db.woff2') format('woff2'),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-cbbb70dec22dafdd00716b179ea45f54947dab043b1daa0796dd101ccc0b67ff.woff') format('woff'),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-7aa2268dabb0037837f3afe96957aeb0f43bb44573812cdaeaee046f907635be.ttf') format('truetype'),
            url('https://static-x.jamesedition.com/assets/inter/inter-600-0d4f387df6a81f8c83f6d68366995b383f0b2c62447bd6b27bb40bff43a22589.svg#Inter') format('svg');
    }

    @font-face {
        font-family: heldane;
        src: url('https://static-x.jamesedition.com/assets/heldane/Regular-f974ddb7f76e56d78861adcc3c37eda4217d32b3d4f400eac018ef5ccfc947f7.woff2') format('woff2'),
            url('https://static-x.jamesedition.com/assets/heldane/Regular-16de9bcc4536394668bb93690b1b14e151045f0e27d811fd6c5f9d45c2116903.woff') format('woff');
        font-weight: normal;
        font-style: normal;
        font-display: swap;
    }

    @font-face {
        font-family: prata;
        src: url('https://static-x.jamesedition.com/assets/Prata-Regular-574345a3423feeb31f801fef6a127cd4a1e38f744212c73b83f0ab881d34b14a.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
        font-display: swap;
    }
</style>

  </head>
  <body class="EUR ">
    <svg width="0" height="0" style="display:none" xmlns="http://www.w3.org/2000/svg" id="je-shared-icons">
  <symbol viewBox="0 0 8 12" id="arrow-left" fill="none">
      <path d="M7 1L2 6L7 11" stroke-width="2" fill="none" />
  </symbol>
  <symbol viewBox="0 0 8 12" id="arrow-right" fill="none">
      <path d="M1 1L6 6L1 11" stroke-width="2" fill="none" />
  </symbol>
  <svg viewBox="0 0 24 43" id="arrow-left-thin">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M20.8953 0.939331L23 3.05454L4.20933 21.9393L23 40.8241L20.8953 42.9393L9.17939e-07 21.9393L20.8953 0.939331Z" />
  </svg>
  <svg viewBox="0 0 24 43" id="arrow-right-thin">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M3.04412 0.939331L0.939453 3.05454L19.7301 21.9393L0.939451 40.8241L3.04412 42.9393L23.9395 21.9393L3.04412 0.939331Z" />
  </svg>
  <symbol viewBox="0 0 10 16" id="arrow-right-v2">
    <path d="m1.5 1 7 7-7 7" stroke="#151515" stroke-width="1.6" />
  </symbol>
  <symbol viewBox="0 0 10 16" id="arrow-left-v2">
    <path d="m8.5 1-7 7 7 7" stroke="#151515" stroke-width="1.6" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="cars">
      <path d="M16.125 8a2.625 2.625 0 0 1 2.625 2.625v2.188a.437.437 0 0 1-.438.437H17a2.625 2.625 0 0 1-5.25 0h-3.5a2.625 2.625 0 0 1-5.25 0H1.687a.437.437 0 0 1-.437-.438V9.75c0-.815.559-1.493 1.313-1.688l1.31-3.337a1.75 1.75 0 0 1 1.624-1.1h5.85c.464 0 1.076.294 1.366.657L15.688 8h.437zm-10.5 6.563a1.314 1.314 0 0 0 0-2.625 1.314 1.314 0 0 0 0 2.625zM7.594 8V5.375H5.497L4.447 8h3.147zm1.312 0h4.54l-2.1-2.625h-2.44V8zm5.469 6.563a1.314 1.314 0 0 0 0-2.625 1.314 1.314 0 0 0 0 2.625z" />
  </symbol>
  <symbol viewBox="0 0 32 32" id="heart">
      <path d="M14.0929 7.00711L14.1083 7.02247L14.1243 7.03715L15.3243 8.13715L16.0301 8.78414L16.7071 8.10711L17.8071 7.00711C20.3166 4.49763 24.3834 4.49763 26.8929 7.00711C29.4024 9.51658 29.4024 13.5834 26.8929 16.0929L15.997 26.9888L5.00711 16.0929C5.0066 16.0924 5.00609 16.0919 5.00558 16.0914C2.49763 13.5818 2.49814 9.51607 5.00711 7.00711C7.51658 4.49763 11.5834 4.49763 14.0929 7.00711Z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="white-heart">
      <path d="M8.82574 4.36176L8.83495 4.37098L8.84457 4.37979L9.59457 5.06729L10.018 5.45548L10.4243 5.04926L11.1118 4.36176C12.6899 2.78358 15.2476 2.78358 16.8257 4.36176C18.4039 5.93995 18.4039 8.49755 16.8257 10.0757L9.99818 16.9033L3.11176 10.0757C3.11146 10.0754 3.11116 10.0751 3.11085 10.0748C1.53358 8.49656 1.53388 5.93965 3.11176 4.36176C4.68995 2.78358 7.24755 2.78358 8.82574 4.36176Z" stroke="#151515" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="helicopters">
      <path d="M9.562 13.25a.985.985 0 0 1-.7-.35L6.5 9.75 2.125 8l-.862-2.956a.437.437 0 0 1 .425-.544H2.78c.138 0 .268.065.35.175L4.312 6.25H10V4.5H5.187a.437.437 0 0 1-.437-.438v-.875c0-.241.196-.437.437-.437h11.375c.242 0 .438.196.438.438v.874a.437.437 0 0 1-.438.438H11.75v1.75a6.125 6.125 0 0 1 6.125 6.125.875.875 0 0 1-.875.875H9.562zm3.063-5.154V11.5h3.412a4.384 4.384 0 0 0-3.412-3.404zm5.998 7.2c.18.18.165.479-.027.647-.906.794-1.464.807-1.871.807H7.812a.438.438 0 0 1-.437-.439v-.876c0-.242.196-.439.437-.439h8.913c.295 0 .48-.122.674-.307a.441.441 0 0 1 .619 0l.605.607z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="jets">
      <path d="M15.25 8c.967 0 2.625.783 2.625 1.75s-1.658 1.75-2.625 1.75h-3.125L9.25 16.53a.438.438 0 0 1-.38.22H7.08c-.29 0-.5-.278-.42-.558L8 11.5H5.187l-1.18 1.575a.437.437 0 0 1-.35.175H2.562a.437.437 0 0 1-.425-.544L3 9.75l-.862-2.956a.437.437 0 0 1 .425-.544h1.093c.138 0 .268.065.35.175L5.187 8H8L6.66 3.308a.437.437 0 0 1 .42-.558h1.791c.14 0 .31.099.38.22L12.125 8h3.125z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="jewelery">
      <path d="M15.4 2.75l2.475 4.375h-2.764L13.217 2.75H15.4zm-3.5 0l1.893 4.375H6.207L8.1 2.75h3.8zm-7.3 0h2.182L4.889 7.125H2.125L4.6 2.75zM2.125 8h2.754l3.363 6.882c.04.085-.074.162-.137.09L2.125 8zm4.052 0h7.646l-3.747 8.7c-.027.066-.123.066-.15 0L6.177 8zm5.581 6.882L15.121 8h2.754l-5.98 6.97c-.063.074-.178-.003-.137-.088z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="lifestyle">
      <path d="M5.625 8.875c0-.965-.785-1.75-1.75-1.75H3A2.626 2.626 0 0 1 5.625 4.5h8.75A2.626 2.626 0 0 1 17 7.125h-.875c-.965 0-1.75.785-1.75 1.75v1.75h-8.75v-1.75zM17 8c.965 0 1.75.785 1.75 1.75 0 .645-.355 1.203-.875 1.507v3.306c0 .24-.197.437-.438.437h-1.75a.439.439 0 0 1-.437-.438v-.437H4.75v.438c0 .24-.197.437-.438.437h-1.75a.439.439 0 0 1-.437-.438v-3.305A1.746 1.746 0 0 1 1.25 9.75C1.25 8.785 2.035 8 3 8h.875c.484 0 .875.391.875.875V11.5h10.5V8.875c0-.484.391-.875.875-.875H17z" />
  </symbol>
  <symbol viewBox="0 0 135 18" id="logo">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M.209 1.632l3.52-.65v11.74c0 2.371-1.43 3.996-3.644 4.14L0 16.867v.91h.09c1.578 0 3.003-.501 4.012-1.413 1.013-.914 1.57-2.206 1.57-3.638V.235H.21v1.397zm133.309 1.497l.433 10.462-10.462-10.48-.027-.026h-.646v13.396h1.482l-.495-10.355 10.391 10.355h.753V3.129h-1.429zm-16.022 2.803c-1.15-1.141-2.762-1.77-4.54-1.77-3.341 0-3.84 3.28-3.84 5.236 0 1.794.467 3.19 1.387 4.15 1.072 1.119 2.795 1.686 5.12 1.686 1.314 0 2.24-.461 2.831-1.411.518-.833.77-2.03.77-3.66 0-1.622-.613-3.125-1.728-4.231zm3.761 3.603a7.042 7.042 0 0 1-2.148 5.1c-1.375 1.333-3.216 2.067-5.184 2.067-3.884 0-6.814-2.87-6.814-6.675 0-1.947.764-3.758 2.151-5.1 1.378-1.333 3.228-2.067 5.208-2.067 3.869 0 6.787 2.87 6.787 6.675zm-17.562 6.858l.001.088h1.612l.185-13.352h-1.981l.183 13.264zm-14.1-11.86l5.282-.52.188 12.468h1.604l.186-12.468 5.281.52V3.13h-12.54v1.404zm-3.233 11.86v.088h1.613l.184-13.352h-1.98l.183 13.264zM78.617 4.356h-4.439v11.172c.553-.043 2.593-.202 3.348-.267 1.48-.129 2.715-.655 3.574-1.524.873-.884 1.335-2.104 1.335-3.529 0-1.872-.25-3.24-.762-4.178-.614-1.127-1.614-1.674-3.056-1.674zm3.985.634c1.203 1.17 1.865 2.803 1.865 4.6 0 2.127-.586 3.781-1.743 4.916-1.338 1.311-3.48 1.976-6.37 1.976h-.132L72.2 16.48V3.129h5.426c2.003 0 3.724.644 4.976 1.86zM54.28 8.827c-2.302-1.03-3.41-1.577-3.41-2.73 0-1.19.407-1.982 1.853-1.982 3.173 0 4.981 1.621 4.999 1.638l.153.14.123-1.763-.033-.029c-.014-.013-.356-.317-1.04-.62-.63-.28-1.683-.614-3.128-.614-2.985 0-4.767 1.33-4.767 3.558 0 1.953 1.362 2.903 4.225 4.177 2.368 1.06 3.557 1.593 3.557 2.811 0 1.633-.991 1.976-1.822 1.976-1.906 0-3.38-.49-4.283-.9-.976-.444-1.507-.893-1.513-.897l-.152-.13-.117 1.848.036.029c.004.003.437.348 1.224.683.725.308 1.916.676 3.465.676 1.564 0 2.851-.368 3.724-1.066.817-.653 1.25-1.562 1.25-2.628 0-1.918-1.527-2.948-4.344-4.177zm-13.388 1.247l5.498.227V8.986l-5.498.227V4.06l6.342.41V3.13h-8.32v13.35h8.402v-1.34l-6.424.434v-5.5zm-11.5 2.53l-5.866-9.432-.027-.043h-1.642v13.352h1.61L23.032 5.65l6.149 9.734 5.862-10.299-.4 11.396h2.097V3.129h-1.858l-5.492 9.476zM13.123 5.808l-3.036 6.06 5.922-.255-2.886-5.805zm7.553 10.674h-2.219l-1.816-3.6-6.94-.238-1.91 3.838H6.309l.065-.13L13.081 3.13h.714l6.882 13.352zm41.826-1.012l7.909-.494v1.498h-10V.047h9.899v1.4L62.503.986v6.625l6.77-.28v1.46l-6.77-.28v6.958z" />
  </symbol>
  <symbol viewBox="0 0 140 18" id="logo-new">
      <path d="M8.54 0v.321298c-.595.249898-.805.571196-.805 1.320892V12.7091c0 3.1416-1.225 4.1055-3.465 4.641-1.61.357-3.99-.0357-3.99-.0357L0 14.9582l.385-.1428c.665 1.1067 1.54 2.4276 2.835 2.1063 1.4-.3213 1.295-4.2483 1.295-4.2483V1.60649c0-.785395-.175-1.106693-.77-1.320892V0H8.54zm2.905 12.8162h4.34l.84 2.7132c.07.2142.105.3927.105.5712 0 .3927-.175.6069-.63.7854v.2499h4.83v-.2499c-.525-.2142-.84-.5712-1.085-1.3566L16.1 3.53428h-2.555L9.695 15.5294c-.105.3927-.385.7854-.665.9996-.21.1785-.385.2499-.805.357v.2499h3.43v-.2499c-.84-.1785-1.155-.4284-1.155-.8925 0-.1428.035-.2856.07-.4284l.875-2.7489zm.28-.8211l1.89-5.96184 1.89 5.96184h-3.78zm36.435 3.6414c-.7.714-1.505.9996-2.695.9996H44.45c-.875 0-1.4-.1785-1.575-.4998-.07-.1785-.105-.4284-.105-.7854V9.92454h1.82c1.4 0 1.995.42836 2.065 1.46366h.42V7.92535h-.42c-.14.96389-.77 1.39229-2.065 1.39229h-1.82V5.28357c0-.8211.385-1.1424 1.295-1.1424h1.085c1.54 0 2.45.6426 3.045 2.07059h.455l-.21-2.60608h-9.73v.2856c.595.24989.805.57119.805 1.32089V15.458c0 .7497-.21 1.071-.805 1.3209v.357h9.94l.7-2.7846-.42-.1785c-.245.7497-.42 1.071-.77 1.4637zm10.64-5.4621c-.56-.28556-1.26-.60686-2.03-.92816-1.785-.71399-2.45-1.10669-2.94-1.74929-.28-.3927-.42-.85679-.42-1.39229 0-1.28519.945-2.17768 2.31-2.17768 1.715 0 3.01 1.28519 3.185 3.21297h.49l.49-2.64178c-1.365-.60689-1.89-.82109-2.555-.96389-.595-.1428-1.225-.2142-1.89-.2142-2.905 0-4.725 1.53509-4.725 3.96267 0 1.57079.7 2.64179 2.24 3.42715.455.2499.98.4998 1.61.7854 2.38 1.0353 3.185 1.785 3.185 3.0702 0 1.3209-1.015 2.2491-2.485 2.2491-2.275 0-3.745-1.4637-3.745-3.7128l-.49-.0714-.595 2.8917c1.26.7497 1.82.9639 3.01 1.2852.77.2142 1.54.2856 2.31.2856 2.835 0 4.9-1.785 4.9-4.2126.035-1.428-.56-2.3919-1.855-3.1059zm12.425 5.4621c-.7.714-1.505.9996-2.695.9996h-.98c-.875 0-1.4-.1785-1.575-.4998-.07-.1785-.105-.4284-.105-.7854V8.31805h1.82c1.4 0 1.995.42839 2.065 1.46369h.42V6.31886h-.42c-.14.96389-.77 1.39229-2.065 1.39229h-1.82V1.64219c0-.821095.385-1.142393 1.295-1.142393h1.085c1.54 0 2.45.642593 3.045 2.070583h.455L71.54 0h-9.73v.285598c.595.249899.805.571197.805 1.320892V15.4937c0 .7497-.21 1.071-.805 1.3209v.3213h9.94l.7-2.7846-.42-.1785c-.245.7497-.42 1.071-.805 1.4637zm15.505-4.8909c0 4.0698-2.45 6.426-6.65 6.426h-6.335v-.2856c.595-.2499.805-.5712.805-1.3209V5.28357c0-.7854-.21-1.1067-.805-1.3209v-.28559H75.6c.28 0 .84-.0357 1.575-.0714.805-.0714 1.505-.0714 2.065-.0714 4.585-.0357 7.49 2.74888 7.49 7.21132zm-3.255-.2142c0-4.06974-1.68-6.49733-4.41-6.49733-.98 0-1.435.3927-1.435 1.2852V15.5294c0 .714.56 1.071 1.68 1.071 2.73 0 4.165-2.0706 4.165-6.069zm4.655-6.56873c.595.2499.805.5712.805 1.3209V15.5294c0 .7497-.21 1.071-.805 1.3209v.2856h4.865v-.2856c-.63-.2499-.805-.5712-.805-1.3209V5.28357c0-.7854.175-1.1067.805-1.3209v-.28559H88.13v.28559zm6.335-.32129l-.735 2.96308.455.0714c.385-.7497.56-1.0353 1.05-1.42799.63-.5355 1.365-.8211 2.205-.8211.84 0 1.19.2856 1.19.9996V15.4937c0 .7497-.21 1.071-.805 1.3209v.3213h4.83v-.2856c-.595-.2499-.805-.5712-.805-1.3209V5.56916c0-.78539.315-1.10669 1.155-1.10669.84 0 1.47.2499 2.135.8568.455.39269.665.67829 1.05 1.39229l.49-.0714-.735-2.96308h-11.48v-.0357zm12.95.32129c.595.2499.805.5712.805 1.3209V15.5294c0 .7497-.21 1.071-.805 1.3209v.2856h4.865v-.2856c-.63-.2499-.805-.5712-.805-1.3209V5.28357c0-.7854.175-1.1067.805-1.3209v-.28559h-4.865v.28559zm19.25 6.46163c0 4.0341-2.87 7.0686-6.72 7.0686-3.815 0-6.685-3.0345-6.685-7.0686 0-4.03404 2.87-7.06852 6.685-7.06852 3.85-.0357 6.72 2.99878 6.72 7.06852zm-3.255 0c0-4.06974-1.295-6.53302-3.465-6.53302-2.1 0-3.36 2.53468-3.36 6.56872 0 4.0698 1.295 6.4974 3.465 6.4974 2.065-.0357 3.36-2.499 3.36-6.5331zm13.51-6.78292v.2856c.84.17849 1.12.49979 1.12 1.39229v8.81783l-6.825-10.49572h-4.025v.2856c.84.17849 1.12.49979 1.12 1.39229V15.458c0 .8568-.28 1.2138-1.12 1.3923v.2856h3.045v-.2856c-.84-.1785-1.12-.5355-1.12-1.3923V6.35456l7 10.81704h2.765V5.31927c0-.8568.245-1.1781 1.12-1.39229v-.2856h-3.08zm-100.065.32129v-.28559h-3.99l-3.5 11.20972L25.69 3.64138h-4.025v.2856c.315.07139.525.14279.7.28559 0 0 .035 0 .035.0357l.035.0357.14.1428c.14.2142.21.4998.21.8925V15.458c0 .8568-.28 1.2138-1.12 1.3923v.2856h3.045v-.2856c-.84-.1785-1.12-.5355-1.12-1.3923V7.17565l3.29 9.96025h2.52l3.36-10.70994v9.06774c0 .7497-.21 1.071-.805 1.3209v.3213h4.865v-.2856c-.63-.2499-.805-.5712-.805-1.3209V5.28357c.035-.7497.21-1.071.84-1.3209z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="motorcycles">
      <path d="M15.275 8a3.516 3.516 0 0 1 3.478 3.47A3.5 3.5 0 0 1 15.22 15a3.51 3.51 0 0 1-3.467-3.475 3.495 3.495 0 0 1 1.225-2.686l-.342-.568a4.142 4.142 0 0 0-1.537 3.418.657.657 0 0 1-.656.686H8.141a3.5 3.5 0 0 1-6.89-.957 3.51 3.51 0 0 1 4.497-3.273l.309-.56c-.249-.38-.637-.679-1.307-.679H3.219a.655.655 0 0 1-.656-.642c-.009-.37.3-.67.67-.67H4.75c1.504 0 2.248.462 2.732 1.093h4.202l-.525-.875H9.344a.439.439 0 0 1-.438-.437v-.438c0-.24.197-.437.438-.437h2.187c.23 0 .443.12.563.317l.624 1.04 1.025-1.141a.657.657 0 0 1 .487-.216h1.239c.363 0 .656.293.656.656v.875a.655.655 0 0 1-.656.657h-2.253l.9 1.5A3.46 3.46 0 0 1 15.274 8zM4.75 13.688c.894 0 1.665-.542 2.004-1.313H4.531a.657.657 0 0 1-.574-.973L5.092 9.34a2.19 2.19 0 0 0-2.53 2.16 2.19 2.19 0 0 0 2.188 2.188zm12.685-2.068a2.187 2.187 0 0 0-2.62-2.261l1.33 2.212a.44.44 0 0 1-.151.602l-.375.224a.44.44 0 0 1-.601-.15l-1.351-2.254a2.17 2.17 0 0 0-.604 1.507 2.19 2.19 0 0 0 2.307 2.185 2.192 2.192 0 0 0 2.065-2.065z" />
  </symbol>
  <symbol viewBox="0 0 32 32" id="real-estate">
      <path d="M28 12L16 4L4 12V28H13V20H19V28H28V12Z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="recent">
      <path d="M10 2.969a6.78 6.78 0 0 1 6.781 6.781A6.78 6.78 0 0 1 10 16.531 6.78 6.78 0 0 1 3.219 9.75 6.78 6.78 0 0 1 10 2.969zm1.561 9.573a.33.33 0 0 0 .46-.071l.77-1.061a.328.328 0 0 0-.07-.46l-1.737-1.263V5.922a.33.33 0 0 0-.328-.328H9.344a.33.33 0 0 0-.328.328v4.602a.33.33 0 0 0 .134.265l2.411 1.753z" />
  </symbol>
  <symbol viewBox="0 0 18 18" id="recent-search">
    <path d="M9 16.428A7.429 7.429 0 1 0 9 1.571a7.429 7.429 0 0 0 0 14.857Z" stroke-width="1.6" />
    <path d="M9 6.143V9l2.903 3.383" stroke-width="1.6" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="search">
      <path d="M14.2499 1.5C9.67493 1.5 5.99994 5.175 5.99994 9.75C5.99994 11.775 6.74994 13.575 7.94994 15L2.62495 20.325L3.67495 21.375L8.99994 16.05C10.4249 17.25 12.2999 18 14.2499 18C18.8249 18 22.4999 14.325 22.4999 9.75C22.4999 5.175 18.8249 1.5 14.2499 1.5ZM14.2499 16.5C10.4999 16.5 7.49994 13.5 7.49994 9.75C7.49994 6 10.4999 3 14.2499 3C17.9999 3 20.9999 6 20.9999 9.75C20.9999 13.5 17.9999 16.5 14.2499 16.5Z" />
  </symbol>
  <symbol viewBox="0 0 17 17" id="search-icon">
    <path d="M6.8 12.8a6 6 0 1 0 0-12 6 6 0 0 0 0 12ZM15.47 15.47l-4.8-4.8" stroke-width="1.6" />
  </symbol>
  <symbol width="16" height="17" viewBox="0 0 16 17" id="nearby" fill="none">
    <path d="M14 2.5L8.95833 13.5L8.04167 8.22917L3 7.08333L14 2.5Z" stroke="#404040" stroke-width="1.6" />
    </symbol>
  <symbol viewBox="0 0 20 20" id="yachts">
      <path d="M2.48 12.38a.33.33 0 01-.23-.57l1.83-1.83a.33.33 0 01.47 0l1.83 1.83c.2.21.06.56-.24.56h-.96c.56 1.5 2.33 2.37 3.94 2.58v-5.2H7.7a.33.33 0 01-.32-.33v-1.1c0-.17.14-.32.32-.32h1.43v-.15a2.63 2.63 0 01.9-5.1 2.63 2.63 0 012.6 2.62c0 1.15-.74 2.12-1.76 2.48V8h1.43c.18 0 .32.15.32.33v1.1a.33.33 0 01-.32.32h-1.43v5.2c1.62-.2 3.4-1.09 3.95-2.58h-.97a.33.33 0 01-.23-.56l1.84-1.83a.33.33 0 01.46 0l1.83 1.83c.2.21.06.56-.23.56h-.89c-.6 2.81-3.73 4.38-6.63 4.38s-6.04-1.57-6.63-4.38h-.89zM10 4.5a.88.88 0 000 1.75.88.88 0 000-1.75z" />
  </symbol>
  <symbol viewBox="0 0 12 8" id="arrow-down">
      <path d="M0 1.53033L1.06066 0.469666L5.53033 4.93934L10 0.469666L11.0607 1.53033L5.53033 7.06066L0 1.53033Z" />
  </symbol>
  <symbol viewBox="0 0 18 14" id="check">
    <path fill-rule="evenodd" d="M17.533 2.587 6.416 13.15.885 7.003l2.23-2.006L6.584 8.85 15.467.412l2.066 2.175Z" clip-rule="evenodd" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="cross">
      <path d="M21.6 1.8L20.2.4 11 9.6 1.8.4.4 1.8 9.6 11 .4 20.2l1.4 1.4 9.2-9.2 9.2 9.2 1.4-1.4-9.2-9.2 9.2-9.2z" />
  </symbol>
  <symbol viewBox="0 0 19 16" id="message-bubble">
      <path d="M0.75 0.125V12H4.5V15.8125L9.6875 12H18.25V0.125H0.75Z" />
  </symbol>
  <symbol viewBox="0 0 32 32" id="small-cross">
      <path d="M24 9.4L22.6 8L16 14.6L9.4 8L8 9.4L14.6 16L8 22.6L9.4 24L16 17.4L22.6 24L24 22.6L17.4 16L24 9.4Z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="globe">
      <path d="M10 0C4.47581 0 0 4.47581 0 10C0 15.5242 4.47581 20 10 20C15.5242 20 20 15.5242 20 10C20 4.47581 15.5242 0 10 0ZM17.2177 6.45161H14.5161C14.2339 5 13.7903 3.70968 13.2258 2.66129C14.9597 3.42742 16.371 4.75806 17.2177 6.45161ZM10 1.93548C10.7258 1.93548 11.9355 3.62903 12.5403 6.45161H7.41935C8.02419 3.62903 9.23387 1.93548 10 1.93548ZM1.93548 10C1.93548 9.47581 1.97581 8.91129 2.09677 8.3871H5.20161C5.16129 8.95161 5.16129 9.47581 5.16129 10C5.16129 10.5645 5.16129 11.0887 5.20161 11.6129H2.09677C1.97581 11.129 1.93548 10.5645 1.93548 10ZM2.74194 13.5484H5.44355C5.72581 15.0403 6.16935 16.3306 6.73387 17.379C5 16.6129 3.58871 15.2419 2.74194 13.5484ZM5.44355 6.45161H2.74194C3.58871 4.75806 5 3.42742 6.73387 2.66129C6.16935 3.70968 5.72581 5 5.44355 6.45161ZM10 18.0645C9.23387 18.0645 8.02419 16.4113 7.41935 13.5484H12.5403C11.9355 16.4113 10.7258 18.0645 10 18.0645ZM12.8226 11.6129H7.1371C7.09677 11.129 7.09677 10.5645 7.09677 10C7.09677 9.43548 7.09677 8.91129 7.1371 8.3871H12.8226C12.8629 8.91129 12.9032 9.43548 12.9032 10C12.9032 10.5645 12.8629 11.129 12.8226 11.6129ZM13.2258 17.379C13.7903 16.3306 14.2339 15.0403 14.5161 13.5484H17.2177C16.371 15.2419 14.9597 16.6129 13.2258 17.379ZM14.7581 11.6129C14.7984 11.0887 14.8387 10.5645 14.8387 10C14.8387 9.47581 14.7984 8.95161 14.7581 8.3871H17.9032C17.9839 8.91129 18.0645 9.47581 18.0645 10C18.0645 10.5645 17.9839 11.129 17.9032 11.6129H14.7581Z" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="arrow-left-alt">
      <path d="M8.625 4.57495L9.675 5.62495L4.05 11.25H22.5V12.75H4.05L9.675 18.3749L8.625 19.4249L1.2 12L8.625 4.57495Z" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="arrow-right-alt">
      <path d="M15.375 4.57495L14.325 5.62495L19.95 11.25H1.5V12.75H19.95L14.325 18.375L15.375 19.425L22.8 12L15.375 4.57495Z" />
  </symbol>
  <symbol viewBox="0 0 18 18" id="globe-alt">
      <path d="M17.25 12.4375C17.6625 11.4062 17.9375 10.2375 17.9375 9C17.9375 7.7625 17.6625 6.59375 17.25 5.5625C15.875 2.33125 12.7125 0.0625 9 0.0625C5.2875 0.0625 2.125 2.33125 0.75 5.5625C0.3375 6.59375 0.0625 7.7625 0.0625 9C0.0625 10.2375 0.3375 11.4062 0.75 12.4375C2.125 15.6687 5.2875 17.9375 9 17.9375C12.7125 17.9375 15.875 15.6687 17.25 12.4375ZM9 16.5625C7.83125 16.5625 6.59375 14.9812 5.975 12.4375H12.025C11.4062 14.9812 10.1687 16.5625 9 16.5625ZM5.7 11.0625C5.63125 10.4438 5.5625 9.75625 5.5625 9C5.5625 8.24375 5.63125 7.55625 5.7 6.9375H12.3C12.3687 7.55625 12.4375 8.24375 12.4375 9C12.4375 9.75625 12.3687 10.4438 12.3 11.0625H5.7ZM1.4375 9C1.4375 8.3125 1.575 7.625 1.7125 6.9375H4.325C4.25625 7.625 4.1875 8.3125 4.1875 9C4.1875 9.6875 4.25625 10.375 4.325 11.0625H1.7125C1.575 10.375 1.4375 9.6875 1.4375 9ZM9 1.4375C10.1687 1.4375 11.4062 3.01875 12.025 5.5625H5.975C6.59375 3.01875 7.83125 1.4375 9 1.4375ZM13.675 6.9375H16.2875C16.4937 7.625 16.5625 8.3125 16.5625 9C16.5625 9.6875 16.425 10.375 16.2875 11.0625H13.675C13.7437 10.375 13.8125 9.6875 13.8125 9C13.8125 8.3125 13.7437 7.625 13.675 6.9375ZM15.7375 5.5625H13.4688C13.1938 4.1875 12.7125 3.01875 12.0938 2.125C13.675 2.8125 14.9125 4.05 15.7375 5.5625ZM5.90625 2.125C5.2875 3.01875 4.875 4.25625 4.53125 5.5625H2.2625C3.0875 4.05 4.325 2.8125 5.90625 2.125ZM2.2625 12.4375H4.53125C4.80625 13.8125 5.2875 14.9812 5.90625 15.875C4.325 15.1875 3.0875 13.95 2.2625 12.4375ZM12.0938 15.875C12.7125 14.9812 13.125 13.7437 13.4688 12.4375H15.7375C14.9125 13.95 13.675 15.1875 12.0938 15.875Z" />
  </symbol>
  <symbol viewBox="0 0 16 16" id="short-arrow">
      <path d="M8.00005 10.85L3.05005 5.85002L3.75005 5.15002L8.00005 9.40002L12.25 5.15002L12.95 5.85002L8.00005 10.85Z" />
  </symbol>
  <symbol viewBox="0 0 6 10" id="breadcrumb-arrow">
    <path d="M1 1L5 5L1 9" stroke="#ADADAD" />
  </symbol>
  <symbol viewBox="0 0 24 24" id="phone-solid-icon">
    <path d="M0.0559626 3.09404C1.93013 12.8082 10.9261 21.775 20.6718 23.8922C21.4214 24.1413 21.6713 24.0167 22.296 22.8959C24.545 18.0388 23.9203 16.7934 23.9203 16.7934C23.9203 16.7934 19.2974 13.6799 18.2978 13.6799C17.2983 13.5554 14.6744 17.0425 14.6744 17.0425C12.5504 16.1707 8.42723 12.0609 6.9279 9.44558C6.9279 9.44558 10.4263 6.83024 10.4263 5.83392C10.4263 4.8376 7.17778 0.105081 7.17778 0.105081C7.17778 0.105081 5.92834 -0.642159 1.18046 1.84864C0.430795 2.22226 -0.193926 2.3468 0.0559626 3.09404Z" />
  </symbol>
  <symbol viewBox="0 0 16 16" id="contact">
    <path stroke="currentColor" fill="none" d="M1.33398 4.66663C2.86052 5.63713 8.00065 8.66663 8.00065 8.66663C8.00065 8.66663 13.1408 5.63713 14.6673 4.66663" />
    <path stroke="currentColor" fill="none" d="M3.15217 2.66663C2.14801 2.66663 1.33398 3.46257 1.33398 4.4444V11.5555C1.33398 12.5374 2.14801 13.3333 3.15217 13.3333H12.8491C13.8533 13.3333 14.6673 12.5374 14.6673 11.5555V4.4444C14.6673 3.46256 13.8533 2.66663 12.8491 2.66663H3.15217Z" />
  </symbol>
  <symbol viewBox="0 0 20 20" id="pointing-hand">
    <path d="M7.99212 18.1318C5.83024 16.8482 3.66886 12.9974 2.48939 10.6635C1.30992 8.32965 3.79146 6.14167 5.24079 7.86288C6.69012 9.5841 6.81307 9.72996 6.81307 9.72996V2.49503C6.81307 1.59276 7.42901 0.861328 8.18881 0.861328C8.94862 0.861328 9.56456 1.59276 9.56456 2.49503V6.46257C9.56456 5.5603 10.1805 4.82888 10.9403 4.82888C11.7001 4.82888 12.316 5.5603 12.316 6.46257V7.16273C12.316 6.26046 12.932 5.52903 13.6918 5.52903C14.4516 5.52903 15.0675 6.25976 15.0675 7.16203V9.49667C15.0675 8.59441 15.6835 7.86288 16.4433 7.86288C17.2031 7.86288 17.819 8.59431 17.819 9.49658V13.578C17.819 14.117 17.7157 14.6516 17.46 15.097C17.0005 15.897 16.0903 17.2147 14.6743 18.1318C12.5124 19.5321 10.154 19.4154 7.99212 18.1318Z" stroke="#151515" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" />
  </symbol>
  <symbol viewBox="0 0 17 16" id="list">
    <g stroke="#151515" stroke-width="1.6" clip-path="url(#a)"><path d="M4.66 3.52h12M4.66 8h12M4.66 12.48h12M2.66 3.52h-2M2.66 8h-2M2.66 12.48h-2" /></g><defs><clipPath id="a"><path fill="#fff" d="M.66 0h16v16h-16z" /></clipPath></defs>
  </symbol>
  <symbol viewBox="0 0 17 16" id="list-white">
    <g stroke="#EEE" stroke-width="1.6" clip-path="url(#a)"><path d="M4.66 3.52h12M4.66 8h12M4.66 12.48h12M2.66 3.52h-2M2.66 8h-2M2.66 12.48h-2" /></g><defs><clipPath id="a"><path fill="#fff" d="M.66 0h16v16h-16z" /></clipPath></defs>
  </symbol>
  <symbol viewBox="0 0 18 18" id="layer">
    <g stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path d="m9.7 3.56 4.04 2.71c1.16.52 1.16 1.37 0 1.88l-4.05 2.71c-.46.2-1.21.2-1.67 0l-4.04-2.7c-1.17-.52-1.17-1.37 0-1.89l4.04-2.7c.46-.21 1.21-.21 1.67 0Z" /><path d="M2.83 10.02c0 .57.43 1.24.96 1.47l4.66 2.98c.35.16.76.16 1.1 0l4.66-2.98c.53-.23.96-.9.96-1.47" /></g>
  </symbol>
</svg>

    <div class="real_estate show" id="view">
      

<div class="je3-header js-header _without-space _sticky-v2 _feed-v2 _v3">
  <header>
    <button class="je2-button js-hamburger-menu _noborder" aria-label="Menu">

    <svg width="20" height="14" viewBox="0 0 20 14" xmlns="http://www.w3.org/2000/svg">
  <path d="M0 13.0444H20" stroke-width="1.6" />
  <path d="M0 7.04443H20" stroke-width="1.6" />
  <path d="M0 1.04443H20" stroke-width="1.6" />
</svg>







  
  


</button>

    <a href="/" class="je2-button _noborder" aria-label="JamesEdition">

    <svg class="je2-icon"><use xlink:href="#logo-new" /></svg>







    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M16 0C7.36932 0 2 0.737706 2 0.737706C2 0.737706 2 9.66955 2 16.1362C2 21.6573 4.07286 24.8065 8.19987 27.022L16 31L23.8001 27.022C27.9295 24.8065 30 21.6573 30 16.1362C30 9.66955 30 0.737706 30 0.737706C30 0.737706 24.633 0 16 0ZM14.7015 6.01604C14.2243 6.20747 14.0652 6.46193 14.0652 7.06424V16.0778C14.0652 18.5407 13.0896 19.3018 11.2717 19.7126C9.9756 20.0068 8.05481 19.5539 8.05481 19.5539L7.84191 17.8497L8.16009 17.7423C8.71223 18.7975 9.38135 19.6403 10.4248 19.4068C11.5478 19.1523 11.4542 16.0801 11.4542 16.0801C11.4542 16.0801 11.4542 7.56382 11.4542 7.06657C11.4542 6.46193 11.3115 6.20747 10.8342 6.01838V5.78025H10.8506H14.6898H14.7062V6.01604H14.7015ZM23.5872 19.2387H15.6093V19.0169C16.0866 18.8115 16.2457 18.557 16.2457 17.9687V7.06657C16.2457 6.46193 16.0866 6.20747 15.6093 6.01838V5.78025H23.4141L23.5896 7.81362H23.2246C22.7473 6.6697 22.0127 6.17712 20.7704 6.17712H19.8954C19.1467 6.17712 18.8449 6.43158 18.8449 7.06657V11.8336H20.2931C21.3272 11.8336 21.8372 11.4998 21.9495 10.7364H22.2841V13.4538H21.9495C21.9027 12.6437 21.4231 12.2935 20.2931 12.2935H18.8449V17.824C18.8449 18.1112 18.8777 18.3166 18.9408 18.445C19.0836 18.7158 19.4977 18.8419 20.1995 18.8419H20.995C21.9495 18.8419 22.6046 18.6037 23.1614 18.0481C23.4632 17.747 23.6083 17.5089 23.8305 16.9206L24.1651 17.063L23.5872 19.2387Z" fill="#151515" />
</svg>


  


</a>



    
<div class="je2-user-block _compact">

      <ul>
        <li>
          <a href="/buyer/feed" class="je2-button _noborder je2-feed-entrypoint">

  

    <span>
          Just for You
    </span>




  
  


</a>
        </li>
      </ul>

        <ul>
          <li>
  <button class="je2-button js-sell-with-us _noborder _light"
          aria-expanded="false" aria-haspopup="true">
    <div>
      <span>Sell</span>
      <svg viewBox="0 0 12 8">
  <path fill="none" d="M11 1.49997L6 6.49997L1 1.49997" stroke="currentColor" stroke-width="1.6" />
</svg>

    </div>
  </button>
</li>

<nav class="je2-sell-with-us js-seller-dropdown _hidden _light">
  <ul>
    <li>
      <a href="/professional_seller/real_estate">
        Sell as a Business / Agent
      </a>
    </li>
    <li>
      <a href="https://join.jamesedition.com/sell-your-home">
        Sell as a Private Owner
      </a>
    </li>
  </ul>
</nav>

        </ul>

    <ul>
        <li>
          <a href="/offices/real_estate" class="je2-button _noborder">

  

    <span>
          Find Agencies
    </span>




  
  


</a>
        </li>
    </ul>

  <ul class="je2-user-controls js-user-controls">

    <li>
        <div class="je2-user-controls__login">
          <button class="je2-button js-login" aria-haspopup="true">

    <svg viewBox="0 0 14 15" stroke-width="1.2">
  <path fill="none" d="M7 8C8.79493 8 10.25 6.54493 10.25 4.75C10.25 2.95507 8.79493 1.5 7 1.5C5.20507 1.5 3.75 2.95507 3.75 4.75C3.75 6.54493 5.20507 8 7 8Z" stroke="currentColor" />
  <path fill="none" d="M13.1801 14.5C12.7602 13.1908 11.9355 12.0488 10.8249 11.2386C9.71416 10.4284 8.37487 9.99182 7.00007 9.99182C5.62526 9.99182 4.28597 10.4284 3.17528 11.2386C2.0646 12.0488 1.23989 13.1908 0.820068 14.5" stroke="currentColor" />
</svg>



    <span>
          Log in
    </span>




  
  


</button>
        </div>
    </li>

  </ul>
</div>

  </header>



  

  <div class="je2-secondary-menu js-secondary-menu _v2">
  <nav>
      <button class="je2-button js-hamburger-menu _noborder" aria-label="Menu">

    <svg width="20" height="14" viewBox="0 0 20 14" xmlns="http://www.w3.org/2000/svg">
  <path d="M0 13.0444H20" stroke-width="1.6" />
  <path d="M0 7.04443H20" stroke-width="1.6" />
  <path d="M0 1.04443H20" stroke-width="1.6" />
</svg>







  
  


</button>

    <ul>
        <li>
            <a href="/real_estate/france" class="je2-button js-menu-button _noborder" data-name="Back+to+search" id="back-to-search">

    <svg viewBox="0 0 13 12">
  <path d="M0.5 6L11 6" stroke-width="1.6" />
  <path d="M6 11L11 6L6 1" stroke-width="1.6" />
</svg>



    <span>
          Back to search
    </span>




  
  


</a>
        </li>
    </ul>

      <div class="je2-breadcrumbs">
  <ol>
        <li>
              <a href="/real_estate">Real Estate</a>
        </li>
        <li>
              <a href="/real_estate/france">France</a>
        </li>
        <li>
              <a href="/real_estate/nouvelle-aquitaine-france">Nouvelle-Aquitaine</a>
        </li>
        <li>
              <a href="/real_estate/angouleme-france">Angoulême</a>
        </li>


  </ol>
</div>


      <div class="je2-listing__actions">
        <div>
          
          <a href="/real_estate/saint-valery-en-caux-france/rare-beachfront-villa-with-2-converted-dependencies-near-marina-beach-and-restaurants-16247522" class="je2-button _noborder js-menu-button" data-name="Next listing" aria-label="Next property">

  

    <span>
          Next property
    </span>




    <svg width="8" height="12" viewBox="0 0 8 12" fill="none">
  <path d="M1.1568 0.902554L6.25484 6.00059L1.1568 11.0986" stroke-width="1.22353" />
</svg>


  


</a>
        </div>
        <div>
        <button class="je2-button _noborder js-heart " data-listing-id="16460690" data-saved="Saved" data-location="Sticky header" aria-label="Save">

    <svg xmlns="http://www.w3.org/2000/svg" width="17" height="15" viewBox="0 0 17 15" fill="none"><path d="M8.242 13.207 1.934 7.492C-1.495 4.064 3.545-2.519 8.242 2.807c4.697-5.326 9.714 1.28 6.309 4.685l-6.309 5.715Z" stroke="#151515" stroke-width="1.6" /></svg>



    <span>
          Save
    </span>




  
  


</button>
        <button class="je2-button _noborder js-share" data-location="Sticky header" data-listing-id="16460690" aria-label="Share">

    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="17" viewBox="0 0 15 17" fill="none"><path d="M3.825 7.303H2.797a2 2 0 0 0-2 2v4.171a2.286 2.286 0 0 0 2.286 2.286h8.685a2.285 2.285 0 0 0 2.286-2.286V9.303a2 2 0 0 0-2-2h-1.029M3.828 4.73l3.6-3.6 3.6 3.6M7.422.902v10.286" stroke="#151515" stroke-width="1.6" /></svg>



    <span>
          Share
    </span>




  
  


</button>
      </div>

      </div>
  </nav>

</div>

    <aside class="je3-hamburger js-hamburger _loading _mobile-right" aria-hidden="true">
    <nav>
      <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>

    </nav>
  </aside>

</div>


  <script type="application/ld+json">
      {
        "@context": "http://schema.org",
        "@type": "BreadcrumbList",
        "name": "JamesEdition",
        "itemListElement": [
          {"@type":"ListItem","position":1,"item":{"@id":"https://www.jamesedition.com/","name":"JamesEdition"}}, {"@type":"ListItem","position":2,"item":{"@id":"https://www.jamesedition.com/real_estate","name":"Real Estate"}}, {"@type":"ListItem","position":3,"item":{"@id":"https://www.jamesedition.com/real_estate/france","name":"France"}}, {"@type":"ListItem","position":4,"item":{"@id":"https://www.jamesedition.com/real_estate/nouvelle-aquitaine-france","name":"Nouvelle-Aquitaine"}}, {"@type":"ListItem","position":5,"item":{"@id":"https://www.jamesedition.com/real_estate/angouleme-france","name":"Angoulême"}}, {"@type":"ListItem","position":6,"item":{"@id":"https://www.jamesedition.com/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690","name":"LUXURY FAMILY ESTATE WITH HEATED POOL AND OUTBUILDINGS IN VARS, NEAR ANGOULEME"}}
        ]
      }
  </script>


      <div id="page_content" class="_w-bottom-offset" role="main">
          
<main class="je2-listing js-listing _lead_call_flow_mobile _gallery-grid _v3 _v3_p3">

  <div class="je2-listing__top _max-width _top-margin">
    

<div class="je2-top-gallery js-top-gallery _w-side-images _grid-gallery-re  _mobile-v2">

  <div class="je2-top-gallery__image _2"
       style="">

        <picture class="je-background-pixel ">
  <source media="(max-width: 450px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/760xxsxm.jpg">
  <source media="(max-width: 768px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/900xxsxm.jpg">
  <source media="(max-width: 1100px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/768xxsxm.jpg,
             https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/1536xxsxm.jpg 2x">
    <source media="(max-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/1100xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/2200xxs.jpg 2x">
    <source media="(min-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/1900xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/2200xxs.jpg 2x">
  <img src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/1100xxs.jpg" fetchpriority="high" alt="House in Angoulême, Nouvelle-Aquitaine, France 1 - 16460690">
</picture>


      <div class="je2-top-gallery__side-images _2">


          <div>
              <picture class="je-background-pixel ">
  <source media="(max-width: 450px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/760xxsxm.jpg">
  <source media="(max-width: 768px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/900xxsxm.jpg">
  <source media="(max-width: 1100px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/768xxsxm.jpg,
             https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/1536xxsxm.jpg 2x">
    <source media="(max-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/1100xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/2200xxs.jpg 2x">
    <source media="(min-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/1900xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/2200xxs.jpg 2x">
  <img src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/1100xxs.jpg" fetchpriority="high" alt="House in Angoulême, Nouvelle-Aquitaine, France 2 - 16460690">
</picture>

              <picture class="je-background-pixel ">
  <source media="(max-width: 450px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/760xxsxm.jpg">
  <source media="(max-width: 768px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/900xxsxm.jpg">
  <source media="(max-width: 1100px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/768xxsxm.jpg,
             https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/1536xxsxm.jpg 2x">
    <source media="(max-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/1100xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/2200xxs.jpg 2x">
    <source media="(min-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/1900xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/2200xxs.jpg 2x">
  <img src="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/2288e986-e6a0-495d-85c7-e6bd40693a9b/je/1100xxs.jpg" fetchpriority="high" alt="House in Angoulême, Nouvelle-Aquitaine, France 3 - 16460690">
</picture>

          </div>

          <div>
              <picture class="je-background-pixel ">
  <source media="(max-width: 450px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/760xxsxm.jpg">
  <source media="(max-width: 768px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/900xxsxm.jpg">
  <source media="(max-width: 1100px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/768xxsxm.jpg,
             https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/1536xxsxm.jpg 2x">
    <source media="(max-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/1100xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/2200xxs.jpg 2x">
    <source media="(min-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/1900xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/2200xxs.jpg 2x">
  <img src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/3d34e32a-b449-41a6-92e3-0f3b51d26c16/je/1100xxs.jpg" fetchpriority="high" alt="House in Angoulême, Nouvelle-Aquitaine, France 4 - 16460690">
</picture>

              <picture class="je-background-pixel ">
  <source media="(max-width: 450px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/760xxsxm.jpg">
  <source media="(max-width: 768px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/900xxsxm.jpg">
  <source media="(max-width: 1100px)"
          srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/768xxsxm.jpg,
             https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/1536xxsxm.jpg 2x">
    <source media="(max-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/1100xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/2200xxs.jpg 2x">
    <source media="(min-width: 1900px)"
            srcset="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/1900xxs.jpg,
               https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/2200xxs.jpg 2x">
  <img src="https://img.jamesedition.com/listing_images/2025/10/20/12/26/52/fabfc752-fc2e-4ad6-8e0b-1c6395113b74/je/1100xxs.jpg" fetchpriority="high" alt="House in Angoulême, Nouvelle-Aquitaine, France 5 - 16460690">
</picture>

          </div>

      </div>


  </div>

    <div class="je2-top-gallery__top-right-controls">
        <button class="je2-button _noborder js-share" data-location="Gallery block" data-listing-id="16460690" aria-label="Share">

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 18" width="16" height="18" fill="none"><path d="M4.404 7.969H3.375a2 2 0 0 0-2 2v4.171a2.286 2.286 0 0 0 2.286 2.286h8.685a2.286 2.286 0 0 0 2.286-2.286V9.97a2 2 0 0 0-2-2h-1.028M4.406 5.4l3.6-3.6 3.6 3.6M8 1.57v10.286" stroke="#151515" stroke-width="1.2" /></svg>



    <span>
          Share
    </span>




  
  


</button>
        <button class="je2-button je2-top-gallery__save js-heart " data-listing-id="16460690" data-saved="Saved" data-location="Gallery block" aria-label="Save">

    <svg><use xlink:href="#heart"></use></svg>


    <span>
          Save
    </span>




  
  


</button>
    </div>

  <div class="je2-top-gallery__controls">

    <div class="je2-top-gallery__details">
        <button class="je2-button _noborder js-photos" data-open="Photos" data-photos-text="Show all photos" aria-label="Show all photos">

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="none"><circle cx="3.2" cy="3.2" r="1.2" fill="#151515" /><circle cx="3.2" cy="8.001" fill="#151515" r="1.2" /><circle cx="3.2" cy="12.802" fill="#151515" r="1.2" /><circle cx="7.997" cy="3.2" fill="#151515" r="1.2" /><circle cx="7.997" cy="8.001" r="1.2" fill="#151515" /><circle cx="7.997" cy="12.802" r="1.2" fill="#151515" /><circle cx="12.802" cy="3.2" fill="#151515" r="1.2" /><circle cx="12.802" cy="8.001" r="1.2" fill="#151515" /><circle cx="12.802" cy="12.802" r="1.2" fill="#151515" /></svg>



    <span>
          <span>Show all photos</span>
    </span>




  
  


</button>

    </div>
  </div>

</div>

  </div>

  <div class="je2-listing__body-wrapper">
    <div class="je2-listing__body">
      <div class="je2-listing__section _overview" id="overview">
        
<div class="je2-listing-info js-listing-info">

  <div class="je2-listing-info__price">
    <span>€667,800</span>

  </div>

      <h1>
    Luxury Family Estate With Heated Pool And Outbuildings In Vars, Near Angouleme
  </h1>


  <ul class="je2-listing-info__specs">
      <li>4 Beds</li>

      <li>2 Baths</li>

      <li>
        256 Sqm</li>

      <li>1,746 Sqm lot</li>

  </ul>

    <button class="je2-button je2-listing-info__location js-open-gallery _noborder" data-open="Map" aria-label="Angoulême, Nouvelle-Aquitaine, France">

    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M13.786 6.893c0 3.907-4.521 7.383-5.59 8.15a.852.852 0 0 1-.502.158.852.852 0 0 1-.502-.157c-1.069-.768-5.59-4.244-5.59-8.15a6.092 6.092 0 0 1 12.184 0Z" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /><path d="M5.477 6.338a2.215 2.215 0 1 0 4.43 0 2.215 2.215 0 0 0-4.43 0Z" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /></svg>



    <span>
          Angoulême, Nouvelle-Aquitaine, France
    </span>




  
  


</button>


  <ul class="je2-listing-info__insights">
      <li>
        <span>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M8.99986 16.4286C13.1025 16.4286 16.4284 13.1027 16.4284 8.99998C16.4284 4.8973 13.1025 1.57141 8.99986 1.57141C4.89717 1.57141 1.57129 4.8973 1.57129 8.99998C1.57129 13.1027 4.89717 16.4286 8.99986 16.4286Z" stroke-width="1.6" />
  <path d="M9 6.14282V8.99997L11.9029 12.3828" stroke-width="1.6" />
</svg>

          Updated: October 20
        </span>
      </li>

        <li>
          <span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="none"><circle cx="8.002" cy="8.002" r="1.8" stroke="#717171" stroke-width="1.2" /><path d="m.813 7.9.091-.258C3.323.823 13.027 1 15.196 7.902a.083.083 0 0 1 0 .049c-2.055 7.07-12.01 7.24-14.305.244l-.079-.241a.084.084 0 0 1 0-.055Z" stroke="#717171" stroke-width="1.2" /></svg>

            365
          </span>
          <span>
            <div class="je2-listing-info__tooltip _icon">
            <svg viewBox="0 0 12 12">
  <circle cx="6" cy="6" r="6"/>
  <rect x="5" y="5" width="2" height="5" fill="white"/>
  <rect x="5" y="2" width="2" height="2" fill="white"/>
</svg>

              <div class="je2-listing-info__tooltip__container">
                Views for last 30 days
              </div>
            </div>
          </span>
        </li>

      <li class="_save">
        <span>
            <svg><use xlink:href="#heart"></use></svg>
          39
        </span>
      </li>


  </ul>
</div>

      </div>


      <div class="je2-listing__section _in-details" id="in-detail">

          <div class="je2-listing-in-details__container js-listing-in-details-container">
            <button class="je2-button je2-listing-in-details__slide-button _prev _noborder js-listing-details-button _hidden">

    <svg width="8" height="12" viewBox="0 0 8 12" fill="none">
  <path d="M1.1568 0.902554L6.25484 6.00059L1.1568 11.0986" stroke-width="1.22353" />
</svg>







  
  


</button>
            <div class="je2-listing-in-details__slider-container">
              
<div class="je2-listing-in-details js-listing-in-details"
     data-listing-id="16460690"
     data-real-estate-id="5655978">

    <button class="js-open-gallery" data-open="Photos">
      <div
        style="background-image: url(&#39;data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAADAAUDAREAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAAB//EAB8QAAEEAAcAAAAAAAAAAAAAAAIBAwQFAAYHFCIxQf/EABUBAQEAAAAAAAAAAAAAAAAAAAAD/8QAFhEBAQEAAAAAAAAAAAAAAAAAAAEx/9oADAMBAAIRAxEAPwB30yztdXVPIOdN3JNPK2Cm0HEU86xObR//2Q==&#39;)">

          <div class="je2-lazy-load"
               data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/160x120xc.jpg"
               alt="All photos (37)"></div>
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M27 10C27 9.46957 26.7893 8.96086 26.4142 8.58579C26.0391 8.21071 25.5304 8 25 8H21L18 4H10L7 8H3C2.46957 8 1.96086 8.21071 1.58579 8.58579C1.21071 8.96086 1 9.46957 1 10V22C1 22.5304 1.21071 23.0391 1.58579 23.4142C1.96086 23.7893 2.46957 24 3 24H25C25.5304 24 26.0391 23.7893 26.4142 23.4142C26.7893 23.0391 27 22.5304 27 22V10Z" stroke="white" stroke-width="1.6" />
<path d="M14 19.5C16.4853 19.5 18.5 17.4853 18.5 15C18.5 12.5147 16.4853 10.5 14 10.5C11.5147 10.5 9.5 12.5147 9.5 15C9.5 17.4853 11.5147 19.5 14 19.5Z" stroke="white" stroke-width="1.6" />
</svg>

      </div>

      <span>All photos (37)</span>
</button>
    <button class="js-open-gallery" data-open="Request plan">
      <div
        style="background-image: url(&#39;data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAADAAUDAREAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAAB//EAB8QAAEEAAcAAAAAAAAAAAAAAAIBAwQFAAYHFCIxQf/EABUBAQEAAAAAAAAAAAAAAAAAAAAD/8QAFhEBAQEAAAAAAAAAAAAAAAAAAAEx/9oADAMBAAIRAxEAPwB30yztdXVPIOdN3JNPK2Cm0HEU86xObR//2Q==&#39;)">

          <div class="je2-lazy-load"
               data-src="https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/11e90d0a-3665-42f2-86d7-e035ee21ad0e/je/160x120xc.jpg"
               alt="Floor Plan"></div>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M1.5 14.5C1.5 15.0304 1.71071 15.5391 2.08579 15.9142C2.46086 16.2893 2.96957 16.5 3.5 16.5C4.03043 16.5 4.53914 16.2893 4.91421 15.9142C5.28929 15.5391 5.5 15.0304 5.5 14.5C5.5 13.9696 5.28929 13.4609 4.91421 13.0858C4.53914 12.7107 4.03043 12.5 3.5 12.5C2.96957 12.5 2.46086 12.7107 2.08579 13.0858C1.71071 13.4609 1.5 13.9696 1.5 14.5V14.5Z" stroke="white" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M1.5 14.5V3.5C1.5 2.96957 1.71071 2.46086 2.08579 2.08579C2.46086 1.71071 2.96957 1.5 3.5 1.5C4.03043 1.5 4.53914 1.71071 4.91421 2.08579C5.28929 2.46086 5.5 2.96957 5.5 3.5V14.5" stroke="white" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M3.5 16.5H15.5C15.7652 16.5 16.0196 16.3946 16.2071 16.2071C16.3946 16.0196 16.5 15.7652 16.5 15.5V5C16.5 4.73478 16.3946 4.48043 16.2071 4.29289C16.0196 4.10536 15.7652 4 15.5 4H5.5" stroke="white" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M13 9.16675V13.0001H9V9.16675" stroke="white" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M8 10L11 7.5L14 10" stroke="white" stroke-linecap="round" stroke-linejoin="round" />
</svg>

      </div>

      <span>Floor Plan</span>
</button>
    <button class="js-open-gallery" data-open="Video">
      <div
        style="background-image: url(&#39;data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAADAAUDAREAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAAB//EAB8QAAEEAAcAAAAAAAAAAAAAAAIBAwQFAAYHFCIxQf/EABUBAQEAAAAAAAAAAAAAAAAAAAAD/8QAFhEBAQEAAAAAAAAAAAAAAAAAAAEx/9oADAMBAAIRAxEAPwB30yztdXVPIOdN3JNPK2Cm0HEU86xObR//2Q==&#39;)">
            <div class="je2-listing-in-details__video-container">
              <iframe
                class="je2-listing-in-details__video"
                src="https://www.youtube.com/embed/N9oDQAUN6nI?rel=0&amp;autoplay=1&amp;mute=1&amp;loop=1&amp;playlist=N9oDQAUN6nI&amp;controls=0&amp;modestbranding=1&amp;t=10"
                frameborder="0"
                allow="autoplay; encrypted-media"
                title="Video">
              </iframe>
            </div>
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="13.9984" cy="14.0004" r="12.6" stroke="white" stroke-width="1.6" />
<path d="M10.0234 17.5284V10.4711C10.0234 9.65586 10.9723 9.14058 11.7444 9.53648L18.6263 13.0651C19.4207 13.4725 19.4207 14.527 18.6263 14.9343L11.7444 18.463C10.9723 18.8589 10.0234 18.3436 10.0234 17.5284Z" stroke="white" stroke-width="1.6" />
</svg>

      </div>

      <span>Video</span>
</button>
    <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>

</div>

            </div>
            <button class="je2-button je2-listing-in-details__slide-button _next _noborder js-listing-details-button _hidden">

    <svg width="8" height="12" viewBox="0 0 8 12" fill="none">
  <path d="M1.1568 0.902554L6.25484 6.00059L1.1568 11.0986" stroke-width="1.22353" />
</svg>







  
  


</button>
          </div>
      </div>

        <div class="je2-listing__section _about-property" id="about-property">
          <h2>About the Property</h2>
          
<div class="je2-listing-about-property js-listing-about-property">
  <div class="je2-read-more js-read-more _v2 _original" data-block="">

  <div class="je2-read-more__preview _translated"></div>
  <div class="je2-read-more__preview _original">ELITE GROUP Real Estate is delighted to present this magnificent family estate, a true haven of peace, located in the sought-after commune of Vars, just a few minutes from Angoulême.<br/><br/>With approximately 256 m² of living space, this home boasts generous volumes and is set within a serene, verdant environment, featuring a landscaped and fenced garden of over 1,700 m², a large heated saltwater pool, and numerous outbuildings, combining authentic charm with modern comfort.<br/><br/>Main House:<br/><br/>Ground Floor:<br/>A refined entrance leads to an exceptional 50 m² living area, bathed in natural light thanks to its south-facing exposur</div>

    <div class="je2-read-more__content _translated"></div>
    <div class="je2-read-more__content _original">ELITE GROUP Real Estate is delighted to present this magnificent family estate, a true haven of peace, located in the sought-after commune of Vars, just a few minutes from Angoulême.<br/><br/>With approximately 256 m² of living space, this home boasts generous volumes and is set within a serene, verdant environment, featuring a landscaped and fenced garden of over 1,700 m², a large heated saltwater pool, and numerous outbuildings, combining authentic charm with modern comfort.<br/><br/>Main House:<br/><br/>Ground Floor:<br/>A refined entrance leads to an exceptional 50 m² living area, bathed in natural light thanks to its south-facing exposure, highlighted by an elegant fireplace. The high-end, fully equipped kitchen offers direct access to a traditional vaulted cellar, perfectly blending authenticity and prestige.<br/><br/>First Floor:<br/>Two bedrooms with built-in wardrobes, a stylish shower room, and a private master area featuring a bedroom opening onto a terrace, a large dressing room, and a luxurious bathroom with shower, bathtub, and WC.<br/><br/>Top Floor:<br/>A spacious bedroom with storage, as well as an attic easily convertible into additional living space or used for storage.<br/><br/>Outdoor Features:<br/><br/>Two garages and ample parking<br/><br/>70 m² outbuilding<br/><br/>42 m² barn<br/><br/>Summer kitchen<br/><br/>Second outbuilding suitable for a guest house<br/><br/>Boiler room with gas heating and thermodynamic water heater<br/><br/>The heated saltwater pool (11x5 m) with an integrated safety cover, the well, and the automatic irrigation system complete this property, offering elegant and functional outdoor spaces.<br/><br/>Comfort and Premium Features:<br/><br/>Gas heating<br/><br/>Thermodynamic water heater<br/><br/>Double-glazed PVC windows<br/><br/>Fiber optic internet<br/><br/>Electric gate and wooden shutters<br/><br/>Solar panels for hot water production<br/><br/>This rare property combines refinement, functionality, and authenticity, offering an exceptional lifestyle for a family seeking serenity, space, and absolute comfort.<br/><br/>Contact ELITE GROUP Real Estate today to schedule a private visit and discover this outstanding property, where every detail has been thoughtfully designed.<br/>Information on the risks to which this property is exposed is available on the Géorisques website: https://www.georisques.gouv.fr/</div>
    <div class="je2-read-more__expand js-expand">
      <span>…</span>
      <button class="je2-button je2-link" aria-expanded="false">

  

    <span>
          View more
    </span>




    <svg><use xlink:href="#short-arrow"></use></svg>

  


</button>
    </div>
    <div class="je2-read-more__collapse">
      <button class="je2-button je2-link js-collapse" aria-expanded="true">

  

    <span>
          View less
    </span>




    <svg><use xlink:href="#short-arrow"></use></svg>

  


</button>
    </div>
</div>

  
  <div class="je2-listing-about-building">
      <ul>
          <li>
            <h3>Property type</h3>
            <p>House</p>
          </li>
          <li>
            <h3>Floors</h3>
            <p>2</p>
          </li>
          <li>
            <h3>Year built</h3>
            <p>1850</p>
          </li>
          <li>
            <h3>Price/sqm</h3>
            <p>€2,608</p>
          </li>
      </ul>
      <ul>
          <li>
            <h3>Emissions</h3>
            <p>D</p>
          </li>
          <li>
            <h3>Consumption</h3>
            <p>D</p>
          </li>
      </ul>
  </div>


  <div class="je2-listing-about-property__report">
    <button class="je2-button _noborder js-report je2-link" data-href="/listing_reports/new?listing_report%5Blisting_id%5D=16460690">

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 18 18" width="18" height="18" fill="none"><path d="M2.5 17.177V9.34m0 0V1.5H16l-2.177 3.92L16 9.338H2.5Z" stroke="#717171" stroke-width="1.2" /></svg>



    <span>
          <span class="translation_missing" title="translation missing: en.components.je2.Components.listing-about-property.report">Report</span>
    </span>




  
  


</button>
  </div>
</div>

        </div>

        <div class="je2-listing__section _features" id="features">
          <h2>Features</h2>
          <div class="je2-listing-features js-listing-features">
  <div class="je2-listing-features__features-top-9">
    <ul>
        <li>
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M18.75 9.37499c-.0017-.83357-.2419-1.64925-.6923-2.35068-.4504-.70142-1.0921-1.25928-1.8494-1.60766.0676-.35885.0544-.72823-.0385-1.08137-.0928-.35315-.2631-.68121-.4984-.96041-.2353-.27921-.5298-.50256-.8622-.65388-.3323-.15132-.6941-.22681-1.0592-.221-.0525 0-.1017.0125-.1542.01583-.4011-.58318-.938-1.06006-1.5644-1.38952-.6265-.329455-1.3236-.501605-2.03142-.501605-.70779 0-1.40496.17215-2.0314.501605-.62644.32946-1.16335.80634-1.56443 1.38952-.0525-.00333-.10167-.01583-.15417-.01583-.3651-.00581-.72693.06968-1.05925.221-.33232.15132-.62682.37467-.86215.65388-.23533.2792-.40559.60726-.49846.96041-.09287.35314-.10601.72252-.03847 1.08137-.83373.38362-1.52536 1.02022-1.97664 1.81936-.45128.79913-.63925 1.72016-.5372 2.63222.10205.91207.48892 1.76877 1.10565 2.44837.61673.6797 1.43196 1.1477 2.32986 1.3376.22029.4754.54743.8935.95591 1.2217.40848.3281.88725.5575 1.39897.6702.51173.1127 1.04256.1056 1.55111-.0206.50855-.1262.98106-.3683 1.38067-.7072.39982.3389.87242.5807 1.38112.7068.5087.1261 1.0396.1329 1.5513.02.5118-.113.9905-.3426 1.3989-.671.4083-.3285.7353-.7468.9553-1.2224.9798-.2085 1.8583-.7469 2.4887-1.5254.6304-.7784.9745-1.7496.9747-2.75131v0ZM10 6.875v12.5" /><path d="M10 12.5c2.5 0 3.75-1.25 3.75-3.75M9.99999 10c-.41694.0252-.83448-.03843-1.22502-.18657-.39055-.14815-.74521-.37748-1.04057-.67284-.29536-.29535-.52469-.65002-.67283-1.04057-.14815-.39054-.21174-.80808-.18658-1.22502" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

            <span>
                Garden
              </span>
        </li>
        <li>
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M18.1 6.3H2v10H18v-10Z" /><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M6.9 16.3v-2a3.1 3.1 0 1 1 6.2 0v2M1.9 8.8H18M1.9 11.3h3.7M4.4 6.3v2.5M5.6 8.8v2.4M8.1 6.3v2.5M11.9 6.3v2.5M13.1 8.8V10M15.6 6.3v2.5M19.4 3.8H.6v2.5h18.8V3.8ZM14.4 11.3H18M1.9 13.8h2.5M15.6 13.8h2.5M4.4 13.8v-2.6M15.6 13.8v-2.6" /></svg>

            <span>
                Fireplace
              </span>
        </li>
        <li>
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M.625 19.0117c.8889.3584 1.86199.4541 2.8037.2758.94171-.1783 1.81245-.6231 2.5088-1.2817.92861.8792 2.15875 1.3691 3.4375 1.3691 1.2787 0 2.5089-.4899 3.4375-1.3691.8768.8299 2.0242 1.3146 3.2304 1.3645 1.2062.05 2.3898-.3382 3.3321-1.0928M14.375 15.625v-12.5c0-.66304.2634-1.29893.7322-1.76777C15.5761.888392 16.212.625 16.875.625s1.2989.263392 1.7678.73223c.4688.46884.7322 1.10473.7322 1.76777M6.875 15.625v-12.5c0-.66304.26339-1.29893.73223-1.76777C8.07607.888392 8.71196.625 9.375.625c.663 0 1.2989.263392 1.7678.73223.4688.46884.7322 1.10473.7322 1.76777M6.875 9.375h7.5M6.875 13.125h7.5M6.875 5.625h7.5" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

            <span>
                Pool
              </span>
        </li>
        <li>
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M2.29167 2.39999H17.7083c.1105 0 .2165.0439.2947.12204.0781.07814.122.18412.122.29463v2.5H1.875v-2.5c0-.11051.0439-.21649.12204-.29463.07814-.07814.18412-.12204.29463-.12204v0Z" /><path d="M1.875 5.31665h16.25v2.5c0 .11051-.0439.21649-.122.29463-.0782.07814-.1842.12204-.2947.12204H2.29167c-.11051 0-.21649-.0439-.29463-.12204-.07814-.07814-.12204-.18412-.12204-.29463v-2.5 0ZM19.375 13.4333c0 .4421-.1756.866-.4882 1.1785-.3125.3126-.7364.4882-1.1785.4882H2.29167c-.44203 0-.86595-.1756-1.17851-.4882C.800595 14.2993.625 13.8754.625 13.4333c0-.442.175595-.8659.48816-1.1785.31256-.3125.73648-.4881 1.17851-.4881H17.7083c.4421 0 .866.1756 1.1785.4881.3126.3126.4882.7365.4882 1.1785ZM4.375 8.23334v3.53336M15.625 8.23334v3.53336M4.375 1.14999v1.25M15.625 1.14999v1.25M2.91675 15.1l-1.25 3.75M17.0833 15.1l1.25 3.75" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

            <span>
                Terrace
              </span>
        </li>
        <li>
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M5.625.625h-2.5c-.69036 0-1.25.55964-1.25 1.25V13.75c0 .6904.55964 1.25 1.25 1.25h2.5c.69036 0 1.25-.5596 1.25-1.25V1.875c0-.69036-.55964-1.25-1.25-1.25ZM10.625.625h-2.5c-.69036 0-1.25.55964-1.25 1.25V13.75c0 .6904.55964 1.25 1.25 1.25h2.5c.6904 0 1.25-.5596 1.25-1.25V1.875c0-.69036-.5596-1.25-1.25-1.25ZM14.9752 1.83176l-1.237.17973c-.6832.09926-1.1565.73356-1.0572 1.41674l1.5277 10.51457c.0992.6832.7335 1.1566 1.4167 1.0573l1.237-.1797c.6832-.0993 1.1566-.7336 1.0573-1.4168L16.392 2.88904c-.0993-.68319-.7336-1.15655-1.4168-1.05728Z" /><path d="M.625 16.25c0 .3315.131696.6495.366117.8839.234423.2344.552363.3661.883883.3661h16.25c.3315 0 .6495-.1317.8839-.3661.2344-.2344.3661-.5524.3661-.8839s-.1317-.6495-.3661-.8839c-.2344-.2344-.5524-.3661-.8839-.3661H1.875c-.33152 0-.64946.1317-.883883.3661C.756696 15.6005.625 15.9185.625 16.25v0ZM2.5 17.5v1.875M17.5 17.5v1.875" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

            <span>
                Library
              </span>
        </li>
        <li>
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="m14.8935 5.10501-4.1242 4.12583M13.4208 3.63165l-4.12417 4.125M16.3684 6.57916l-4.125 4.12414M19.5832 7.02168c0-.11029-.0437-.21608-.1216-.29417L13.2724.538346c-.0781-.078113-.1841-.121995-.2946-.121995-.1105 0-.2164.043882-.2946.121995L7.95657 5.26835c-.17882.17884-.31459.39604-.39703.63513-.08244.2391-.10939.49382-.0788.74487L7.92241 10.27c.05488.4604.26295.8889.59078 1.2167.32783.3279.75636.5359 1.21672.5908l3.62169.4417c.251.0306.5057.0036.7448-.0788.2391-.0825.4563-.2182.6352-.3971l4.73-4.72662c.0386-.03877.0693-.08477.0902-.13539.0208-.05062.0315-.10486.0314-.15961v0Z" /><path d="M7.92749 10.305.782494 17.4492c-.234496.2345-.366234.5525-.366234.8841 0 .3317.131738.6497.366234.8842.234496.2345.552536.3662.884166.3662s.64967-.1317.88417-.3662l7.14416-7.145M3.43408 14.7975l1.76834 1.7683" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

            <span>
                Outdoor Kitchen
              </span>
        </li>
        <li>
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M7.5 19.375h5M10 19.375v-7.2408M15.7391 5.43083c.155 1.00881.0415 2.04066-.3292 2.9916-.3708.95094-.9856 1.78737-1.7825 2.42507-1.0296.8237-2.3089 1.2725-3.62748 1.2725-1.31857 0-2.59788-.4488-3.6275-1.2725v0C5.5755 10.2098 4.96072 9.37337 4.59 8.42243c-.37073-.95094-.48429-1.98279-.32924-2.9916L4.91659 1.155c.02273-.1478.0977-.28256.21131-.379806s.25831-.150534.40786-.150192h8.92834c.1492.000056.2936.053525.4068.150735.1133.09721.188.231743.2107.379263l.6575 4.27583ZM4.23413 5.625H15.7658" /></svg>

            <span>
                Wine Cellar
              </span>
        </li>
        <li>
          <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M17.5433 16.875c.1932-.0009.3834-.0487.5541-.1393.1707-.0905.3168-.2212.4259-.3807.1122-.1626.1856-.3489.2145-.5443.0289-.1955.0126-.395-.0478-.5832-.6524-1.7632-1.8423-3.2768-3.4017-4.327-1.5593-1.05015-3.4092-1.58379-5.28832-1.52549-1.87868-.05777-3.72804.47612-5.28688 1.52629-1.55884 1.0501-2.74838 2.5634-3.40062 4.3262-.06075.1881-.07732.3877-.04841.5832.0289.1956.1025.3818.21508.5443.10891.1595.25492.2901.42548.3807.17056.0906.36057.1384.55369.1393H17.5433Z" /><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M11.875 5c0-.37084-.11-.73335-.316-1.04169-.206-.30835-.4989-.54867-.8415-.69058-.3426-.14192-.71958-.17905-1.08329-.1067-.36372.07235-.69781.25092-.96003.51315-.26223.26222-.4408.59631-.51315.96003-.07235.36371-.03522.74071.1067 1.08332.14191.34261.38223.63545.69058.84148.30834.20602.67085.31599 1.04169.31599v2.5" /></svg>

            <span>
                Walk In Closet
              </span>
        </li>
        <li>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M.605 18.641h18.75M1.855 7.391h16.25v11.25H1.855V7.392ZM19.355 5.891a.627.627 0 0 0-.333-.551L10.272.673a.629.629 0 0 0-.589 0L.933 5.34A.627.627 0 0 0 .6 5.89v.875a.625.625 0 0 0 .625.625h17.5a.625.625 0 0 0 .625-.625l.005-.875Z" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /><path d="M4.355 9.891h11.25v8.75H4.355v-8.75ZM6.855 13.641h6.25M6.855 16.141h6.25" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /></svg>

            <span>
                Garage
              </span>
        </li>
    </ul>
  </div>
    <button class="je2-button js-show-features-popup _noborder je2-link">

  

    <span>
          View all 16 features
    </span>




    <svg><use xlink:href="#arrow-right"></use></svg>

  


</button>
    <div class="je2-listing-features__popup js-listing-features-popup">
      <button class="je2-button _noborder js-close">

    <svg><use xlink:href='#cross'></use></svg>






  
  


</button>
      <div>Features</div>
        <h3>Lot</h3>
        <ul>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="m12.3983 19.3475 4.285.0275V9.85417h2.6917L9.86082.625h-.07917l-1.09 1.09M7.16593 3.24167l-1.09 1.09M4.54923 5.85751l-1.09 1.09M1.93333 8.47418.625 9.85418h2.61667V12.19M7.16577 12.3983v-.8725h.87167M3.2417 15.0142v.8725M7.16577 15.0142v.8725M7.16577 18.5025v.8725M3.2417 18.5025v.8725h3.92417" /><path d="M12.3983 19.3475v-7.8217h-1.315" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  Renovated
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M.656738 17.1425H19.3751M8.1442 17.1425H1.90503V9.03168l6.23917-1.2475v9.35832Z" /><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M18.1273 17.1425H8.14404V3.41751l9.98326 4.36667v9.35832Z" /><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M15.6316 17.1425h-4.9917v-3.7433c0-.3315.1317-.6495.3662-.8839.2344-.2345.5523-.3661.8838-.3661h2.5c.3316 0 .6495.1316.8839.3661.2344.2344.3661.5524.3661.8839l-.0083 3.7433ZM.625 9.28835l7.51917-1.50417M6.86499 2.85751 19.3716 8.32835M15.6318 6.68501v-3.2675h2.4959v4.36667" /><path stroke="#151515" stroke-width="1.2" d="M10.6392 8.0975c-.1726 0-.3125-.1399-.3125-.3125 0-.17258.1399-.3125.3125-.3125M10.6392 8.0975c.1725 0 .3125-.1399.3125-.3125 0-.17258-.14-.3125-.3125-.3125" /></svg>

                <span>
                  Mansion
                </span>
            </li>
        </ul>
        <h3>Indoor</h3>
        <ul>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M18.1 6.3H2v10H18v-10Z" /><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M6.9 16.3v-2a3.1 3.1 0 1 1 6.2 0v2M1.9 8.8H18M1.9 11.3h3.7M4.4 6.3v2.5M5.6 8.8v2.4M8.1 6.3v2.5M11.9 6.3v2.5M13.1 8.8V10M15.6 6.3v2.5M19.4 3.8H.6v2.5h18.8V3.8ZM14.4 11.3H18M1.9 13.8h2.5M15.6 13.8h2.5M4.4 13.8v-2.6M15.6 13.8v-2.6" /></svg>

                <span>
                  Fireplace
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M5.625.625h-2.5c-.69036 0-1.25.55964-1.25 1.25V13.75c0 .6904.55964 1.25 1.25 1.25h2.5c.69036 0 1.25-.5596 1.25-1.25V1.875c0-.69036-.55964-1.25-1.25-1.25ZM10.625.625h-2.5c-.69036 0-1.25.55964-1.25 1.25V13.75c0 .6904.55964 1.25 1.25 1.25h2.5c.6904 0 1.25-.5596 1.25-1.25V1.875c0-.69036-.5596-1.25-1.25-1.25ZM14.9752 1.83176l-1.237.17973c-.6832.09926-1.1565.73356-1.0572 1.41674l1.5277 10.51457c.0992.6832.7335 1.1566 1.4167 1.0573l1.237-.1797c.6832-.0993 1.1566-.7336 1.0573-1.4168L16.392 2.88904c-.0993-.68319-.7336-1.15655-1.4168-1.05728Z" /><path d="M.625 16.25c0 .3315.131696.6495.366117.8839.234423.2344.552363.3661.883883.3661h16.25c.3315 0 .6495-.1317.8839-.3661.2344-.2344.3661-.5524.3661-.8839s-.1317-.6495-.3661-.8839c-.2344-.2344-.5524-.3661-.8839-.3661H1.875c-.33152 0-.64946.1317-.883883.3661C.756696 15.6005.625 15.9185.625 16.25v0ZM2.5 17.5v1.875M17.5 17.5v1.875" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  Library
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M.625 19.375v-6.6667M11.875 12.7083h7.5v6.25c0 .1106-.0439.2165-.122.2947-.0782.0781-.1842.122-.2947.122h-6.6666c-.1105 0-.2165-.0439-.2947-.122-.0781-.0782-.122-.1841-.122-.2947v-6.25ZM1.04167 9.375H18.9583c.1105 0 .2165.0439.2947.12204.0781.07814.122.18412.122.29463v2.91663H.625V9.79167c0-.11051.043899-.21649.122039-.29463.07814-.07814.184121-.12204.294631-.12204v0ZM11.875 16.0417h7.5M11.875.625h-7.5c-.69036 0-1.25.55964-1.25 1.25v3.75c0 .69036.55964 1.25 1.25 1.25h7.5c.6904 0 1.25-.55964 1.25-1.25v-3.75c0-.69036-.5596-1.25-1.25-1.25ZM8.125 6.875v2.5" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  Office
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M1.25 7.5 9.47583.84083C9.62417.720813 9.80919.655334 10 .655334c.1908 0 .3758.065479.5242.185496L18.75 7.5" /><path d="m9.46909 4.18833-7.065 5.83337c-.19113.1775-.30611.422-.32084.6825V18.75c0 .221.0878.433.24408.5892.15628.1563.36824.2441.58926.2441H17.0833c.221 0 .4329-.0878.5892-.2441.1563-.1562.2441-.3682.2441-.5892v-8.0433c-.0147-.2605-.1297-.505-.3208-.6825l-7.065-5.83337c-.1491-.12378-.3367-.19174-.5304-.1922-.19379-.00046-.38166.06662-.53131.1897Z" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  High Ceiling
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M.625 7.70833h17.0833c.4421 0 .866-.17559 1.1785-.48815.3126-.31256.4882-.73649.4882-1.17851 0-.44203-.1756-.86595-.4882-1.17851-.3125-.31257-.7364-.48816-1.1785-.48816H.625M.625.625v18.75M18.125 7.64999V19.375M5.625 19.375v-6.25M13.125 19.375v-6.25M6.875 13.125c.33152 0 .64946-.1317.88388-.3661.23442-.2344.36612-.5524.36612-.8839s-.1317-.6495-.36612-.8839c-.23442-.2344-.55236-.3661-.88388-.3661h-2.5c-.33152 0-.64946.1317-.88388.3661-.23442.2344-.36612.5524-.36612.8839s.1317.6495.36612.8839c.23442.2344.55236.3661.88388.3661h2.5ZM14.375 13.125c.3315 0 .6495-.1317.8839-.3661.2344-.2344.3661-.5524.3661-.8839s-.1317-.6495-.3661-.8839c-.2344-.2344-.5524-.3661-.8839-.3661h-2.5c-.3315 0-.6495.1317-.8839.3661-.2344.2344-.3661.5524-.3661.8839s.1317.6495.3661.8839c.2344.2344.5524.3661.8839.3661h2.5ZM16.25.625H12.5l.625 3.75h2.5l.625-3.75Z" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  Kitchen island
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M17.5433 16.875c.1932-.0009.3834-.0487.5541-.1393.1707-.0905.3168-.2212.4259-.3807.1122-.1626.1856-.3489.2145-.5443.0289-.1955.0126-.395-.0478-.5832-.6524-1.7632-1.8423-3.2768-3.4017-4.327-1.5593-1.05015-3.4092-1.58379-5.28832-1.52549-1.87868-.05777-3.72804.47612-5.28688 1.52629-1.55884 1.0501-2.74838 2.5634-3.40062 4.3262-.06075.1881-.07732.3877-.04841.5832.0289.1956.1025.3818.21508.5443.10891.1595.25492.2901.42548.3807.17056.0906.36057.1384.55369.1393H17.5433Z" /><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M11.875 5c0-.37084-.11-.73335-.316-1.04169-.206-.30835-.4989-.54867-.8415-.69058-.3426-.14192-.71958-.17905-1.08329-.1067-.36372.07235-.69781.25092-.96003.51315-.26223.26222-.4408.59631-.51315.96003-.07235.36371-.03522.74071.1067 1.08332.14191.34261.38223.63545.69058.84148.30834.20602.67085.31599 1.04169.31599v2.5" /></svg>

                <span>
                  Walk In Closet
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M7.5 19.375h5M10 19.375v-7.2408M15.7391 5.43083c.155 1.00881.0415 2.04066-.3292 2.9916-.3708.95094-.9856 1.78737-1.7825 2.42507-1.0296.8237-2.3089 1.2725-3.62748 1.2725-1.31857 0-2.59788-.4488-3.6275-1.2725v0C5.5755 10.2098 4.96072 9.37337 4.59 8.42243c-.37073-.95094-.48429-1.98279-.32924-2.9916L4.91659 1.155c.02273-.1478.0977-.28256.21131-.379806s.25831-.150534.40786-.150192h8.92834c.1492.000056.2936.053525.4068.150735.1133.09721.188.231743.2107.379263l.6575 4.27583ZM4.23413 5.625H15.7658" /></svg>

                <span>
                  Wine Cellar
                </span>
            </li>
        </ul>
        <h3><span class="translation_missing" title="translation missing: en.components.je2.Components.listing-features.listing.property_features_component.outdoor">Outdoor</span></h3>
        <ul>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M2.29167 2.39999H17.7083c.1105 0 .2165.0439.2947.12204.0781.07814.122.18412.122.29463v2.5H1.875v-2.5c0-.11051.0439-.21649.12204-.29463.07814-.07814.18412-.12204.29463-.12204v0Z" /><path d="M1.875 5.31665h16.25v2.5c0 .11051-.0439.21649-.122.29463-.0782.07814-.1842.12204-.2947.12204H2.29167c-.11051 0-.21649-.0439-.29463-.12204-.07814-.07814-.12204-.18412-.12204-.29463v-2.5 0ZM19.375 13.4333c0 .4421-.1756.866-.4882 1.1785-.3125.3126-.7364.4882-1.1785.4882H2.29167c-.44203 0-.86595-.1756-1.17851-.4882C.800595 14.2993.625 13.8754.625 13.4333c0-.442.175595-.8659.48816-1.1785.31256-.3125.73648-.4881 1.17851-.4881H17.7083c.4421 0 .866.1756 1.1785.4881.3126.3126.4882.7365.4882 1.1785ZM4.375 8.23334v3.53336M15.625 8.23334v3.53336M4.375 1.14999v1.25M15.625 1.14999v1.25M2.91675 15.1l-1.25 3.75M17.0833 15.1l1.25 3.75" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  Terrace
                </span>
            </li>
            <li>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M.605 18.641h18.75M1.855 7.391h16.25v11.25H1.855V7.392ZM19.355 5.891a.627.627 0 0 0-.333-.551L10.272.673a.629.629 0 0 0-.589 0L.933 5.34A.627.627 0 0 0 .6 5.89v.875a.625.625 0 0 0 .625.625h17.5a.625.625 0 0 0 .625-.625l.005-.875Z" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /><path d="M4.355 9.891h11.25v8.75H4.355v-8.75ZM6.855 13.641h6.25M6.855 16.141h6.25" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /></svg>

                <span>
                  Garage
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M2.08325 14.1667v1.6666M17.9167 14.1667v1.6666M.416748 9.16666V12.5c0 .442.175595.8659.488155 1.1785.312557.3126.736487.4882 1.178507.4882H17.9167c.4421 0 .866-.1756 1.1786-.4882.3125-.3126.4881-.7365.4881-1.1785V9.16666" /><path d="M17.0834 9.16666v.83333c0 .22101-.0878.43301-.2441.58921-.1562.1563-.3682.2441-.5892.2441H3.75008c-.22101 0-.43297-.0878-.58925-.2441-.15628-.1562-.24408-.3682-.24408-.58921v-.83333M17.9166 7.96916v-.46917c0-.88406-.3512-1.7319-.9763-2.35702-.6251-.62512-1.473-.97631-2.357-.97631H5.41659c-.88406 0-1.73191.35119-2.35703.97631-.62512.62512-.97631 1.47296-.97631 2.35702v.48083" /><path d="M.416748 9.16666c0-.33152.131696-.64947.366117-.88389.234425-.23442.552365-.36611.883885-.36611.33152 0 .64946.13169.88388.36611.23442.23442.36612.55237.36612.88389M19.5833 9.16666c0-.33152-.1317-.64947-.3662-.88389-.2344-.23442-.5523-.36611-.8838-.36611-.3316 0-.6495.13169-.8839.36611-.2345.23442-.3661.55237-.3661.88389M10 4.16666v6.66664" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  Outdoor Living Space
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M10 .666656c1.9891 0 3.8968.790174 5.3033 2.196704C16.7098 4.26988 17.5 6.17753 17.5 8.16666 17.5 14.75 11.7233 18.4425 10.3092 19.25c-.0944.0537-.2011.0819-.30962.0819-.10855 0-.21524-.0282-.30958-.0819-1.41417-.8067-7.19-4.5-7.19-11.08334 0-1.98913.79018-3.89678 2.1967-5.3033C6.10322 1.45683 8.01088.666656 10 .666656v0Z" /><path stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" d="M8.125 9.33331h2.8125c.5802 0 1.1366-.23047 1.5468-.6407.4102-.41024.6407-.96664.6407-1.5468 0-.58016-.2305-1.13656-.6407-1.54679-.4102-.41024-.9666-.64071-1.5468-.64071H8.125M8.125 4.95667v8.12503" /></svg>

                <span>
                  Parking
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M18.75 9.37499c-.0017-.83357-.2419-1.64925-.6923-2.35068-.4504-.70142-1.0921-1.25928-1.8494-1.60766.0676-.35885.0544-.72823-.0385-1.08137-.0928-.35315-.2631-.68121-.4984-.96041-.2353-.27921-.5298-.50256-.8622-.65388-.3323-.15132-.6941-.22681-1.0592-.221-.0525 0-.1017.0125-.1542.01583-.4011-.58318-.938-1.06006-1.5644-1.38952-.6265-.329455-1.3236-.501605-2.03142-.501605-.70779 0-1.40496.17215-2.0314.501605-.62644.32946-1.16335.80634-1.56443 1.38952-.0525-.00333-.10167-.01583-.15417-.01583-.3651-.00581-.72693.06968-1.05925.221-.33232.15132-.62682.37467-.86215.65388-.23533.2792-.40559.60726-.49846.96041-.09287.35314-.10601.72252-.03847 1.08137-.83373.38362-1.52536 1.02022-1.97664 1.81936-.45128.79913-.63925 1.72016-.5372 2.63222.10205.91207.48892 1.76877 1.10565 2.44837.61673.6797 1.43196 1.1477 2.32986 1.3376.22029.4754.54743.8935.95591 1.2217.40848.3281.88725.5575 1.39897.6702.51173.1127 1.04256.1056 1.55111-.0206.50855-.1262.98106-.3683 1.38067-.7072.39982.3389.87242.5807 1.38112.7068.5087.1261 1.0396.1329 1.5513.02.5118-.113.9905-.3426 1.3989-.671.4083-.3285.7353-.7468.9553-1.2224.9798-.2085 1.8583-.7469 2.4887-1.5254.6304-.7784.9745-1.7496.9747-2.75131v0ZM10 6.875v12.5" /><path d="M10 12.5c2.5 0 3.75-1.25 3.75-3.75M9.99999 10c-.41694.0252-.83448-.03843-1.22502-.18657-.39055-.14815-.74521-.37748-1.04057-.67284-.29536-.29535-.52469-.65002-.67283-1.04057-.14815-.39054-.21174-.80808-.18658-1.22502" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  Garden
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="M.625 19.0117c.8889.3584 1.86199.4541 2.8037.2758.94171-.1783 1.81245-.6231 2.5088-1.2817.92861.8792 2.15875 1.3691 3.4375 1.3691 1.2787 0 2.5089-.4899 3.4375-1.3691.8768.8299 2.0242 1.3146 3.2304 1.3645 1.2062.05 2.3898-.3382 3.3321-1.0928M14.375 15.625v-12.5c0-.66304.2634-1.29893.7322-1.76777C15.5761.888392 16.212.625 16.875.625s1.2989.263392 1.7678.73223c.4688.46884.7322 1.10473.7322 1.76777M6.875 15.625v-12.5c0-.66304.26339-1.29893.73223-1.76777C8.07607.888392 8.71196.625 9.375.625c.663 0 1.2989.263392 1.7678.73223.4688.46884.7322 1.10473.7322 1.76777M6.875 9.375h7.5M6.875 13.125h7.5M6.875 5.625h7.5" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  Pool
                </span>
            </li>
            <li>
              <svg viewBox="0 0 20 20" width="20" height="20" fill="none"><g stroke="#151515" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" clip-path="url(#a)"><path d="m14.8935 5.10501-4.1242 4.12583M13.4208 3.63165l-4.12417 4.125M16.3684 6.57916l-4.125 4.12414M19.5832 7.02168c0-.11029-.0437-.21608-.1216-.29417L13.2724.538346c-.0781-.078113-.1841-.121995-.2946-.121995-.1105 0-.2164.043882-.2946.121995L7.95657 5.26835c-.17882.17884-.31459.39604-.39703.63513-.08244.2391-.10939.49382-.0788.74487L7.92241 10.27c.05488.4604.26295.8889.59078 1.2167.32783.3279.75636.5359 1.21672.5908l3.62169.4417c.251.0306.5057.0036.7448-.0788.2391-.0825.4563-.2182.6352-.3971l4.73-4.72662c.0386-.03877.0693-.08477.0902-.13539.0208-.05062.0315-.10486.0314-.15961v0Z" /><path d="M7.92749 10.305.782494 17.4492c-.234496.2345-.366234.5525-.366234.8841 0 .3317.131738.6497.366234.8842.234496.2345.552536.3662.884166.3662s.64967-.1317.88417-.3662l7.14416-7.145M3.43408 14.7975l1.76834 1.7683" /></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h20v20H0z" /></clipPath></defs></svg>

                <span>
                  Outdoor Kitchen
                </span>
            </li>
        </ul>
    </div>
</div>

        </div>


      <div class="je2-listing__section _map" id="map">
        <h2>Explore the Area</h2>
        <div class="je2-listing-map js-listing-map">
    <div class="je2-listing-map__above-map">
      <div>
        <span>Angoulême, France, Angoulême, Nouvelle-Aquitaine, France.</span>
          <a href="https://www.google.com/maps/search/?api=1&amp;query=45.6488766,0.1567288" class="je2-button je2-button _noborder _link" target="_blank" data-name="See on Google Maps">

  

    <span>
          View on Google Maps
    </span>




    <svg xmlns="http://www.w3.org/2000/svg" width="17" height="18" viewBox="0 0 17 18" fill="none"><path d="m4.188 13.477 8.485-8.486M13.144 12.066V4.523H5.602" stroke="#006C75" stroke-width="1.6" /></svg>


  


</a>
      </div>
      <button class="je2-button js-request-location">

  

    <span>
          Request exact location
    </span>




  
  


</button>
    </div>

      
<div class="je2-map js-map-root _loading 
  
  ">

    <div class="je2-map__single-marker js-single-marker"
         data-lat="45.6488766" data-lng="0.1567288">
      <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
  <g filter="url(#filter0_d)">
    <circle cx="28" cy="28" r="24" fill="#151515"/>
    <circle cx="28" cy="28" r="23" stroke="white" stroke-width="2"/>
  </g>
  <path d="M37 37H30.0769V30.7692H25.9231V37H19V25.9231L28 19L37 25.9231V37Z" fill="white"/>
  <defs>
    <filter id="filter0_d" x="0" y="0" width="56" height="56" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feFlood flood-opacity="0" result="BackgroundImageFix"/>
      <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"/>
      <feOffset/>
      <feGaussianBlur stdDeviation="2"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.3 0"/>
      <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow"/>
      <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow" result="shape"/>
    </filter>
  </defs>
</svg>

    </div>

  <div class="je2-map__heatmap__scale js-heatmap-scale _hidden">
    <div>Price per sqm</div>
    <div></div>
    <div>
      <div>Low</div>
      <div>
          <div style="background: rgba(253, 243, 216, 1)"></div>
          <div style="background: rgba(252, 216, 118, 1)"></div>
          <div style="background: rgba(243, 181, 101, 1)"></div>
          <div style="background: rgba(242, 147, 100, 1)"></div>
          <div style="background: rgba(229, 105, 91, 1)"></div>
      </div>
      <div>High</div>
    </div>
  </div>

  <div class="je2-map__zoom">
    <button class="je2-button js-plus-map _onlyicon _noborder" aria-label="Zoom in">

    <svg viewBox="0 0 32 32">
  <path d="M15 5V15H5V17H15V27H17V17H27V15H17V5H15Z"/>
</svg>







  
  


</button>
    <button class="je2-button js-minus-map _onlyicon _noborder" aria-label="Zoom out">

    <svg viewBox="0 0 32 32">
  <path d="M5 15V17H27V15H5Z"/>
</svg>







  
  


</button>
  </div>
  <div class="je2-map__map js-mapbox-map"></div>




    <div class="je2-map__style-switcher">
      <button class="je2-button js-map-style-button">

  

    <span>
          Map
    </span>




  
  


</button>
      <button class="je2-button js-map-style-button" data-id="satellite-v9">

  

    <span>
          Satellite
    </span>




  
  


</button>
    </div>

    <button class="je2-button je2-map__expand-button js-expand-map _noborder">

    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none" viewBox="0 0 22 22"><path stroke="#151515" stroke-width="1.6" d="m13.14 8.858 7.143-7.143M14.57 1.715h5.715v5.714M8.854 8.858 1.71 1.715M7.425 1.715H1.711v5.714M13.14 13.145l7.143 7.142M14.57 20.285h5.715V14.57M8.854 13.145 1.71 20.287M7.425 20.285H1.711V14.57" /></svg>







  
  


</button>



</div>


    

  <p>

        <a href="/real_estate/angouleme-france" class="je2-button je2-button _link _noborder" target="_blank" data-name="See more listings">

  

    <span>
          View 56 more listings in Angoulême
    </span>




    <svg xmlns="http://www.w3.org/2000/svg" width="17" height="18" viewBox="0 0 17 18" fill="none"><path d="m4.188 13.477 8.485-8.486M13.144 12.066V4.523H5.602" stroke="#006C75" stroke-width="1.6" /></svg>


  


</a>
  </p>
</div>

      </div>


      <div class="je2-listing__section _listed-by">

        <div id="listed-by">
          <h2>Listed by</h2>
            <div class="je2-listed-by__actions">
              <div class="je3-listing-contact-card js-listing-contact-card">
  <div class="je3-listing-contact-card__agent-or-office">
    <div class="je3-listing-contact-card__agent-or-office-info">
        <div class="je3-listing-contact-card__agent-or-office-info__name">Antoine BEAUDOU</div>
            <div class="je3-listing-contact-card__agent-or-office-info__address">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M13.786 6.893c0 3.907-4.521 7.383-5.59 8.15a.852.852 0 0 1-.502.158.852.852 0 0 1-.502-.157c-1.069-.768-5.59-4.244-5.59-8.15a6.092 6.092 0 0 1 12.184 0Z" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /><path d="M5.477 6.338a2.215 2.215 0 1 0 4.43 0 2.215 2.215 0 0 0-4.43 0Z" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /></svg>

                <span>France</span>
            </div>
            <a href="/agents/antoine-beaudou-1728859" class="je2-button je3-listing-contact-card__agent-or-office-info__view-profile _link _noborder" target="_blank" aria-label="View agent profile">

  

    <span>
          View agent profile
    </span>




    <svg xmlns="http://www.w3.org/2000/svg" width="17" height="18" viewBox="0 0 17 18" fill="none"><path d="m4.188 13.477 8.485-8.486M13.144 12.066V4.523H5.602" stroke="#006C75" stroke-width="1.6" /></svg>


  


</a>
    </div>
      <div class="je3-listing-contact-card__agent-or-office__avatar">
            <div class="je3-avatar ">
    <div class="je3-avatar__content">
        <div class="je3-avatar__mask"></div>
        <img class="je3-avatar__image je2-lazy-load" alt="Antoine BEAUDOU" data-src="https://img.jamesedition.com/agent_images/2025/05/05/09/56/36/b49713c4-1257-4f62-918b-053cc5df1dc9/je/80x80xc.jpg" />
        <img class="je3-avatar__blur-background je2-lazy-load" alt="Antoine BEAUDOU background" data-src="https://img.jamesedition.com/agent_images/2025/05/05/09/56/36/b49713c4-1257-4f62-918b-053cc5df1dc9/je/80x80xc.jpg" />
    </div>
</div>

      </div>
  </div>
  <div class="je3-listing-contact-card__info">
    <div class="je3-listing-contact-card__info__listings">
        <a href="/offices/real_estate/elite-group-real-estate-359439#listings" class="je2-button _noborder _link" target="_blank" aria-label="11 Listings">

  

    <span>
          11
    </span>




  
  


</a>
        <div>Listings</div>
    </div>
    <div>
        <div>2025</div>
        <div>Joined</div>
    </div>
  </div>
  <div class="je3-listing-contact-card__buttons">
    <button class="je2-button _cyan js-message _message" data-name="Contact card">

  

    <span>
          Message agent
    </span>




  
  


</button>

    <form class="je2-phone-button" id="contact-card-phone">
  <div data-sitekey="6LeNK2caAAAAABqNVS2GtBowWgxSInPKc9XdX4PE" data-size="invisible"></div>

  <a href="#" class="je2-button js-phone-button _uppercase _cyan js-phone-button" data-error="Try again later." data-missing-number-error="Currently unavailable" data-call-on-click="true" data-location="Contact card" data-fetch-phone-numbers-url="/listings/16460690/fetch-phones-numbers" data-success-text1="Start phone call with:" data-success-text2="Hello, I&#39;m calling for the property with the reference 478AB16, which I discovered on JamesEdition." aria-label="Click to call">
    <div class="je2-button__temporary"></div>

    <svg viewBox="0 0 16 16" >
  <path d="M4.35002 1.5C4.10002 1.5 3.85002 1.6 3.60002 1.75H3.55002L2.00002 3.4C1.50002 3.85 1.35002 4.5 1.60002 5.1C2.00002 6.3 3.10002 8.65 5.20002 10.75C7.30002 12.85 9.70002 13.9 10.85 14.35C11.45 14.55 12.1 14.4 12.6 14L14.2 12.4C14.6 12 14.6 11.25 14.2 10.85L12.15 8.8V8.75C11.75 8.35 11 8.35 10.6 8.75L9.60002 9.75C9.25002 9.6 8.40002 9.15 7.55002 8.35C6.75002 7.55 6.30002 6.65 6.15002 6.3L7.15002 5.3C7.55002 4.9 7.60002 4.2 7.15002 3.75L7.10002 3.7L5.10002 1.65H5.05002C4.85002 1.6 4.60002 1.5 4.35002 1.5Z"/>
</svg>







  
  


</a>

  <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>


</form>

  </div>
</div>

              <div class="je3-listing-book-tour js-book-tour">
  <div class="je3-listing-book-tour__icon">
    <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="none"><path stroke="#151515" stroke-width="1.6" d="M20.427 12.666h-4.852m12.678 0h-4.852m-2.974 6.999h-4.852m-2.817 0H7.906m20.347 0h-4.852M20.427 26.5h-4.852m-2.817 0H7.906m20.347 0h-4.852M10.41 2.086v6.836m15.34-6.836v6.836M3.68 6.481h28.8v26.205H3.68V6.48Z" /></svg>

  </div>
  <div class="je3-listing-book-tour__content">
    <h3 class="je3-listing-book-tour__title">Book home tour with Antoine BEAUDOU</h3>
    <p class="je3-listing-book-tour__description">Choose a date and whether you&#39;d like a virtual or in-person tour with the agent.</p>
  </div>

  <form id="book-tour-form" class="simple_form je3-listing-book-tour__form je2-form js-form" novalidate="novalidate" action="" accept-charset="UTF-8" method="post"><input type="hidden" name="authenticity_token" value="lvglWkTiuDVGWWIeFZBoGZeRkd5gnoxQXafYls616hxOSEFkNjWZRVFK0eCEDUtrNX26jVaGmqsOc_V-emMrvw" autocomplete="off" />
    <div class="je3-listing-book-tour__inputs">
      <div class="je2-select je2-select je3-listing-book-tour__select _with-placeholder">
  <svg class="je2-select__right-icon"><use xlink:href="#arrow-down"></use></svg>
  <select name="request_tour[reason]" id="request_tour_reason" aria-label="request_tour[reason]"><option selected="selected" value="Video chat">Virtual tour</option>
<option value="In-person">In-person tour</option></select>
    <span>Virtual tour</span>
</div>

      <div class="je3-listing-book-tour__input js-datepicker-container _loading">
        <input class="je2-input js-datepicker" aria-label="Date" type="text" name="date" autocomplete="off"
            data-required-error="Please enter the date" readonly>
        <svg><use xlink:href="#arrow-down"></use></svg>
        <div class="je3-spinner"><div></div><div></div><div></div></div>
      </div>
    </div>

    <button class="je2-button je3-listing-book-tour__button _primary">

    <svg viewBox="0 0 32 32">
  <path d="M20.5 6.09998L19.1 7.49998L26.6 15H2V17H26.6L19.1 24.5L20.5 25.9L30.4 16L20.5 6.09998Z"/>
</svg>







  
  


</button>
</form>
</div>



            </div>
          
<div class='je2-listed-by js-listed-by '>

        <a href="/offices/real_estate/elite-group-real-estate-359439" data-type="internal-office-link">
    <img alt="ELITE GROUP Real Estate" class="je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/05/05/12/16/09/b5c8a2bb-244b-4c69-86ed-f507f830785f/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" src="" />
    </a>

<div class='je2-listed-by-info__office-info'>
    <div class="je2-listed-by-info__office-info__name">ELITE GROUP Real Estate</div>
        <div class="je2-listed-by-info__office-info__address">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M13.786 6.893c0 3.907-4.521 7.383-5.59 8.15a.852.852 0 0 1-.502.158.852.852 0 0 1-.502-.157c-1.069-.768-5.59-4.244-5.59-8.15a6.092 6.092 0 0 1 12.184 0Z" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /><path d="M5.477 6.338a2.215 2.215 0 1 0 4.43 0 2.215 2.215 0 0 0-4.43 0Z" stroke="#151515" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" /></svg>

            21 Avenue des maréchaux, 16000, Angoulême, France
        </div>

    <a href="/offices/real_estate/elite-group-real-estate-359439" class="je2-button je3-listing-listed-by-info__view-profile _link _noborder" target="_blank" aria-label="View agency profile">

  

    <span>
          View agency profile
    </span>




    <svg xmlns="http://www.w3.org/2000/svg" width="17" height="18" viewBox="0 0 17 18" fill="none"><path d="m4.188 13.477 8.485-8.486M13.144 12.066V4.523H5.602" stroke="#006C75" stroke-width="1.6" /></svg>


  


</a>
</div>

    <div class='je2-listed-by-info__description'>
        <div class="je2-read-more js-read-more _v2 _original" data-block="Office">

  <div class="je2-read-more__preview _translated"></div>
  <div class="je2-read-more__preview _original">ELITE GROUP Real Estate is a network of agencies and real estate professionals specializing in the luxury market, committed to providing clients with a tailor-made, exceptional service. Our mission is to manage, enhance, and sell prestigious properties with standards that surpass those of the market. Our clientele, composed of discerning buyers and investors, extends internationally, strengthening</div>

    <div class="je2-read-more__content _translated"></div>
    <div class="je2-read-more__content _original">ELITE GROUP Real Estate is a network of agencies and real estate professionals specializing in the luxury market, committed to providing clients with a tailor-made, exceptional service. Our mission is to manage, enhance, and sell prestigious properties with standards that surpass those of the market. Our clientele, composed of discerning buyers and investors, extends internationally, strengthening our position as a leader in luxury real estate.<br/><br/>Iconic sales and recognized expertise<br/>Our expertise is reflected in exceptional transactions, including sales exceeding €4 million, demonstrating our ability to handle high-end real estate projects and meet the most demanding expectations.<br/><br/>Experience at the heart of excellence<br/>We work exclusively with highly experienced agents and agencies, trained to deliver comprehensive, personalized expertise. This strategic choice ensures tailored guidance and flawless project management. Our professionals, renowned for their skill and rigor, guarantee optimal management and maximum value for every property, while providing impeccable client service.<br/><br/>ELITE GROUP Real Estate is more than a real estate network: it is the perfect combination of prestige, performance, and excellence, turning every project into a unique and memorable experience.</div>
    <div class="je2-read-more__expand js-expand">
      <span>…</span>
      <button class="je2-button je2-link" aria-expanded="false">

  

    <span>
          View more
    </span>




    <svg><use xlink:href="#short-arrow"></use></svg>

  


</button>
    </div>
    <div class="je2-read-more__collapse">
      <button class="je2-button je2-link js-collapse" aria-expanded="true">

  

    <span>
          View less
    </span>




    <svg><use xlink:href="#short-arrow"></use></svg>

  


</button>
    </div>
</div>

    </div>

<div class='je2-listed-by-info__info-blocks'>
        <div class='je2-listed-by-info__info-block'>
            <div class='je2-listed-by-info__info-block__label'>
                Last updated
            </div>
            <div class='je2-listed-by-info__info-block__value'>
                    Oct 20
            </div>
        </div>
        <div class='je2-listed-by-info__info-block'>
            <div class='je2-listed-by-info__info-block__label'>
                First listed
            </div>
            <div class='je2-listed-by-info__info-block__value'>
                    Oct 20
            </div>
        </div>
        <div class='je2-listed-by-info__info-block'>
            <div class='je2-listed-by-info__info-block__label'>
                Agent licence
            </div>
            <div class='je2-listed-by-info__info-block__value'>
                    #299
            </div>
        </div>
        <div class='je2-listed-by-info__info-block'>
            <div class='je2-listed-by-info__info-block__label'>
                Listing reference
            </div>
            <div class='je2-listed-by-info__info-block__value'>
                    478AB16
            </div>
        </div>
</div>



</div>

        </div>
      </div>


    </div>


      <aside class="je2-listing__inquiry">
        <div class="je2-inquiry js-inquiry  _v2">

  <div class="je2-agent-info _v2">
    <div class="je3-avatar ">
    <div class="je3-avatar__content">
        <div class="je3-avatar__mask"></div>
        <img class="je3-avatar__image je2-lazy-load" alt="Antoine BEAUDOU" data-src="https://img.jamesedition.com/agent_images/2025/05/05/09/56/36/b49713c4-1257-4f62-918b-053cc5df1dc9/je/80x80xc.jpg" />
        <img class="je3-avatar__blur-background je2-lazy-load" alt="Antoine BEAUDOU background" data-src="https://img.jamesedition.com/agent_images/2025/05/05/09/56/36/b49713c4-1257-4f62-918b-053cc5df1dc9/je/80x80xc.jpg" />
    </div>
</div>


  <div>
    <div class="je2-agent-info__name-and-rating">
      <p aria-label="Agent name">
          Antoine BEAUDOU
      </p>
      
    </div>
    <span>Joined 7 months ago</span>

  </div>

    <div class="je2-contact-agent-buttons">
      <form class="je2-phone-button" id="agent-info-phone">
  <div data-sitekey="6LeNK2caAAAAABqNVS2GtBowWgxSInPKc9XdX4PE" data-size="invisible"></div>

  <a href="#" class="je2-button js-phone-button _noborder js-phone-button" data-error="Try again later." data-missing-number-error="Currently unavailable" data-call-on-click="true" data-location="Inquiry" data-fetch-phone-numbers-url="/listings/16460690/fetch-phones-numbers" data-success-text1="Start phone call with:" data-success-text2="Hello, I&#39;m calling for the property with the reference 478AB16, which I discovered on JamesEdition." aria-label="Call Agent">
    <div class="je2-button__temporary"></div>

    <svg viewBox="0 0 16 16" >
  <path d="M4.35002 1.5C4.10002 1.5 3.85002 1.6 3.60002 1.75H3.55002L2.00002 3.4C1.50002 3.85 1.35002 4.5 1.60002 5.1C2.00002 6.3 3.10002 8.65 5.20002 10.75C7.30002 12.85 9.70002 13.9 10.85 14.35C11.45 14.55 12.1 14.4 12.6 14L14.2 12.4C14.6 12 14.6 11.25 14.2 10.85L12.15 8.8V8.75C11.75 8.35 11 8.35 10.6 8.75L9.60002 9.75C9.25002 9.6 8.40002 9.15 7.55002 8.35C6.75002 7.55 6.30002 6.65 6.15002 6.3L7.15002 5.3C7.55002 4.9 7.60002 4.2 7.15002 3.75L7.10002 3.7L5.10002 1.65H5.05002C4.85002 1.6 4.60002 1.5 4.35002 1.5Z"/>
</svg>



    <span>
          Call Agent
    </span>




  
  


</a>

  <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>


    <div class="js-success-text"></div>
</form>


    </div>
</div>


  <div class="je2-inquiry__form js-form-container">
    <form id="general-form" class="simple_form je2-form js-inquiry-form" novalidate="novalidate" action="/inquiries" accept-charset="UTF-8" method="post"><input type="hidden" name="authenticity_token" value="aBql9Dh56i4cQyxdYV5bgPkavAkQUeywsOf9skjIdugDDIYkywIgwA_gxE2cwPXcYPisdp-xAB9j8EpJ6R7DMg" autocomplete="off" />
  <div data-sitekey="6LeNK2caAAAAABqNVS2GtBowWgxSInPKc9XdX4PE" data-size="invisible"></div>
  <input value="1" autocomplete="off" type="hidden" name="inquiry_type" id="inquiry_type" />
  <input value="16460690" autocomplete="off" type="hidden" name="subject_id" id="subject_id" />
  <input value="eyJ1dG1fbWVkaXVtIjoiZGlyZWN0IiwidXRtX3NvdXJjZSI6ImRpcmVjdCJ9
" autocomplete="off" type="hidden" name="je_utm" id="je_utm" />
  <input value="eyJpc19hdXRoZW50aWNhdGVkIjoiTm8iLCJvZmZpY2VfaWQiOjM1OTQzOSwi
YWdlbnRfaWQiOjE3Mjg4NTksImxpc3RpbmdfaWQiOjE2NDYwNjkwLCJjb3Vu
dHJ5IjoiRnJhbmNlIiwiY2l0eSI6IkFuZ291bMOqbWUiLCJwYWdlX3R5cGUi
OiJMaXN0aW5nIiwiY2F0ZWdvcnkiOiJyZWFsX2VzdGF0ZSIsImxpc3Rpbmdf
cHJpY2UiOiI2Njc4MDAuMDAiLCJzZWN0aW9uIjoiRm9yIHNhbGUiLCJzdWJf
c2VjdGlvbiI6IlJlYWxFc3RhdGUiLCJwbGFjZV9pZCI6OTcwMDgsInN1YnNj
cmlwdGlvbiI6ImVsaXRlX3BsdXMifQ==
" autocomplete="off" type="hidden" name="je_session" id="je_session" />
  <input class="js-country-code" autocomplete="off" type="hidden" name="country_code" id="country_code" />
  <input class="js-dial-code" autocomplete="off" type="hidden" name="dial_code" id="dial_code" />
  <input value="general_form" autocomplete="off" type="hidden" name="source" id="source" />

      <div class="je2-inquiry__field">
    <input class="je2-input" type="text" placeholder="Your name" name="name"
           value="" aria-label="Name" autocapitalize="none"
           data-invalid-error="Invalid characters used. Check your name"
           autocorrect="off" autocomplete="name" spellcheck="false" required
           data-required-error="Enter your name">
  </div>

  <div class="je2-inquiry__field je2-input__container">
    <input class="je2-input "
           
           type="email" placeholder="Your email address"
           name="email" value=""
           autocomplete="email"
           aria-label="Email" autocapitalize="none" autocorrect="off" spellcheck="false" required
           data-required-error="Enter your email address"
           data-invalid-error="Check your email address">
  </div>

  <div class="je2-inquiry__field">
    <input class="je2-input" type="tel"
           placeholder="Phone number (optional)"
           name="phone" value="" aria-label="Phone"
           autocomplete="phone" 
           data-required-error="This agent requires a phone number for inquiries"
           data-invalid-error="Check your phone number">
  </div>


    <div class="je2-inquiry__field">
        <div>Your message</div>
      <textarea class="je2-input" name="message" rows="3" aria-label="Message"
                data-required-error="Enter your message"
                data-too-long-error="The message is too long"
                data-max-length="400"
                placeholder="Ask the seller for more information about this property..."
                required>Please contact me regarding LUXURY FAMILY ESTATE WITH HEATED POOL AND OUTBUILDINGS IN VARS, NEAR ANGOULEME</textarea>
    </div>

  <div class="js-error-message"></div>

  <div class="je2-inquiry__submit">
    <button class="je2-button _cyan" type="submit">
      <span>Send message</span>
      <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>

    </button>
  </div>

    <div class="je2-inquiry__checkbox">
      <label class="je2-checkbox
        js-checkbox
         
        ">
  <input type="checkbox" name="save_search" checked="checked" />
    <span class="je2-checkbox__icon">
      <svg><use xlink:href="#check"></use></svg>
    </span>
  <span class="je2-checkbox__text"
    
    >
    Notify me via email when similar listings appear
  </span>
</label>

    </div>

  <div class="je2-inquiry__checkbox">
    <label class="je2-checkbox
        js-checkbox
          _required
        ">
  <input type="checkbox" name="terms" required="required" data-required-error="You must accept the Terms to send your message" checked="checked" />
    <span class="je2-checkbox__icon">
      <svg><use xlink:href="#check"></use></svg>
    </span>
  <span class="je2-checkbox__text"
    
    >
    I agree to <a href="/about/terms-of-use" target="_blank" class="je2-link">Terms of Use</a> and <a href="/about/privacy-policy" target="_blank" class="je2-link">Privacy Policy</a>, including sharing my activity and interests with the seller
  </span>
</label>

  </div>

</form>
  <div class="je2-inquiry__already-sent">
  <svg width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="1" width="50" height="50" rx="25" fill="white" />
  <rect x="1" y="1" width="50" height="50" rx="25" stroke="#006C75" stroke-width="2" />
  <path d="M16.7144 28.2144L20.6144 33.2286C20.746 33.3996 20.9146 33.5386 21.1076 33.6351C21.3006 33.7316 21.5129 33.7831 21.7286 33.7858C21.9409 33.7882 22.1511 33.7434 22.3438 33.6544C22.5366 33.5654 22.7071 33.4346 22.8429 33.2715L35.2858 18.2144" stroke="#006C75" stroke-width="1.6" />
</svg>


  <span>You have inquired about this property</span>

  <p>
    The agent will contact you soon by
    <span class="js-sent-email"></span>

    <span class="js-sent-phone" data-or="or">
      </span>
  </p>

  <div></div>

  <button class="je2-link js-send-another">
    Send another message
  </button>
</div>


  </div>

</div>

      </aside>

  </div>

  <div class="je2-listing__bottom-bar">
    

<div class="je2-listing-bottom-bar js-listing-bottom-bar _plain-text _floating-buttons-with-copies">
    <button class="je2-button _cyan _uppercase js-message je2-listing-bottom-bar__message" data-name="Bottom bar">

  

    <span>
          Message
    </span>




  
  


</button>
    <form class="je2-phone-button" id="bottom-bar-phone">
  <div data-sitekey="6LeNK2caAAAAABqNVS2GtBowWgxSInPKc9XdX4PE" data-size="invisible"></div>

  <a href="#" class="je2-button js-phone-button _uppercase _cyan js-phone-button" data-error="Try again later." data-missing-number-error="Currently unavailable" data-call-on-click="true" data-location="Bottom bar" data-fetch-phone-numbers-url="/listings/16460690/fetch-phones-numbers" data-success-text1="Start phone call with:" data-success-text2="Hello, I&#39;m calling for the property with the reference 478AB16, which I discovered on JamesEdition." aria-label="Click to call">
    <div class="je2-button__temporary"></div>

  

    <span>
          Call
    </span>




  
  


</a>

  <div class="je3-spinner js-spinner ">
    <div></div>
    <div></div>
    <div></div>
</div>


</form>


</div>

  </div>

  <div class="je2-listing__footer">

    <div class="je2-listing__section _similar-homes" id="similar-homes">
      <h2>Similar Properties Nearby</h2>
      
<div class="js-you-might-like">
    <div class="je2-slider _alt fit-parent grid-align" data-items-count="3">
      <div class="je2-slider__wrapper">
        <div class="je2-slider__content">
            <div class="je2-slider__item-3">
              <div class="ListingCard _fit-parent _initialized">
                <div class="ListingCard__picture _loading"></div>
                <p>&nbsp;</p>
                <p>&nbsp;</p>
                <p>&nbsp;</p>
              </div>
            </div>
            <div class="je2-slider__item-3">
              <div class="ListingCard _fit-parent _initialized">
                <div class="ListingCard__picture _loading"></div>
                <p>&nbsp;</p>
                <p>&nbsp;</p>
                <p>&nbsp;</p>
              </div>
            </div>
            <div class="je2-slider__item-3">
              <div class="ListingCard _fit-parent _initialized">
                <div class="ListingCard__picture _loading"></div>
                <p>&nbsp;</p>
                <p>&nbsp;</p>
                <p>&nbsp;</p>
              </div>
            </div>
        </div>
      </div>
    </div>
</div>

    </div>

      <div class="je2-listing__section _new-listings">
        <h2>New Listings in Angoulême</h2>
        <div class="je2-new-listings js-new-listings">
          
<div>

  
<div class="je2-slider js-je2-slider _alt fit-parent grid-align collapsed no-title"
     data-slider-config="{&quot;showDots&quot;:false,&quot;paged&quot;:true,&quot;mobilePaged&quot;:null}"
     data-items-count="3">

  <div class="je2-slider__wrapper">
    <div class="je2-slider__content">
              <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16742059" data-price-usd="849427" data-price-euro="729000" data-price="729000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="107706" data-agent-id="1189584" data-category="RealEstate" data-lat="45.6323344" data-lng="0.1553345" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/angouleme-france/bright-architect-designed-house-enclosed-wooded-grounds-quiet-wooded-setting-10-minutes-from-ango-16742059" title="Bright architect-designed house, enclosed wooded grounds, quiet wooded setting, 10 minutes from Ango" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16742059">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 10
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 10 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/c09a1da0-db11-4219-b903-42d8e60e4bfe/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/76805875-6ebc-412c-bd7b-5daad8bf281b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/43804060-248b-4412-9dd7-ed059d819b42/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/341bc920-0fd4-4b27-b035-28a149de4fa5/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/8339ca71-a43a-4b2d-abf5-1e8099b21584/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/ef78a593-aaa5-4f8b-b1df-614cc3a1f35d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/b5e42808-f1a0-4819-9eaf-dbcb5cfa5ad4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/9968a88c-073c-4547-94c1-255407c5fd88/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/e8b08290-56ed-4e61-b702-9fc8b5ed8ec8/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/12/03/17/10/46/c276e94f-054a-4266-9f89-6f3b11e4e019/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €729,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">5 Beds</span>
    <span class="ListingCard__tag">3 Baths</span>
    <span class="ListingCard__tag">270 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "3",
        "numberOfBedrooms": "5",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  
</div>
      </div>
      <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16667511" data-price-usd="2306970" data-price-euro="1979900" data-price="1979900" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="219883" data-agent-id="1497423" data-group-id="395" data-category="RealEstate" data-lat="45.64402" data-lng="0.14841" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/angouleme-france/an-authentic-and-self-sufficient-hamlet-at-the-gateway-to-the-perigord-vert-16667511" title="An Authentic and Self-Sufficient Hamlet at the Gateway to the Périgord Vert" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16667511">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 22
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 22 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/215fc2c3-6edf-4004-a40b-e2e9cf69ac2e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/aefc1113-2567-41ed-8b83-8891456d1b3a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/2d422d58-1f24-435e-b311-394fe6754f21/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/44ff4bd6-5e5c-498d-acda-8493acaee5c3/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/d31243ae-47fd-407d-942b-e1b832a44103/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/17f29456-9b65-44a5-8e0e-f1449da4ccfd/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/cd3244dc-7d95-4fe7-b99e-f0c213da306a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/3cbb8814-cbc4-408c-b5dd-22019027e1bc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/1c9bd030-a44e-4460-8259-f162f39feb1a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/11/20/12/53/15/391398dd-7765-403c-8ab3-c7087ed155d6/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,979,900
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">17 Beds</span>
    <span class="ListingCard__tag">13 Baths</span>
    <span class="ListingCard__tag">1225 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "13",
        "numberOfBedrooms": "17",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  <a href="/offices/real_estate/maxwell-baynes-residential-and-vineyards-christie-s-international-real-estate-219883" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_logos/2025/12/06/10/12/55/9e52b44e-19ad-46d1-99d0-a31741089e61/je/320x160xs.jpg" data-type="office_logo" data-watermark="true" alt="Maxwell-Baynes Residential and Vineyards - Christie&#39;s International Real Estate" src="" />

      <div class="ListingCard__footer__agent">Olivier Demessemakers</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/09/44/23b4cfa0-5ed0-4635-9874-bcd8c59f0fb7/je/80x80xc.jpg" alt="Olivier Demessemakers photo" src="" />
  </div>
</a>
</div>
      </div>
      <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16623379" data-price-usd="637362" data-price-euro="547000" data-price="547000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="465438" data-agent-id="1960902" data-group-id="2771" data-category="RealEstate" data-lat="45.647372131" data-lng="0.145140856" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/angouleme-france/angouleme-center-prefecture-district-character-home-of-approximately-200m-with-terrace-and-garage-16623379" title="ANGOULEME CENTER: Prefecture district, character home of approximately 200m² with terrace and garage" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16623379">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 15
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 15 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/95faa1fd-ae47-4b02-843b-46a67e393c1c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/5dcb093a-394e-4936-bf51-8a5e8397a919/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/76d5c379-d950-4c5a-950a-3dee14e848d7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/c22224e3-900b-4c43-9637-dca92cb81f07/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/de15270f-9fde-4ea4-a407-b3c9b9317a36/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/dcb26106-ed92-4e0e-8ca0-4b1745dc61db/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/5c1b7e73-b078-41d7-add3-427feb7784dc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/a211098f-ad45-42ad-8ab4-212b22671df2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/bc972f78-d8da-4f05-823a-c3f797bd3a63/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/23/1ce02c74-7e1e-4426-beba-9b4c230af51c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €547,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">4 Beds</span>
    <span class="ListingCard__tag">197 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "",
        "numberOfBedrooms": "4",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  
</div>
      </div>
      <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16623220" data-price-usd="3180984" data-price-euro="2730000" data-price="2730000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="219883" data-agent-id="1497423" data-group-id="395" data-category="RealEstate" data-lat="45.64402" data-lng="0.14841" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/angouleme-france/extraordinary-estate-5-minutes-from-angouleme-16623220" title="Extraordinary Estate 5 Minutes from Angoulême" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16623220">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 60
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 60 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/0ecdb866-5f09-4111-9270-e3c6514e044b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/fa335782-8269-443f-a571-b0fd7ef8a4d9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/d46b8be5-3774-46e1-9bf3-8806db8fda51/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/40162539-a7e6-4cd6-92cc-67efbde43d73/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/0118ba19-8160-4b02-8b8f-922438429288/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/e224b4be-9b66-4216-a267-b4a2ec5f7692/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/b80234aa-e7c9-448b-9075-9d2d2ddfb460/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/b72a77f7-1732-46ee-93e4-75ae1770a4ae/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/3b8c9c89-d64f-419c-a2ce-1ae265cf5af2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/11/13/15/19/21/26736d49-36a8-4456-ac62-1b20a1922bd2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €2,730,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">13 Beds</span>
    <span class="ListingCard__tag">10 Baths</span>
    <span class="ListingCard__tag">700 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "10",
        "numberOfBedrooms": "13",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  <a href="/offices/real_estate/maxwell-baynes-residential-and-vineyards-christie-s-international-real-estate-219883" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_logos/2025/12/06/10/12/55/9e52b44e-19ad-46d1-99d0-a31741089e61/je/320x160xs.jpg" data-type="office_logo" data-watermark="true" alt="Maxwell-Baynes Residential and Vineyards - Christie&#39;s International Real Estate" src="" />

      <div class="ListingCard__footer__agent">Olivier Demessemakers</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/09/44/23b4cfa0-5ed0-4635-9874-bcd8c59f0fb7/je/80x80xc.jpg" alt="Olivier Demessemakers photo" src="" />
  </div>
</a>
</div>
      </div>
      <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16546438" data-price-usd="5825978" data-price-euro="5000000" data-price="5000000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="339112" data-agent-id="1790938" data-group-id="395" data-category="RealEstate" data-lat="45.62918" data-lng="0.18001" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/chantilly-france/chateau-chantilly-481-0-sqm-6-bedrooms-16546438" title="Château - Chantilly - 481.0 sqm - 6 bedrooms" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16546438">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="8">1</span> / 8
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 8 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="Castle in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/90361653-9eb8-4f3d-a534-55edff9c3ab4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="Castle in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/4063e242-fd64-4468-b2e1-d7e80164afbf/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Castle in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/489ff333-343b-40d2-b55f-f6ebd6f4119e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Castle in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/3841eeec-256b-4616-846e-d3e543483f16/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Castle in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/034028ab-d7d4-45c8-979f-19cb36e3054b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Castle in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/c8a00f8f-9b33-4e60-afc6-9e4a9b7b8ee3/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Castle in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/da33663f-b72f-455d-86e2-f7c511d2a962/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="Castle in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/31/14/17/36/9ff57b3a-d30e-41db-80b9-951b50ef3c74/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €5,000,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">6 Beds</span>
    <span class="ListingCard__tag">7 Baths</span>
    <span class="ListingCard__tag">481 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "Castle",
        "numberOfBathroomsTotal": "7",
        "numberOfBedrooms": "6",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          Castle<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  <a href="/offices/real_estate/junot-chateaux-patrimoine-339112" target="_blank" class="js-office">
  <div class="ListingCard__footer">
      <img width="97" height="40" class="ListingCard__footer__office je2-lazy-load" data-src="https://img.jamesedition.com/dealer_listings_logos/2025/11/14/14/11/41/2e908460-36e7-438f-a41a-0f9d7b85a062/je/192x80xs.jpg" data-type="office_logo" data-watermark="true" alt="Junot Châteaux &amp; Patrimoine" src="" />

      <div class="ListingCard__footer__agent">Olivier De hauteclocque</div>
        <img class="ListingCard__footer__icon je2-lazy-load" data-src="https://img.jamesedition.com/agent_images/2025/08/07/17/15/56/acb8b4fc-2a42-4779-bee1-b4c7975aa615/je/80x80xc.jpg" alt="Olivier De hauteclocque photo" src="" />
  </div>
</a>
</div>
      </div>
      <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16498241" data-price-usd="559293" data-price-euro="480000" data-price="480000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="465438" data-agent-id="1960902" data-group-id="2771" data-category="RealEstate" data-lat="45.6510794" data-lng="0.1590747" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/angouleme-france/18km-angouleme-beautifully-renovated-house-annex-outbuildings-on-a-lovely-plot-of-land-with-pool-16498241" title="18KM ANGOULEME Beautifully renovated house + annex, outbuildings on a lovely plot of land with pool" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16498241">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 16
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 16 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/c03b5531-d657-4845-8b88-66372711ca70/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/42d0fdc4-d490-49a9-abf6-d193ce4d4c54/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/a83771cd-8b6a-4753-98cf-97cb18934ff6/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/6e30ba19-d19d-4da7-875e-71b24c9f7aad/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/4ebdda9b-94b6-4e37-9d12-c456e9fd6787/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/a12c6aad-8b89-417b-869e-3832141a71e7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/8cc78953-abcd-48c1-a640-4c266b4fb863/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/f25b01ca-bba5-4461-b345-222e577f40b4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/aab0e3c6-0325-45d4-9c24-d3ab4098da2e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/05a515fa-a6f8-4002-b373-401edfcc6967/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €480,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">6 Beds</span>
    <span class="ListingCard__tag">313 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "",
        "numberOfBedrooms": "6",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  
</div>
      </div>
      <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16498216" data-price-usd="1514754" data-price-euro="1300000" data-price="1300000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="465438" data-agent-id="1960902" data-group-id="2771" data-category="RealEstate" data-lat="45.647372131" data-lng="0.145140856" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/angouleme-france/angouleme-plateau-elegant-townhouse-in-a-remarkable-location-16498216" title="ANGOULEME PLATEAU: ELEGANT TOWNHOUSE IN A REMARKABLE LOCATION!" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16498216">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 14
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 14 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/70f59eb9-6782-4b72-9dfe-1a79dbd62815/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/bff5dd5f-022d-40f0-a2fb-7c10934a5d1c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/f830e72d-2765-4827-b67b-b6d2cd12e268/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/776456c5-6299-49ed-8b48-5be228b34256/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/cdf6d1c4-6fe9-4caf-9dc4-84323cfb44f4/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/30b6e81b-467a-4109-9846-2bdbad44d32e/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/24f1e108-b0d8-4879-bf8d-8e8a226e41c7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/9e3a90e6-cd9d-4ab4-8190-712bb2477de1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/3e36c4eb-6c66-4eaa-b2af-64ab895d1d62/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/4327e812-7744-42b8-aa00-31bdf40d479d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €1,300,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">6 Beds</span>
    <span class="ListingCard__tag">3 Baths</span>
    <span class="ListingCard__tag">504 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "3",
        "numberOfBedrooms": "6",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  
</div>
      </div>
      <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16498147" data-price-usd="917008" data-price-euro="787000" data-price="787000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="465438" data-agent-id="1960902" data-group-id="2771" data-category="RealEstate" data-lat="45.647372131" data-lng="0.145140856" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/angouleme-france/exceptional-angouleme-plateau-townhouse-with-garage-and-garden-16498147" title="EXCEPTIONAL ANGOULEME PLATEAU! Townhouse with garage and garden." target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16498147">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="8">1</span> / 8
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 8 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/09078039-ff9a-437d-96d6-9527096b799f/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/5cc526e1-62b3-4353-a9b4-80f103802c4f/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/eced9785-fa49-4f7e-9a21-e2b455e37565/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/3881ec18-746e-4684-9312-984bd99c99e1/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/9ddf2129-2cc9-4f90-8a68-188636a7beaa/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/ee748567-4fcf-48b2-8e16-87d27cd1a5c5/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/b9bcc167-0486-4d95-ae0c-d2a583640dd5/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/5f9a21f8-d800-476d-8002-fd5babcef9a5/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €787,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">13 Beds</span>
    <span class="ListingCard__tag">4 Baths</span>
    <span class="ListingCard__tag">524 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "4",
        "numberOfBedrooms": "13",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  
</div>
      </div>
      <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16498092" data-price-usd="576771" data-price-euro="495000" data-price="495000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="465438" data-agent-id="1960902" data-group-id="2771" data-category="RealEstate" data-lat="45.65" data-lng="0.159" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/angouleme-france/at-the-gates-of-angouleme-amenities-nearby-beautiful-charentaise-house-with-pool-and-park-16498092" title="AT THE GATES OF ANGOULEME, amenities nearby, beautiful Charentaise house with pool and park" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16498092">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 10
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 10 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/28ed6d1d-0f75-4b97-9fef-826b98f154e7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/e5411d53-5a09-4de8-a97e-716d180d0b60/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/97bb3bf3-842b-40a4-be26-dab66d2c9b36/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/efc366df-5eff-4bca-ac6e-080de2786dd7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/bbb90b00-0a4e-430f-9615-407dc46199f2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/95a964d9-258a-4f36-a9ef-5710ed10b25d/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/ad70d86c-f1e7-45dc-9dcc-092eab8b7720/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/c54df037-2ac9-4304-9510-fced36c9f39b/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/56f01dce-5a45-4f38-b7c5-1f7d72a0f7a7/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/396aed4e-07e4-40f2-b031-d83cc830d8a9/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €495,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">6 Beds</span>
    <span class="ListingCard__tag">1 Baths</span>
    <span class="ListingCard__tag">324 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "1",
        "numberOfBedrooms": "6",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  
</div>
      </div>
      <div class="je2-slider__item-3">
        <div class="ListingCard _fit-parent" data-id="16497544" data-price-usd="669987" data-price-euro="575000" data-price="575000" data-currency="EUR" data-country-code="FR" data-country="France" data-city="Angoulême" data-office-id="465438" data-agent-id="1960902" data-group-id="2771" data-category="RealEstate" data-lat="45.65" data-lng="0.1667" data-location="Listing page" data-position="New listings" data-type="Listing card">
  <a href="/real_estate/angouleme-france/country-property-west-of-angouleme-16497544" title="Country Property West of Angoulême" target="_blank" class="js-link">

    

    <div class="ListingCard__save js-heart " data-listing-id="16497544">
      <svg><use xlink:href="#white-heart"></use></svg>
    </div>

    <div class="ListingCard__picture">
        <div class="je2-single-slider js-single-slider js-listing-gallery">
  <div class="je2-single-slider__navigation">
      <div class="je2-single-slider__left js-left"><svg><use xlink:href="#arrow-left"></use></svg></div>
      <div class="je2-single-slider__images-count">
        <span>
          <span class="js-current-images-index" data-total="10">1</span> / 10
        </span>
      </div>
      <div class="je2-single-slider__right js-right"><svg><use xlink:href="#arrow-right"></use></svg></div>
    <div class="je2-single-slider__show-more js-show-more">
      <div class="je2-single-slider__show-more-button">
        View 10 photos
      </div>
    </div>
  </div>
  <div class="je2-single-slider__slides js-single-slides">
       <div class="je-background-pixel"> 
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 1" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/f469fb60-a181-4e7f-988f-aaa6e67fbe29/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
       </div> 
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 2" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/a6881a75-9985-4fcb-8a2d-7e90c2420adc/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 3" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/6f9e8caa-153a-4576-a817-f0c1ca799ca6/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 4" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/e9d955ca-a84e-499b-b2c9-6b34d74c0cc6/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 5" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/fdab66ca-93af-4afb-bffb-5d62c5fd892c/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 6" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/5c2e0049-b123-4b23-9eca-4c5464afc4dd/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 7" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/219d9e7c-9991-46de-bb06-892b5ae4b3f2/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 8" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/04922ef9-8a71-4408-9368-0f0f5c26bd53/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 9" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/18ceb82d-fda4-428d-87c9-042eb1a58a94/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
      
        <div class="je2-lazy-load" alt="House in Angoulême, Nouvelle-Aquitaine, France 10" data-src="https://img.jamesedition.com/listing_images/2025/10/27/15/22/06/b6b11684-ba09-46ed-a233-e689a9d2db7a/je/507x312xc.jpg" data-type="card_horizontal" data-watermark="true"></div>
      
  </div>
</div>

    </div>

    <div class="ListingCard__description">
      <div class="ListingCard__price">
          €575,000
      </div>


        <div class="ListingCard__tags">
    <span class="ListingCard__tag">8 Beds</span>
    <span class="ListingCard__tag">2 Baths</span>
    <span class="ListingCard__tag">334 sqm</span>
</div>
<script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "House",
        "accommodationCategory": "House",
        "numberOfBathroomsTotal": "2",
        "numberOfBedrooms": "8",
        "address": "Angoulême, Nouvelle-Aquitaine, France"
    }
</script>


      <div class="ListingCard__title">
          House<span> in </span>Angoulême, Nouvelle-Aquitaine, France
      </div>


      <div class="ListingCard__actions">
      </div>

    </div>

</a>
  
</div>
      </div>

    </div>
  </div>

    <div class="je2-slider__navigation">

        <div class="je2-slider__scroll left">
          <svg><use xlink:href="#short-arrow"></use></svg>
        </div>
        <div class="je2-slider__scroll right">
          <svg><use xlink:href="#short-arrow"></use></svg>
        </div>
    </div>
</div>

</div>

          <button class="je2-button je2-button je2-link js-view-all" data-url="/real_estate/angouleme-france?order=recent" data-location="Angoulême">

  

    <span>
          View all new listings in Angoulême
    </span>




  
  


</button>
        </div>
      </div>


      <div class="je2-listing__section _explore-more-homes">
        <h2>Explore More Homes for Sale</h2>
        
<div class="je2-popular-links">

  <div class="je2-popular-links__grid _2">

      <div class="je2-popular-links__section">
        <input id="group-0" class="je2-popular-links__toggle" type="checkbox" />

          <h3 class="je2-popular-links__label">
            <span>
                Angoulême, France property types
            </span>
</h3>
        <ul class="je2-popular-links__list" id="je-group-0">
          <li>
                <a target="_blank" href="/real_estate/house-angouleme-france"><strong>Houses</strong> for sale in Angoulême, France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/castle-angouleme-france"><strong>Castles</strong> for sale in Angoulême, France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/estate-angouleme-france"><strong>Estates</strong> for sale in Angoulême, France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/farm_ranch-angouleme-france"><strong>Farm Ranches</strong> for sale in Angoulême, France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/villa-angouleme-france"><strong>Villas</strong> for sale in Angoulême, France</a>
          </li>
        </ul>

        <label class="je2-popular-links__more" for="group-0">
          <div class="je2-popular-links__more-open">Show all</div>
          <div class="je2-popular-links__more-close">Show less</div>
          <svg><use xlink:href="#short-arrow"></use></svg>
</label>      </div>

      <div class="je2-popular-links__section">
        <input id="group-1" class="je2-popular-links__toggle" type="checkbox" />

          <h3 class="je2-popular-links__label">
            <span>
                Angoulême, France popular searches
            </span>
</h3>
        <ul class="je2-popular-links__list" id="je-group-1">
          <li>
                <button class="je2-button je2-button _noborder js-popular-link-button" data-url="/real_estate/angouleme-france?order=recent">

  

    <span>
          Newest homes for sale in Angoulême, France
    </span>




  
  


</button>
          </li>
          <li>
                <a target="_blank" href="/real_estate/pool--angouleme-france"><strong>Properties with Pool</strong> in Angoulême, France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/river-view--angouleme-france"><strong>River View properties</strong> in Angoulême, France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/duplex--angouleme-france"><strong>Duplex properties</strong> in Angoulême, France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/lake-view--angouleme-france"><strong>Lake View properties</strong> in Angoulême, France</a>
          </li>
          <li>
                <a target="_blank" href="/real_estate/riverfront--angouleme-france"><strong>Riverfront properties</strong> in Angoulême, France</a>
          </li>
        </ul>

        <label class="je2-popular-links__more" for="group-1">
          <div class="je2-popular-links__more-open">Show all</div>
          <div class="je2-popular-links__more-close">Show less</div>
          <svg><use xlink:href="#short-arrow"></use></svg>
</label>      </div>
  </div>
</div>

      </div>


    <div class="je2-listing__section">
      
<div class="je2-journal js-journal">
  <h2 class="je2-texts__heading-34">Related Guides &amp; Stories</h2>

        
<div class="je2-slider js-je2-slider _alt fit-parent grid-align collapsed no-title"
     data-slider-config="{&quot;showDots&quot;:false,&quot;paged&quot;:true,&quot;mobilePaged&quot;:null}"
     data-items-count="3">

  <div class="je2-slider__wrapper">
    <div class="je2-slider__content">
                    <div class="je2-slider__item-3">
              <div class="je2-journal__article-v2 _empty">
                <div class="je2-journal__article-v2-image"></div>
                <div class="je2-journal__article-v2-content">
                  <div class="je2-journal__article-v2-date"></div>
                  <div class="je2-journal__article-v2-title"></div>
                </div>
                <div class="je2-journal__article-v2-button"></div>
              </div>
            </div>
            <div class="je2-slider__item-3">
              <div class="je2-journal__article-v2 _empty">
                <div class="je2-journal__article-v2-image"></div>
                <div class="je2-journal__article-v2-content">
                  <div class="je2-journal__article-v2-date"></div>
                  <div class="je2-journal__article-v2-title"></div>
                </div>
                <div class="je2-journal__article-v2-button"></div>
              </div>
            </div>
            <div class="je2-slider__item-3">
              <div class="je2-journal__article-v2 _empty">
                <div class="je2-journal__article-v2-image"></div>
                <div class="je2-journal__article-v2-content">
                  <div class="je2-journal__article-v2-date"></div>
                  <div class="je2-journal__article-v2-title"></div>
                </div>
                <div class="je2-journal__article-v2-button"></div>
              </div>
            </div>

    </div>
  </div>

    <div class="je2-slider__navigation">

        <div class="je2-slider__scroll left">
          <svg><use xlink:href="#short-arrow"></use></svg>
        </div>
        <div class="je2-slider__scroll right">
          <svg><use xlink:href="#short-arrow"></use></svg>
        </div>
    </div>
</div>



</div>

    </div>

  </div>


  
</main>




<script type="application/ld+json">{"@context":"https://schema.org","@type":"Product","url":"https://www.jamesedition.com/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690","name":"LUXURY FAMILY ESTATE WITH HEATED POOL AND OUTBUILDINGS IN VARS, NEAR ANGOULEME","description":"ELITE GROUP Real Estate is delighted to present this magnificent family estate, a true haven of peace, located in the sought-after commune of Vars, just a few minutes from Angoulême.\n\nWith approximately 256 m² of living space, this home boasts generous volumes and is set within a serene, verdant environment, featuring a landscaped and fenced garden of over 1,700 m², a large heated saltwater pool, and numerous outbuildings, combining authentic charm with modern comfort.\n\nMain House:\n\nGround Floor:\nA refined entrance leads to an exceptional 50 m² living area, bathed in natural light thanks to its south-facing exposure, highlighted by an elegant fireplace. The high-end, fully equipped kitchen offers direct access to a traditional vaulted cellar, perfectly blending authenticity and prestige.\n\nFirst Floor:\nTwo bedrooms with built-in wardrobes, a stylish shower room, and a private master area featuring a bedroom opening onto a terrace, a large dressing room, and a luxurious bathroom with shower, bathtub, and WC.\n\nTop Floor:\nA spacious bedroom with storage, as well as an attic easily convertible into additional living space or used for storage.\n\nOutdoor Features:\n\nTwo garages and ample parking\n\n70 m² outbuilding\n\n42 m² barn\n\nSummer kitchen\n\nSecond outbuilding suitable for a guest house\n\nBoiler room with gas heating and thermodynamic water heater\n\nThe heated saltwater pool (11x5 m) with an integrated safety cover, the well, and the automatic irrigation system complete this property, offering elegant and functional outdoor spaces.\n\nComfort and Premium Features:\n\nGas heating\n\nThermodynamic water heater\n\nDouble-glazed PVC windows\n\nFiber optic internet\n\nElectric gate and wooden shutters\n\nSolar panels for hot water production\n\nThis rare property combines refinement, functionality, and authenticity, offering an exceptional lifestyle for a family seeking serenity, space, and absolute comfort.\n\nContact ELITE GROUP Real Estate today to schedule a private visit and discover this outstanding property, where every detail has been thoughtfully designed.","image":"https://img.jamesedition.com/listing_images/2025/10/20/12/27/22/77ecfea9-54b0-4cd6-ad13-98ba2f21f06e/je/1040x620xc.jpg","category":"RealEstate","offers":{"@type":"Offer","availability":"https://schema.org/InStock","priceCurrency":"EUR","price":667800.0,"seller":{"@type":"Organization","name":"ELITE GROUP Real Estate"}}}</script>

          

<div class="je2-newsletter js-newsletter _listing_page_v3_p3" id="newsletter" style="min-height: 250px">
</div>


          

          
<div class="je2-footer ">
  <div class="je2-footer__top">
    <div class="je2-footer__menu">
      <div class="je2-footer__menu-section">
        <div class="je2-footer__label">JAMESEDITION</div>
        <ul class="js-foooter-submenu">
          <li><a href="https://www.jamesedition.com/about">About</a></li>
          <li><a href="https://help.jamesedition.com/en/" class="js-intercom-show-message">Contact</a></li>
          <li><a href="https://careers.jamesedition.com">Careers</a></li>
          <li><a href="https://help.jamesedition.com/en/">Help &amp; FAQ</a></li>
          <li><a href="https://www.jamesedition.com/about/terms-of-use">Terms</a></li>
          <li><a href="https://www.jamesedition.com/about/privacy-policy">Privacy</a></li>
        </ul>
      </div>
      <div class="je2-footer__menu-section">
        <div class="je2-footer__label">CATEGORIES</div>
        <ul class="js-foooter-submenu">
          <li><a href="https://www.jamesedition.com/real_estate">Real Estate</a></li>
          <li><a href="https://www.jamesedition.com/cars">Cars</a></li>
          <li><a href="https://www.jamesedition.com/yachts">Yachts</a></li>
          <li><a href="https://www.jamesedition.com/jets">Jets</a></li>
          <li><a href="https://www.jamesedition.com/helicopters">Helicopters</a></li>
          <li><a href="https://www.jamesedition.com/watches">Watches</a></li>
          <li><a href="https://www.jamesedition.com/jewelry">Jewelry</a></li>
          <li><a href="https://www.jamesedition.com/extraordinaire">Extraordinaire</a></li>
          <li><a href="https://www.jamesedition.com/lifestyle-collectibles">Lifestyle</a></li>
        </ul>
      </div>
      <div class="je2-footer__menu-section">
        <div class="je2-footer__label">CATALOG</div>
        <ul class="js-foooter-submenu">
          <li><a href="https://www.jamesedition.com/brands">All Brands</a></li>
          <li><a href="https://www.jamesedition.com/offices">All Businesses</a></li>
        </ul>
      </div>
      <div class="je2-footer__menu-section">
        <div class="je2-footer__label">FOR BUSINESS</div>
        <ul class="js-foooter-submenu">
          <li><a href="/professional_seller">
            Sell With Us
          </a></li>
          <li><a href="mailto:marketing@jamesedition.com">Partner</a></li>
          <li><a href="/widgets">Linking</a></li>
        </ul>
      </div>
        <div class="je2-footer__qr">
          <div class="je2-footer__label">MOBILE APP</div>
          <div class="je2-footer__qr__content">
            <svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" fill="none">
    <path fill="#fff" d="M96 0H0v96h96V0Z" />
    <path fill="#000" d="M5.1885 5.1891H7.783v2.5946H5.1885V5.1892Zm2.5946 0h2.5946v2.5946H7.7831V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5945v2.5946h-2.5945V5.1892Zm2.5945 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946H20.756V5.1892Zm7.7838 0h2.5946v2.5946h-2.5946V5.1892Zm10.3784 0h2.5946v2.5946h-2.5946V5.1892Zm10.3784 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946H59.675V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5945v2.5946h-2.5945V5.1892Zm7.7837 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892Zm2.5946 0h2.5946v2.5946h-2.5946V5.1892ZM5.1885 7.7837H7.783v2.5946H5.1885V7.7837Zm15.5675 0h2.5946v2.5946H20.756V7.7837Zm5.1892 0h2.5946v2.5946h-2.5946V7.7837Zm2.5946 0h2.5946v2.5946h-2.5946V7.7837Zm5.1892 0h2.5946v2.5946H33.729V7.7837Zm2.5946 0h2.5946v2.5946h-2.5946V7.7837Zm2.5946 0h2.5946v2.5946h-2.5946V7.7837Zm5.1892 0h2.5946v2.5946h-2.5946V7.7837Zm12.973 0h2.5946v2.5946h-2.5946V7.7837Zm2.5946 0h2.5946v2.5946H59.675V7.7837Zm12.9729 0h2.5946v2.5946h-2.5946V7.7837Zm15.5676 0h2.5946v2.5946h-2.5946V7.7837Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H33.729v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm15.5675 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946Zm15.5676 0h2.5946v2.5946H59.675v-2.5946Zm12.9729 0h2.5946v2.5946h-2.5946v-2.5946Zm15.5676 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H46.702v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm-51.8919 2.5946h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946ZM5.1885 25.9459H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 28.5405H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm18.1622 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 31.1351h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3783 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H33.729v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 33.7297h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm15.5675 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 36.3243h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H33.729v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm-67.4594 2.5946h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H46.702v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 41.5135h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm12.9729 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946ZM7.7831 44.1081h2.5946v2.5946H7.7831v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H46.702v-2.5946Zm12.973 0h2.5946v2.5946H59.675v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946Zm10.3783 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 46.7027H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm15.5676 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm-75.2432 2.5946h2.5946v2.5945h-2.5946v-2.5945Zm15.5675 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm7.7838 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm12.973 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945H59.675v-2.5945Zm5.1892 0h2.5945v2.5945h-2.5945v-2.5945Zm7.7837 0h2.5946v2.5945h-2.5946v-2.5945Zm7.7838 0h2.5946v2.5945h-2.5946v-2.5945Zm5.1892 0h2.5946v2.5945h-2.5946v-2.5945Zm2.5946 0h2.5946v2.5945h-2.5946v-2.5945Zm-83.027 2.5945H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7837 0h2.5946v2.5946H20.756v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H33.729v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H59.675v-2.5946Zm10.3783 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-75.2432 2.5946h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm18.1622 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 57.081H7.783v2.5946H5.1885V57.081Zm2.5946 0h2.5946v2.5946H7.7831V57.081Zm7.7838 0h2.5945v2.5946h-2.5945V57.081Zm5.1891 0h2.5946v2.5946H20.756V57.081Zm10.3784 0h2.5946v2.5946h-2.5946V57.081Zm2.5946 0h2.5946v2.5946H33.729V57.081Zm10.3784 0h2.5946v2.5946h-2.5946V57.081Zm2.5946 0h2.5946v2.5946H46.702V57.081Zm2.5946 0h2.5946v2.5946h-2.5946V57.081Zm7.7838 0h2.5946v2.5946h-2.5946V57.081Zm5.1892 0h2.5946v2.5946h-2.5946V57.081Zm2.5946 0h2.5945v2.5946h-2.5945V57.081Zm2.5945 0h2.5946v2.5946h-2.5946V57.081Zm7.7838 0h2.5946v2.5946h-2.5946V57.081Zm2.5946 0h2.5946v2.5946h-2.5946V57.081Zm7.7838 0h2.5946v2.5946h-2.5946V57.081ZM5.1885 59.6756H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7837 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 64.8648H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm18.1621 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm12.973 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3783 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 67.4594H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7837 0h2.5946v2.5946H20.756v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946ZM25.9452 70.054h2.5946v2.5946h-2.5946V70.054Zm20.7568 0h2.5946v2.5946H46.702V70.054Zm2.5946 0h2.5946v2.5946h-2.5946V70.054Zm2.5946 0h2.5946v2.5946h-2.5946V70.054Zm2.5946 0h2.5946v2.5946h-2.5946V70.054Zm2.5946 0h2.5946v2.5946h-2.5946V70.054Zm2.5946 0h2.5946v2.5946H59.675V70.054Zm7.7837 0h2.5946v2.5946h-2.5946V70.054Zm10.3784 0h2.5946v2.5946h-2.5946V70.054Zm5.1892 0h2.5946v2.5946h-2.5946V70.054Zm5.1892 0h2.5946v2.5946h-2.5946V70.054Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm12.973 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 75.2432H7.783v2.5946H5.1885v-2.5946Zm15.5675 0h2.5946v2.5946H20.756v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H33.729v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H46.702v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H33.729v-2.5946Zm15.5676 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm-83.027 2.5946H7.783v2.5946H5.1885v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm10.3784 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946H46.702v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm5.1891 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 83.027H7.783v2.5946H5.1885V83.027Zm5.1892 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5945v2.5946h-2.5945V83.027Zm5.1891 0h2.5946v2.5946H20.756V83.027Zm5.1892 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm7.7838 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946h-2.5946V83.027Zm2.5946 0h2.5946v2.5946H46.702V83.027Zm5.1892 0h2.5946v2.5946h-2.5946V83.027Zm5.1892 0h2.5946v2.5946h-2.5946V83.027Zm7.7838 0h2.5945v2.5946h-2.5945V83.027Zm7.7837 0h2.5946v2.5946h-2.5946V83.027Zm10.3784 0h2.5946v2.5946h-2.5946V83.027ZM5.1885 85.6216H7.783v2.5946H5.1885v-2.5946Zm15.5675 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946H46.702v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H59.675v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm12.9729 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946ZM5.1885 88.2162H7.783v2.5946H5.1885v-2.5946Zm2.5946 0h2.5946v2.5946H7.7831v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946H20.756v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm7.7838 0h2.5946v2.5946h-2.5946v-2.5946Zm12.973 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5945v2.5946h-2.5945v-2.5946Zm2.5945 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm2.5946 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Zm5.1892 0h2.5946v2.5946h-2.5946v-2.5946Z" />
</svg>

            <a href="https://apps.apple.com/us/app/jamesedition-luxury-homes/id6737836918" class="je2-button js-app-download" target="_blank" rel="noreferrer" aria-label="Download the app on the App Store">

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 138 40" fill="none"><path fill="#000" d="M137.234 35.387c0 2.132-1.755 3.858-3.927 3.858H4.803c-2.17 0-3.931-1.726-3.931-3.858V4.618c0-2.13 1.761-3.863 3.931-3.863h128.503c2.173 0 3.927 1.732 3.927 3.863l.001 30.769Z" /><path fill="#A6A6A6" d="M132.893.801c2.365 0 4.289 1.884 4.289 4.199v30c0 2.315-1.924 4.199-4.289 4.199H5.213c-2.365 0-4.29-1.884-4.29-4.199V5c0-2.315 1.925-4.199 4.29-4.199h127.68Zm0-.801H5.213C2.405 0 .105 2.251.105 5v30c0 2.749 2.3 5 5.108 5h127.68c2.808 0 5.107-2.251 5.107-5V5c0-2.749-2.299-5-5.107-5Z" /><path fill="#fff" d="M30.88 19.784c-.03-3.223 2.695-4.791 2.82-4.864-1.544-2.203-3.936-2.504-4.776-2.528-2.01-.207-3.959 1.177-4.982 1.177-1.044 0-2.62-1.157-4.319-1.123-2.186.033-4.23 1.272-5.352 3.196-2.315 3.923-.588 9.688 1.63 12.859 1.108 1.553 2.405 3.287 4.101 3.226 1.66-.067 2.28-1.036 4.283-1.036 1.985 0 2.567 1.036 4.297.997 1.782-.028 2.903-1.56 3.974-3.127 1.282-1.78 1.797-3.533 1.817-3.623-.042-.014-3.46-1.291-3.493-5.154ZM27.611 10.306c.893-1.093 1.504-2.58 1.334-4.089-1.292.056-2.908.875-3.838 1.944-.824.942-1.56 2.486-1.37 3.938 1.452.106 2.943-.717 3.874-1.793ZM50.207 10.009c0 1.177-.36 2.063-1.08 2.658-.668.549-1.616.824-2.843.824-.61 0-1.13-.026-1.566-.078V6.982c.569-.09 1.182-.136 1.843-.136 1.17 0 2.051.249 2.646.747.666.563 1 1.368 1 2.416Zm-1.129.029c0-.763-.206-1.348-.619-1.756-.412-.407-1.015-.611-1.809-.611-.337 0-.624.022-.862.068v4.889c.132.02.373.029.723.029.82 0 1.452-.223 1.897-.669.446-.446.67-1.096.67-1.95ZM56.192 11.037c0 .725-.211 1.319-.634 1.785-.444.479-1.03.718-1.764.718-.707 0-1.27-.229-1.69-.689-.419-.459-.628-1.038-.628-1.736 0-.73.216-1.329.649-1.794.433-.465 1.015-.698 1.748-.698.707 0 1.275.229 1.705.688.409.446.614 1.022.614 1.726Zm-1.11.034c0-.435-.096-.808-.287-1.119-.225-.376-.545-.564-.96-.564-.43 0-.757.188-.982.564-.192.311-.287.69-.287 1.138 0 .435.096.808.287 1.119.232.376.555.564.971.564.409 0 .73-.191.96-.574.199-.317.298-.693.298-1.128ZM64.216 8.719l-1.506 4.714h-.981l-.624-2.047a15.061 15.061 0 0 1-.387-1.523h-.02a10.947 10.947 0 0 1-.387 1.523l-.663 2.047h-.992L57.24 8.719h1.1l.544 2.241c.132.53.24 1.035.327 1.513h.02c.08-.394.211-.896.397-1.503l.683-2.25h.873l.654 2.202c.159.537.287 1.054.386 1.552h.03c.073-.485.182-1.002.327-1.552l.584-2.202h1.051v-.001ZM69.766 13.433h-1.07v-2.7c0-.832-.323-1.248-.97-1.248a.975.975 0 0 0-.774.343 1.202 1.202 0 0 0-.297.808v2.796h-1.07v-3.366c0-.414-.014-.863-.04-1.349h.941l.05.737h.03c.124-.229.31-.418.555-.569.29-.176.614-.265.97-.265.45 0 .823.142 1.12.427.37.349.555.87.555 1.562v2.824ZM72.718 13.433h-1.07V6.556h1.07v6.877ZM79.02 11.037c0 .725-.211 1.319-.634 1.785-.443.479-1.032.718-1.764.718-.708 0-1.27-.229-1.69-.689-.418-.459-.628-1.038-.628-1.736 0-.73.216-1.329.649-1.794.433-.465 1.015-.698 1.748-.698.707 0 1.274.229 1.705.688.409.446.614 1.022.614 1.726Zm-1.111.034c0-.435-.096-.808-.287-1.119-.224-.376-.545-.564-.96-.564-.43 0-.757.188-.98.564-.193.311-.288.69-.288 1.138 0 .435.096.808.287 1.119.232.376.555.564.972.564.408 0 .728-.191.959-.574.199-.317.297-.693.297-1.128ZM84.201 13.433h-.961l-.08-.543h-.03c-.328.433-.797.65-1.406.65-.455 0-.822-.143-1.099-.427a1.323 1.323 0 0 1-.377-.96c0-.576.245-1.015.739-1.319.492-.304 1.184-.453 2.076-.446V10.3c0-.621-.333-.931-1-.931-.475 0-.894.117-1.255.349l-.218-.688c.448-.271 1-.407 1.652-.407 1.258 0 1.89.65 1.89 1.95v1.736c0 .471.023.846.069 1.124Zm-1.111-1.62v-.727c-1.181-.02-1.772.297-1.772.95 0 .246.068.43.206.553a.758.758 0 0 0 .523.184c.235 0 .454-.073.654-.218a.89.89 0 0 0 .389-.742ZM90.284 13.433h-.95l-.05-.757h-.03c-.303.576-.82.864-1.547.864-.58 0-1.063-.223-1.446-.669-.383-.446-.574-1.025-.574-1.736 0-.763.207-1.381.624-1.853.404-.44.898-.66 1.486-.66.647 0 1.1.213 1.357.64h.02V6.556h1.072v5.607c0 .459.012.882.038 1.27Zm-1.11-1.988v-.786a1.19 1.19 0 0 0-.417-.965c-.199-.171-.439-.257-.716-.257-.399 0-.712.155-.941.466-.228.311-.343.708-.343 1.193 0 .466.109.844.328 1.135.232.31.545.465.936.465.351 0 .632-.129.846-.388.206-.239.307-.527.307-.863ZM99.439 11.037c0 .725-.212 1.319-.635 1.785-.443.479-1.03.718-1.764.718-.706 0-1.268-.229-1.69-.689-.418-.459-.627-1.038-.627-1.736 0-.73.215-1.329.648-1.794.433-.465 1.016-.698 1.75-.698.706 0 1.275.229 1.704.688.408.446.614 1.022.614 1.726Zm-1.11.034c0-.435-.096-.808-.287-1.119-.225-.376-.544-.564-.96-.564-.43 0-.757.188-.982.564-.192.311-.287.69-.287 1.138 0 .435.096.808.287 1.119.231.376.554.564.971.564.409 0 .73-.191.961-.574.197-.317.297-.693.297-1.128ZM105.195 13.433h-1.07v-2.7c0-.832-.323-1.248-.971-1.248a.97.97 0 0 0-.772.343 1.193 1.193 0 0 0-.298.808v2.796h-1.071v-3.366c0-.414-.012-.863-.038-1.349h.94l.05.737h.029c.126-.229.312-.418.555-.569.291-.176.615-.265.972-.265.448 0 .822.142 1.119.427.371.349.555.87.555 1.562v2.824ZM112.399 9.504h-1.179v2.29c0 .582.21.873.624.873.192 0 .352-.016.477-.049l.028.795c-.212.078-.489.117-.832.117-.423 0-.751-.126-.989-.378-.239-.252-.358-.676-.358-1.271V9.504h-.704v-.785h.704v-.864l1.049-.31v1.173h1.179v.786h.001ZM118.066 13.433h-1.072v-2.68c0-.845-.323-1.268-.969-1.268-.497 0-.836.245-1.022.735-.031.103-.05.229-.05.377v2.835h-1.069V6.556h1.069v2.841h.021c.337-.517.82-.775 1.446-.775.443 0 .81.142 1.101.427.363.355.545.883.545 1.581v2.803ZM123.911 10.853c0 .188-.014.346-.04.475h-3.21c.014.466.168.821.465 1.067.271.22.622.33 1.051.33.475 0 .908-.074 1.298-.223l.168.728c-.457.194-.994.291-1.616.291-.746 0-1.333-.215-1.758-.645-.427-.43-.639-1.007-.639-1.731 0-.711.198-1.303.595-1.775.415-.504.975-.756 1.683-.756.693 0 1.219.252 1.574.756.287.4.429.895.429 1.483Zm-1.021-.271a1.39 1.39 0 0 0-.208-.805c-.185-.291-.468-.437-.851-.437-.35 0-.635.142-.852.427a1.567 1.567 0 0 0-.318.815h2.229ZM54.9 31.504h-2.319l-1.27-3.909h-4.417l-1.21 3.909h-2.26l4.377-13.308h2.702l4.398 13.308Zm-3.973-5.549-1.149-3.475c-.121-.355-.35-1.191-.685-2.507h-.041c-.134.566-.35 1.402-.646 2.507l-1.128 3.475h3.65ZM66.154 26.588c0 1.632-.45 2.922-1.351 3.869-.807.843-1.81 1.264-3.005 1.264-1.292 0-2.219-.454-2.784-1.362h-.04v5.055h-2.178V25.067c0-1.026-.028-2.079-.081-3.159h1.915l.122 1.521h.04c.727-1.146 1.829-1.718 3.308-1.718 1.156 0 2.121.447 2.894 1.342.774.896 1.16 2.074 1.16 3.535Zm-2.219.078c0-.934-.214-1.704-.645-2.31-.471-.632-1.103-.948-1.896-.948-.537 0-1.026.176-1.462.523-.437.35-.723.807-.857 1.373-.067.264-.1.48-.1.65v1.6c0 .698.218 1.287.655 1.768.437.481 1.005.721 1.704.721.82 0 1.458-.31 1.915-.928.458-.619.686-1.435.686-2.449ZM77.428 26.588c0 1.632-.45 2.922-1.352 3.869-.806.843-1.808 1.264-3.005 1.264-1.29 0-2.218-.454-2.782-1.362h-.04v5.055H68.07V25.067c0-1.026-.027-2.079-.08-3.159h1.915l.121 1.521h.041c.726-1.146 1.828-1.718 3.308-1.718 1.155 0 2.12.447 2.895 1.342.77.896 1.158 2.074 1.158 3.535Zm-2.219.078c0-.934-.215-1.704-.646-2.31-.471-.632-1.101-.948-1.895-.948-.538 0-1.026.176-1.463.523-.437.35-.722.807-.856 1.373a2.79 2.79 0 0 0-.1.65v1.6c0 .698.218 1.287.653 1.768.437.48 1.005.721 1.706.721.82 0 1.458-.31 1.915-.928.458-.619.686-1.435.686-2.449ZM90.032 27.772c0 1.132-.401 2.053-1.207 2.764-.886.777-2.119 1.165-3.703 1.165-1.463 0-2.635-.276-3.523-.829l.505-1.777c.956.566 2.005.85 3.148.85.82 0 1.458-.182 1.917-.544.457-.362.684-.848.684-1.454 0-.54-.188-.995-.564-1.364-.375-.369-1.002-.712-1.876-1.029-2.38-.869-3.569-2.142-3.569-3.816 0-1.094.417-1.991 1.252-2.689.831-.699 1.94-1.048 3.327-1.048 1.237 0 2.265.211 3.085.632l-.544 1.738c-.766-.408-1.632-.612-2.602-.612-.766 0-1.364.185-1.793.553-.363.329-.545.73-.545 1.205 0 .526.207.961.624 1.303.363.316 1.022.658 1.978 1.027 1.17.461 2.028 1 2.58 1.618.551.616.826 1.387.826 2.307ZM97.233 23.508h-2.4v4.659c0 1.185.422 1.777 1.27 1.777.389 0 .712-.033.967-.099l.06 1.619c-.429.157-.993.236-1.693.236-.86 0-1.532-.257-2.018-.77-.483-.514-.726-1.376-.726-2.587v-4.837h-1.43v-1.6h1.43v-1.757l2.14-.632v2.389h2.4v1.602ZM108.062 26.627c0 1.475-.431 2.686-1.291 3.633-.902.975-2.099 1.461-3.591 1.461-1.438 0-2.583-.467-3.437-1.401-.854-.934-1.281-2.113-1.281-3.534 0-1.487.44-2.705 1.32-3.652.88-.948 2.067-1.422 3.559-1.422 1.439 0 2.596.467 3.469 1.402.836.907 1.252 2.078 1.252 3.513Zm-2.259.069c0-.885-.193-1.644-.584-2.277-.457-.766-1.11-1.148-1.955-1.148-.876 0-1.541.383-1.997 1.148-.391.634-.584 1.405-.584 2.317 0 .885.193 1.644.584 2.276.471.766 1.128 1.148 1.977 1.148.832 0 1.484-.39 1.955-1.168.402-.645.604-1.412.604-2.296ZM115.142 23.783a3.871 3.871 0 0 0-.687-.059c-.766 0-1.358.283-1.775.85-.363.5-.545 1.132-.545 1.895v5.035h-2.176l.02-6.574c0-1.106-.027-2.113-.082-3.021h1.897l.08 1.836h.06c.23-.631.593-1.139 1.089-1.52a2.67 2.67 0 0 1 1.574-.514c.201 0 .383.014.545.039v2.033ZM124.881 26.252c0 .382-.026.704-.08.967h-6.533c.025.948.341 1.673.948 2.173.55.447 1.262.671 2.137.671.967 0 1.85-.151 2.643-.454l.341 1.48c-.927.396-2.022.593-3.286.593-1.52 0-2.713-.438-3.581-1.313-.866-.875-1.3-2.05-1.3-3.524 0-1.447.403-2.652 1.211-3.613.846-1.026 1.989-1.539 3.427-1.539 1.413 0 2.482.513 3.209 1.539.575.815.864 1.823.864 3.02Zm-2.077-.553c.014-.632-.127-1.178-.423-1.639-.377-.593-.956-.889-1.735-.889-.712 0-1.291.289-1.734.869-.362.461-.578 1.014-.644 1.658h4.536v.001Z" /></svg>







  
  


</a>
          </div>
        </div>
    </div>
    <div class="je2-footer__settings">
      <div class="je2-footer__label">SETTINGS</div>

      <form class="js-form">
        <div class="je2-select">
  <svg class="je2-select__right-icon"><use xlink:href="#arrow-down"></use></svg>
  <select name="je_language" id="je_language" aria-label="je_language"><option selected="selected" value="en">English</option>
<option value="de">German</option>
<option value="fr">French</option>
<option value="es">Spanish</option>
<option value="it">Italian</option></select>
</div>
        <div class="je2-select">
  <svg class="je2-select__right-icon"><use xlink:href="#arrow-down"></use></svg>
  <select name="je_currency" id="je_currency" aria-label="je_currency"><option value="AUD">Australian dollar - AUD $</option>
<option value="BRL">Brazilian real - BRL R$</option>
<option value="CAD">Canadian dollar - CAD $</option>
<option value="CZK">Czech korun - CZK Kč</option>
<option value="DKK">Danish krone - DKK kr.</option>
<option value="AED">Emirati dirham - AED AED</option>
<option selected="selected" value="EUR">Euro - EUR €</option>
<option value="HKD">Hong Kong dollar - HKD HK$</option>
<option value="HUF">Hungarian forint - HUF Ft</option>
<option value="INR">Indian rupee - INR ₹</option>
<option value="JPY">Japanese yen - JPY ¥</option>
<option value="MYR">Malaysian ringgit - MYR RM</option>
<option value="MXN">Mexican peso - MXN $</option>
<option value="NZD">New Zealand dollar - NZD $</option>
<option value="NOK">Norwegian krone - NOK kr</option>
<option value="PLN">Polish zloty - PLN zł</option>
<option value="GBP">Pound sterling - GBP £</option>
<option value="RUB">Russian ruble - RUB RUB</option>
<option value="SAR">Saudi Arabian riyal - SAR ر.س</option>
<option value="SGD">Singapore dollar - SGD $</option>
<option value="ZAR">South African rand - ZAR R</option>
<option value="KRW">South Korean won - KRW ₩</option>
<option value="SEK">Swedish krona - SEK kr</option>
<option value="CHF">Swiss franc - CHF CHF</option>
<option value="TRY">Turkish lira - TRY ₺</option>
<option value="USD">United States dollar - USD $</option></select>
</div>
        <div class="je2-select">
  <svg class="je2-select__right-icon"><use xlink:href="#arrow-down"></use></svg>
  <select name="je_measurement_units" id="je_measurement_units" aria-label="je_measurement_units"><option value="sqft">Square Feet — ft² / Acre - Ac</option>
<option selected="selected" value="sqm">Square Meter — m² / Hectare - Ha</option></select>
</div>
      </form>
    </div>
  </div>
  <div class="je2-footer__bottom">
    <div class="je2-footer__copyright">
      <div class="je2-footer__logo">
        <svg width="26" height="28" viewBox="0 0 26 28" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12.7263 0C4.88083 0 0 0.666315 0 0.666315C0 0.666315 0 8.73379 0 14.5746C0 19.5614 1.88428 22.4059 5.63582 24.407L12.7263 28L19.8168 24.407C23.5705 22.4059 25.4526 19.5614 25.4526 14.5746C25.4526 8.73379 25.4526 0.666315 25.4526 0.666315C25.4526 0.666315 20.5739 0 12.7263 0ZM11.546 5.43384C11.1121 5.60675 10.9675 5.83658 10.9675 6.3806V14.5219C10.9675 16.7464 10.0807 17.4338 8.42821 17.805C7.25 18.0706 5.50396 17.6616 5.50396 17.6616L5.31043 16.1223L5.59966 16.0253C6.10157 16.9784 6.70981 17.7396 7.65833 17.5287C8.67916 17.2989 8.59409 14.524 8.59409 14.524C8.59409 14.524 8.59409 6.83184 8.59409 6.38271C8.59409 5.83658 8.46436 5.60675 8.03051 5.43595V5.22088H8.0454H11.5354H11.5502V5.43384H11.546ZM19.6233 17.3769H12.3712V17.1766C12.805 16.991 12.9496 16.7612 12.9496 16.2298V6.38271C12.9496 5.83658 12.805 5.60675 12.3712 5.43595V5.22088H19.4659L19.6254 7.05746H19.2936C18.8598 6.02425 18.192 5.57934 17.0627 5.57934H16.2673C15.5868 5.57934 15.3124 5.80917 15.3124 6.38271V10.6885H16.6289C17.5689 10.6885 18.0325 10.3869 18.1346 9.69742H18.4387V12.1518H18.1346C18.092 11.4201 17.6561 11.1038 16.6289 11.1038H15.3124V16.0991C15.3124 16.3585 15.3422 16.544 15.3996 16.66C15.5293 16.9046 15.9058 17.0185 16.5438 17.0185H17.2669C18.1346 17.0185 18.7301 16.8034 19.2362 16.3015C19.5106 16.0295 19.6424 15.8144 19.8445 15.2831L20.1486 15.4117L19.6233 17.3769Z" fill="#606060"/>
</svg>

      </div>
      Copyright © 2025 JamesEdition B.V.®
    </div>
    <div class="je2-footer__social">
      <a alt="Instagram" aria-label="Instagram" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://www.instagram.com/jameseditioncom/">
        <svg viewBox="0 0 30 30">
  <path d="M11.2559 6C10.3079 6 9.42773 6.23698 8.61523 6.71094C7.81966 7.1849 7.1849 7.82812 6.71094 8.64062C6.23698 9.4362 6 10.3079 6 11.2559V18.6191C6 19.5671 6.23698 20.4473 6.71094 21.2598C7.1849 22.0553 7.81966 22.6901 8.61523 23.1641C9.42773 23.638 10.3079 23.875 11.2559 23.875H18.6191C19.5671 23.875 20.4388 23.638 21.2344 23.1641C22.0469 22.6901 22.6901 22.0553 23.1641 21.2598C23.638 20.4473 23.875 19.5671 23.875 18.6191V11.2559C23.875 10.3079 23.638 9.4362 23.1641 8.64062C22.6901 7.82812 22.0469 7.1849 21.2344 6.71094C20.4388 6.23698 19.5671 6 18.6191 6H11.2559ZM11.2559 7.625H18.6191C19.2793 7.625 19.8887 7.78581 20.4473 8.10742C21.0059 8.42904 21.446 8.86914 21.7676 9.42773C22.0892 9.98633 22.25 10.5957 22.25 11.2559V18.6191C22.25 19.2793 22.0892 19.8887 21.7676 20.4473C21.446 21.0059 21.0059 21.446 20.4473 21.7676C19.8887 22.0892 19.2793 22.25 18.6191 22.25H11.2559C10.5957 22.25 9.98633 22.0892 9.42773 21.7676C8.86914 21.446 8.42904 21.0059 8.10742 20.4473C7.78581 19.8887 7.625 19.2793 7.625 18.6191V11.2559C7.625 10.5957 7.78581 9.98633 8.10742 9.42773C8.42904 8.86914 8.86914 8.42904 9.42773 8.10742C9.98633 7.78581 10.5957 7.625 11.2559 7.625ZM19.7363 9.40234C19.5332 9.40234 19.3555 9.47852 19.2031 9.63086C19.0677 9.76628 19 9.93555 19 10.1387C19 10.3418 19.0677 10.5195 19.2031 10.6719C19.3555 10.8073 19.5332 10.875 19.7363 10.875C19.9395 10.875 20.1087 10.8073 20.2441 10.6719C20.3965 10.5195 20.4727 10.3418 20.4727 10.1387C20.4727 9.93555 20.3965 9.76628 20.2441 9.63086C20.1087 9.47852 19.9395 9.40234 19.7363 9.40234ZM14.9375 10.0625C14.0573 10.0625 13.2448 10.2826 12.5 10.7227C11.7552 11.1628 11.1628 11.7552 10.7227 12.5C10.2826 13.2448 10.0625 14.0573 10.0625 14.9375C10.0625 15.8177 10.2826 16.6302 10.7227 17.375C11.1628 18.1198 11.7552 18.7122 12.5 19.1523C13.2448 19.5924 14.0573 19.8125 14.9375 19.8125C15.8177 19.8125 16.6302 19.5924 17.375 19.1523C18.1198 18.7122 18.7122 18.1198 19.1523 17.375C19.5924 16.6302 19.8125 15.8177 19.8125 14.9375C19.8125 14.0573 19.5924 13.2448 19.1523 12.5C18.7122 11.7552 18.1198 11.1628 17.375 10.7227C16.6302 10.2826 15.8177 10.0625 14.9375 10.0625ZM14.9375 11.6875C15.5299 11.6875 16.0716 11.8314 16.5625 12.1191C17.0703 12.4069 17.4681 12.8047 17.7559 13.3125C18.0436 13.8034 18.1875 14.3451 18.1875 14.9375C18.1875 15.5299 18.0436 16.0801 17.7559 16.5879C17.4681 17.0788 17.0703 17.4681 16.5625 17.7559C16.0716 18.0436 15.5299 18.1875 14.9375 18.1875C14.3451 18.1875 13.7949 18.0436 13.2871 17.7559C12.7962 17.4681 12.4069 17.0788 12.1191 16.5879C11.8314 16.0801 11.6875 15.5299 11.6875 14.9375C11.6875 14.3451 11.8314 13.8034 12.1191 13.3125C12.4069 12.8047 12.7962 12.4069 13.2871 12.1191C13.7949 11.8314 14.3451 11.6875 14.9375 11.6875Z"/>
</svg>

</a>      <a alt="Facebook" aria-label="Facebook" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://www.facebook.com/thejamesedition">
        <svg viewBox="0 0 30 30">
  <path d="M7.625 6C7.1849 6 6.80404 6.16081 6.48242 6.48242C6.16081 6.80404 6 7.1849 6 7.625V22.25C6 22.6901 6.16081 23.071 6.48242 23.3926C6.80404 23.7142 7.1849 23.875 7.625 23.875H22.25C22.6901 23.875 23.071 23.7142 23.3926 23.3926C23.7142 23.071 23.875 22.6901 23.875 22.25V7.625C23.875 7.1849 23.7142 6.80404 23.3926 6.48242C23.071 6.16081 22.6901 6 22.25 6H7.625ZM7.625 7.625H22.25V22.25H18.0352V16.7656H20.1426L20.4473 14.3281H18.0352V12.7539C18.0352 12.3477 18.1029 12.0599 18.2383 11.8906C18.4245 11.6706 18.7546 11.5605 19.2285 11.5605H20.5488V9.35156C20.1426 9.30078 19.5078 9.27539 18.6445 9.27539C17.6797 9.27539 16.9095 9.55469 16.334 10.1133C15.7754 10.6719 15.4961 11.4674 15.4961 12.5V14.3281H13.3633V16.7656H15.4961V22.25H7.625V7.625Z"/>
</svg>

</a>      <a alt="Youtube" aria-label="Youtube" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://www.youtube.com/channel/UC0ilNPVLpRHDMFgfLVr3v4Q">
      <svg viewBox="0 0 32 32">
  <path d="M26.7809 11.4524C26.7809 11.4524 26.566 9.88392 25.9043 9.19522C25.0664 8.28881 24.1297 8.28437 23.7 8.23105C20.6234 8 16.0043 8 16.0043 8H15.9957C15.9957 8 11.3766 8 8.3 8.23105C7.87031 8.28437 6.93359 8.28881 6.0957 9.19522C5.43398 9.88392 5.22344 11.4524 5.22344 11.4524C5.22344 11.4524 5 13.2963 5 15.1358V16.8598C5 18.6992 5.21914 20.5432 5.21914 20.5432C5.21914 20.5432 5.43398 22.1116 6.09141 22.8003C6.9293 23.7067 8.0293 23.6756 8.51914 23.7734C10.2809 23.9467 16 24 16 24C16 24 20.6234 23.9911 23.7 23.7645C24.1297 23.7112 25.0664 23.7067 25.9043 22.8003C26.566 22.1116 26.7809 20.5432 26.7809 20.5432C26.7809 20.5432 27 18.7037 27 16.8598V15.1358C27 13.2963 26.7809 11.4524 26.7809 11.4524ZM13.727 18.9525V12.5587L19.6695 15.7667L13.727 18.9525Z"/>
</svg>

</a>      <a alt="Twitter" aria-label="Twitter" target="_blank" rel="noreferrer" class="je2-footer__social-link _twitter" href="https://twitter.com/JamesEdition">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1227"><path d="M714.16 519.28 1160.9 0h-105.86l-387.9 450.89L357.34 0H0l468.5 681.82L0 1226.37h105.87l409.62-476.15 327.18 476.15H1200L714.14 519.28h.02Zm-145 168.55-47.46-67.9L144 79.7h162.6l304.8 436 47.47 67.89 396.2 566.72h-162.6L569.16 687.85v-.02Z" /></svg>

</a>      <a alt="linkedin" aria-label="linkedin" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://www.linkedin.com/company/jamesedition/">
        <svg viewBox="0 0 32 32">
  <path d="M9.63546 5.3335C9.00351 5.3335 8.46185 5.55919 8.01046 6.01058C7.55907 6.44391 7.33337 6.98558 7.33337 7.63558C7.33337 8.26752 7.55907 8.80919 8.01046 9.26058C8.46185 9.71197 8.99449 9.93766 9.60837 9.93766C10.2403 9.93766 10.782 9.71197 11.2334 9.26058C11.6848 8.80919 11.9105 8.26752 11.9105 7.63558C11.9105 7.00363 11.6848 6.46197 11.2334 6.01058C10.8 5.55919 10.2674 5.3335 9.63546 5.3335ZM20.7938 11.4002C19.9091 11.4002 19.1417 11.6078 18.4917 12.0231C17.9681 12.3661 17.5528 12.8266 17.2459 13.4043H17.1917V11.671H13.4V24.4002H17.3542V18.0897C17.3542 17.4036 17.3903 16.88 17.4625 16.5189C17.5709 15.9772 17.7695 15.571 18.0584 15.3002C18.4014 14.9932 18.8889 14.8397 19.5209 14.8397C20.1528 14.8397 20.6313 15.0203 20.9563 15.3814C21.2271 15.6703 21.4077 16.1036 21.498 16.6814C21.5521 17.0245 21.5792 17.53 21.5792 18.1981V24.4002H25.5334V17.4127C25.5334 16.1307 25.416 15.1016 25.1813 14.3252C24.9105 13.3863 24.45 12.6731 23.8 12.1856C23.0778 11.662 22.0757 11.4002 20.7938 11.4002ZM7.65837 11.671V24.4002H11.6125V11.671H7.65837Z"/>
</svg>

</a>      <a alt="pinterest" aria-label="pinterest" target="_blank" rel="noreferrer" class="je2-footer__social-link" href="https://pinterest.com/jamesedition/">
        <svg viewBox="0 0 32 32">
  <path d="M15.4667 6.6665C13.8056 6.6665 12.2563 7.08178 10.8188 7.91234C9.42922 8.72692 8.32714 9.829 7.51256 11.2186C6.682 12.6561 6.26672 14.2054 6.26672 15.8665C6.26672 17.1443 6.52228 18.3662 7.03339 19.5321C7.51256 20.6502 8.19138 21.6405 9.06985 22.503C9.96429 23.3495 10.9785 23.9964 12.1126 24.4436C11.9848 23.3096 11.9928 22.4231 12.1365 21.7842L13.2146 17.2321L13.1428 17.0405C13.0948 16.8967 13.0549 16.737 13.023 16.5613C12.9751 16.3377 12.9511 16.0981 12.9511 15.8425C12.9511 15.2196 13.1108 14.6925 13.4303 14.2613C13.7497 13.83 14.141 13.6144 14.6042 13.6144C14.9876 13.6144 15.2751 13.7422 15.4667 13.9978C15.6744 14.2373 15.7782 14.5408 15.7782 14.9082C15.7782 15.1318 15.7383 15.4193 15.6584 15.7707C15.5945 15.9943 15.4907 16.3297 15.3469 16.7769C15.1872 17.32 15.0754 17.7193 15.0115 17.9748C14.8997 18.438 14.9796 18.8373 15.2511 19.1728C15.5386 19.4922 15.9139 19.6519 16.3771 19.6519C16.9202 19.6519 17.4073 19.4762 17.8386 19.1248C18.2858 18.7575 18.6372 18.2544 18.8928 17.6155C19.1483 16.9766 19.2761 16.2498 19.2761 15.4353C19.2761 14.7005 19.1084 14.0537 18.773 13.4946C18.4535 12.9196 17.9983 12.4804 17.4073 12.1769C16.8323 11.8575 16.1695 11.6978 15.4188 11.6978C14.5883 11.6978 13.8455 11.8894 13.1907 12.2728C12.5837 12.6241 12.1126 13.1113 11.7771 13.7342C11.4417 14.3412 11.274 14.988 11.274 15.6748C11.274 16.0582 11.3379 16.4495 11.4657 16.8488C11.5935 17.2321 11.7612 17.5436 11.9688 17.7832C12.0327 17.863 12.0487 17.9509 12.0167 18.0467L11.7771 19.0769C11.7292 19.2526 11.6254 19.2925 11.4657 19.1967C10.9067 18.9571 10.4514 18.47 10.1001 17.7353C9.76464 17.0484 9.59693 16.3537 9.59693 15.6509C9.59693 14.6606 9.82853 13.7502 10.2917 12.9196C10.7709 12.0412 11.4497 11.3623 12.3282 10.8832C13.2865 10.3401 14.4046 10.0686 15.6823 10.0686C16.7205 10.0686 17.6709 10.3002 18.5334 10.7634C19.4119 11.2266 20.0987 11.8655 20.5938 12.68C21.0889 13.4946 21.3365 14.3971 21.3365 15.3873C21.3365 16.4415 21.1289 17.4078 20.7136 18.2863C20.3143 19.1488 19.7473 19.8356 19.0126 20.3467C18.2938 20.8578 17.4792 21.1134 16.5688 21.1134C16.1056 21.1134 15.6744 21.0096 15.2751 20.8019C14.8917 20.5943 14.6202 20.3467 14.4605 20.0592L13.8855 22.2394C13.7258 22.8783 13.3424 23.6849 12.7355 24.6592C13.6299 24.9307 14.5403 25.0665 15.4667 25.0665C17.1278 25.0665 18.6771 24.6512 20.1146 23.8207C21.5042 23.0061 22.6063 21.904 23.4209 20.5144C24.2514 19.0769 24.6667 17.5276 24.6667 15.8665C24.6667 14.2054 24.2514 12.6561 23.4209 11.2186C22.6063 9.829 21.5042 8.72692 20.1146 7.91234C18.6771 7.08178 17.1278 6.6665 15.4667 6.6665Z"/>
</svg>

</a>    </div>
  </div>
</div>

      </div>
    </div>
      <script data-turbolinks-track="reload" type="81dfcc4b5c125fb5b214f294-text/javascript">
  (function () {
      window.dataLayer = window.dataLayer || [];

      const dimensions = {"dimension1":"359439","dimension2":"1728859","dimension3":"16460690","dimension4":null,"dimension5":null,"dimension6":"France","dimension7":"Angoulême","dimension8":"real_estate","dimension9":"Listing","dimension10":"No","dimension11":"667800.00","dimension12":"For sale","dimension13":"RealEstate","dimension14":null,"dimension15":null,"dimension16":null,"dimension17":"97008","dimension18":"elite_plus"};
      const events = [];

      window.dataLayer.push({
        office_id: dimensions.dimension1,
        agent_id: dimensions.dimension2,
        listing_id: dimensions.dimension3,
        group_id: dimensions.dimension4,
        country: dimensions.dimension6,
        city: dimensions.dimension7,
        category: dimensions.dimension8,
        page_type: dimensions.dimension9,
        is_authenticated: dimensions.dimension10,
        listing_price: dimensions.dimension11,
        section: dimensions.dimension12,
        sub_section: dimensions.dimension13,
        current_experiment: dimensions.dimension16,
        place_id: dimensions.dimension17,
        subscription: dimensions.dimension18,
      });

      for (let event of events) {
        window.dataLayer.push({ event: event });
      }

        window.dataLayer.push({ userAuth: 0});

  })();
</script>

  <script type="81dfcc4b5c125fb5b214f294-text/javascript" data-turbolinks-track="reload">
  window.addEventListener("load", () => {
    setTimeout(() => {
      (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
      new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
      j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
      'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
      })(window,document,'script','dataLayer','GTM-N8N6RLK');
    },1);
  });

  window.dataLayer = window.dataLayer || []
</script>


  <noscript>
  <iframe height="0" src="https://www.googletagmanager.com/ns.html?id=GTM-N8N6RLK" style="display:none;visibility:hidden" width="0"></iframe>
</noscript>


    <script id="Cookiebot" src="https://consent.cookiebot.com/uc.js" data-cbid="a5081197-ee35-4671-954e-50cefb375242" type="81dfcc4b5c125fb5b214f294-text/javascript"></script>

<script type="81dfcc4b5c125fb5b214f294-text/javascript">
    SIGNUP_PATH = "/signup";
    RECENT_LISTINGS_PATH = "/buyer/recent-listings/create";
    SAVE_LISTING_PATH = "/buyer/saved-listings/create";
    UNSAVE_LISTING_PATH = "/buyer/saved-listings/remove";

    window.mixpanelToken = "bfe35bec091a7744f92d5d75ca232054";

    window.DATA = window.DATA || {};
    window.DATA.currenciesConvertTable = {"USD":1.1651956072125609,"EUR":"1.0","AED":"4.27918086748812956975152203676194521610142125412","AUD":"1.7549022692184450464621748376009","CAD":"1.6184916542864633400332080748055545545540767365","CHF":"0.936135628768679542078126365463565335999322877065","CNY":"8.2393311777214599900958373386932","GBP":"0.872724518628564770310815928223986673302475234288","HKD":"9.0714847505024906056104168487285","HRK":"7.5340312855020536572577121384252","MXN":"21.202124151591948498354161204812","NOK":"11.75828832765300474817209939118528707310503202438","RUB":"89.432259605581286958548166273413","SEK":"10.958912872498470680765533513939","THB":"37.11148008972006175536718226572229175287462456488","ZAR":"19.73451600687465408255410877101","TWD":"36.439744822162020449182906580442","PHP":"68.734891199860176527134492702963","CZK":"24.201811879169215532057444143436","MUR":"53.68056395467389087943138454367963900967381397581","SGD":"1.5089236505578373969530134871392","KYD":"0.97070465204346179614902851816249","CLP":"1071.44396865623816598211424742928540157142677116807","PAB":"1.1651956072125608086457514055172","BBD":"2.3303912144251216172915028110344","INR":"104.79695301348713915348539136007","JPY":"180.83486265256779981939468088205336562656860022823","XCD":"3.1489993882723062134055754609805","NZD":"2.01591307640770194296367502694513859108602724549","GIP":"0.87272451862856477031081592822395","BRL":"6.2210958664685834134405313291969","ILS":"3.762614698942584986454601066154","OMR":"0.44799790264790701739054443764747","PLN":"4.2316583646479652771709050656879","FJD":"2.63386641032363307990328876460137335781720586353","COP":"4424.82603046986512860846514608632846624800013598938","XPF":"119.3318045966966704535523901074898662131785789749","BSD":"1.1651956072125608086457514055172","QAR":"4.2455766261761193160301785662268","CRC":"568.96400477730198957149931544758","HUF":"381.99319059687144979463427422879313804759208607514","MAD":"10.756197966733665414081388913164","DKK":"7.4683328963849806286230300911766","BMD":"1.1651956072125608086457514055172","LKR":"359.27035334556788720906522182411","TRY":"49.536047073902531387456669288357661634880214305","MYR":"4.7901191412508374843426840280812","SAR":"4.3731760319263596376241661568936","KRW":"1715.8745736840572111043141367356910150575917158209","BZD":"2.3425523609775991144513385184538","PYG":"8098.7334626700457339275830930117","IDR":"19437.71685164146931166069503918","DOP":"74.207299950479186693466165632556","JMD":"186.43091380465495645081418043054","EGP":"55.431268024119549069300008738967","XOF":"655.95734218881994814879547904104","NGN":"1690.5590025925602260479477992368","TND":"3.4167834775262897258877334032451","RSD":"117.39345742666550147105945410586","CVE":"110.25987008068979579946983599872","NAD":"19.74051326866497713303620845349410016168766090801","VES":"289.65117422587316845815491275598","MZN":"74.455991144513385184537854292289","KES":"150.65979201258411255789565673337","CLF":"0.027300533076990299746569955431268","ANG":"2.0857001369104838474758950158758","ARS":"1677.2847446765125695476128054997","AWG":"2.0988085874916251565731597191879","VND":"30719.66525328439511783040577937"}

    window.GTM_DATA = window.GTM_DATA || {};
    window.GTM_DATA.country_code = 'DE';
</script>





<script data-cfasync="false" type="text/javascript" id="exposed-vars">
  window.JEParams = window.JEParams || {};
  Object.assign(JEParams, {"inquiry":{"tourRequest":"tour request","inLocation":"in LUXURY FAMILY ESTATE WITH HEATED POOL AND OUTBUILDINGS IN VARS, NEAR ANGOULEME (Angoulême, Nouvelle-Aquitaine, France)"},"listing":{"id":16460690,"priceUsd":778117,"priceEuro":667800,"price":667800,"currency":"EUR","countryCode":"FR","country":"France","countrySubdivision":"Nouvelle-Aquitaine","city":"Angoulême","officeId":359439,"agentId":1728859,"groupId":null,"category":"RealEstate","brand":null,"model":null,"lat":45.6488766,"lng":0.1567288},"inquiryPlanRequest":"I'm interested in LUXURY FAMILY ESTATE WITH HEATED POOL AND OUTBUILDINGS IN VARS, NEAR ANGOULEME (Angoulême, Nouvelle-Aquitaine, France). Please contact me with more information about the property.","inquiryLocationRequest":"I'm interested in LUXURY FAMILY ESTATE WITH HEATED POOL AND OUTBUILDINGS IN VARS, NEAR ANGOULEME (Angoulême, Nouvelle-Aquitaine, France). Please share more detailed location information with me.","listingPageV3Enabled":true,"listingPageV3P3Enabled":true,"isProduction":true,"isStaging":false,"isTest":false,"locale":"en","category":"RealEstate","pageType":"listing_page_v2","rental":false,"recaptchaSiteKey":"6LeNK2caAAAAABqNVS2GtBowWgxSInPKc9XdX4PE","googlePlacesApiKey":"AIzaSyCk0QTmI7K69eXqOgdFf9ty82mOsYcCIME","withBottomBar":true,"isUsOrEmployee":null,"currentCurrency":"EUR","showSellerEntryPoints":true,"preventInquirySendingWithOtp":true,"singleAgentFlow":false,"showQuestionnaireAfterInquiry":true,"previewFeaturedAgent":false});
</script>

   <script src="https://static-x.jamesedition.com/assets/dist/je2_listing_page_v2.bundle-f6ad5ddb1a1c7905f629f4232a21e8143bcb02cc4e8927d7d1477ac7e87c7610.js" async="async" type="81dfcc4b5c125fb5b214f294-text/javascript"></script>


  <script type="81dfcc4b5c125fb5b214f294-text/javascript">
  window.addEventListener("load", () => {
      setTimeout(() => {
          const loader = document.createElement("script");
          loader.src = "https://accounts.google.com/gsi/client";
          loader.async = true;
          loader.defer = true;
          document.body.appendChild(loader);
      },2000);
  });
</script>

  <div id="g_id_onload" data-client_id="193019720404-9qm8r0ovhh67sdh5hent9vc9akiskg2l.apps.googleusercontent.com" data-auto_select="true" data-use_fedcm_for_prompt="true" data-login_uri="https://www.jamesedition.com/auth/google/using_one_tap" data-after_auth_redirect_url="https://www.jamesedition.com/real_estate/angouleme-france/luxury-family-estate-with-heated-pool-and-outbuildings-in-vars-near-angouleme-16460690"></div>



<script type="81dfcc4b5c125fb5b214f294-text/javascript">
    const connection = window.navigator.connection || window.navigator.mozConnection || window.navigator.webkitConnection || {};

    if (!connection) window.navigator.connection = {};

    if (!connection.effectiveType) {
        window.navigator.connection = { effectiveType: '4g' };
        const trigger = setTimeout(() => window.navigator.connection.effectiveType =  '2g', 5000); // set to 2g if there is no "load" event in 5 sec
        window.addEventListener("load", () => clearTimeout(trigger) );
    }
</script>

<script type="81dfcc4b5c125fb5b214f294-text/javascript">
    JEParams.canLoadImmediately = false;
    if (document.readyState !== "complete") window.addEventListener("load", () => setTimeout(() => (JEParams.canLoadImmediately = true), 2000));
    else setTimeout(() => (JEParams.canLoadImmediately = true), 2000)
</script>

<script type="application/ld+json">
  {
    "@context" : "http://schema.org",
    "@type" : "Organization",
    "name" : "JamesEdition",
    "alternateName": ["JE", "James Edition"],
    "url" : "https://www.jamesedition.com/",
    "logo" : "https://assets.jamesedition.com/android-chrome-512x512.png",
    "sameAs": [
      "https://www.facebook.com/thejamesedition",
      "https://twitter.com/JamesEdition",
      "https://www.instagram.com/jameseditioncom/",
      "https://pinterest.com/jamesedition/"
    ],
    "address": {
      "@type": "PostalAddress",
      "postalCode": "1043NX",
      "addressCountry": "The Netherlands",
      "addressLocality": "Amsterdam",
      "streetAddress": "Radarweg 29"
    },
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+31 85 888 5346",
      "contactType": "Customer Service",
      "areaServed": "Worldwide"
    },
    "foundingDate": "2008",
    "foundingLocation": "Stockholm, Sweden",
    "email": "support@jamesedition.com"
  }
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "JamesEdition: Luxury Homes",
  "operatingSystem": "iOS",
  "applicationCategory": "LifestyleApplication",
  "applicationSubCategory": "RealEstateListing",
  "url": "https://www.jamesedition.com/",
  "downloadUrl": "https://apps.apple.com/app/jamesedition-luxury-homes/id6737836918",
  "installUrl": "ios-app://6737836918",
  "identifier": "ios:6737836918",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "10"
  },
  "publisher": {
    "@type": "Organization",
    "name": "JamesEdition B.V.",
    "url": "https://www.jamesedition.com"
  },
  "screenshot": [
    "https://assets.jamesedition.com/app/app_screenshot_1.webp",
    "https://assets.jamesedition.com/app/app_screenshot_2.webp",
    "https://assets.jamesedition.com/app/app_screenshot_3.webp",
    "https://assets.jamesedition.com/app/app_screenshot_4.webp"
  ],
  "description": "Discover the world’s finest luxury properties with JamesEdition. Browse exclusive listings, save searches, and connect with top agents — all in one seamless experience."
}
</script>

  <script src="/cdn-cgi/scripts/7d0fa10a/cloudflare-static/rocket-loader.min.js" data-cf-settings="81dfcc4b5c125fb5b214f294-|49" defer></script></body>
</html>
    """
    result = extract_xpaths(list_html, detail_html)
    # save this result to a json file
    import json
    json_file = "extracted_xpaths.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(json.dumps(result, indent=2, ensure_ascii=False))
