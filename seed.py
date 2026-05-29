from datetime import date, timedelta
from decimal import Decimal
import argparse

from sqlalchemy import delete

from retailiq.database import SessionLocal, init_db
from retailiq.models import Customer, Product, Sale, StockMovement, Supplier


SUPPLIERS = [
    ("FreshMart Wholesale", "orders@freshmart.example"),
    ("Daily Goods Co", "supply@dailygoods.example"),
    ("Urban Pantry Distributors", "hello@urbanpantry.example"),
]

CUSTOMERS = [
    ("Manuu Stores", "Patna", "Retailer"),
    ("Nisha Home Needs", "Ranchi", "Retailer"),
    ("City Cafe", "Kolkata", "Restaurant"),
    ("Metro Mini Mart", "Delhi", "Retailer"),
]

PRODUCTS = [
    ("RICE-5KG", "Basmati Rice 5kg", "Grocery", "620.00", "510.00", 42, 20, 1),
    ("OIL-1L", "Sunflower Oil 1L", "Grocery", "145.00", "118.00", 18, 25, 1),
    ("TEA-500", "Premium Tea 500g", "Beverages", "260.00", "190.00", 36, 15, 2),
    ("BISC-12", "Butter Cookies Pack", "Snacks", "80.00", "52.00", 12, 20, 2),
    ("SOAP-4", "Bath Soap Combo", "Personal Care", "170.00", "125.00", 55, 18, 3),
    ("NOOD-6", "Instant Noodles Pack of 6", "Snacks", "135.00", "96.00", 24, 30, 3),
]


def reset_tables() -> None:
    with SessionLocal() as session:
        for model in (Sale, StockMovement, Product, Customer, Supplier):
            session.execute(delete(model))
        session.commit()


def seed_database(reset: bool = False) -> None:
    init_db()

    if reset:
        reset_tables()

    with SessionLocal() as session:
        if session.query(Product).first():
            print("Database already has data. Use --reset to recreate sample data.")
            return

        suppliers = [
            Supplier(name=name, contact_email=email)
            for name, email in SUPPLIERS
        ]
        customers = [
            Customer(name=name, city=city, segment=segment)
            for name, city, segment in CUSTOMERS
        ]
        session.add_all(suppliers + customers)
        session.flush()

        products = [
            Product(
                sku=sku,
                name=name,
                category=category,
                unit_price=Decimal(unit_price),
                cost_price=Decimal(cost_price),
                current_stock=stock,
                reorder_level=reorder,
                supplier_id=supplier_id,
            )
            for sku, name, category, unit_price, cost_price, stock, reorder, supplier_id in PRODUCTS
        ]
        session.add_all(products)
        session.flush()

        today = date.today()
        sales: list[Sale] = []
        for index, product in enumerate(products):
            for day_offset in range(1, 46, 5):
                quantity = (index + day_offset) % 7 + 1
                customer = customers[(index + day_offset) % len(customers)]
                sales.append(
                    Sale(
                        product_id=product.id,
                        customer_id=customer.id,
                        sale_date=today - timedelta(days=day_offset),
                        quantity=quantity,
                        unit_price=product.unit_price,
                    )
                )

        stock_movements = [
            StockMovement(
                product_id=product.id,
                movement_type="stock_in",
                quantity=product.current_stock,
                note="Initial sample stock",
            )
            for product in products
        ]

        session.add_all(sales + stock_movements)
        session.commit()

    print("RetailIQ sample database created successfully.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed RetailIQ sample data.")
    parser.add_argument("--reset", action="store_true", help="Delete existing data before seeding.")
    args = parser.parse_args()
    seed_database(reset=args.reset)


if __name__ == "__main__":
    main()
