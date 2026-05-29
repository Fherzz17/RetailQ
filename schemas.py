from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    name: str
    category: str
    unit_price: Decimal
    cost_price: Decimal
    current_stock: int
    reorder_level: int
    supplier_id: int | None


class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str
    unit_price: Decimal
    cost_price: Decimal
    current_stock: int = 0
    reorder_level: int = 10
    supplier_id: int | None = None


class SaleCreate(BaseModel):
    product_id: int
    customer_id: int | None = None
    sale_date: date
    quantity: int
    unit_price: Decimal


class SaleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    customer_id: int | None
    sale_date: date
    quantity: int
    unit_price: Decimal


class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    segment: str


class SupplierOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    contact_email: str | None
