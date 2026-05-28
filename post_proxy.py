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
# =====================

def get_country(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                cc = data.get("countryCode", "").lower()
                flags = {
                    "ru": "🇷🇺", "nl": "🇳🇱", "us": "🇺🇸", "de": "🇩🇪",
                    "fi": "🇫🇮", "fr": "🇫🇷", "gb": "🇬🇧", "ca": "🇨🇦",
                    "jp": "🇯🇵", "sg": "🇸🇬", "ro": "🇷🇴", "ae": "🇦🇪",
                    "pl": "🇵🇱", "it": "🇮🇹", "es": "🇪🇸", "se": "🇸🇪",
                    "no": "🇳🇴", "dk": "🇩🇰", "be": "🇧🇪", "at": "🇦🇹",
                    "ch": "🇨🇭", "cz": "🇨🇿", "gr": "🇬🇷", "pt": "🇵🇹",
                    "hu": "🇭🇺", "tr": "🇹🇷", "il": "🇮🇱", "in": "🇮🇳",
                    "br": "🇧🇷", "au": "🇦🇺", "nz": "🇳🇿", "za": "🇿🇦"
                }
                flag = flags.get(cc, "🌍")
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
    chat_id = os.environ.get('TG_PROXY_CHAT_ID')
    topic_id = os.environ.get('TG_PROXY_TOPIC_ID')
    
    if not token or not chat_id:
        print("❌ Не хватает секретов")
        return

    keyboard = []
    for proxy in proxies:
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
    # Загружаем ВСЕ прокси из обоих источников
    all_ru = fetch_proxies(RU_URL)
    all_eu = fetch_proxies(EU_URL)
    
    print(f"📊 Загружено: RU = {len(all_ru)}, EU = {len(all_eu)}")
    
    # Берём минимум MIN_RU_PROXIES из России
    ru_selected = all_ru[:MIN_RU_PROXIES] if len(all_ru) >= MIN_RU_PROXIES else all_ru
    
    # Сколько ещё прокси нужно добить из Европы
    needed = TOTAL_PROXIES - len(ru_selected)
    eu_selected = all_eu[:needed] if needed > 0 else []
    
    # Если всё равно не хватает — добиваем из России (если есть)
    final_proxies = ru_selected + eu_selected
    if len(final_proxies) < TOTAL_PROXIES and len(all_ru) > len(ru_selected):
        extra = all_ru[len(ru_selected):TOTAL_PROXIES - len(eu_selected)]
        final_proxies += extra
    
    # Перемешиваем, чтобы порядок был случайным
    random.shuffle(final_proxies)
    
    print(f"✅ Итоговых прокси: {len(final_proxies)} (Россия: {len(ru_selected)}, Европа: {len(eu_selected)})")
    
    if final_proxies:
        send_to_telegram(final_proxies)
    else:
        print("❌ Прокси не найдены")
