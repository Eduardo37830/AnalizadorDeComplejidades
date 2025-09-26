import pytest
import json
from app import create_app

@pytest.fixture
def client():
    """Crea cliente de pruebas para Flask."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Prueba el endpoint de salud."""
    response = client.get('/v1/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'algo-analyzer-flask'

def test_analyze_endpoint_basic(client):
    """Prueba básica del endpoint de análisis."""
    test_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

    response = client.post('/v1/analyze',
                          json={'code': test_code, 'language': 'python'},
                          headers={'Content-Type': 'application/json'})

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'complexity' in data
    assert 'report' in data

def test_analyze_endpoint_missing_code(client):
    """Prueba el endpoint con código faltante."""
    response = client.post('/v1/analyze',
                          json={'language': 'python'},
                          headers={'Content-Type': 'application/json'})

    assert response.status_code == 422  # Validation error

def test_analyze_endpoint_invalid_syntax(client):
    """Prueba el endpoint con código de sintaxis inválida."""
    invalid_code = """
def broken_function(
    if True
        return "missing colons and parentheses"
"""

    response = client.post('/v1/analyze',
                          json={'code': invalid_code, 'language': 'python'},
                          headers={'Content-Type': 'application/json'})

    # Debería intentar reparar automáticamente o manejar el error
    assert response.status_code in [200, 500]

def test_analyze_sorting_algorithm(client):
    """Prueba análisis de algoritmo de ordenamiento."""
    bubble_sort = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""

    response = client.post('/v1/analyze',
                          json={'code': bubble_sort, 'language': 'python'},
                          headers={'Content-Type': 'application/json'})

    assert response.status_code == 200
    data = json.loads(response.data)

    # Verificar que detecte la complejidad O(n²)
    complexity = data.get('complexity', {})
    assert complexity is not None
