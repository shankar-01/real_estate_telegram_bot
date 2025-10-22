# parser_config.py
# ----------------------------------------------
# Central configuration file for all websites
# Cleaned for DB storage: no line breaks, clean numbers, single-line strings
# ----------------------------------------------

import re

CLEAN_TEXT = r"re.sub(r'\s+', '', value).strip()"  # used for all text fields except description

WEBSITE_CONFIGS = {
    "jamesedition.com": {
        "fields": {
            "Название": {"xpath": r"//*[@id='overview']/div/h1/text()", "transform": CLEAN_TEXT},
            "Цена": {
                "xpath": r"//*[@id='overview']/div/div/span/text()",
                "transform": r"re.sub(r'[^0-9]', '', value)"
            },
            "Валюта": {
                "xpath": r"//*[@id='overview']/div/div/span/text()",
                "transform": r"(re.findall(r'[€$£¥]', value)[0] if re.findall(r'[€$£¥]', value) else None)"
            },
            "Площадь": {
                "xpath": r"//li[contains(text(),'sqm')][1]/text()",
                "transform": r"re.sub(r'\D', '', value)"
            },
            "Площадь земли": {
                "xpath": r"//li[contains(text(),'lot')][1]/text()",
                "transform": (
                    "re.sub(r'\D', '', value) if 'sqm' in value else "
                    "str(float(value.split(' ')[0]) * 10000) if 'ha' in value else 'Error'"
                )
            },
            "Тип объекта": {"xpath": r"//li[h3[contains(text(), 'Property type')]]/p/text()", "transform": CLEAN_TEXT},
            "Год постройки": {"xpath": r"//li[h3[contains(text(), 'Year built')]]/p/text()", "transform": CLEAN_TEXT},
            "Количество комнат": {
                "xpath": r"//li[contains(text(),'Beds')][1]/text()",
                "transform": r"re.sub(r'\D', '', value)"
            },
            "Описание": {
                "xpath": r"//*[@id='about-property']/div/div[1]/div[4]/text()",
                "transform": r"'\n'.join([v.strip() for v in value.split('\n') if v.strip()])"
            },
            "Инфраструктура": {
                "xpath": r"//*[@id='features']//ul/li/a/text() | //*[@id='features']//ul/li/span/text()",
                "transform": r"re.sub(r'\s+', ' ', value).strip()"
            },
            "С/у": {"xpath": r"//li[contains(text(),'Baths')][1]/text()", "transform": r"re.sub(r'\D', '', value)"},
            "Этаж": {"xpath": r"//li[h3[contains(text(), 'Floor')]]/p/text()", "transform": CLEAN_TEXT},
            "Локация": {
                "xpath": r"//*[@id='map']/div/div[1]/div/span/text()",
                "transform": r"re.sub(r'\s+', ' ', value.split(',')[-3].strip())"
            },
            "Координаты": {
                "xpath": r"substring-after(//*[@id='map']/div/div[1]/div/a/@href, 'query=')",
                "transform": CLEAN_TEXT
            },
            "Фото_ссылки": {"xpath": r"//picture/source[1]/@srcset", "transform": None},
            "Фото_уникальные_названия": {
                "xpath": r"//picture/source[1]/@srcset",
                "transform": r"value.split('/')[-1]"
            },
            "Контактное лицо": {"xpath": r"string(//p[@aria-label='Agent name'])", "transform": CLEAN_TEXT},
            "Телефон контактного лица": {"xpath": None, "transform": None},
            "Компания": {"xpath": r"//*[@id='listed-by']/div[2]/div[1]/div[1]/text()", "transform": CLEAN_TEXT},
            "Телефон компании": {"xpath": None, "transform": None},
        },
        "list_page_check": r"//div[contains(@class,'ListingCard')]/a[1]/@href",
        "page_query": "p",
        "next_page_xpath": "//span[@class='_next']"
    },

    "properstar.ru": {
        "fields": {
            "Название": {
                "xpath": r"//*[@id='app']//section[1]//h1/text()",
                "transform": CLEAN_TEXT
            },
            "Цена": {
                "xpath": r"//*[@class='listing-price-main']/span/text()",
                "transform": r"re.sub(r'[^0-9]', '', value)"
            },
            "Валюта": {
                "xpath": r"//*[@class='listing-price-main']/span/text()",
                "transform": r"re.sub(r'[0-9.,\s\xa0]', '', value).strip()"
            },
            "Площадь": {
                "xpath": r"//div[@class='feature-list']//div[span[contains(text(),'Жилые')]]/span[@class='property-value']/text()",
                "transform": r"re.sub(r'\D', '', value)"
            },
            "Площадь земли": {
                "xpath": r"//div[@class='feature-list']//div[span[contains(text(),'Земельный участок')]]/span[@class='property-value']/text()",
                "transform": r"re.sub(r'\D', '', value)"
            },
            "Тип объекта": {
                "xpath": r"//div[@class='feature-list']//div[span[contains(text(),'Тип')]]/span[@class='property-value']/text()",
                "transform": CLEAN_TEXT
            },
            "Год постройки": {
                "xpath": r"//div[@class='feature-list']//div[span[contains(text(),'Год постройки')]]/span[@class='property-value']/text()",
                "transform": CLEAN_TEXT
            },
            "Количество комнат": {
                "xpath": r"//div[@class='feature-list']//div[span[contains(text(),'Комнаты')]]/span[@class='property-value']/text()",
                "transform": CLEAN_TEXT
            },
            "Описание": {"xpath": r"string(//*[@class='description-text'])", "transform": r"value.strip()"},
            "Инфраструктура": {
                "xpath": r"//*[@id='app']//section[4]//span/font/font/text()",
                "transform": r"re.sub(r'\s+', '', value).strip()"
            },
            "С/у": {
                "xpath": r"//div[@class='feature-list']//div[span[contains(text(),'Ванных')]]/span[@class='property-value']/text()",
                "transform": r"re.sub(r'\D', '', value)"
            },
            "Этаж": {
                "xpath": r"//div[@class='feature-list']//div[span[contains(text(),'Этажи')]]/span[@class='property-value']/text()",
                "transform": CLEAN_TEXT
            },
            "Локация": {"xpath": r"string(//*[@class='address']/span)", "transform": r"value.split(',')[0].strip()"},
            "Координаты": {
                "xpath": r"//*[@aria-label='Map']/@style",
                "transform": r"value.split('center=')[1].split('&')[0].replace('%2C', ',')"
            },
            "Фото_ссылки": {
                "xpath": r"//picture[contains(@class, 'picture-fit')]/source/@srcset",
                "transform": None
            },
            "Фото_уникальные_названия": {
                "xpath": r"//picture[contains(@class, 'picture-fit')]/source/@srcset",
                "transform": r"value.split('/')[-1]"
            },
            "Контактное лицо": {
                "xpath": r"//*[@id='app']//section[7]//h4/font/font/text()",
                "transform": CLEAN_TEXT
            },
            "Телефон контактного лица": {"xpath": r"string(//*[@class='agent-contacts-item'])", "transform": CLEAN_TEXT},
            "Компания": {"xpath": r"string(//*[@class='account-name'])", "transform": CLEAN_TEXT},
            "Телефон компании": {"xpath": r"string(//*[@class='agency-phone phone-number'])", "transform": CLEAN_TEXT},
        },
        "list_page_check": r"//article/a/@href",
        "page_query": "p",
        "next_page_xpath": "//li[contains(@class,'next')]/a"
    }
}
