import pytest
import json
import os
from app import app, CONFIG


@pytest.fixture
def client():
    """Тестовый клиент Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Flask Application' in response.data


def test_health_endpoint(client):
    """Тест health check"""
    response = client.get('/health')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'version' in data
    assert 'environment' in data


def test_api_info(client):
    """Тест /api/info endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['application'] == 'flask-app'
    assert 'version' in data
    assert 'environment' in data
    assert 'git_commit' in data


def test_api_metrics(client):
    """Тест /api/metrics endpoint"""
    response = client.get('/api/metrics')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'requests_total' in data
    assert 'uptime_seconds' in data
    assert 'errors_total' in data
    assert data['requests_total'] > 0


def test_api_config(client):
    """Тест /api/config endpoint"""
    response = client.get('/api/config')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'environment' in data
    assert 'version' in data
    assert 'features' in data


def test_get_users(client):
    """Тест GET /api/users"""
    response = client.get('/api/users')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'users' in data
    assert 'total' in data
    assert len(data['users']) == 3
    assert data['total'] == 3


def test_create_user_success(client):
    """Тест создания пользователя - успешный"""
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'user'
    }

    response = client.post(
        '/api/users',
        data=json.dumps(user_data),
        content_type='application/json'
    )

    assert response.status_code == 201

    data = json.loads(response.data)
    assert data['message'] == 'User created successfully'
    assert data['user']['name'] == 'Test User'
    assert data['user']['email'] == 'test@example.com'


def test_create_user_validation_error(client):
    """Тест создания пользователя - ошибка валидации"""
    user_data = {
        'name': 'Test User'
        # email отсутствует
    }

    response = client.post(
        '/api/users',
        data=json.dumps(user_data),
        content_type='application/json'
    )

    assert response.status_code == 400

    data = json.loads(response.data)
    assert 'error' in data


def test_api_status(client):
    """Тест /api/status endpoint"""
    response = client.get('/api/status')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['status'] == 'running'
    assert 'git' in data
    assert 'deployment' in data
    assert 'runtime' in data
    assert 'health_checks' in data


def test_404_error(client):
    """Тест 404 ошибки"""
    response = client.get('/nonexistent')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data['error'] == 'Not Found'


def test_environment_variable_usage():
    """Тест использования переменных окружения"""
    assert 'version' in CONFIG
    assert 'environment' in CONFIG
    assert 'git_commit' in CONFIG


def test_multiple_requests_increment_counter(client):
    """Тест что счётчик запросов увеличивается"""
    # Первый запрос
    response1 = client.get('/api/metrics')
    data1 = json.loads(response1.data)
    count1 = data1['requests_total']

    # Второй запрос
    response2 = client.get('/api/metrics')
    data2 = json.loads(response2.data)
    count2 = data2['requests_total']

    # Счётчик должен увеличиться
    assert count2 > count1


def test_cors_headers_not_present(client):
    """Тест что CORS заголовки отсутствуют (можно добавить в будущем)"""
    response = client.get('/api/info')
    assert 'Access-Control-Allow-Origin' not in response.headers


def test_health_endpoint_response_format(client):
    """Тест формата ответа health endpoint"""
    response = client.get('/health')
    data = json.loads(response.data)

    required_fields = ['status', 'environment', 'version', 'timestamp']
    for field in required_fields:
        assert field in data, f"Field '{field}' missing in health response"
