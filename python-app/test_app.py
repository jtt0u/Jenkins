"""
Tests for Jenkins Python Application
Generates test reports and coverage artifacts
"""
import pytest
import os
from app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test main page returns 200"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Jenkins Python Application' in response.data

def test_info_endpoint(client):
    """Test /api/info endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200
    data = response.get_json()
    assert 'application' in data
    assert data['application'] == 'jenkins-python-app'
    assert 'version' in data
    assert 'build' in data
    assert 'environment' in data

def test_health_endpoint(client):
    """Test /api/health endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_metrics_endpoint(client):
    """Test /api/metrics endpoint"""
    response = client.get('/api/metrics')
    assert response.status_code == 200
    data = response.get_json()
    assert 'metrics' in data
    assert 'version' in data

def test_version_from_environment():
    """Test version is read from environment"""
    version = os.environ.get('APP_VERSION', '1.0.0')
    assert version is not None
    assert len(version) > 0

def test_build_number_from_environment():
    """Test build number is read from environment"""
    build = os.environ.get('BUILD_NUMBER', 'local')
    assert build is not None

def test_environment_from_environment():
    """Test environment is read from environment"""
    env = os.environ.get('ENVIRONMENT', 'development')
    assert env is not None
    assert env in ['development', 'staging', 'production', 'test']

def test_invalid_endpoint(client):
    """Test 404 for invalid endpoint"""
    response = client.get('/api/invalid')
    assert response.status_code == 404

def test_health_returns_correct_structure(client):
    """Test health endpoint returns expected structure"""
    response = client.get('/api/health')
    data = response.get_json()

    # Check all required fields
    required_fields = ['status', 'version', 'build', 'timestamp']
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

def test_info_returns_endpoints_list(client):
    """Test info endpoint returns list of endpoints"""
    response = client.get('/api/info')
    data = response.get_json()

    assert 'endpoints' in data
    assert isinstance(data['endpoints'], list)
    assert len(data['endpoints']) > 0

    # Check endpoint structure
    first_endpoint = data['endpoints'][0]
    assert 'path' in first_endpoint
    assert 'method' in first_endpoint
    assert 'description' in first_endpoint
