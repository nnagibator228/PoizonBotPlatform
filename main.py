import os

def proceed_bool_env(env):
    if env.lower() in ['true', '1']: return True
    elif env.lower() in ['false', '0']: return False
    else: return None

envs = os.environ
token = envs['TOKEN'] if 'TOKEN' in envs else None
collection_token = envs['COLTOKEN'] if 'COLTOKEN' in envs else "None"
about_text = envs['ABOUT'] if 'ABOUT' in envs else "powered by poizonbot"
info_text = envs['INFO'] if 'INFO' in envs else "info about poizonbot"
items_text = envs['ITEMS'] if 'ITEMS' in envs else "items are here - https://google.com"
mainmenu_text = envs['MAINMENU'] if 'MAINMENU' in envs else "Проект poizonbot"
adminpanel_username = envs['USERNAME'] if 'USERNAME' in envs else "admin"
adminpanel_password = envs['PASSWORD'] if 'PASSWORD' in envs else "@poizonbotthebest))1234"
mainimage_url = envs['MAINIMG'] if 'MAINIMG' in envs else None
aboutimage_url = envs['ABOUTIMG'] if 'ABOUTIMG' in envs else None
vk_link = envs['VKLINK'] if 'VKLINK' in envs else "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # установить ссылку на репозиторий бота
tg_link = envs['TGLINK'] if 'TGLINK' in envs else "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # установить ссылку на репозиторий бота
review_link = envs['REVIEWLINK'] if 'REVIEWLINK' in envs else "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
chat_link = envs['CHATLINK'] if 'CHATLINK' in envs else "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
admin_id = envs['ADMINID'] if 'ADMINID' in envs else None
use_extended_formula = proceed_bool_env(envs['EXTFORMULA']) if 'EXTFORMULA' in envs and proceed_bool_env(envs['EXTFORMULA']) is not None else True

base_url = "https://api.telegram.org/bot"

url=f"{base_url}{token}/sendMessage"
url_image=f"{base_url}{token}/sendPhoto"

from EmojiCaptcha import EmojiCaptcha
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
from deta import Deta
import requests
import secrets
import shutil
import html
import json
import re
from pydantic import BaseModel

if (collection_token != "None") and (collection_token is not None):
    deta = Deta(collection_token)
else:
    deta = Deta()
user_db = deta.Base('UserDB')
all_orders = deta.Base('AllOrders')
confirmed_orders = deta.Base('ConfirmedOrders')
user_tmp = deta.Drive("usertmp")
config_storage = deta.Drive('confstor')

app = FastAPI()
security = HTTPBasic()

emojis = ['🃏', '🎤', '🎥', '🎨', '🎩', '🎬', '🎭', '🎮', '🎯', '🎱', '🎲', '🎷', '🎸', '🎹', '🎾', '🏀', '🏆', '🏈', '🏉', '🏐', '🏓', '💠', '💡', '💣', '💨', '💸', '💻', '💾', '💿', '📈', '📉', '📊', '📌', '📍', '📎', '📏', '📐', '📞', '📟', '📠', '📡', '📢', '📣', '📦', '📹', '📺', '📻', '📼', '📽', '🖥', '🖨', '🖲', '🗂', '🗃', '🗄', '🗜', '🗝', '🗡', '🚧', '🚨', '🛒', '🛠', '🛢', '🧀', '🌭', '🌮', '🌯', '🌺', '🌻', '🌼', '🌽', '🌾', '🌿', '🍊', '🍋', '🍌', '🍍', '🍎', '🍏', '🍚', '🍛', '🍜', '🍝', '🍞', '🍟', '🍪', '🍫', '🍬', '🍭', '🍮', '🍯', '🍺', '🍻', '🍼', '🍽', '🍾', '🍿', '🎊', '🎋', '🎍', '🎏', '🎚', '🎛', '🎞', '🐌', '🐍', '🐎', '🐚', '🐛', '🐝', '🐞', '🐟', '🐬', '🐭', '🐮', '🐯', '🐻', '🐼', '🐿', '👛', '👜', '👝', '👞', '👟', '💊', '💋', '💍', '💎', '🔋', '🔌', '🔪', '🔫', '🔬', '🔭', '🔮', '🕯', '🖊', '🖋', '🖌', '🖍', '🥚', '🥛', '🥜', '🥝', '🥞', '🦊', '🦋', '🦌', '🦍', '🦎', '🦏', '🌀', '🌂', '🌑', '🌕', '🌡', '🌤', '⛅️', '🌦', '🌧', '🌨', '🌩', '🌰', '🌱', '🌲', '🌳', '🌴', '🌵', '🌶', '🌷', '🌸', '🌹', '🍀', '🍁', '🍂', '🍃', '🍄', '🍅', '🍆', '🍇', '🍈', '🍉', '🍐', '🍑', '🍒', '🍓', '🍔', '🍕', '🍖', '🍗', '🍘', '🍙', '🍠', '🍡', '🍢', '🍣', '🍤', '🍥', '🍦', '🍧', '🍨', '🍩', '🍰', '🍱', '🍲', '🍴', '🍵', '🍶', '🍷', '🍸', '🍹', '🎀', '🎁', '🎂', '🎃', '🎄', '🎈', '🎉', '🎒', '🎓', '🎙', '🐀', '🐁', '🐂', '🐃', '🐄', '🐅', '🐆', '🐇', '🐕', '🐉', '🐓', '🐖', '🐗', '🐘', '🐙', '🐠', '🐡', '🐢', '🐣', '🐤', '🐥', '🐦', '🐧', '🐨', '🐩', '🐰', '🐱', '🐴', '🐵', '🐶', '🐷', '🐸', '🐹', '👁\u200d🗨', '👑', '👒', '👠', '👡', '👢', '💄', '💈', '🔗', '🔥', '🔦', '🔧', '🔨', '🔩', '🔰', '🔱', '🕰', '🕶', '🕹', '🖇', '🚀', '🤖', '🥀', '🥁', '🥂', '🥃', '🥐', '🥑', '🥒', '🥓', '🥔', '🥕', '🥖', '🥗', '🥘', '🥙', '🦀', '🦁', '🦂', '🦃', '🦄', '🦅', '🦆', '🦇', '🦈', '🦉', '🦐', '🦑', '⭐️', '⏰', '⏲', '⚠️', '⚡️', '⚰️', '⚽️', '⚾️', '⛄️', '⛅️', '⛈', '⛏', '⛓', '⌚️', '☎️', '⚜️', '✏️', '⌨️', '☁️', '☃️', '☄️', '☕️', '☘️', '☠️', '♨️', '⚒', '⚔️', '⚙️', '✈️', '✉️', '✒️']

reply_keyboard_buttons = {
  "🧮 Калькулятор" : "/calculator",
  "⚡️ Заказать" : "/order",
  "📦 Товары в наличии" : "/items",
  "ℹ️ О нас" : "/about",
  "💬 Чат и отзывы" : "/contact",
  "🛟 FAQ" : "/faq"
}

class sendMessage(BaseModel):
    update_id: int
    message: Optional[dict] = None
    callback_query: Optional[dict] = None

user_json_model = {
    "order": {
        "type": None,
        "link": None,
        "size": None,
        "price": None,
        "fio": None,
        "adress": None,
        "number": None,
        "captcha_answer": None,
    },
    "calc": {
        "type": None,
        "price": None
    }
}

item_weight = {
    "sneaker": 2000,
    "boot": 3000,
    "winterJacket": 1750,
    "jacket": 1350,
    "cotton": 450,
    "laptop": 3250,
    "smartphone": 300,
    "accessory": 250
}

item_size_type = {
    "sneaker": "number",
    "boot": "number",
    "winterJacket": "size",
    "jacket": "size",
    "cotton": "size",
    "laptop": None,
    "smartphone": None,
    "accessory": None
}
def check_regex(regex, string):
  pattern = re.compile(regex)
  if pattern.fullmatch(string):
    return True
  else:
    return False

price_config_path = 'price_conf.json'


def get_price_var(key: str) -> float | None:
    prices_deta = config_storage.get(price_config_path)
    if prices_deta is None:
        default_price_config = {
            "kg_cost": 750.0,
            "change": 11.5,
            "commission": 700,
        }
        raw_json = json.dumps(default_price_config)
        config_storage.put(price_config_path, raw_json)
        if key in default_price_config:
            return default_price_config[key]
        else:
            return None
    price_config = json.loads(prices_deta.read())
    prices_deta.close()
    if key in price_config:
        return price_config[key]
    else:
        return None


def get_price_vars(*keys: str) -> tuple | None:
    prices_deta = config_storage.get(price_config_path)
    if prices_deta is None:
        default_price_config = {
            "kg_cost": 750.,
            "change": 11.5,
            "commission": 700.,
        }
        raw_json = json.dumps(default_price_config)
        config_storage.put(price_config_path, raw_json)

        if not all(key in default_price_config for key in keys):
            return None
        return tuple(default_price_config[key] for key in keys)

    price_config = json.loads(prices_deta.read())
    prices_deta.close()
    if not all(key in price_config for key in keys):
        return None
    return tuple(price_config[key] for key in keys)

def set_price_var(key: str, value: float):
    prices_deta = config_storage.get(price_config_path)
    if prices_deta is None:
        raise IOError
    price_config = json.loads(prices_deta.read())
    prices_deta.close()
    if key not in price_config:
        raise KeyError

    price_config[key] = value
    config_storage.put(price_config_path, price_config)

def order_formula(type, price):
    price_vars = get_price_vars('commission', 'kg_cost', 'change')
    if price_vars is None:
        raise KeyError
    commission, kg_cost, change = price_vars
    if use_extended_formula:
        final_price = commission+((item_weight[type]/1000)*kg_cost)+(price*change)
    else:
        final_price = price * change + commission
    return final_price

def copy_file(current_path, new_path):
    shutil.copyfile(f"{str(current_path)}", f"{str(new_path)}")

def create_userfile(id):
    filename = str(id)+'.json'
    return user_tmp.put(name=filename, data=json.dumps(user_json_model), content_type="application/json")

def download_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        with open(f'/tmp/{filename}.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    except Exception as e:
        copy_file(f"./{filename}.png", f"/tmp/{filename}.png")

def add_admin(id):
    user = user_db.put({
        "key": str(id),
        "state": "MAIN_MENU",
        "lvl": "admin"
    })
    create_userfile(id)
    return user

if mainimage_url is not None:
    download_image(mainimage_url, "main")
else:
    copy_file("./main.png", "/tmp/main.png")

if aboutimage_url is not None:
    download_image(aboutimage_url, "about")
else:
    copy_file("./about.png", "/tmp/about.png")

if admin_id is not None:
    add_admin(admin_id)

# ------------------------------- DATA CONTROL FUNCTIONS -------------------------------

# ~USER FUNCTIONS~
def modify_userfile(id, val, field, category=None):
    filename = str(id)+'.json'
    file = json.loads(json.load(user_tmp.get(name=filename)))
    if category is None:
        file[field]=val
    else:
        file[category][field]=val
    return user_tmp.put(name=filename, data=json.dumps(file), content_type="application/json")

def get_userfile(id):
    filename = str(id)+'.json'
    file = json.loads(json.load(user_tmp.get(name=filename)))
    return file

def add_user(id):
    user = user_db.put({
        "key": str(id),
        "state": "MAIN_MENU",
        "lvl": "user"
    })
    create_userfile(id)
    return user

def get_user(id):
    user = user_db.get(str(id))
    return user if user else None

def change_user_state(id, state):
    user_old = get_user(id)
    user = user_db.put({
        "state": state,
        "lvl": user_old["lvl"]
    }, str(id))
    return user

def get_admins():
    admins = user_db.fetch({"lvl": "admin"})
    return admins if admins else None

def add_order(id, type, link, size, price, fio, adress, number):
    order = all_orders.put({
        "id": str(id),
        "data": {
            "product_type": type,
            "product_link": link,
            "product_size": size,
            "price": price,
            "fio": fio,
            "ship_to": adress,
            "phone_number": number
        }
    })
    return order

def get_order(key):
    order = all_orders.get(str(key))
    return order if order else None

def confirm_order(id, key):
    order_from_all_orders = get_order(key)
    confirmed_order = None
    if order_from_all_orders is not None:
        send_confirm_prompt(order_from_all_orders["id"], order_from_all_orders)
        send_text(id, f"Заказ номер `{key}` подтверждён. Спасибо!")
        all_orders.delete(str(key))
        confirmed_order = confirmed_orders.put({
            "id": str(order_from_all_orders["id"]),
            "data": {
                "product_type": order_from_all_orders["data"]["product_type"],
                "product_link": order_from_all_orders["data"]["product_link"],
                "product_size": order_from_all_orders["data"]["product_size"],
                "price": order_from_all_orders["data"]["price"],
                "fio": order_from_all_orders["data"]["fio"],
                "ship_to": order_from_all_orders["data"]["ship_to"],
                "phone_number": order_from_all_orders["data"]["phone_number"]
            }
        })
    else:
        send_text(id, f"Заказ номер `{key}` уже обработан либо не найден.")
    return confirmed_order

def decline_order(id, key):
    parsed_order = get_order(key)
    deleted_order = None
    if parsed_order is not None:
        send_decline_prompt(parsed_order["id"], parsed_order)
        deleted_order = all_orders.delete(str(key))
    content = send_text(id, f"Заказ номер `{key}` отклонён. Спасибо!")
    return content, deleted_order

def fetch_orders(filter: dict = None):
    orders = all_orders.fetch(filter)
    return orders if orders else None

def fetch_confirmed_orders(filter: dict = None):
    confirm_orders = confirmed_orders.fetch(filter)
    return confirm_orders if confirm_orders else None

# ------------------------------- MESSAGE FUNCTIONS -------------------------------
def init_user(id):
    if get_user(id) is None:
        add_user(id)
        create_userfile(id)
    else:
        change_user_state(id, "MAIN_MENU")
    return display_menu(id)

def display_menu(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '🧮 Калькулятор стоимости', 'callback_data': 'calculator'}],
            [{'text': '🛒 Оформить заказ', 'callback_data': 'makeorder'}],
            [{'text': '👥 Информация о компании, гарантии', 'callback_data': 'about'}],
            [{'text': '❓ Как заказать?', 'callback_data': 'howtoorder'}]
        ],
        'keyboard': [[{"text": k, "callback_data": v} for k, v in list(reply_keyboard_buttons.items())[i:i+2]] for i in range(0, len(reply_keyboard_buttons), 2)],
        "is_persistent": True,
        "resize_keyboard": True
    })
    mes_params = {
        "caption": str(mainmenu_text),
        "parse_mode": "markdown",
        "reply_markup": reply
    }
    resp = requests.post(url_image+(f"?chat_id={id}"), files={'photo': open("/tmp/main.png", 'rb')}, params=mes_params)
    return resp.content


def send_ordertype_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'Кроссовки', 'callback_data': 'sneaker'}, {'text': 'Ботинки', 'callback_data': 'boot'}],
            [{'text': 'Пуховик', 'callback_data': 'winterJacket'}, {'text': 'Куртка', 'callback_data': 'jacket'}],
            [{'text': 'Одежда', 'callback_data': 'cotton'}, {'text': 'Ноутбук', 'callback_data': 'laptop'}],
            [{'text': 'Смартфон', 'callback_data': 'smartphone'}, {'text': 'Аксессуар/Парфюмерия', 'callback_data': 'accessory'}],
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "👀 Выберите категорию товара:",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_orderprice_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'ℹ️ Как узнать цену своего размера?', 'callback_data': 'instruction'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "🏷️ Введите цену товара в юанях:",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def main_send_orderprice_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "🏷️ Введите цену товара в юанях:",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_ordercost_prompt(id, price):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '↩️ Главное меню', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": f"Итоговая стоимость в рублях: `{int(price)}₽`\n Цена без учета доставки по РФ.",
    "parse_mode": "markdown",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def escape_special_chars(text):
   text = html.escape(text)
   return text

def send_text(id, text="Test"):
    mes_params = {
    "chat_id": id,
    "parse_mode": "HTML",
    "text": escape_special_chars(text)
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_captcha_prompt(id):
    try:
        captcha = EmojiCaptcha(file_name=f"captcha{id}", background="./background.png")
        generated_captcha = captcha.generate()
    except Exception as e:
        resp = str(e)

    reply = json.dumps({'inline_keyboard': [
            [{'text': str(i), 'callback_data': str(i)} for i in generated_captcha.variants]
        ]
    })
    mes_params = {
        "caption": "🤖 Подтвердите свою человечность!\nНажмите на эмодзи, соответствующий изображению.",
        "reply_markup": reply
    }
    resp = requests.post(url_image+(f"?chat_id={id}"), files={'photo': open(f"/tmp/captcha{id}.png", 'rb')}, params=mes_params).content
    generated_captcha.remove()
    modify_userfile(id, generated_captcha.answer, "captcha_answer", "order")
    return resp

def send_ordersize_prompt(id):
    type = get_userfile(id)["order"]["type"]
    text = ""
    if item_size_type[type] == "number":
        text = "📏 Введите размер (от 16 до 63)"
    elif item_size_type[type] == "size":
        text = "📏 Введите размер (от XXXS до XXXL)"
    elif item_size_type[type] == None:
        text = "📏 Введите модель товара. Если у товара нет модели — введите слово \"Нет\""
    else:
        text = "Неверный тип товара."
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'ℹ️ Как узнать цену своего размера?', 'url': 'https://telegra.ph/Kak-oformit-zakaz-s-DEWU-Poizon-01-10#%D0%9A%D0%B0%D0%BA-%D1%83%D0%B7%D0%BD%D0%B0%D1%82%D1%8C-%D1%81%D1%82%D0%BE%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C-%D0%BD%D1%83%D0%B6%D0%BD%D0%BE%D0%B3%D0%BE-%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%80%D0%B0-%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%B0'}],
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": text,
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_orderfio_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "👤 Введите Ваше ФИО",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_orderadress_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'ℹ️ Подобрать пункт выдачи', 'url': 'http://www.cdek.ru/ru/offices'}],
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "🚚 Введите адрес доставки — пункта *«СДЕК»*",
    "parse_mode": "markdown",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_ordernumber_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "📞 Введите номер телефона получателя",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_orderlink_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'Как скопировать ссылку на товар?', 'url': 'https://telegra.ph/Kak-oformit-zakaz-s-DEWU-Poizon-01-10#%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%D1%82%D1%8C%D1%81%D1%8F-%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%BE%D0%B9-%D0%BD%D0%B0-%D1%82%D0%BE%D0%B2%D0%B0%D1%80'}],
            [{'text': '❌ Отменить заказ', 'callback_data': 'mainmenu'}]
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "Введите ссылку на товар",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_admin_prompt(id, order):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '✔️ Подтвердить', 'callback_data': f"confirm{order['key']}"}, {'text': '❌ Отменить', 'callback_data': f"decline{order['key']}"}],
            [{'text': '👤 Cвязь с клиентом', 'url': f"tg://user?id={order['id']}"}]
        ]
    })
    text = f"У Вас новая заявка!\nДетали заказа номер `{order['key']}`:\n"
    text += f"*Тип заказа:* {order['data']['product_type']}\n"
    text += f"*Ссылка на товар:* {str(order['data']['product_link'])}\n"
    text += f"*Размер товара:* {order['data']['product_size']}\n"
    text += f"*Стоимость заказа (в юанях):* {order['data']['price']}¥\n"
    text += f"*ФИО клиента:* {order['data']['fio']}\n"
    text += f"*Номер телефона:* {order['data']['phone_number']}\n"
    text += f"*Пункт СДЕК:* {order['data']['ship_to']}\n"
    mes_params = {
        "chat_id": id,
        "text": text,
        "parse_mode": "markdown",
        "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)

def send_decline_prompt(id, order):
    text = f"❌ Ваш заказ номер `{order['key']}` был отклонен. Детали заказа:\n"
    text += f"*Тип заказа:* {order['data']['product_type']}\n"
    text += f"*Ссылка на товар:* {str(order['data']['product_link'])}\n"
    text += f"*Размер товара:* {order['data']['product_size']}\n"
    text += f"*Стоимость заказа (в юанях):* {order['data']['price']}¥\n"
    text += f"*ФИО клиента:* {order['data']['fio']}\n"
    text += f"*Номер телефона:* {order['data']['phone_number']}\n"
    text += f"*Пункт СДЕК:* {order['data']['ship_to']}\n"
    mes_params = {
        "chat_id": id,
        "text": text,
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)

def send_confirm_prompt(id, order):
    text = f"✔️ Ваш заказ номер `{order['key']}` был подтвержден.\n В ближайшее время с Вами свяжется администратор. Детали заказа:\n"
    text += f"*Тип заказа:* {order['data']['product_type']}\n"
    text += f"*Ссылка на товар:* {str(order['data']['product_link'])}\n"
    text += f"*Размер товара:* {order['data']['product_size']}\n"
    text += f"*Стоимость заказа (в юанях):* {order['data']['price']}¥\n"
    text += f"*ФИО заказчика:* {order['data']['fio']}\n"
    text += f"*Номер телефона для доставки:* {order['data']['phone_number']}\n"
    text += f"*Пункт СДЕК:* {order['data']['ship_to']}\n"
    mes_params = {
        "chat_id": id,
        "text": text,
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)

def send_orderconfirm_prompt(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': '✔️ Оформить', 'callback_data': 'acceptorder'}, {'text': '❌ Отменить', 'callback_data': 'cancelorder'}],
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "Подтвердите оформление заказа",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def price_calc(id):
    change_user_state(id, "CALC_ORDERTYPE")
    return send_ordertype_prompt(id)

def make_order(id):
    change_user_state(id, "ORDER_CAPTCHA")
    return send_captcha_prompt(id)

def order_type(id):
    change_user_state(id, "ORDER_ORDER_TYPE")
    return send_ordertype_prompt(id)

def send_faq(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': 'ℹ️ Как заказать товар с Poizon', 'url': 'https://telegra.ph/Kak-oformit-zakaz-s-DEWU-Poizon-01-10'}],
        ]
    })
    mes_params = {
    "chat_id": id,
    "text": "Инструкции по работе с каждой площадкой:",
    "reply_markup": reply
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_about(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': "👉🏼 Наша группа в ВК", 'url': str(vk_link)}],
            [{'text': "👉🏼 Наша группа в TG", 'url': str(tg_link)}]
        ]
    })
    mes_params = {
        "caption": str(about_text),
        "reply_markup": reply
    }
    resp = requests.post(url_image+(f"?chat_id={id}"), files={'photo': open("/tmp/about.png", 'rb')}, params=mes_params)
    return resp.content

def send_contact(id):
    reply = json.dumps({'inline_keyboard': [
            [{'text': "👉🏼 Отзывы", 'url': str(review_link)}],
            [{'text': "👉🏼 Наш чат", 'url': str(chat_link)}]
        ]
    })
    mes_params = {
        "caption": str(info_text),
        "reply_markup": reply
    }
    resp = requests.post(url_image+(f"?chat_id={id}"), files={'photo': open("/tmp/about.png", 'rb')}, params=mes_params)
    return resp.content

def display_order(id, order):
    text = f"Заказ номер `{order['key']}`:\n\n"
    text += f"*Id клиента:* {order['id']}\n"
    text += f"*Тип заказа:* {order['data']['product_type']}\n"
    text += f"*Ссылка на товар:* {str(order['data']['product_link'])}\n"
    text += f"*Размер товара:* {order['data']['product_size']}\n"
    text += f"*Стоимость заказа (в юанях):* {order['data']['price']}¥\n"
    text += f"*ФИО клиента:* {order['data']['fio']}\n"
    text += f"*Номер телефона для доставки:* {order['data']['phone_number']}\n"
    text += f"*Пункт СДЕК:* {order['data']['ship_to']}\n"
    mes_params = {
        "chat_id": id,
        "text": text,
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_parameterchange_info(id, param):
    mes_params = {
        "chat_id": id,
        "text": f"⏩ Курс ¥/₽ изменён на `{param}`",
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_parameterkgcost_info(id, param):
    mes_params = {
        "chat_id": id,
        "text": f"⏩ Цена за кг в ₽ изменена на `{param}`",
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

def send_parametercommission_info(id, param):
    mes_params = {
        "chat_id": id,
        "text": f"⏩ Стоимость коммисии изменена на `{param}`",
        "parse_mode": "markdown"
    }
    resp = requests.post(url, params=mes_params)
    return resp.content

@app.get("/")
def read_route():
    return "CHATBOT IS UP!"

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(adminpanel_username, encoding='utf-8')
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(adminpanel_password, encoding='utf-8')
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/setwhook")
def read_current_user(link: str = None, username: str = Depends(get_current_username)):
    if link is not None:
        resp = requests.get(url=f"https://api.telegram.org/bot{token}/setWebhook?url={link}")
        return f"Hello, {username}\n{resp.content}"
    else:
        return f"Hello, {username}"

@app.post("/")
def chatbot(in_message: sendMessage):
    message = in_message.message
    query = in_message.callback_query
    value = None
    if (message is not None) or (query is not None):
        if query is None:
            user = get_user(message["from"]["id"])
            if (user is None) or (user["lvl"] != "banned"):
                try:
                    value = handle_message(message)
                except Exception as e:
                    value = e
        else:
            user = get_user(query["from"]["id"])
            if (user is None) or (user["lvl"] != "banned"):
                try:
                    value = handle_queries(query)
                except Exception as e:
                    value = e
    return value

def handle_message(mess):
    answer = None
    if "entities" in mess:
        if mess["entities"][0]["type"] == "bot_command":
            answer = handle_command(mess)
        elif mess["entities"][0]["type"] == "phone_number":
            answer = handle_number(mess)
        elif mess["entities"][0]["type"] == "url":
            answer = handle_url(mess)
        else:
            answer = None
    else:
        if mess["text"] in reply_keyboard_buttons.keys():
            answer = handle_replykeyboard(mess)
        else:
            answer = handle_input(mess)
    return answer

def handle_replykeyboard(mess):
    mess["text"] = reply_keyboard_buttons[mess["text"]]
    return handle_command(mess)

def handle_command(mess):
    chat_id = mess["from"]["id"]
    user = get_user(chat_id)
    command_answer = None
    if mess["text"] == "/start":
        try:
            command_answer = init_user(chat_id)
        except Exception as e:
            command_answer = send_text(id, str(e))
    elif mess["text"] == "/menu":
        change_user_state(chat_id, "MAIN_MENU")
        command_answer = display_menu(chat_id)
    elif mess["text"] == "/calculator":
        command_answer = price_calc(chat_id)
    elif mess["text"] == "/order":
        command_answer = make_order(chat_id)
    elif mess["text"] == "/about":
        command_answer = send_about(chat_id)
    elif mess["text"] == "/items":
        command_answer = send_text(chat_id, str(items_text))
    elif mess["text"] == "/contact":
        command_answer = send_contact(chat_id)
    elif mess["text"] == "/faq":
        command_answer = send_faq(chat_id)

    if user is not None:
        if user["lvl"] == "admin":
            if mess["text"] ==  "/allorders":
                aorders = fetch_orders()
                if aorders is not None:
                    command_answer = send_text(chat_id, "⤵️ Список заказов в модерации:")
                    for order in aorders.items:
                        display_order(chat_id, order)
                else:
                    command_answer = send_text(chat_id, "🙂 Нет заказов в модерации")
            elif mess["text"] ==  "/confirmedorders":
                corders = fetch_confirmed_orders()
                if corders is not None:
                    command_answer = send_text(chat_id, "⤵️ Список активных заказов:")
                    for order in corders.items:
                        display_order(chat_id, order)
                else:
                    command_answer = send_text(chat_id, "🙂 Нет активных заказов")
            elif mess["text"].startswith("/setexchange"):
                if check_regex('\/setexchange {1}(\d{1,100})+(\.\d{1,100})?$', mess["text"]):
                    mess_split = mess["text"].split(" ")
                    change = float(mess_split[1])
                    try:
                        set_price_var("change", change)
                    except Exception as e:
                        command_answer = send_text(chat_id, f"Ошибка: {str(e)}")
                    else:
                        command_answer = send_parameterchange_info(chat_id, change)
                else:
                    command_answer = send_text(chat_id, "Ошибка в вызове команды.")
            elif mess["text"].startswith("/setkgcost"):
                if check_regex('\/setkgcost {1}(\d{1,100})+(\.\d{1,100})?$', mess["text"]):
                    mess_split = mess["text"].split(" ")
                    kg_cost = float(mess_split[1])
                    try:
                        set_price_var("commission", kg_cost)
                    except Exception as e:
                        command_answer = send_text(chat_id, f"Ошибка: {str(e)}")
                    else:
                        command_answer = send_parameterkgcost_info(chat_id, kg_cost)
                else:
                    command_answer = send_text(chat_id, "Ошибка в вызове команды.")
            elif mess["text"].startswith("/setcommission"):
                if check_regex('\/setcommission {1}(\d{1,100})+(\.\d{1,100})?$', mess["text"]):
                    mess_split = mess["text"].split(" ")
                    commission = float(mess_split[1])
                    try:
                        set_price_var("commission", commission)
                    except Exception as e:
                        command_answer = send_text(chat_id, f"Ошибка: {str(e)}")
                    else:
                        command_answer = send_parametercommission_info(chat_id, commission)
                else:
                    command_answer = send_text(chat_id, "Ошибка в вызове команды.")
    return command_answer

def handle_number(mess):
    chat_id = mess["from"]["id"]
    resp = None
    curr_state = get_user(chat_id)["state"]
    userdata = get_userfile(chat_id)
    if curr_state == "ORDER_NUMBER":
        if(check_regex('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "number", "order")
            try:
                final_price = int(order_formula(userdata["order"]["type"], userdata["order"]["price"]))
            except Exception as e:
                resp = (send_text(chat_id, "Ошибка при расчете итоговой стоимости. Попробуйте еще раз"), send_orderprice_prompt(chat_id))
            else:
                send_text(chat_id, f"Итоговая стоимость в рублях: `{final_price}₽`\n  Цена без учета доставки по РФ.")
                resp = send_orderconfirm_prompt(chat_id)
                change_user_state(chat_id, "ORDER_CONFIRM")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз"), send_ordernumber_prompt(chat_id))
    return resp

def handle_url(mess):
    chat_id = mess["from"]["id"]
    resp = None
    curr_state = get_user(chat_id)["state"]
    userdata = get_userfile(chat_id)
    if curr_state == "ORDER_LINK":
        if(check_regex('https:\/\/dw4\.co\/t\/A\/[a-zA-Z0-9]{8,10}$', mess["text"]) or check_regex('https:\/\/dwz\.cn\/[a-zA-Z0-9]{8,10}$', mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "link", "order")
            resp = send_ordersize_prompt(chat_id)
            change_user_state(chat_id, "ORDER_SIZE")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderlink_prompt(chat_id))
    return resp

def handle_input(mess):
    chat_id = mess["from"]["id"]
    resp = None
    curr_state = get_user(chat_id)["state"]
    userdata = get_userfile(chat_id)
    if curr_state == "CALC_PRICE":
        if(check_regex("([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9])", mess["text"])):
            modify_userfile(chat_id, int(mess["text"]), "price", "calc")
            userdata = get_userfile(chat_id)
            try:
                resp = send_ordercost_prompt(chat_id, order_formula(userdata["calc"]["type"], userdata["calc"]["price"]))
            except Exception as e:
                resp = (send_text(chat_id, "Ошибка при расчёте итоговой стоимости. Попробуйте еще раз."), send_orderprice_prompt(chat_id))
            else:
                change_user_state(chat_id, "MAIN_MENU")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderprice_prompt(chat_id))
    elif curr_state == "ORDER_SIZE":
        type = userdata["order"]["type"]
        regex_str = "^.{1,4095}$"
        if item_size_type[type] == "number":
            regex_str = "(1[6-9]|[2-5][0-9]|6[0-3])"
        elif item_size_type[type] == "size":
            regex_str = "(\d*(?:M|X{0,3}[SL]))(?:$|\s+.*$)"
        elif item_size_type[type] == None:
            regex_str = "^.{1,4095}$"

        if(check_regex(regex_str, mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "size", "order")
            resp = main_send_orderprice_prompt(chat_id)
            change_user_state(chat_id, "ORDER_PRICE")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_ordersize_prompt(chat_id))
    elif curr_state == "ORDER_PRICE":
        if(check_regex("([1-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9])", mess["text"])):
            modify_userfile(chat_id, int(mess["text"]), "price", "order")
            resp = send_orderfio_prompt(chat_id)
            change_user_state(chat_id, "ORDER_FIO")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), main_send_orderprice_prompt(chat_id))
    elif curr_state == "ORDER_FIO":
        if(check_regex("^.{1,4095}$", mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "fio", "order")
            resp = send_orderadress_prompt(chat_id)
            change_user_state(chat_id, "ORDER_ADRESS")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderfio_prompt(chat_id))
    elif curr_state == "ORDER_ADRESS":
        if(check_regex("^.{1,4095}$", mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "adress", "order")
            resp = send_ordernumber_prompt(chat_id)
            change_user_state(chat_id, "ORDER_NUMBER")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderadress_prompt(chat_id))
    elif curr_state == "ORDER_NUMBER":
        if(check_regex('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "number", "order")
            try:
                final_price = int(order_formula(userdata["order"]["type"], userdata["order"]["price"]))
            except Exception as e:
                resp = (send_text(chat_id, send_text(chat_id, "Ошибка при расчёте формулы. Попробуйте еще раз")), send_ordernumber_prompt(chat_id))
            else:
                send_text(chat_id, f"Итоговая стоимость c учетом доставки будет: `{final_price}₽`\n Цена не учитывает доставку сдеком от склада в России.")
                resp = send_orderconfirm_prompt(chat_id)
                change_user_state(chat_id, "ORDER_CONFIRM")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_ordernumber_prompt(chat_id))
    elif curr_state == "ORDER_LINK":
        if(check_regex('https:\/\/dw4\.co\/t\/A\/[a-zA-Z0-9]{8,10}$', mess["text"]) or check_regex('https:\/\/dwz\.cn\/[a-zA-Z0-9]{8,10}$', mess["text"])):
            modify_userfile(chat_id, str(mess["text"]), "link", "order")
            resp = send_ordersize_prompt(chat_id)
            change_user_state(chat_id,  "ORDER_SIZE")
        else:
            resp = (send_text(chat_id, "✖️ Неверное значение. Попробуйте еще раз."), send_orderlink_prompt(chat_id))
    return resp

def handle_queries(quer):
    chat_id = quer["from"]["id"]
    resp = None
    user = get_user(chat_id)
    curr_state = user["state"]
    if quer["data"] == "mainmenu":
        resp = display_menu(chat_id)
        change_user_state(chat_id, "MAIN_MENU")
    elif quer["data"] == "calculator":
        resp = price_calc(chat_id)
    elif quer["data"] == "makeorder":
        resp = make_order(chat_id)
    elif quer["data"] == "howtoorder":
        resp = send_faq(chat_id)
    elif quer["data"] == "about":
        resp = send_about(chat_id)
    elif quer["data"] == "contact":
        resp = send_contact(chat_id)
    elif quer["data"] == "items":
        resp = send_text(chat_id, str(items_text))
    elif quer["data"].startswith("confirm"):
        if user["lvl"] == "admin":
            key = quer["data"].replace("confirm", "")
            resp = confirm_order(chat_id, key)
    elif quer["data"].startswith("decline"):
        if user["lvl"] == "admin":
            key = quer["data"].replace("decline", "")
            resp = decline_order(chat_id, key)
    elif curr_state == "CALC_ORDERTYPE":
        if quer["data"] in item_weight:
            modify_userfile(chat_id, quer["data"], "type", "calc")
            resp = send_orderprice_prompt(chat_id)
            change_user_state(chat_id, "CALC_PRICE")
    elif curr_state == "ORDER_CAPTCHA":
        if quer["data"] in emojis:
            if get_userfile(chat_id)["order"]["captcha_answer"] == quer["data"]:
                resp = order_type(chat_id)
            else:
                resp = send_text(chat_id, "😖 Неправильно! Попробуйте еще раз."), send_captcha_prompt(chat_id)
    elif curr_state == "ORDER_ORDER_TYPE":
        if quer["data"] in item_weight:
            modify_userfile(chat_id, str(quer["data"]), "type", "order")
            resp = send_orderlink_prompt(chat_id)
            change_user_state(chat_id, "ORDER_LINK")
    elif curr_state == "ORDER_CONFIRM":
        if quer["data"] == "acceptorder":
            userdata = get_userfile(chat_id)
            order = add_order(str(chat_id),str(userdata["order"]["type"]), str(userdata["order"]["link"]), str(userdata["order"]["size"]), str(userdata["order"]["price"]), str(userdata["order"]["fio"]), str(userdata["order"]["adress"]), str(userdata["order"]["number"]))
            resp = send_text(chat_id, f"😃 Спасибо за Ваш заказ!\n\n Заказ номер `{order['key']}` зарегестрирован и передан на модерацию")
            admin_list = get_admins()
            if admin_list is not None:
                for admin in admin_list.items:
                    send_admin_prompt(admin["key"], order)
            change_user_state(chat_id, "MAIN_MENU")
        elif quer["data"] == "cancelorder":
            resp = send_text(chat_id, "🟢 Заказ успешно отменен"), display_menu(chat_id)
            change_user_state(chat_id, "MAIN_MENU")
    return resp
