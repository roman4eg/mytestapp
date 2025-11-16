# 🚀 Швидкий Старт

## Найпростіший спосіб запуску

### Windows
Просто двічі клацніть на файл `start.bat`

### Linux / macOS
```bash
./start.sh
```

Скрипт автоматично:
1. Знайде Python або Node.js на вашому комп'ютері
2. Встановить необхідні залежності
3. Запустить проксі-сервер
4. Відкриє http://localhost:5000 у браузері

---

## Альтернативні методи

### Використання Python (якщо скрипт не працює)

```bash
# 1. Встановіть залежності
pip install flask flask-cors requests

# 2. Запустіть сервер
python proxy-server.py

# 3. Відкрийте в браузері
# http://localhost:5000
```

### Використання Node.js (якщо скрипт не працює)

```bash
# 1. Встановіть залежності
npm install express cors axios

# 2. Запустіть сервер
node proxy-server.js

# 3. Відкрийте в браузері
# http://localhost:5000
```

---

## ❓ Що робити якщо не працює?

### Помилка: "python: command not found"
Встановіть Python 3: https://www.python.org/downloads/

### Помилка: "node: command not found"
Встановіть Node.js: https://nodejs.org/

### Помилка: "Port 5000 is already in use"
Змініть порт у файлі proxy-server.py або proxy-server.js з 5000 на інший (наприклад, 8080)

### CORS помилки у браузері
Це означає, що ви відкрили HTML файл безпосередньо замість через сервер.
Використовуйте один з методів запуску вище.

---

## 📖 Детальна документація

Дивіться повну документацію у файлі [README-POLYMARKET.md](README-POLYMARKET.md)
