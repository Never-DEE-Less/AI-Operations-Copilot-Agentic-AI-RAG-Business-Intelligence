
import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pandas as pd
from sqlalchemy import insert, text

from ai_ops.db.models import Customer, Order, Product
from ai_ops.db.session import engine


random.seed(42)

FIRST_NAMES = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey",
    "Riley", "Jamie", "Sam", "Avery", "Cameron",
]

LAST_NAMES = [
    "Miller", "Schmidt", "Brown", "Patel", "Garcia",
    "Wilson", "Meyer", "Khan", "Davis", "Fischer",
]

COMPANIES = [
    "Northstar GmbH", "BluePeak AG", "Greenfield Labs",
    "NovaTech GmbH", "BrightPath Ltd", "UrbanWorks",
    "CloudNine GmbH", "Silverline AG", "Redwood Systems",
    "Horizon Digital",
]

PRODUCTS = [
    ("Analytics Platform", "Software", "499.00"),
    ("AI Assistant", "Software", "799.00"),
    ("Data Pipeline", "Software", "349.00"),
    ("Security Suite", "Security", "599.00"),
    ("Cloud Backup", "Cloud", "129.00"),
    ("Compute Instance", "Cloud", "249.00"),
    ("Storage Pro", "Cloud", "89.00"),
    ("Laptop Pro", "Hardware", "1499.00"),
    ("Workstation", "Hardware", "2299.00"),
    ("Monitor 27", "Hardware", "329.00"),
    ("Keyboard Pro", "Hardware", "119.00"),
    ("Mouse Pro", "Hardware", "69.00"),
    ("ML Consulting", "Services", "1200.00"),
    ("Data Audit", "Services", "850.00"),
    ("AI Workshop", "Services", "1500.00"),
    ("API Package", "Software", "199.00"),
    ("Database Pro", "Software", "399.00"),
    ("Network Shield", "Security", "279.00"),
    ("Cloud Migration", "Services", "2400.00"),
    ("Backup Drive", "Hardware", "159.00"),
]

STATUSES = [
    "completed",
    "completed",
    "completed",
    "pending",
    "cancelled",
]


def main():
    now = datetime.now(timezone.utc)

    # Build 100 synthetic customers.
    customers = []

    for i in range(100):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)

        customers.append(
            {
                "name": f"{first} {last}",
                "email": f"customer{i + 1:03d}@example.com",
                "company": random.choice(COMPANIES),
            }
        )

    # Build the product catalogue.
    products = [
        {
            "name": name,
            "category": category,
            "price": Decimal(price),
        }
        for name, category, price in PRODUCTS
    ]

    # Build the dataset and insert everything in one transaction.
    # Existing demo rows are replaced; do not use this against real data.
    with engine.begin() as connection:
        # Delete dependent rows before their referenced rows.
        connection.execute(text("DELETE FROM orders"))
        connection.execute(text("DELETE FROM customers"))
        connection.execute(text("DELETE FROM products"))

        # Insert customers using SQLAlchemy model types.
        customer_df = pd.DataFrame(customers)

        connection.execute(
            insert(Customer),
            customer_df.to_dict("records"),
        )

        # Insert products. Decimal prices remain numeric.
        product_df = pd.DataFrame(products)

        connection.execute(
            insert(Product),
            product_df.to_dict("records"),
        )

        # Retrieve database-generated IDs.
        customer_ids = connection.execute(
            text("SELECT id FROM customers ORDER BY id")
        ).scalars().all()

        product_rows = connection.execute(
            text("SELECT id, price FROM products ORDER BY id")
        ).all()

        # Generate 1,000 orders spread across the last 12 months.
        orders = []

        for _ in range(1000):
            product_id, product_price = random.choice(product_rows)

            ordered_at = now - timedelta(
                days=random.randint(0, 364),
                hours=random.randint(0, 23),
            )

            orders.append(
                {
                    "customer_id": random.choice(customer_ids),
                    "product_id": product_id,
                    "quantity": random.randint(1, 5),
                    "unit_price": Decimal(str(product_price)),
                    "status": random.choice(STATUSES),
                    "ordered_at": ordered_at,
                }
            )

        # Insert orders using SQLAlchemy model types.
        order_df = pd.DataFrame(orders)

        connection.execute(
            insert(Order),
            order_df.to_dict("records"),
        )

    print("Synthetic business dataset loaded successfully.")
    print(f"Customers: {len(customers)}")
    print(f"Products: {len(products)}")
    print(f"Orders: {len(orders)}")


if __name__ == "__main__":
    main()
