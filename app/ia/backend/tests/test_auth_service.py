"""
Unit tests for AuthService
"""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from ..services.auth_service import AuthService
from ..models.user import UserCreate, UserLogin, UserRole, SubscriptionPlan


class TestAuthService:
    """Test cases for AuthService"""
    
    @pytest.fixture
    def auth_service(self):
        """Create AuthService instance for testing"""
        with patch('firebase_admin.initialize_app'), \
             patch('firebase_admin.credentials.Certificate'), \
             patch('firebase_admin.firestore.client'):
            return AuthService()
    
    @pytest.fixture
    def mock_user_data(self):
        """Mock user data for testing"""
        return {
            'id': 'test_user_123',
            'email': 'test@example.com',
            'username': 'testuser',
            'password_hash': 'hashed_password',
            'avatar_url': None,
            'favorite_instrument': None,
            'subscription_plan': SubscriptionPlan.COPPER,
            'role': UserRole.REGISTERED,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True
        }
    
    def test_verify_password(self, auth_service):
        """Test password verification"""
        password = "test_password"
        hashed = auth_service.get_password_hash(password)
        
        assert auth_service.verify_password(password, hashed) == True
        assert auth_service.verify_password("wrong_password", hashed) == False
    
    def test_get_password_hash(self, auth_service):
        """Test password hashing"""
        password = "test_password"
        hashed = auth_service.get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 0
    
    def test_create_access_token(self, auth_service):
        """Test JWT token creation"""
        data = {"sub": "test_user", "email": "test@example.com"}
        token = auth_service.create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_verify_token(self, auth_service):
        """Test JWT token verification"""
        data = {"sub": "test_user", "email": "test@example.com"}
        token = auth_service.create_access_token(data)
        
        payload = auth_service.verify_token(token)
        assert payload is not None
        assert payload["sub"] == "test_user"
        assert payload["email"] == "test@example.com"
    
    def test_verify_invalid_token(self, auth_service):
        """Test invalid token verification"""
        invalid_token = "invalid_token"
        payload = auth_service.verify_token(invalid_token)
        assert payload is None
    
    @patch('firebase_admin.firestore.client')
    async def test_register_user_success(self, mock_firestore, auth_service, mock_user_data):
        """Test successful user registration"""
        # Mock Firestore
        mock_db = Mock()
        mock_firestore.return_value = mock_db
        
        # Mock collection and query
        mock_collection = Mock()
        mock_db.collection.return_value = mock_collection
        mock_collection.where.return_value.get.return_value = []  # No existing user
        
        # Mock document creation
        mock_doc = Mock()
        mock_collection.document.return_value = mock_doc
        
        # Create user data
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="test_password",
            avatar_url=None,
            favorite_instrument=None,
            subscription_plan=SubscriptionPlan.COPPER,
            role=UserRole.REGISTERED
        )
        
        # Test registration
        user = await auth_service.register_user(user_data)
        
        # Verify user creation
        assert user.email == user_data.email
        assert user.username == user_data.username
        assert user.role == user_data.role
    
    @patch('firebase_admin.firestore.client')
    async def test_register_user_email_exists(self, mock_firestore, auth_service):
        """Test user registration with existing email"""
        # Mock Firestore
        mock_db = Mock()
        mock_firestore.return_value = mock_db
        
        # Mock existing user
        mock_collection = Mock()
        mock_db.collection.return_value = mock_collection
        mock_collection.where.return_value.get.return_value = [Mock()]  # Existing user
        
        user_data = UserCreate(
            email="existing@example.com",
            username="testuser",
            password="test_password"
        )
        
        # Test registration should fail
        with pytest.raises(Exception):
            await auth_service.register_user(user_data)
    
    @patch('firebase_admin.firestore.client')
    async def test_authenticate_user_success(self, mock_firestore, auth_service, mock_user_data):
        """Test successful user authentication"""
        # Mock Firestore
        mock_db = Mock()
        mock_firestore.return_value = mock_db
        
        # Mock user query
        mock_collection = Mock()
        mock_db.collection.return_value = mock_collection
        mock_doc = Mock()
        mock_doc.to_dict.return_value = mock_user_data
        mock_collection.where.return_value.get.return_value = [mock_doc]
        
        # Mock document update
        mock_doc_ref = Mock()
        mock_collection.document.return_value = mock_doc_ref
        
        login_data = UserLogin(
            email="test@example.com",
            password="test_password"
        )
        
        # Test authentication
        result = await auth_service.authenticate_user(login_data)
        
        assert "access_token" in result
        assert "token_type" in result
        assert "user" in result
        assert result["token_type"] == "bearer"
    
    @patch('firebase_admin.firestore.client')
    async def test_authenticate_user_invalid_credentials(self, mock_firestore, auth_service):
        """Test authentication with invalid credentials"""
        # Mock Firestore
        mock_db = Mock()
        mock_firestore.return_value = mock_db
        
        # Mock no user found
        mock_collection = Mock()
        mock_db.collection.return_value = mock_collection
        mock_collection.where.return_value.get.return_value = []
        
        login_data = UserLogin(
            email="nonexistent@example.com",
            password="wrong_password"
        )
        
        # Test authentication should fail
        with pytest.raises(Exception):
            await auth_service.authenticate_user(login_data)
    
    @patch('firebase_admin.firestore.client')
    async def test_get_current_user_success(self, mock_firestore, auth_service, mock_user_data):
        """Test getting current user with valid token"""
        # Mock Firestore
        mock_db = Mock()
        mock_firestore.return_value = mock_db
        
        # Mock user document
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = mock_user_data
        mock_db.collection.return_value.document.return_value.get.return_value = mock_doc
        
        # Create valid token
        token = auth_service.create_access_token({"sub": "test_user_123"})
        
        # Test getting current user
        user = await auth_service.get_current_user(token)
        
        assert user.id == mock_user_data["id"]
        assert user.email == mock_user_data["email"]
    
    @patch('firebase_admin.firestore.client')
    async def test_change_password_success(self, mock_firestore, auth_service):
        """Test successful password change"""
        # Mock Firestore
        mock_db = Mock()
        mock_firestore.return_value = mock_db
        
        # Mock user document
        mock_doc = Mock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {
            'password_hash': auth_service.get_password_hash("old_password")
        }
        mock_db.collection.return_value.document.return_value.get.return_value = mock_doc
        
        # Mock document update
        mock_doc_ref = Mock()
        mock_db.collection.return_value.document.return_value = mock_doc_ref
        
        # Test password change
        result = await auth_service.change_password(
            "test_user_123", "old_password", "new_password"
        )
        
        assert result == True
        mock_doc_ref.update.assert_called_once()
    
    def test_forgot_password(self, auth_service):
        """Test forgot password functionality"""
        result = auth_service.forgot_password("test@example.com")
        assert result == True
    
    def test_reset_password(self, auth_service):
        """Test password reset functionality"""
        result = auth_service.reset_password("reset_token", "new_password")
        assert result == True
