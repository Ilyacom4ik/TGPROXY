#!/usr/bin/env python3
import os
import re
import requests
import random

# ===== НАСТРОЙКИ =====
RU_URL = "https://raw.githubusercontent.com/Ilyacom4ik/TGPROXY/refs/heads/main/proxy_ru.txt"
EU_URL = "https://raw.githubusercontent.com/Ilyacom4ik/TGPROXY/refs/heads/main/proxy_eu.txt"

MIN_RU_PROXIES = 2   # Минимум прокси из России
TOTAL_PROXIES = 5    # Всего прокси в посте

# Жёсткая привязка (замени на свои данные)
FORCE_CHAT_ID = "-1003700039599"
FORCE_TOPIC_ID = 63
# =====================

# ========== ВСЕ ФЛАГИ СТРАН МИРА ==========
FLAGS = {
    # Европа
    "ru": "🇷🇺", "nl": "🇳🇱", "us": "🇺🇸", "de": "🇩🇪",
    "fi": "🇫🇮", "fr": "🇫🇷", "gb": "🇬🇧", "ca": "🇨🇦",
    "jp": "🇯🇵", "sg": "🇸🇬", "ro": "🇷🇴", "ae": "🇦🇪",
    "pl": "🇵🇱", "it": "🇮🇹", "es": "🇪🇸", "se": "🇸🇪",
    "no": "🇳🇴", "dk": "🇩🇰", "be": "🇧🇪", "at": "🇦🇹",
    "ch": "🇨🇭", "cz": "🇨🇿", "gr": "🇬🇷", "pt": "🇵🇹",
    "hu": "🇭🇺", "tr": "🇹🇷", "il": "🇮🇱", "in": "🇮🇳",
    "br": "🇧🇷", "au": "🇦🇺", "nz": "🇳🇿", "za": "🇿🇦",
    "ie": "🇮🇪", "lu": "🇱🇺", "ua": "🇺🇦", "by": "🇧🇾",
    "lt": "🇱🇹", "lv": "🇱🇻", "ee": "🇪🇪", "bg": "🇧🇬",
    "rs": "🇷🇸", "hr": "🇭🇷", "si": "🇸🇮", "sk": "🇸🇰",
    "is": "🇮🇸", "mt": "🇲🇹", "al": "🇦🇱", "mk": "🇲🇰",
    "ba": "🇧🇦", "md": "🇲🇩", "am": "🇦🇲", "ge": "🇬🇪",
    "az": "🇦🇿", "cy": "🇨🇾",
    # Азия
    "cn": "🇨🇳", "hk": "🇭🇰", "mo": "🇲🇴", "tw": "🇹🇼",
    "kr": "🇰🇷", "kp": "🇰🇵", "mn": "🇲🇳", "vn": "🇻🇳",
    "th": "🇹🇭", "my": "🇲🇾", "id": "🇮🇩", "ph": "🇵🇭",
    "la": "🇱🇦", "kh": "🇰🇭", "mm": "🇲🇲", "bn": "🇧🇳",
    "tl": "🇹🇱", "pk": "🇵🇰", "bd": "🇧🇩", "lk": "🇱🇰",
    "np": "🇳🇵", "bt": "🇧🇹", "mv": "🇲🇻", "kz": "🇰🇿",
    "kg": "🇰🇬", "tj": "🇹🇯", "uz": "🇺🇿", "tm": "🇹🇲",
    "af": "🇦🇫", "ir": "🇮🇷", "iq": "🇮🇶", "kw": "🇰🇼",
    "sa": "🇸🇦", "ye": "🇾🇪", "om": "🇴🇲", "qa": "🇶🇦",
    "bh": "🇧🇭", "jo": "🇯🇴", "lb": "🇱🇧", "sy": "🇸🇾",
    "ps": "🇵🇸",
    # Америка
    "mx": "🇲🇽", "gt": "🇬🇹", "bz": "🇧🇿", "sv": "🇸🇻",
    "hn": "🇭🇳", "ni": "🇳🇮", "cr": "🇨🇷", "pa": "🇵🇦",
    "cu": "🇨🇺", "jm": "🇯🇲", "ht": "🇭🇹", "do": "🇩🇴",
    "pr": "🇵🇷", "bs": "🇧🇸", "tt": "🇹🇹", "bb": "🇧🇧",
    "lc": "🇱🇨", "vc": "🇻🇨", "gd": "🇬🇩", "ag": "🇦🇬",
    "dm": "🇩🇲", "kn": "🇰🇳", "co": "🇨🇴", "ve": "🇻🇪",
    "gy": "🇬🇾", "sr": "🇸🇷", "ec": "🇪🇨", "pe": "🇵🇪",
    "bo": "🇧🇴", "py": "🇵🇾", "cl": "🇨🇱", "ar": "🇦🇷",
    "uy": "🇺🇾",
    # Африка
    "eg": "🇪🇬", "ly": "🇱🇾", "tn": "🇹🇳", "dz": "🇩🇿",
    "ma": "🇲🇦", "mr": "🇲🇷", "sn": "🇸🇳", "gm": "🇬🇲",
    "gw": "🇬🇼", "gn": "🇬🇳", "ml": "🇲🇱", "bf": "🇧🇫",
    "ne": "🇳🇪", "td": "🇹🇩", "sd": "🇸🇩", "ss": "🇸🇸",
    "er": "🇪🇷", "dj": "🇩🇯", "so": "🇸🇴", "et": "🇪🇹",
    "ke": "🇰🇪", "ug": "🇺🇬", "rw": "🇷🇼", "bi": "🇧🇮",
    "tz": "🇹🇿", "mz": "🇲🇿", "mw": "🇲🇼", "zm": "🇿🇲",
    "zw": "🇿🇼", "na": "🇳🇦", "bw": "🇧🇼", "sz": "🇸🇿",
    "ls": "🇱🇸", "mg": "🇲🇬", "km": "🇰🇲", "mu": "🇲🇺",
    "sc": "🇸🇨",
    # Австралия и Океания
    "pg": "🇵🇬", "sb": "🇸🇧", "fj": "🇫🇯", "vu": "🇻🇺",
    "nc": "🇳🇨", "pf": "🇵🇫", "ws": "🇼🇸", "to": "🇹🇴",
    "ki": "🇰🇮", "fm": "🇫🇲", "mh": "🇲🇭", "pw": "🇵🇼",
    "nr": "🇳🇷", "tv": "🇹🇻",
}

def get_country(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,countryCode,country", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                cc = data.get("countryCode", "").lower()
                flag = FLAGS.get(cc, "🌍")
                return f"{data.get('country', 'Неизвестно')} {flag}"
        return "🌍 Неизвестно"
    except:
        return "🌍 Неизвестно"

def extract_ip(proxy):
    match = re.search(r'server=([^&]+)', proxy)
    return match.group(1) if match else None

def fetch_proxies(url, limit=None):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            proxies = [line.strip() for line in r.text.splitlines() if line.strip().startswith("tg://proxy?")]
            if limit:
                return proxies[:limit]
            return proxies
        return []
    except:
        return []

def send_to_telegram(proxies):
    token = os.environ.get('TG_BOT_TOKEN')
    
    if not token:
        print("❌ Нет TG_BOT_TOKEN")
        return

    keyboard = []
    for proxy in proxies:
        ip = extract_ip(proxy)
        country = get_country(ip) if ip else "🌍 Неизвестно"
        keyboard.append([{"text": f"🔵 {country}", "url": proxy}])

    keyboard.append([{"text": "📢 Наш канал", "url": "https://t.me/FreeCFGHub"}])

    payload = {
        "chat_id": FORCE_CHAT_ID,
        "message_thread_id": FORCE_TOPIC_ID,
        "text": "✅ <b>Свежие MTProto прокси</b>\n\n📌 Нажми на кнопку с нужной страной",
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": keyboard}
    }

    print(f"DEBUG: Отправляем в чат {FORCE_CHAT_ID}, тему {FORCE_TOPIC_ID}")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            print(f"✅ Отправлено {len(proxies)} прокси")
        else:
            print(f"❌ Ошибка: {resp.text}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    # Загружаем ВСЕ прокси из обоих источников
    all_ru = fetch_proxies(RU_URL)
    all_eu = fetch_proxies(EU_URL)
    
    print(f"📊 Загружено: RU = {len(all_ru)}, EU = {len(all_eu)}")
    
    if len(all_ru) < MIN_RU_PROXIES:
        print(f"⚠️ Внимание: в RU всего {len(all_ru)} прокси, будет взято сколько есть")
    
    # ВЫБИРАЕМ РАНДОМНО из России
    if len(all_ru) >= MIN_RU_PROXIES:
        ru_selected = random.sample(all_ru, MIN_RU_PROXIES)
    else:
        ru_selected = all_ru.copy() if all_ru else []
    
    # Сколько ещё прокси нужно добить из Европы
    needed = TOTAL_PROXIES - len(ru_selected)
    
    # ВЫБИРАЕМ РАНДОМНО из Европы
    if needed > 0 and all_eu:
        if len(all_eu) >= needed:
            eu_selected = random.sample(all_eu, needed)
        else:
            eu_selected = all_eu.copy()
    else:
        eu_selected = []
    
    # Если всё равно не хватает — добиваем из России (рандомно из оставшихся)
    final_proxies = ru_selected + eu_selected
    if len(final_proxies) < TOTAL_PROXIES and len(all_ru) > len(ru_selected):
        remaining_ru = [p for p in all_ru if p not in ru_selected]
        extra_needed = TOTAL_PROXIES - len(final_proxies)
        if remaining_ru:
            extra = random.sample(remaining_ru, min(extra_needed, len(remaining_ru)))
            final_proxies += extra
    
    # Перемешиваем финальный порядок
    random.shuffle(final_proxies)
    
    print(f"✅ Итоговых прокси: {len(final_proxies)} (Россия: {len(ru_selected)}, Европа: {len(eu_selected)})")
    
    if final_proxies:
        send_to_telegram(final_proxies)
    else:
        print("❌ Прокси не найдены")
