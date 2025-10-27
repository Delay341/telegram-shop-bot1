
# SMM Digital Bot — UptimeRobot

Добавлены эндпоинты:
- `GET /healthz` — быстрый ответ 200 OK, если процесс жив.
- `GET /ready` — 200 OK, если бот инициализирован и есть свежий пинг к Telegram; иначе 503.

Как это работает:
- В процессе бота запускается встроенный FastAPI сервер (uvicorn) в отдельном потоке.
- Бот периодически пингует Telegram API (`getMe`) и отмечает состояние для `/ready`.

Настройка UptimeRobot:
1. Тип: HTTPS
2. URL: `https://<твой-домен>/healthz` (и опционально `/ready`)
3. Интервал: 5 минут (или чаще)
4. Alerts: Telegram/Email

Требуемые зависимости:
- fastapi
- uvicorn
