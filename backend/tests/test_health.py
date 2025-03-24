import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.database import SessionLocal

client = TestClient(app)

@pytest.fixture
def mock_db():
    db = MagicMock(spec=SessionLocal)
    db.execute = MagicMock()
    db.close = MagicMock()
    
    yield db
    db.close()

def test_health_check_success(mock_db):
    # Mock the execute method to simulate a successful database connection
    mock_db.execute.return_value = None  # No exception is raised

    with patch("app.main.SessionLocal", return_value=mock_db):
        response = client.get("/health")

        # Validate the response
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

def test_health_check_failure(mock_db):
    # Mock the execute method to raise an exception (simulate a database connection failure)
    mock_db.execute.side_effect = Exception("Database connection failed")

    with patch("app.main.SessionLocal", return_value=mock_db):
        response = client.get("/health")

        # Validate the response
        assert response.status_code == 200
        assert response.json() == {"status": "error", "detail": "Database connection failed"}
