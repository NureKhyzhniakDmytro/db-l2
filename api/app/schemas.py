from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Category(BaseModel):
    id: int = Field(..., validation_alias='category_id')
    name: str = Field(..., validation_alias='category_name')
    description: str
    products_count: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    id: int = Field(..., validation_alias='product_id')
    name: str = Field(..., validation_alias='product_name')
    unit_price: float

class ProductCategory(ProductBase):
    orders_count: int
    units_in_stock: int
    discontinued: int

    class Config:
        from_attributes = True

class ProductOrder(ProductBase):
    quantity: int
    discount: float
    total_price: float

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    id: Optional[int]
    name: Optional[str]

    class Config:
        from_attributes = True

class Customer(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

class Shipper(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Shipment(BaseModel):
    ship_via: Shipper
    name: str
    address: str
    city: str
    postal_code: str
    country: str
    required_date: datetime
    shipped_date: datetime

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    employee: EmployeeBase
    customer: Customer
    order_date: datetime
    shipment: Shipment

    class Config:
        from_attributes = True

class Employee(EmployeeBase):
    title: str
    birth_date: datetime
    hire_date: datetime
    address: str
    city: str
    postal_code: str
    country: str
    notes: str
    reports_to: EmployeeBase
    total_sales: float
