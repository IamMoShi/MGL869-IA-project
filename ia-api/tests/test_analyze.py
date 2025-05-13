from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_analyze():
    """Test if the analysis works.

    Returns: Nothing
    """
    with open("tests/assets/sample.jpg", "rb") as img:
        response = client.post(
            "/api/v1/analyze/",
            files={"file": ("sample.jpg", img, "image/jpeg")},
        )
    assert response.status_code == 200
    assert "result" in response.json()
