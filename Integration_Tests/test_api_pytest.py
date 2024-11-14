import pytest
import os
import sys 
from app import app, get_most_relevant_chunk, get_orca_response, preprocess_query

print(f"Current working directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>Sienna Senior Living Bot</title>' in response.data


def test_chat_endpoint(client):
    response = client.post('/chat', json={'message': 'What services do you offer?'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert isinstance(data['response'], str)
    assert len(data['response']) > 0

def test_chat_endpoint_invalid_input(client):
    response = client.post('/chat', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_security_headers(client):
    response = client.get('/')
    assert 'Content-Security-Policy' in response.headers
    assert 'Strict-Transport-Security' in response.headers
    assert 'X-Frame-Options' in response.headers
    assert 'X-Content-Type-Options' in response.headers
    assert 'Referrer-Policy' in response.headers