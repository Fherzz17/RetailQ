from datetime import date, timedelta
from decimal import Decimal

import pandas as pd
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from retailiq.models import Product, Sale


def _money(value: Decimal | float | int | None) -> float:
    return round(float(value or 0), 2)


def overview(session: Session) -> dict:
    revenue_expr = func.sum(Sale.quantity * Sale.unit_price)

    revenue = session.scalar(select(revenue_expr))
    units_sold = session.scalar(select(func.sum(Sale.quantity)))
    order_count = session.scalar(select(func.count(Sale.id))) or 0
    low_stock_count = session.scalar(
        select(func.count(Product.id)).where(Product.current_stock <= Product.reorder_level)
    )

    return {
        "total_revenue": _money(revenue),
        "total_units_sold": int(units_sold or 0),
        "total_orders": int(order_count),
        "average_order_value": _money(float(revenue or 0) / order_count if order_count else 0),
        "low_stock_products": int(low_stock_count or 0),
    }


def revenue_by_month(session: Session) -> list[dict]:
    rows = session.execute(
        select(Sale.sale_date, Sale.quantity, Sale.unit_price).order_by(Sale.sale_date)
    ).all()

    if not rows:
        return []

    df = pd.DataFrame(rows, columns=["sale_date", "quantity", "unit_price"])
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["revenue"] = df["quantity"] * df["unit_price"].astype(float)
    monthly = (
        df.groupby(df["sale_date"].dt.to_period("M"))["revenue"]
        .sum()
        .reset_index()
        .sort_values("sale_date")
    )
    monthly["month"] = monthly["sale_date"].astype(str)

    return [
        {"month": row["month"], "revenue": round(float(row["revenue"]), 2)}
        for _, row in monthly.iterrows()
    ]


def top_products(session: Session, limit: int = 5) -> list[dict]:
    revenue_expr = func.sum(Sale.quantity * Sale.unit_price).label("revenue")
    units_expr = func.sum(Sale.quantity).label("units_sold")

    rows = session.execute(
        select(Product.name, Product.category, units_expr, revenue_expr)
        .join(Sale, Sale.product_id == Product.id)
        .group_by(Product.id)
        .order_by(revenue_expr.desc())
        .limit(limit)
    ).all()

    return [
        {
            "name": name,
            "category": category,
            "units_sold": int(units_sold or 0),
            "revenue": _money(revenue),
        }
        for name, category, units_sold, revenue in rows
    ]


def low_stock_products(session: Session) -> list[dict]:
    rows = session.scalars(
        select(Product)
        .where(Product.current_stock <= Product.reorder_level)
        .order_by(Product.current_stock.asc())
    ).all()

    return [
        {
            "sku": product.sku,
            "name": product.name,
            "category": product.category,
            "current_stock": product.current_stock,
            "reorder_level": product.reorder_level,
        }
        for product in rows
    ]


def stock_risk_forecast(session: Session, lookback_days: int = 30) -> list[dict]:
    since = date.today() - timedelta(days=lookback_days)
    products = session.scalars(select(Product).order_by(Product.name)).all()

    risks: list[dict] = []
    for product in products:
        units_sold = session.scalar(
            select(func.sum(Sale.quantity)).where(
                Sale.product_id == product.id,
                Sale.sale_date >= since,
            )
        )
        avg_daily_sales = float(units_sold or 0) / lookback_days
        days_remaining = product.current_stock / avg_daily_sales if avg_daily_sales else None

        if days_remaining is None:
            status = "No recent demand"
        elif days_remaining <= 7:
            status = "High risk"
        elif days_remaining <= 14:
            status = "Medium risk"
        else:
            status = "Healthy"

        risks.append(
            {
                "sku": product.sku,
                "name": product.name,
                "current_stock": product.current_stock,
                "avg_daily_sales": round(avg_daily_sales, 2),
                "days_remaining": round(days_remaining, 1) if days_remaining is not None else None,
                "status": status,
            }
        )

    return sorted(risks, key=lambda item: item["days_remaining"] or 9999)
