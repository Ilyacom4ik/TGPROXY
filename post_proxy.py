#!/usr/bin/env python3
import os
import re
import requests

# ===== НАСТРОЙКИ =====
RU_URL = "https://raw.githubusercontent.com/Ilyacom4ik/TGPROXY/refs/heads/main/proxy_ru.txt"
EU_URL = "https://raw.githubusercontent.com/Ilyacom4ik/TGPROXY/refs/heads/main/proxy_eu.txt"
# =====================

def get_country(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                cc = data.get("countryCode", "").lower()
                flags = {"ru": "🇷🇺", "nl": "🇳🇱", "us": "🇺🇸", "de": "🇩🇪",
                         "fi": "🇫🇮", "fr": "🇫🇷", "gb": "🇬🇧", "ca": "🇨🇦",
                         "jp": "🇯🇵", "sg": "🇸🇬"}
                flag = flags.get(cc, "🌍")
                return f"{data.get('country', 'Неизвестно')} {flag}"
        return "🌍 Неизвестно"
    except:
        return "🌍 Неизвестно"

def extract_ip(proxy):
    match = re.search(r'server=([^&]+)', proxy)
    return match.group(1) if match else None

def fetch_proxies(url, limit):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            proxies = [line.strip() for line in r.text.splitlines() if line.strip().startswith("tg://proxy?")]
            return proxies[:limit]
        return []
    except:
        return []

def send_to_telegram(proxies):
    token = os.environ.get('TG_BOT_TOKEN')
    chat_id = os.environ.get('TG_PROXY_CHAT_ID')
    topic_id = os.environ.get('TG_PROXY_TOPIC_ID')  # ДОБАВЛЕНО
    
    if not token or not chat_id:
        print("❌ Не хватает секретов")
        return

    keyboard = []
    for i, proxy in enumerate(proxies, 1):
        ip = extract_ip(proxy)
        country = get_country(ip) if ip else "🌍 Неизвестно"
        keyboard.append([{"text": f"🔵 {country}", "url": proxy}])

    keyboard.append([{"text": "📢 Наш канал", "url": "https://t.me/FreeCFGHub"}])

    payload = {
        "chat_id": chat_id,
        "text": "✅ <b>Свежие MTProto прокси</b>\n\n📌 Нажми на кнопку с нужной страной",
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": keyboard}
    }
    
    # ДОБАВЛЕНО: если есть topic_id — отправляем в конкретную тему
    if topic_id:
        payload["message_thread_id"] = int(topic_id)

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
    ru = fetch_proxies(RU_URL, 3)
    eu = fetch_proxies(EU_URL, 2)
    all_proxies = ru + eu
    if all_proxies:
        send_to_telegram(all_proxies)
    else:
        print("❌ Прокси не найдены")
