import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app instance
from app.database import engine, Base
from unittest.mock import MagicMock, patch
from app.models import Transcription
from sqlalchemy.orm import Session
from sqlalchemy import inspect


# Use TestClient to send requests to the FastAPI app
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    inspector = inspect(engine)
    if not inspector.has_table("transcriptions"): 
        Base.metadata.create_all(bind=engine)
    yield



# Mock the database session for the test
@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    # Mock the query chain to return an empty list for the search
    db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    yield db
    db.close()


@patch('app.database.get_db', return_value=mock_db)
def test_search_transcription_no_results(mock_get_db, setup_database):
    response = client.get("/search?file_name=nonexistentfile")

    assert response.status_code == 200
    response_json = response.json()

    assert response_json == {"message": "No transcriptions found matching the criteria"}
