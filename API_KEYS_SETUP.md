# Налаштування API Ключів

Цей файл містить інструкції як додати API ключі для платформ Kalshi та Opinion.

## 🟣 Polymarket
**Статус**: ✅ Працює без API ключа

Polymarket API є публічним і не вимагає аутентифікації для читання даних про ринки.

## 🔵 Kalshi
**Статус**: ⏳ Потребує API ключ

### Як отримати Kalshi API Key:

1. Зареєструйтесь на [kalshi.com](https://kalshi.com)
2. Перейдіть в Settings → API Keys
3. Створіть новий API key
4. Скопіюйте ключ (він показується тільки один раз!)

### Як додати до застосунку:

#### Python (`proxy-server.py`):

Знайдіть функцію `get_kalshi_markets()` (близько рядка 107) та додайте header:

```python
@app.route('/api/kalshi/events')
def get_kalshi_markets():
    """Проксі для Kalshi /markets endpoint"""
    try:
        params = request.args.to_dict()

        # Додайте ці рядки:
        headers = {
            'Authorization': 'YOUR_KALSHI_API_KEY_HERE'
        }

        # Оновіть request:
        response = requests.get(
            f'{KALSHI_API}/markets',
            params=kalshi_params,
            headers=headers,  # Додайте це
            timeout=30
        )
```

Повторіть для `get_kalshi_orderbook()` та `get_kalshi_price()`.

#### Node.js (`proxy-server.js`):

Знайдіть endpoint `/api/kalshi/events` (близько рядка 147) та додайте headers:

```javascript
app.get('/api/kalshi/events', async (req, res) => {
    try {
        const params = req.query;
        const kalshiParams = {};

        // ... існуючий код параметрів ...

        const response = await axios.get(`${KALSHI_API}/markets`, {
            params: kalshiParams,
            headers: {
                'Authorization': 'YOUR_KALSHI_API_KEY_HERE'
            },
            timeout: 30000
        });
```

Повторіть для `/api/kalshi/book` та `/api/kalshi/midpoint`.

## 🟡 Opinion
**Статус**: ⏳ Потребує API ключ

### Як отримати Opinion API Key:

1. Зареєструйтесь на [opinion.trade](https://opinion.trade)
2. Надішліть запит на API доступ через email підтримки
3. Дочекайтесь отримання API ключа

### Як додати до застосунку:

#### Python (`proxy-server.py`):

Знайдіть функцію `get_opinion_markets()` (близько рядка 187) та додайте header:

```python
@app.route('/api/opinion/events')
def get_opinion_markets():
    """Проксі для Opinion /markets endpoint"""
    try:
        params = request.args.to_dict()

        # Додайте ці рядки:
        headers = {
            'Authorization': 'Bearer YOUR_OPINION_API_KEY_HERE'
        }

        # Оновіть request:
        response = requests.get(
            f'{OPINION_API}/markets',
            params=params,
            headers=headers,  # Додайте це
            timeout=30
        )
```

Повторіть для `get_opinion_orderbook()` та `get_opinion_price()`.

#### Node.js (`proxy-server.js`):

Знайдіть endpoint `/api/opinion/events` (близько рядка 251) та додайте headers:

```javascript
app.get('/api/opinion/events', async (req, res) => {
    try {
        const response = await axios.get(`${OPINION_API}/markets`, {
            params: req.query,
            headers: {
                'Authorization': 'Bearer YOUR_OPINION_API_KEY_HERE'
            },
            timeout: 30000
        });
```

Повторіть для `/api/opinion/book` та `/api/opinion/midpoint`.

## 🔒 Безпека API Ключів

⚠️ **ВАЖЛИВО**: Ніколи не комітьте API ключі в git!

### Кращі практики:

1. **Використовуйте змінні середовища**:

```python
# Python
import os
KALSHI_API_KEY = os.getenv('KALSHI_API_KEY', '')
```

```javascript
// Node.js
const KALSHI_API_KEY = process.env.KALSHI_API_KEY || '';
```

2. **Створіть файл `.env`** (вже в .gitignore):

```bash
KALSHI_API_KEY=your_key_here
OPINION_API_KEY=your_key_here
```

3. **Використовуйте python-dotenv або dotenv**:

```bash
# Python
pip install python-dotenv

# Node.js
npm install dotenv
```

```python
# У proxy-server.py
from dotenv import load_dotenv
load_dotenv()
```

```javascript
// У proxy-server.js
require('dotenv').config();
```

## Перевірка

Після додавання ключів:

1. Перезапустіть proxy сервер
2. Виберіть платформу (Kalshi або Opinion) в dropdown
3. Натисніть "Завантажити події"
4. Якщо все налаштовано правильно - побачите ринки!

## Допомога

Якщо виникли проблеми:
- Перевірте console в браузері (F12)
- Перевірте логи сервера
- Переконайтесь що API ключ дійсний
- Переконайтесь що header format правильний
