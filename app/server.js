const express = require('express');
const app = express();

// Читаем переменные окружения
const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';
const APP_VERSION = process.env.APP_VERSION || '1.0.0';
const BUILD_NUMBER = process.env.BUILD_NUMBER || 'local';
const API_KEY = process.env.API_KEY || 'not-set';
const DATABASE_URL = process.env.DATABASE_URL || 'not-configured';

app.get('/', (req, res) => {
  res.json({
    status: 'running',
    message: 'Jenkins Sample Application',
    environment: NODE_ENV,
    version: APP_VERSION,
    build: BUILD_NUMBER,
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

app.get('/config', (req, res) => {
  res.json({
    environment: NODE_ENV,
    version: APP_VERSION,
    build: BUILD_NUMBER,
    port: PORT,
    apiKeyConfigured: API_KEY !== 'not-set',
    databaseConfigured: DATABASE_URL !== 'not-configured'
  });
});

app.get('/info', (req, res) => {
  res.json({
    nodeVersion: process.version,
    platform: process.platform,
    architecture: process.arch,
    memory: {
      total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024) + ' MB',
      used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024) + ' MB'
    }
  });
});

const server = app.listen(PORT, () => {
  console.log('=================================');
  console.log('Jenkins Sample Application');
  console.log('=================================');
  console.log(`Environment: ${NODE_ENV}`);
  console.log(`Version: ${APP_VERSION}`);
  console.log(`Build: ${BUILD_NUMBER}`);
  console.log(`Port: ${PORT}`);
  console.log(`API Key: ${API_KEY === 'not-set' ? 'NOT CONFIGURED' : 'CONFIGURED ✓'}`);
  console.log(`Database: ${DATABASE_URL === 'not-configured' ? 'NOT CONFIGURED' : 'CONFIGURED ✓'}`);
  console.log('=================================');
  console.log(`Server running on http://localhost:${PORT}`);
  console.log('=================================');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

module.exports = app;
