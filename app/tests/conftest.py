from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.core.config import settings


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {
        "Authorization": f"Bearer {settings.app_token}"
    }
