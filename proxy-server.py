#!/usr/bin/env python3
"""
Polymarket API Proxy Server
Простий Flask сервер для проксування запитів до Polymarket API з підтримкою CORS
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import sys

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Дозволяємо CORS для всіх маршрутів

POLYMARKET_API = 'https://gamma-api.polymarket.com'
CLOB_API = 'https://clob.polymarket.com'
OPINION_API = 'https://proxy.opinion.trade:8443'

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

# ===== Opinion API Endpoints =====

@app.route('/api/opinion/events')
def get_opinion_markets():
    """Проксі для Opinion /markets endpoint"""
    try:
        params = request.args.to_dict()
        response = requests.get(f'{OPINION_API}/markets', params=params, timeout=30)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Opinion markets: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/api/opinion/book')
def get_opinion_orderbook():
    """Проксі для Opinion /orderbook endpoint"""
    try:
        params = request.args.to_dict()
        response = requests.get(f'{OPINION_API}/orderbook', params=params, timeout=30)
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
        response = requests.get(f'{OPINION_API}/prices', params=params, timeout=30)
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
    print("🟡 Opinion API: " + OPINION_API)
    print("=" * 60)
    print("\n⚠️  Make sure you have installed dependencies:")
    print("   pip install flask flask-cors requests\n")
    print("Press Ctrl+C to stop the server\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
