"""
Jenkins Course - Python Application
Demonstrates artifact generation and workspace management
"""
import os
import json
from datetime import datetime
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Read version from environment or default
VERSION = os.environ.get('APP_VERSION', '1.0.0')
BUILD_NUMBER = os.environ.get('BUILD_NUMBER', 'local')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

@app.route('/')
def index():
    """Main page with application info"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jenkins Python App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 8px; max-width: 800px; margin: 0 auto; }
            h1 { color: #333; }
            .info { background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .label { font-weight: bold; color: #555; }
            .value { color: #007bff; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 3px solid #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐍 Jenkins Python Application</h1>
            <div class="info">
                <p><span class="label">Version:</span> <span class="value">{{ version }}</span></p>
                <p><span class="label">Build:</span> <span class="value">{{ build }}</span></p>
                <p><span class="label">Environment:</span> <span class="value">{{ env }}</span></p>
                <p><span class="label">Timestamp:</span> <span class="value">{{ timestamp }}</span></p>
            </div>
            <h2>Available Endpoints</h2>
            <div class="endpoint"><strong>GET /</strong> - This page</div>
            <div class="endpoint"><strong>GET /api/info</strong> - Application information (JSON)</div>
            <div class="endpoint"><strong>GET /api/health</strong> - Health check</div>
            <div class="endpoint"><strong>GET /api/metrics</strong> - Application metrics</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(
        html,
        version=VERSION,
        build=BUILD_NUMBER,
        env=ENVIRONMENT,
        timestamp=datetime.now().isoformat()
    )

@app.route('/api/info')
def info():
    """Application information endpoint"""
    return jsonify({
        'application': 'jenkins-python-app',
        'version': VERSION,
        'build': BUILD_NUMBER,
        'environment': ENVIRONMENT,
        'timestamp': datetime.now().isoformat(),
        'python_version': os.sys.version,
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Main page'},
            {'path': '/api/info', 'method': 'GET', 'description': 'Application info'},
            {'path': '/api/health', 'method': 'GET', 'description': 'Health check'},
            {'path': '/api/metrics', 'method': 'GET', 'description': 'Metrics'}
        ]
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': VERSION,
        'build': BUILD_NUMBER,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/metrics')
def metrics():
    """Application metrics endpoint"""
    import sys
    return jsonify({
        'application': 'jenkins-python-app',
        'version': VERSION,
        'build': BUILD_NUMBER,
        'environment': ENVIRONMENT,
        'metrics': {
            'uptime': 'N/A',  # Would require tracking start time
            'requests_total': 'N/A',  # Would require counter
            'python_version': sys.version.split()[0],
            'platform': sys.platform
        },
        'timestamp': datetime.now().isoformat()
    })

def main():
    """Main entry point"""
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'

    print('=' * 50)
    print('Jenkins Python Application')
    print('=' * 50)
    print(f'Version: {VERSION}')
    print(f'Build: {BUILD_NUMBER}')
    print(f'Environment: {ENVIRONMENT}')
    print(f'Port: {port}')
    print(f'Debug: {debug}')
    print('=' * 50)

    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()
