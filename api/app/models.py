from sqlalchemy import Column, Integer, String, Date, Float, Text, SmallInteger, ForeignKey
from database import Base

class Category(Base):
    __tablename__ = 'category'

    category_id = Column(SmallInteger, primary_key=True)
    category_name = Column(String(15))
    description = Column(Text)
    products_count = Column(SmallInteger)

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(SmallInteger, primary_key=True)
    product_name = Column(String(40))
    unit_price = Column(Float)

class ProductCategory(Product):
    __tablename__ = 'products_category'
    product_id = Column(SmallInteger, ForeignKey('products.product_id'), primary_key=True)

    orders_count = Column(SmallInteger)
    units_in_stock = Column(SmallInteger)
    discontinued = Column(Integer)

class ProductOrder(Product):
    __tablename__ = 'products_order'
    product_id = Column(SmallInteger, ForeignKey('products.product_id'), primary_key=True)

    quantity = Column(SmallInteger)
    discount = Column(Float)
    total_price = Column(Float)

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(SmallInteger, primary_key=True)
    employee_id = Column(String(5))
    employee_full_name = Column(String(31))
    order_date = Column(Date)
    required_date = Column(Date)
    shipped_date = Column(Date)
    ship_via = Column(SmallInteger)
    ship_company_name = Column(String(40))
    ship_name = Column(String(40))
    ship_address = Column(String(60))
    ship_city = Column(String(15))
    ship_region = Column(String(15))
    ship_postal_code = Column(String(10))
    ship_country = Column(String(15))
    customer_id = Column(String(5))
    customer_company_name = Column(String(40))

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(SmallInteger, primary_key=True)
    employee_full_name = Column(String(31))
    title = Column(String(30))
    birth_date = Column(Date)
    hire_date = Column(Date)
    address = Column(String(60))
    city = Column(String(15))
    region = Column(String(15))
    postal_code = Column(String(10))
    country = Column(String(15))
    notes = Column(Text)
    reports_to = Column(SmallInteger)
    reports_to_full_name = Column(String(31))
    total_sales = Column(Float)
