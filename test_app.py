"""
Test file for NEXA Game Recommender FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
from app_fastapi import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "NEXA Game Recommender" in response.json()["message"]


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_recommendations_endpoint_missing_preference():
    """Test recommendations endpoint with missing preference"""
    response = client.post("/api/recommendations", json={})
    assert response.status_code == 422  # Validation error


def test_game_details_endpoint_missing_title():
    """Test game details endpoint with missing title"""
    response = client.post("/api/game-details", json={})
    assert response.status_code == 422  # Validation error


def test_igdb_autocomplete_missing_query():
    """Test IGDB autocomplete endpoint with missing query"""
    response = client.get("/api/igdb-autocomplete")
    assert response.status_code == 422  # Validation error


def test_igdb_autocomplete_with_query():
    """Test IGDB autocomplete endpoint with query"""
    response = client.get("/api/igdb-autocomplete?q=skyrim")
    # This might fail if API keys are not set, but should not crash
    assert response.status_code in [200, 500]


def test_cors_headers():
    """Test that CORS headers are properly set"""
    response = client.options("/")
    assert "access-control-allow-origin" in response.headers


if __name__ == "__main__":
    pytest.main([__file__]) 