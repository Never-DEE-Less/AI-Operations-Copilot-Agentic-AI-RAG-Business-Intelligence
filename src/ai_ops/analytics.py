
import pandas as pd
from sqlalchemy import text

from ai_ops.db.session import engine


def get_revenue_by_category() -> pd.DataFrame:
    """Return completed-order revenue grouped by product category."""

    query = text(
        """
        SELECT
            p.category,
            COUNT(o.id) AS order_count,
            SUM(o.quantity) AS units_sold,
            ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue
        FROM orders AS o
        JOIN products AS p ON o.product_id = p.id
        WHERE o.status = :status
        GROUP BY p.category
        ORDER BY total_revenue DESC
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(
            query,
            connection,
            params={"status": "completed"},
        )


def get_monthly_revenue() -> pd.DataFrame:
    """Return completed-order revenue grouped by calendar month."""

    query = text(
        """
        SELECT
            DATE_TRUNC('month', ordered_at) AS month,
            COUNT(id) AS order_count,
            SUM(quantity) AS units_sold,
            ROUND(SUM(quantity * unit_price), 2) AS total_revenue
        FROM orders
        WHERE status = :status
        GROUP BY DATE_TRUNC('month', ordered_at)
        ORDER BY month
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(
            query,
            connection,
            params={"status": "completed"},
        )



def get_top_customers(limit: int = 10) -> pd.DataFrame:
    """Return customers ranked by completed-order revenue."""

    query = text(
        """
        SELECT
            c.id AS customer_id,
            c.name AS customer_name,
            c.company,
            COUNT(o.id) AS order_count,
            SUM(o.quantity * o.unit_price) AS total_revenue
        FROM customers AS c
        JOIN orders AS o ON o.customer_id = c.id
        WHERE o.status = :status
        GROUP BY c.id, c.name, c.company
        ORDER BY total_revenue DESC
        LIMIT :limit
        """
    )

    with engine.connect() as connection:
        return pd.read_sql(
            query,
            connection,
            params={"status": "completed", "limit": limit},
        )




if __name__ == "__main__":
    print("\nRevenue by product category")
    print(get_revenue_by_category().to_string(index=False))

    print("\nMonthly revenue")
    print(get_monthly_revenue().to_string(index=False))

    print("\nTop 10 customers")
    print(get_top_customers().to_string(index=False))


