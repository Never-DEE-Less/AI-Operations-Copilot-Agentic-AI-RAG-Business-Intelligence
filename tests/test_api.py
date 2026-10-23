
from fastapi.testclient import TestClient

from ai_ops.main import app

from unittest.mock import patch, MagicMock

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_database_health_check():
    response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_revenue_by_category():
    response = client.get("/analytics/revenue-by-category")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "category" in data[0]
    assert "total_revenue" in data[0]


def test_monthly_revenue():
    response = client.get("/analytics/monthly-revenue")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "total_revenue" in data[0]


def test_top_customers():
    response = client.get("/analytics/top-customers?limit=5")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

    if data:
        assert "customer_name" in data[0]
        assert "total_revenue" in data[0]


def test_top_customers_rejects_invalid_limit():
    response = client.get("/analytics/top-customers?limit=0")

    assert response.status_code == 422



def test_ai_endpoint_rejects_empty_question():
    response = client.post(
        "/ai/ask",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_ai_endpoint_rejects_question_over_1000_characters():
    response = client.post(
        "/ai/ask",
        json={"question": "a" * 1001},
    )

    assert response.status_code == 422


def test_ai_endpoint_returns_successful_answer():
    fake_agent = MagicMock()
    fake_agent.invoke.return_value = {
        "messages": [
            MagicMock(
                type="ai",
                content="Services generated the most revenue.",
            )
        ]
    }

    with patch("ai_ops.api.ai.build_agent", return_value=fake_agent):
        response = client.post(
            "/ai/ask",
            json={"question": "Which category generated the most revenue?"},
        )

    assert response.status_code == 200
    assert response.json()["question"] == (
        "Which category generated the most revenue?"
    )
    assert response.json()["answer"] == (
        "Services generated the most revenue."
    )
    fake_agent.invoke.assert_called_once()



def test_ai_endpoint_handles_agent_failure():
    with patch(
        "ai_ops.api.ai.build_agent",
        side_effect=RuntimeError("Simulated agent failure"),
    ):
        response = client.post(
            "/ai/ask",
            json={"question": "Which category generated the most revenue?"},
        )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "The AI assistant is unavailable. "
        "Check that Ollama is running and the model is installed."
    )



def test_ai_endpoint_handles_empty_agent_answer():
    fake_agent = MagicMock()
    fake_agent.invoke.return_value = {
        "messages": [
            MagicMock(type="ai", content="")
        ]
    }

    with patch("ai_ops.api.ai.build_agent", return_value=fake_agent):
        response = client.post(
            "/ai/ask",
            json={"question": "Which category generated the most revenue?"},
        )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "The AI assistant did not return a text answer."
    )

