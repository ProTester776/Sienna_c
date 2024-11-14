import pytest
import os
import sys 

# Ensure the parent directory is in the path to access app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Flask app and functions from app.py
from app import app, preprocess_query, get_most_relevant_chunk, get_orca_response

print(f"Current working directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_preprocess_query():
    query = "What are the services for seniors?"
    processed = preprocess_query(query)
    assert "services" in processed
    assert "seniors" in processed
    assert "are" not in processed  # 'are' should be removed as a stopword

def test_get_most_relevant_chunk():
    query = "What services are available for seniors?"
    chunk, score = get_most_relevant_chunk(query)
    assert chunk is not None
    assert score > 0
    assert "services" in chunk.lower() or "seniors" in chunk.lower()

def test_get_orca_response():
    query = "Tell me about senior care"
    response = get_orca_response(query)
    assert isinstance(response, str)
    assert len(response) > 0
    assert "senior" in response.lower() or "care" in response.lower()

def test_chat_integration(client):
    response = client.post('/chat', json={'message': 'What programs are available for seniors?'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert "seniors" in data['response'].lower() or "programs" in data['response'].lower()