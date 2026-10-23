
from langchain.tools import tool
from ai_ops.rag.retriever import search_resume

from ai_ops.analytics import (
    get_monthly_revenue,
    get_revenue_by_category,
    get_top_customers,
)


@tool
def revenue_by_category() -> list[dict]:
    """Retrieve completed order counts, units sold, and total revenue grouped by product category."""
    data = get_revenue_by_category()
    return data.to_dict(orient="records")


@tool
def monthly_revenue() -> list[dict]:
    """Retrieve completed order counts, units sold, and total revenue grouped by month."""
    data = get_monthly_revenue()
    return data.to_dict(orient="records")


@tool
def top_customers(limit: int = 10) -> list[dict]:
    """Retrieve the highest-revenue customers, including their order counts and total revenue. Limit must be between 1 and 100."""
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")

    data = get_top_customers(limit=limit)
    return data.to_dict(orient="records")



@tool
def search_resume_documents(question: str) -> list[dict]:
    """Search the indexed resume for relevant skills, education, work experience, projects, and other resume details. Use this tool for questions about the resume, and answer only from the retrieved evidence."""
    return search_resume(question)


ANALYTICS_TOOLS = [
    revenue_by_category,
    monthly_revenue,
    top_customers,
    search_resume_documents,
]

