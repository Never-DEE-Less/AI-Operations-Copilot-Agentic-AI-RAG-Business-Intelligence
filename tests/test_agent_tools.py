
from ai_ops.agent_tools import (
    ANALYTICS_TOOLS,
    monthly_revenue,
    revenue_by_category,
    top_customers,
)
from ai_ops.agent import build_agent
from unittest.mock import patch
from ai_ops.agent_tools import ANALYTICS_TOOLS, search_resume_documents

def test_all_analytics_tools_are_registered():
    tool_names = {tool.name for tool in ANALYTICS_TOOLS}

    assert tool_names == {
        "revenue_by_category",
        "monthly_revenue",
        "top_customers",
	"search_resume_documents",
    }


def test_revenue_by_category_returns_expected_fields():
    data = revenue_by_category.invoke({})

    assert isinstance(data, list)
    assert len(data) > 0
    assert {
        "category",
        "order_count",
        "units_sold",
        "total_revenue",
    }.issubset(data[0])


def test_monthly_revenue_returns_expected_fields():
    data = monthly_revenue.invoke({})

    assert isinstance(data, list)
    assert len(data) > 0
    assert {
        "month",
        "order_count",
        "units_sold",
        "total_revenue",
    }.issubset(data[0])


def test_top_customers_returns_expected_fields():
    data = top_customers.invoke({"limit": 5})

    assert isinstance(data, list)
    assert len(data) <= 5

    if data:
        assert {
            "customer_id",
            "customer_name",
            "order_count",
            "total_revenue",
        }.issubset(data[0])


def test_top_customers_rejects_invalid_limit():
    try:
        top_customers.invoke({"limit": 0})
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for limit=0")


def test_agent_exposes_only_approved_analytics_tools():
    agent = build_agent()

    assert set(agent.nodes.keys()) >= {"model", "tools"}
    assert {
        tool.name for tool in ANALYTICS_TOOLS
    } == {
        "revenue_by_category",
        "monthly_revenue",
        "top_customers",
	"search_resume_documents",
    }


def test_resume_search_tool_returns_retrieved_documents():
    expected_results = [
        {
            "source": "Resume_BDHM.pdf",
            "page": 0,
            "text": "Python, machine learning, and NLP.",
            "distance": 0.32,
        }
    ]

    with patch(
        "ai_ops.agent_tools.search_resume",
        return_value=expected_results,
    ):
        result = search_resume_documents.invoke(
            {"question": "What AI skills are listed in my resume?"}
        )

    assert result == expected_results
    assert result[0]["source"] == "Resume_BDHM.pdf"
    assert "machine learning" in result[0]["text"]



def test_resume_search_tool_returns_empty_when_no_relevant_matches():
    with patch(
        "ai_ops.agent_tools.search_resume",
        return_value=[],
    ):
        result = search_resume_documents.invoke(
            {"question": "What is my favorite pizza topping?"}
        )

    assert result == []

