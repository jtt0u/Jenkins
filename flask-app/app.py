import os
import json
import time
from datetime import datetime
from flask import Flask, jsonify, render_template_string, request
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация из переменных окружения
CONFIG = {
    'version': os.environ.get('APP_VERSION', 'dev'),
    'environment': os.environ.get('ENVIRONMENT', 'development'),
    'build_time': os.environ.get('BUILD_TIME', datetime.now().isoformat()),
    'git_commit': os.environ.get('GIT_COMMIT', 'unknown'),
    'git_branch': os.environ.get('GIT_BRANCH', 'unknown'),
    'deployed_at': datetime.now().isoformat(),
    'port': int(os.environ.get('PORT', 5000))
}

# Счётчики для метрик
METRICS = {
    'requests_total': 0,
    'requests_by_endpoint': {},
    'errors_total': 0,
    'start_time': time.time()
}

# HTML шаблон для главной страницы
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask App - {{ config.environment }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #667eea;
            margin-top: 0;
        }
        .env-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            margin-left: 10px;
        }
        .env-development { background: #ffd93d; color: #333; }
        .env-staging { background: #6bcf7f; color: white; }
        .env-production { background: #e74c3c; color: white; }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        .info-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }
        .info-card h3 {
            margin: 0 0 10px 0;
            color: #667eea;
            font-size: 14px;
        }
        .info-card p {
            margin: 5px 0;
            font-size: 16px;
            font-weight: 500;
        }
        .endpoints {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .endpoint {
            background: white;
            padding: 10px;
            margin: 10px 0;
            border-radius: 3px;
            border-left: 3px solid #667eea;
            font-family: 'Courier New', monospace;
        }
        .method {
            color: #667eea;
            font-weight: bold;
            margin-right: 10px;
        }
        .description {
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>
            Flask Application
            <span class="env-badge env-{{ config.environment }}">{{ config.environment }}</span>
        </h1>

        <div class="info-grid">
            <div class="info-card">
                <h3>VERSION</h3>
                <p>{{ config.version }}</p>
            </div>
            <div class="info-card">
                <h3>ENVIRONMENT</h3>
                <p>{{ config.environment }}</p>
            </div>
            <div class="info-card">
                <h3>GIT COMMIT</h3>
                <p>{{ config.git_commit[:7] }}</p>
            </div>
            <div class="info-card">
                <h3>GIT BRANCH</h3>
                <p>{{ config.git_branch }}</p>
            </div>
            <div class="info-card">
                <h3>BUILD TIME</h3>
                <p>{{ config.build_time[:19] }}</p>
            </div>
            <div class="info-card">
                <h3>DEPLOYED AT</h3>
                <p>{{ config.deployed_at[:19] }}</p>
            </div>
        </div>

        <div class="endpoints">
            <h2>Available Endpoints</h2>

            <div class="endpoint">
                <span class="method">GET</span> /
                <div class="description">This page - application information</div>
            </div>

            <div class="endpoint">
                <span class="method">GET</span> /health
                <div class="description">Health check endpoint for monitoring</div>
            </div>

            <div class="endpoint">
                <span class="method">GET</span> /api/info
                <div class="description">Detailed application information in JSON</div>
            </div>

            <div class="endpoint">
                <span class="method">GET</span> /api/metrics
                <div class="description">Application metrics and statistics</div>
            </div>

            <div class="endpoint">
                <span class="method">GET</span> /api/config
                <div class="description">Current configuration (non-sensitive)</div>
            </div>

            <div class="endpoint">
                <span class="method">GET</span> /api/users
                <div class="description">Sample API endpoint with mock data</div>
            </div>

            <div class="endpoint">
                <span class="method">POST</span> /api/users
                <div class="description">Create new user (mock endpoint)</div>
            </div>

            <div class="endpoint">
                <span class="method">GET</span> /api/status
                <div class="description">Detailed status information</div>
            </div>
        </div>
    </div>
</body>
</html>
"""


@app.before_request
def before_request():
    """Счётчик запросов перед каждым запросом"""
    METRICS['requests_total'] += 1
    endpoint = request.endpoint or 'unknown'
    METRICS['requests_by_endpoint'][endpoint] = METRICS['requests_by_endpoint'].get(endpoint, 0) + 1


@app.route('/')
def home():
    """Главная страница с информацией о приложении"""
    return render_template_string(HOME_TEMPLATE, config=CONFIG)


@app.route('/health')
def health():
    """Health check endpoint для Kubernetes/Docker"""
    return jsonify({
        'status': 'healthy',
        'environment': CONFIG['environment'],
        'version': CONFIG['version'],
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/info')
def api_info():
    """Детальная информация о приложении"""
    return jsonify({
        'application': 'flask-app',
        'version': CONFIG['version'],
        'environment': CONFIG['environment'],
        'build_time': CONFIG['build_time'],
        'git_commit': CONFIG['git_commit'],
        'git_branch': CONFIG['git_branch'],
        'deployed_at': CONFIG['deployed_at'],
        'python_version': os.sys.version,
        'hostname': os.environ.get('HOSTNAME', 'unknown')
    })


@app.route('/api/metrics')
def api_metrics():
    """Метрики приложения"""
    uptime = time.time() - METRICS['start_time']
    return jsonify({
        'requests_total': METRICS['requests_total'],
        'requests_by_endpoint': METRICS['requests_by_endpoint'],
        'errors_total': METRICS['errors_total'],
        'uptime_seconds': round(uptime, 2),
        'uptime_human': format_uptime(uptime),
        'environment': CONFIG['environment'],
        'version': CONFIG['version']
    })


@app.route('/api/config')
def api_config():
    """Текущая конфигурация (без секретов)"""
    return jsonify({
        'environment': CONFIG['environment'],
        'version': CONFIG['version'],
        'git_branch': CONFIG['git_branch'],
        'git_commit': CONFIG['git_commit'],
        'features': {
            'authentication': CONFIG['environment'] == 'production',
            'debug_mode': CONFIG['environment'] == 'development',
            'rate_limiting': CONFIG['environment'] in ['staging', 'production']
        }
    })


@app.route('/api/users', methods=['GET'])
def get_users():
    """Mock endpoint - список пользователей"""
    users = [
        {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'role': 'admin'},
        {'id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'role': 'user'},
        {'id': 3, 'name': 'Charlie Brown', 'email': 'charlie@example.com', 'role': 'user'}
    ]

    return jsonify({
        'environment': CONFIG['environment'],
        'users': users,
        'total': len(users)
    })


@app.route('/api/users', methods=['POST'])
def create_user():
    """Mock endpoint - создание пользователя"""
    data = request.get_json() or {}

    # Валидация
    if not data.get('name') or not data.get('email'):
        return jsonify({
            'error': 'Name and email are required'
        }), 400

    # Mock создание
    user = {
        'id': 4,
        'name': data.get('name'),
        'email': data.get('email'),
        'role': data.get('role', 'user'),
        'created_at': datetime.now().isoformat()
    }

    logger.info(f"User created: {user['name']} ({user['email']})")

    return jsonify({
        'message': 'User created successfully',
        'user': user,
        'environment': CONFIG['environment']
    }), 201


@app.route('/api/status')
def api_status():
    """Детальный статус приложения"""
    return jsonify({
        'status': 'running',
        'environment': CONFIG['environment'],
        'version': CONFIG['version'],
        'git': {
            'branch': CONFIG['git_branch'],
            'commit': CONFIG['git_commit']
        },
        'deployment': {
            'build_time': CONFIG['build_time'],
            'deployed_at': CONFIG['deployed_at']
        },
        'runtime': {
            'uptime_seconds': round(time.time() - METRICS['start_time'], 2),
            'requests_total': METRICS['requests_total'],
            'errors_total': METRICS['errors_total']
        },
        'health_checks': {
            'database': 'ok',  # Mock
            'cache': 'ok',     # Mock
            'external_api': 'ok'  # Mock
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Обработка 404 ошибок"""
    METRICS['errors_total'] += 1
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource does not exist',
        'environment': CONFIG['environment']
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработка 500 ошибок"""
    METRICS['errors_total'] += 1
    logger.error(f"Internal error: {error}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal error occurred',
        'environment': CONFIG['environment']
    }), 500


def format_uptime(seconds):
    """Форматирование uptime в человекочитаемый вид"""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")

    return " ".join(parts)


if __name__ == '__main__':
    logger.info(f"Starting Flask application...")
    logger.info(f"Version: {CONFIG['version']}")
    logger.info(f"Environment: {CONFIG['environment']}")
    logger.info(f"Git Commit: {CONFIG['git_commit']}")
    logger.info(f"Git Branch: {CONFIG['git_branch']}")

    # Debug mode только для development
    debug = CONFIG['environment'] == 'development'

    app.run(
        host='0.0.0.0',
        port=CONFIG['port'],
        debug=debug
    )
