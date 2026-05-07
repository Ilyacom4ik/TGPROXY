# 🛡️ Telegram Proxy Collector: Anti-Censorship Edition

Умный комбайн для сбора MTProto прокси.  
В отличие от обычных парсеров, этот скрипт анализирует секрет (Secret) каждого прокси и определяет, под какой сайт он маскируется — это критически важно для работы в условиях жестких блокировок (DPI).

🔗 [GitHub репозиторий](https://github.com/kort0881/telegram-proxy-collector)

---

🧩 Участники и интеграции

| Роль        | Описание                                                                 | Ссылка                          |
|-------------|--------------------------------------------------------------------------|----------------------------------|
| **kort0881** | Автор и поддержка `telegram-proxy-collector` — сбор MTProto‑прокси, анализ секретов, мониторинг DPI и автоподдержка списков. | [GitHub: kort0881](https://github.com/kort0881) |
| **Runnin4ik** | Автор **DPI Detector** — инструмента для проверки цензуры трафика (TCP 16–20 KB, DNS‑подмены, TLS/HTTP‑блоки). Встроенный компонент в `telegram-proxy-collector` через `lib/dpi-detector/main.py`. | [GitHub: Runnin4ik](https://github.com/Runnin4ik) |

---

🛡️ Интегрированный DPI-тест (DPI Detector)

Этот репозиторий **включает внешний инструмент DPI Detector** как **зависимый проект** — для проверки прокси на DPI‑блокировки.

- 📦 **DPI Detector**  
  - [GitHub](https://github.com/Runnin4ik/dpi-detector)  
  - Версия: v3.3.0  
  - Лицензия: MIT ([LICENSE](https://github.com/Runnin4ik/dpi-detector/blob/main/LICENSE))

- 🔧 **Как интегрирован в `telegram-proxy-collector`**  
  - В `lib/dpi-detector/` лежит полная копия DPI Detector v3.3.0.  
  - В `main.py` вызывается через `subprocess`:
    ```python
    DPI_PATH = Path("lib/dpi-detector/main.py")
    ```
  - Каждый прокси, прошедший **Telethon‑проверку**, дополнительно проверяется через DPI Detector:
    - TCP 16–20 KB блокировка  
    - DNS‑подмена (UDP/53, DoH)  
    - TLS 1.2/1.3, HTTP  
    - Классификация ошибок: TCP RST, timeout, MITM, SNI‑блокировка  
  - Только те прокси, которые **проходят Telethon + DPI**, попадают в `proxy_ru_verified.txt`.

- 💬 **Поддержите автора DPI Detector**  
  - [GitHub Stars 💫](https://github.com/Runnin4ik/dpi-detector)  
  - [Pay CloudTips](https://pay.cloudtips.ru/p/1421d4c7)

---

🛠️ Community Tools: Утилиты от пользователей

| Инструмент                         | Описание                                                                                                      | Автор                         |
|------------------------------------|---------------------------------------------------------------------------------------------------------------|-------------------------------|
| [Parser-telegram-proxies](https://github.com/ComradeBingo/Parser-telegram-proxies-list/) | Удобная Windows-утилита для парсинга и проверки прокси с отображением пинга в реальном времени. Обновлённая версия исправляет периодические блокировки запросов к .txt со стороны GitHub (HTTP request → HTTP headers + TTL‑CDN‑обход). | [ComradeBingo](https://github.com/ComradeBingo) |
| [Proxy-Telegram-Android](https://github.com/ComradeBingo/Proxy-Telegram-Android) | Приложение для парсинга прокси для Telegram на Android с проверкой доступности и пинга серверов. | [ComradeBingo](https://github.com/ComradeBingo) |
| [Proxy-telegram-windows](https://github.com/ComradeBingo/Proxy-telegram-windows) | Парсер прокси серверов для Telegram на Windows. Обновлён до версии 1.2: переработан GUI, добавлено меню справки, лучшая стабильность парсинга. | [ComradeBingo](https://github.com/ComradeBingo) |

---

# 🔥 Актуальные списки (обновляются автоматически)

Скрипт каждый час запускается через GitHub Actions, собирает свежие MTProto‑прокси, фильтрует их и проверяет, а затем обновляет файлы в репозитории.

🔗 [GitHub Actions](https://github.com/kort0881/telegram-proxy-collector/actions)

<table>
<tr>
<th>Регион</th>
<th>Ссылка</th>
<th>Описание</th>
</tr>
<tr>
<td>🇷🇺 <b>RU Сегмент (Top Tier)</b></td>
<td><a href="https://raw.githubusercontent.com/kort0881/telegram-proxy-collector/main/proxy_ru.txt">proxy_ru.txt</a></td>
<td>Маскировка под Yandex, VK, Mail.ru, Gosuslugi и др. Лучшие для РФ и Ирана.</td>
</tr>
<tr>
<td>🇪🇺 <b>EU / Global</b></td>
<td><a href="https://raw.githubusercontent.com/kort0881/telegram-proxy-collector/main/proxy_eu.txt">proxy_eu.txt</a></td>
<td>Маскировка под Google, Amazon, Microsoft и др. Высокая скорость и стабильность.</td>
</tr>
<tr>
<td>🌍 <b>Все прокси</b></td>
<td><a href="https://raw.githubusercontent.com/kort0881/telegram-proxy-collector/main/proxy_all.txt">proxy_all.txt</a></td>
<td>Полный микс всех проверенных серверов.</td>
</tr>
</table>

⚙️ GitHub Actions сохраняет результаты в `verified/`, а затем копирует их в `proxy_ru.txt`, `proxy_eu.txt` и `proxy_all.txt` в корне репозитория, так что ссылки выше всегда ведут на свежие списки.

---

📱 Использование с телефона

Если вы открываете этот репозиторий с телефона и хотите быстро подключить MTProto‑прокси без копипасты:

1. Откройте страницу:
   - [https://kort0881.github.io/telegram-proxy-collector/mobile.html](https://kort0881.github.io/telegram-proxy-collector/mobile.html)

2. На странице вы увидите кнопки:
   - «Подключить прокси #1», «Подключить прокси #2», ...

3. При нажатии:
   - Браузер открывает ссылку `https://t.me/proxy?server=...&port=...&secret=...`
   - Telegram спрашивает: «Подключиться к прокси?» — подтвердите, и прокси будет включён.

Страница `mobile.html` автоматически читает файл `verified/proxy_links_tme_clean.txt` и превращает каждую строку в отдельную кнопку.

---

🚀 Как это работает?

Скрипт запускается каждые 4 часа через GitHub Actions и выполняет 4 этапа:

### 1. Сбор (Harvesting)
- Скачивает «сырые» прокси из нескольких открытых источников (GitHub‑репозитории, TXT, JSON‑API).
- Использует агрессивный Regex‑парсинг, чтобы вытащить MTProto‑ссылки из любого мусора: `tg://proxy`, `t.me/proxy`, `host:port:secret`, JSON.

### 2. Декодирование (Deep Analysis)
- Расшифровывает Fake‑TLS секреты (начинаются на `ee...`).
- Извлекает домен, под который маскируется трафик: Yandex, VK, Mail.ru, Gosuslugi, Google, Amazon и т.д.

### 3. Фильтрация (Smart Filter)
- ❌ **Blacklist**: отбрасывает прокси, маскирующиеся под заведомо заблокированные ресурсы (Instagram, Facebook, Twitter, BBC, Meduza и т.п.).
- ✅ **RU‑маркер**: помечает прокси как `ru`, если домен секрета содержит `yandex`, `vk.com`, `mail.ru`, `sber`, `gosuslugi`, `ozon`, `wildberries` и др.

### 4. Проверка (Checking)
- Пингует каждый прокси через TCP (или Telethon MTProto, если указаны `API_ID`/`API_HASH`).
- Измеряет real ping‑отклик и availability (timeout = 2s).
- Для каждой пары `(host, port)` оставляет только самый быстрый вариант.
- DPI‑проверка: только те, что проходят **DPI Detector**, попадают в финальный список.

Результат сохраняется в нескольких форматах:
- `proxy_ru.txt`, `proxy_eu.txt`, `proxy_all.txt` — готовые списки `tg://proxy?...` для быстрого импорта в Telegram.
- `verified/proxy_*_verified.txt` — списки, разложенные по регионам (RU / EU / All).
- `verified/proxy_all_tme_verified.txt` — ссылки `https://t.me/proxy?server=...` (удобно кидать людям).
- `verified/proxy_all_verified.json` — подробный JSON с полями `host`, `port`, `secret`, `ping`, `region`, `domain`, `method` (`TCP_OK` / `Telethon_OK`).
- `verified/proxy_stats_verified.json` — статистика по запуску (кол‑во сырья, верифицированных прокси, лучший пинг и т.п.).

---

🔗 Мои проекты

<table>
<tr>
<th>Проект</th>
<th>Описание</th>
<th>Ссылка</th>
</tr>
<tr>
<td><b>VPN KEY VLESS</b></td>
<td>Основной канал с конфигами и новостями.</td>
<td><a href="https://t.me/vlesstrojan">Telegram</a></td>
</tr>
<tr>
<td><b>KiberSos New</b></td>
<td>Резервный канал связи.</td>
<td><a href="https://t.me/kibersosnew">Telegram</a></td>
</tr>
<tr>
<td><b>VlessBots</b></td>
<td>Бот для выдачи ключей.</td>
<td><a href="https://t.me/vlessbots_bot">Bot</a></td>
</tr>
<tr>
<td><b>Internet Access</b></td>
<td>Сайт проекта.</td>
<td><a href="https://kort0881.github.io/internet-access-site/">Website</a></td>
</tr>
<tr>
<td><b>VPN Key Repo</b></td>
<td>Репозиторий скриптов VLESS.</td>
<td><a href="https://github.com/kort0881/vpn-key-vless">GitHub</a></td>
</tr>
</table>

---

🛠️ Локальный запуск (для разработчиков)

Если хотите запустить сборщик на своём ПК:

```bash
# 1. Клонировать репозиторий
git clone https://github.com/kort0881/telegram-proxy-collector.git
cd telegram-proxy-collector

# 2. Установить зависимости
pip install requests telethon

# 3. Запустить (TCP-проверка)
python main.py

# или с ограничением по топу и пользовательской папкой вывода:
python main.py --top 200 --output-dir verified
```
