from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class PaginationMetadata(BaseModel):
    total_items: int
    limit: int
    offset: int

class Category(BaseModel):
    id: int = Field(..., validation_alias='category_id')
    name: str = Field(..., validation_alias='category_name')
    description: str
    products_count: int

    class Config:
        from_attributes = True

class PaginatedCategories(BaseModel):
    data: List[Category]
    metadata: PaginationMetadata

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

class PaginatedCategoryProducts(BaseModel):
    data: List[ProductCategory]
    metadata: PaginationMetadata

class ProductOrder(ProductBase):
    quantity: int
    discount: float
    total_price: float

    class Config:
        from_attributes = True

class PaginatedOrderProducts(BaseModel):
    data: List[ProductOrder]
    metadata: PaginationMetadata

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
    postal_code: Optional[str]
    country: str
    required_date: datetime
    shipped_date: Optional[datetime]

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

class PaginatedOrders(BaseModel):
    data: List[Order]
    metadata: PaginationMetadata

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

class PaginatedEmployees(BaseModel):
    data: List[Employee]
    metadata: PaginationMetadata

class LargestOrder(Order):
    product: ProductOrder

    class Config:
        from_attributes = True