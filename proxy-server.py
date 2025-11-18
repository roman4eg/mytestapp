#!/usr/bin/env python3
"""
Polymarket API Proxy Server
Простий Flask сервер для проксування запитів до Polymarket API з підтримкою CORS
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import sys
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Дозволяємо CORS для всіх маршрутів

POLYMARKET_API = 'https://gamma-api.polymarket.com'
CLOB_API = 'https://clob.polymarket.com'
KALSHI_API = 'https://api.elections.kalshi.com/trade-api/v2'
OPINION_API = 'https://proxy.opinion.trade:8443'

# API Keys from environment variables
OPINION_API_KEY = os.getenv('OPINION_API_KEY', '')
KALSHI_API_KEY = os.getenv('KALSHI_API_KEY', '')

@app.route('/')
def index():
    """Головна сторінка - відкриває polymarket-viewer.html"""
    return app.send_static_file('polymarket-viewer.html')

@app.route('/api/events')
def get_events():
    """Проксі для /events endpoint"""
    try:
        # Отримуємо всі параметри запиту
        params = request.args.to_dict()

        # Робимо запит до Polymarket API
        response = requests.get(f'{POLYMARKET_API}/events', params=params, timeout=30)

        # Повертаємо відповідь
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/markets')
def get_markets():
    """Проксі для /markets endpoint"""
    try:
        params = request.args.to_dict()
        response = requests.get(f'{POLYMARKET_API}/markets', params=params, timeout=30)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching markets: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/price')
def get_price():
    """Проксі для /price endpoint (CLOB API)"""
    try:
        params = request.args.to_dict()
        response = requests.get(f'{CLOB_API}/price', params=params, timeout=30)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching price: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/book')
def get_book():
    """Проксі для /book endpoint (CLOB API) - order book"""
    try:
        params = request.args.to_dict()
        response = requests.get(f'{CLOB_API}/book', params=params, timeout=30)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching order book: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/midpoint')
def get_midpoint():
    """Проксі для /midpoint endpoint (CLOB API)"""
    try:
        params = request.args.to_dict()
        response = requests.get(f'{CLOB_API}/midpoint', params=params, timeout=30)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching midpoint: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

# ===== Kalshi API Endpoints =====

@app.route('/api/kalshi/events')
def get_kalshi_markets():
    """Проксі для Kalshi /markets endpoint"""
    try:
        params = request.args.to_dict()
        # Kalshi використовує параметр 'status' замість 'closed'/'active'
        status_filter = request.args.get('status', '')

        kalshi_params = {}
        if 'limit' in params:
            kalshi_params['limit'] = params['limit']
        if status_filter:
            kalshi_params['status'] = status_filter
        elif 'active' in params and params.get('active') == 'true':
            kalshi_params['status'] = 'open'
        elif 'closed' in params and params.get('closed') == 'true':
            kalshi_params['status'] = 'closed'

        response = requests.get(f'{KALSHI_API}/markets', params=kalshi_params, timeout=30)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Kalshi markets: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/kalshi/book')
def get_kalshi_orderbook():
    """Проксі для Kalshi /markets/{ticker}/orderbook endpoint"""
    try:
        # token_id для Kalshi це ticker
        ticker = request.args.get('token_id', '')
        if not ticker:
            return jsonify({'error': 'ticker required'}), 400

        response = requests.get(f'{KALSHI_API}/markets/{ticker}/orderbook', timeout=30)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Kalshi orderbook: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/kalshi/midpoint')
def get_kalshi_price():
    """Проксі для Kalshi ціни (з orderbook)"""
    try:
        ticker = request.args.get('token_id', '')
        if not ticker:
            return jsonify({'error': 'ticker required'}), 400

        # Kalshi не має окремого midpoint endpoint, беремо з orderbook
        response = requests.get(f'{KALSHI_API}/markets/{ticker}/orderbook', timeout=30)
        orderbook = response.json()

        # Обчислюємо midpoint з yes orderbook
        if 'orderbook' in orderbook and 'yes' in orderbook['orderbook']:
            yes_book = orderbook['orderbook']['yes']
            if yes_book:
                # Беремо найкращі bid/ask для обчислення midpoint
                best_bid = yes_book[0][0] if yes_book else 0
                best_ask = yes_book[0][1] if yes_book else 100
                mid = (best_bid + best_ask) / 200.0  # Конвертуємо в 0-1
                return jsonify({'mid': str(mid)}), 200

        return jsonify({'mid': '0.5'}), 200  # Default

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Kalshi price: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

# ===== Opinion API Endpoints =====

@app.route('/api/opinion/events')
def get_opinion_markets():
    """Проксі для Opinion /markets endpoint"""
    try:
        if not OPINION_API_KEY:
            print("⚠️ WARNING: OPINION_API_KEY not found in environment!", file=sys.stderr)
            return jsonify({'error': 'API key not configured'}), 500

        # Opinion API uses X-API-Key header (discovered through testing)
        headers = {'X-API-Key': OPINION_API_KEY}

        # Endpoint structure: /api/bsc/api/v2/topic
        endpoint = f'{OPINION_API}/api/bsc/api/v2/topic'

        # Get pagination parameters from request
        limit = request.args.get('limit', '1000')

        # Try different pagination parameter names that Opinion API might use
        params = {
            'pageSize': limit,      # Common pagination param
            'limit': limit,         # Alternative
            'size': limit,          # Another alternative
            'page': '1',           # Start from first page
            'pageNum': '1',        # Alternative page param
        }

        print(f"Requesting Opinion API with params: {params}", file=sys.stderr)

        response = requests.get(endpoint, headers=headers, params=params, timeout=30)

        if response.status_code != 200:
            print(f"Opinion API error: {response.status_code} - {response.text[:200]}", file=sys.stderr)
            return jsonify({'error': f'Opinion API returned {response.status_code}'}), response.status_code

        data = response.json()

        # Opinion API returns: {"errno": 0, "errmsg": "", "result": {"list": [...]}}
        # Extract the list from the nested structure
        if 'result' in data and 'list' in data['result']:
            events_list = data['result']['list']
            print(f"✓ Opinion API: Retrieved {len(events_list)} topics", file=sys.stderr)

            # Debug: Print first topic to understand structure
            if events_list:
                import json
                print(f"DEBUG - First topic structure:", file=sys.stderr)
                print(json.dumps(events_list[0], indent=2, ensure_ascii=False)[:1000], file=sys.stderr)

            # Transform Opinion format to match Polymarket structure
            transformed_events = []
            for topic in events_list:
                # Debug each topic's status
                status = topic.get('status', None)
                end_time = topic.get('endTime', 0)
                resolved_time = topic.get('resolvedTime', 0)
                current_time = int(time.time())

                print(f"Topic {topic.get('topicId', 'unknown')}: status={status}, endTime={end_time}, resolvedTime={resolved_time}", file=sys.stderr)

                # Determine if active based on Opinion status codes:
                # status=1: likely draft/pending
                # status=2: active/open for trading
                # status=4: resolved/closed
                # Also check resolvedTime - if present, event is closed
                if resolved_time and resolved_time > 0:
                    is_active = False  # Has been resolved
                elif status == 2:
                    is_active = True   # Open for trading
                elif status == 1:
                    is_active = True   # Pending/draft but might be tradeable
                else:
                    is_active = False  # status=4 or other = closed

                print(f"  → Mapped to: active={is_active}, closed={not is_active}", file=sys.stderr)

                # Map Opinion fields to Polymarket-like structure
                transformed = {
                    'id': str(topic.get('topicId', '')),
                    'title': topic.get('title', ''),
                    'description': topic.get('abstract', '') or topic.get('content', ''),
                    'active': is_active,
                    'closed': not is_active,
                    'created': topic.get('createTime', 0),
                    'end_date': end_time,
                    'image': topic.get('coverUrl', ''),
                    'volume': topic.get('volume', 0),
                    'liquidity': 0,  # Opinion might not have this field
                    'markets': [],  # Will need to fetch separately if needed
                    'outcomes': [],  # Will need to map from Opinion's market structure
                    'platform': 'opinion',
                    '_raw': topic  # Keep raw data for debugging
                }
                transformed_events.append(transformed)

            return jsonify(transformed_events), 200
        else:
            print(f"Unexpected Opinion API response structure: {str(data)[:200]}", file=sys.stderr)
            return jsonify({'error': 'Unexpected API response structure'}), 500

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Opinion markets: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response text: {e.response.text}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/opinion/book')
def get_opinion_orderbook():
    """Проксі для Opinion /orderbook endpoint"""
    try:
        params = request.args.to_dict()

        # Add Authorization header if API key is available
        headers = {}
        if OPINION_API_KEY:
            headers['Authorization'] = f'Bearer {OPINION_API_KEY}'

        response = requests.get(f'{OPINION_API}/orderbook', params=params, headers=headers, timeout=30)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Opinion orderbook: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/opinion/midpoint')
def get_opinion_price():
    """Проксі для Opinion /prices endpoint"""
    try:
        params = request.args.to_dict()

        # Add Authorization header if API key is available
        headers = {}
        if OPINION_API_KEY:
            headers['Authorization'] = f'Bearer {OPINION_API_KEY}'

        response = requests.get(f'{OPINION_API}/prices', params=params, headers=headers, timeout=30)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Opinion prices: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Перевірка здоров'я сервера"""
    return jsonify({
        'status': 'healthy',
        'polymarket_api': POLYMARKET_API,
        'clob_api': CLOB_API,
        'kalshi_api': KALSHI_API,
        'opinion_api': OPINION_API
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Prediction Markets Viewer - Proxy Server")
    print("=" * 60)
    print("📡 Proxy URL: http://localhost:5000")
    print("🌐 Open in browser: http://localhost:5000")
    print("❤️  Health check: http://localhost:5000/health")
    print("=" * 60)
    print("🟣 Polymarket API: " + POLYMARKET_API)
    print("🔵 Kalshi API: " + KALSHI_API)
    print("🟡 Opinion API: " + OPINION_API)
    print("=" * 60)
    print("\n⚠️  Make sure you have installed dependencies:")
    print("   pip install flask flask-cors requests\n")
    print("Press Ctrl+C to stop the server\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
