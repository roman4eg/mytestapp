#!/usr/bin/env node
/**
 * Polymarket API Proxy Server (Node.js)
 * Простий Express сервер для проксування запитів до Polymarket API з підтримкою CORS
 */

require('dotenv').config();

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 5000;
const POLYMARKET_API = 'https://gamma-api.polymarket.com';
const CLOB_API = 'https://clob.polymarket.com';
const KALSHI_API = 'https://api.elections.kalshi.com/trade-api/v2';
const OPINION_API = 'https://proxy.opinion.trade:8443';

// API Keys from environment variables
const OPINION_API_KEY = process.env.OPINION_API_KEY || '';
const KALSHI_API_KEY = process.env.KALSHI_API_KEY || '';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// Головна сторінка
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'polymarket-viewer.html'));
});

// Проксі для /events endpoint
app.get('/api/events', async (req, res) => {
    try {
        const response = await axios.get(`${POLYMARKET_API}/events`, {
            params: req.query,
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching events:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// Проксі для /markets endpoint
app.get('/api/markets', async (req, res) => {
    try {
        const response = await axios.get(`${POLYMARKET_API}/markets`, {
            params: req.query,
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching markets:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// Проксі для /price endpoint (CLOB API)
app.get('/api/price', async (req, res) => {
    try {
        const response = await axios.get(`${CLOB_API}/price`, {
            params: req.query,
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching price:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// Проксі для /book endpoint (CLOB API) - order book
app.get('/api/book', async (req, res) => {
    try {
        const response = await axios.get(`${CLOB_API}/book`, {
            params: req.query,
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching order book:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// Проксі для /midpoint endpoint (CLOB API)
app.get('/api/midpoint', async (req, res) => {
    try {
        const response = await axios.get(`${CLOB_API}/midpoint`, {
            params: req.query,
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching midpoint:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// ===== Kalshi API Endpoints =====

// Проксі для Kalshi /markets endpoint
app.get('/api/kalshi/events', async (req, res) => {
    try {
        const params = req.query;
        const kalshiParams = {};

        // Kalshi використовує параметр 'status' замість 'closed'/'active'
        if (params.limit) kalshiParams.limit = params.limit;
        if (params.status) {
            kalshiParams.status = params.status;
        } else if (params.active === 'true') {
            kalshiParams.status = 'open';
        } else if (params.closed === 'true') {
            kalshiParams.status = 'closed';
        }

        const response = await axios.get(`${KALSHI_API}/markets`, {
            params: kalshiParams,
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching Kalshi markets:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// Проксі для Kalshi /markets/{ticker}/orderbook endpoint
app.get('/api/kalshi/book', async (req, res) => {
    try {
        const ticker = req.query.token_id;
        if (!ticker) {
            return res.status(400).json({ error: 'ticker required' });
        }

        const response = await axios.get(`${KALSHI_API}/markets/${ticker}/orderbook`, {
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching Kalshi orderbook:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// Проксі для Kalshi ціни (з orderbook)
app.get('/api/kalshi/midpoint', async (req, res) => {
    try {
        const ticker = req.query.token_id;
        if (!ticker) {
            return res.status(400).json({ error: 'ticker required' });
        }

        // Kalshi не має окремого midpoint endpoint, беремо з orderbook
        const response = await axios.get(`${KALSHI_API}/markets/${ticker}/orderbook`, {
            timeout: 30000
        });

        const orderbook = response.data;

        // Обчислюємо midpoint з yes orderbook
        if (orderbook.orderbook && orderbook.orderbook.yes && orderbook.orderbook.yes.length > 0) {
            const yesBook = orderbook.orderbook.yes[0];
            const bestBid = yesBook[0] || 0;
            const bestAsk = yesBook[1] || 100;
            const mid = (bestBid + bestAsk) / 200.0; // Конвертуємо в 0-1
            res.json({ mid: mid.toString() });
        } else {
            res.json({ mid: '0.5' }); // Default
        }
    } catch (error) {
        console.error('Error fetching Kalshi price:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// ===== Opinion API Endpoints =====

// Проксі для Opinion /markets endpoint
app.get('/api/opinion/events', async (req, res) => {
    try {
        // Add Authorization header if API key is available
        const headers = {};
        if (OPINION_API_KEY) {
            headers['Authorization'] = `Bearer ${OPINION_API_KEY}`;
        }

        const response = await axios.get(`${OPINION_API}/markets`, {
            params: req.query,
            headers: headers,
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching Opinion markets:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// Проксі для Opinion /orderbook endpoint
app.get('/api/opinion/book', async (req, res) => {
    try {
        // Add Authorization header if API key is available
        const headers = {};
        if (OPINION_API_KEY) {
            headers['Authorization'] = `Bearer ${OPINION_API_KEY}`;
        }

        const response = await axios.get(`${OPINION_API}/orderbook`, {
            params: req.query,
            headers: headers,
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching Opinion orderbook:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// Проксі для Opinion /prices endpoint
app.get('/api/opinion/midpoint', async (req, res) => {
    try {
        // Add Authorization header if API key is available
        const headers = {};
        if (OPINION_API_KEY) {
            headers['Authorization'] = `Bearer ${OPINION_API_KEY}`;
        }

        const response = await axios.get(`${OPINION_API}/prices`, {
            params: req.query,
            headers: headers,
            timeout: 30000
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error fetching Opinion prices:', error.message);

        if (error.response) {
            res.status(error.response.status).json({
                error: error.message,
                details: error.response.data
            });
        } else {
            res.status(500).json({ error: error.message });
        }
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        polymarket_api: POLYMARKET_API,
        clob_api: CLOB_API,
        kalshi_api: KALSHI_API,
        opinion_api: OPINION_API,
        uptime: process.uptime()
    });
});

// Запуск сервера
app.listen(PORT, '0.0.0.0', () => {
    console.log('='.repeat(60));
    console.log('🚀 Prediction Markets Viewer - Proxy Server (Node.js)');
    console.log('='.repeat(60));
    console.log(`📡 Proxy URL: http://localhost:${PORT}`);
    console.log(`🌐 Open in browser: http://localhost:${PORT}`);
    console.log(`❤️  Health check: http://localhost:${PORT}/health`);
    console.log('='.repeat(60));
    console.log(`🟣 Polymarket API: ${POLYMARKET_API}`);
    console.log(`🔵 Kalshi API: ${KALSHI_API}`);
    console.log(`🟡 Opinion API: ${OPINION_API}`);
    console.log('='.repeat(60));
    console.log('\n⚠️  Make sure you have installed dependencies:');
    console.log('   npm install\n');
    console.log('Press Ctrl+C to stop the server\n');
});

// Обробка помилок
process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});
