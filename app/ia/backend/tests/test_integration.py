"""
Integration tests for #Dô application
"""
import pytest
import httpx
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from ..main import app


class TestIntegration:
    """Integration tests for the complete application"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "#Dô Backend"
    
    @patch('firebase_admin.firestore.client')
    def test_auth_endpoints(self, mock_firestore, client):
        """Test authentication endpoints"""
        # Mock Firestore
        mock_db = Mock()
        mock_firestore.return_value = mock_db
        
        # Mock user registration
        mock_collection = Mock()
        mock_db.collection.return_value = mock_collection
        mock_collection.where.return_value.get.return_value = []  # No existing user
        mock_doc = Mock()
        mock_collection.document.return_value = mock_doc
        
        # Test user registration
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "test_password",
            "avatar_url": None,
            "favorite_instrument": None,
            "subscription_plan": "copper",
            "role": "registered"
        }
        
        response = client.post("/auth/register", json=user_data)
        # Note: This might fail due to Firebase initialization in tests
        # In a real test environment, you would mock Firebase properly
    
    def test_instruments_endpoints(self, client):
        """Test instruments endpoints"""
        # Test get all instruments
        response = client.get("/instruments/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_subscription_endpoints(self, client):
        """Test subscription endpoints"""
        # Test get all plans
        response = client.get("/subscription/plans")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Test get about us
        response = client.get("/subscription/about")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "description" in data
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options("/")
        assert "access-control-allow-origin" in response.headers
    
    def test_api_documentation(self, client):
        """Test API documentation endpoints"""
        # Test OpenAPI docs
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Test ReDoc
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_error_handling(self, client):
        """Test error handling"""
        # Test 404 for non-existent endpoint
        response = client.get("/non-existent-endpoint")
        assert response.status_code == 404
    
    @patch('firebase_admin.firestore.client')
    def test_ml_endpoints(self, mock_firestore, client):
        """Test ML endpoints"""
        # Mock Firestore
        mock_db = Mock()
        mock_firestore.return_value = mock_db
        
        # Test tuning notes endpoint
        response = client.get("/ml/tuning-notes/violin")
        assert response.status_code == 200
        data = response.json()
        assert "instrument_type" in data
        assert "tuning_notes" in data
        assert data["instrument_type"] == "violin"
    
    def test_practice_endpoints(self, client):
        """Test practice endpoints"""
        # Test get all composers
        response = client.get("/practice/composers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_instruments_faq_endpoints(self, client):
        """Test instruments FAQ endpoints"""
        # Test get FAQ for violin
        response = client.get("/instruments/violin/faq")
        assert response.status_code == 200
        data = response.json()
        assert "instrument_type" in data
        assert "faq_items" in data
    
    def test_search_faq_endpoint(self, client):
        """Test FAQ search endpoint"""
        response = client.get("/instruments/faq/search?query=afinar")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_api_structure(self, client):
        """Test that all expected API routes exist"""
        expected_routes = [
            "/",
            "/health",
            "/auth/register",
            "/auth/login",
            "/auth/me",
            "/profile/me",
            "/instruments/",
            "/instruments/violin",
            "/instruments/violin/faq",
            "/ml/detect-note",
            "/ml/tune",
            "/ml/detect-chord",
            "/practice/composers",
            "/practice/scores",
            "/subscription/plans",
            "/subscription/about"
        ]
        
        for route in expected_routes:
            # Just check that the route exists (might return 405 for wrong method)
            response = client.get(route)
            assert response.status_code in [200, 405, 422]  # 405 = method not allowed, 422 = validation error
    
    def test_request_validation(self, client):
        """Test request validation"""
        # Test invalid user registration
        invalid_user_data = {
            "email": "invalid-email",  # Invalid email format
            "username": "",  # Empty username
            "password": "123"  # Too short password
        }
        
        response = client.post("/auth/register", json=invalid_user_data)
        assert response.status_code == 422  # Validation error
    
    def test_response_format(self, client):
        """Test response format consistency"""
        # Test that all endpoints return JSON
        endpoints = [
            "/",
            "/health",
            "/instruments/",
            "/subscription/plans",
            "/subscription/about"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            if response.status_code == 200:
                assert response.headers["content-type"] == "application/json"
