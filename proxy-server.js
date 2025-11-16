#!/usr/bin/env node
/**
 * Polymarket API Proxy Server (Node.js)
 * Простий Express сервер для проксування запитів до Polymarket API з підтримкою CORS
 */

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 5000;
const POLYMARKET_API = 'https://gamma-api.polymarket.com';

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

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        polymarket_api: POLYMARKET_API,
        uptime: process.uptime()
    });
});

// Запуск сервера
app.listen(PORT, '0.0.0.0', () => {
    console.log('='.repeat(60));
    console.log('🚀 Polymarket Event Viewer - Proxy Server (Node.js)');
    console.log('='.repeat(60));
    console.log(`📡 Proxy URL: http://localhost:${PORT}`);
    console.log(`🌐 Open in browser: http://localhost:${PORT}`);
    console.log(`❤️  Health check: http://localhost:${PORT}/health`);
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
