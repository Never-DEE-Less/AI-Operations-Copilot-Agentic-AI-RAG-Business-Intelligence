
from unittest.mock import MagicMock

from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool


def test_agent_executes_requested_analytics_tool():
    @tool
    def fake_revenue_by_category() -> str:
        """Retrieve revenue grouped by product category."""
        return "Services: 441350 EUR"

    # First response requests the tool; second response gives the answer.
    responses = iter([
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "fake_revenue_by_category",
                    "args": {},
                    "id": "call_1",
                    "type": "tool_call",
                }
            ],
        ),
        AIMessage(content="Services generated the most revenue."),
    ])

    # RunnableLambda supports invocation, but not bind_tools.
    # Mock bind_tools so create_agent can bind the fake tool.
    fake_model = MagicMock()
    fake_model.bind_tools.return_value = RunnableLambda(
        lambda _: next(responses)
    )

    agent = create_agent(
        model=fake_model,
        tools=[fake_revenue_by_category],
        system_prompt="Use the available tool to answer revenue questions.",
    )

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Which category generated the most revenue?",
            }
        ]
    })

    messages = result["messages"]

    assert any(
        getattr(message, "name", None) == "fake_revenue_by_category"
        for message in messages
    )
    assert messages[-1].content == "Services generated the most revenue."


def test_agent_responds_when_resume_search_finds_no_information():
    @tool
    def fake_resume_search(question: str) -> str:
        """Search the resume for relevant information."""
        return "No relevant resume information was found."

    responses = iter([
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "fake_resume_search",
                    "args": {"question": "What is my favorite pizza topping?"},
                    "id": "call_resume_1",
                    "type": "tool_call",
                }
            ],
        ),
        AIMessage(
            content="I couldn't find that information in your resume."
        ),
    ])

    fake_model = MagicMock()
    fake_model.bind_tools.return_value = RunnableLambda(
        lambda _: next(responses)
    )

    agent = create_agent(
        model=fake_model,
        tools=[fake_resume_search],
        system_prompt=(
            "For resume questions, use the search tool. "
            "If it finds no relevant information, say you couldn't "
            "find that information in the resume. Never guess."
        ),
    )

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "What is my favorite pizza topping?",
            }
        ]
    })

    messages = result["messages"]

    assert any(
        getattr(message, "name", None) == "fake_resume_search"
        for message in messages
    )
    assert messages[-1].content == (
        "I couldn't find that information in your resume."
    )




def test_agent_executes_multiple_analytics_tools():
    @tool
    def fake_monthly_revenue() -> str:
        """Retrieve monthly revenue trends."""
        return "January: 1000 EUR; February: 1500 EUR"

    @tool
    def fake_revenue_by_category() -> str:
        """Retrieve revenue grouped by category."""
        return "Services: 1800 EUR; Products: 700 EUR"

    responses = iter([
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "fake_monthly_revenue",
                    "args": {},
                    "id": "call_monthly",
                    "type": "tool_call",
                },
                {
                    "name": "fake_revenue_by_category",
                    "args": {},
                    "id": "call_category",
                    "type": "tool_call",
                },
            ],
        ),
        AIMessage(
            content=(
                "Revenue increased from January to February. "
                "Services generated more revenue than products."
            )
        ),
    ])

    fake_model = MagicMock()
    fake_model.bind_tools.return_value = RunnableLambda(
        lambda _: next(responses)
    )

    agent = create_agent(
        model=fake_model,
        tools=[fake_monthly_revenue, fake_revenue_by_category],
        system_prompt="Use the available tools to answer analytics questions.",
    )

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    "Compare monthly revenue trends and revenue by category."
                ),
            }
        ]
    })

    messages = result["messages"]
    executed_tools = {
        message.name
        for message in messages
        if getattr(message, "type", None) == "tool"
    }

    assert executed_tools == {
        "fake_monthly_revenue",
        "fake_revenue_by_category",
    }
    assert "January to February" in messages[-1].content
    assert "Services" in messages[-1].content
