from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from models import Category, ProductCategory, Order, ProductOrder, Employee
from typing import Sequence, Optional


async def get_categories(db: AsyncSession, limit: int, offset: int) -> Sequence[Category]:
    query = text("""
                SELECT
                    c.category_id,
                    c.category_name,
                    c.description,
                    COUNT(p.product_id) AS products_count
                FROM categories c
                JOIN products p ON c.category_id = p.category_id
                GROUP BY c.category_id
                ORDER BY c.category_id
                LIMIT :limit
                OFFSET :offset
                """).bindparams(limit=limit, offset=offset)
    stmt = select(Category).from_statement(query)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_category(db: AsyncSession, category_id: int) -> Optional[Category]:
    query = text("""
                SELECT
                    c.category_id,
                    c.category_name,
                    c.description,
                    COUNT(p.product_id) AS products_count
                FROM categories c
                JOIN products p ON c.category_id = p.category_id
                WHERE c.category_id = :category_id
                GROUP BY c.category_id
                """).bindparams(category_id=category_id)
    stmt = select(Category).from_statement(query)
    result = await db.execute(stmt)
    return result.scalars().one_or_none()

async def get_category_products(db: AsyncSession, category_id: int, limit: int, offset: int) -> Sequence[ProductCategory]:
    query = text("""
                SELECT
                    p.product_id,
                    p.product_name,
                    p.unit_price,
                    p.units_in_stock,
                    p.discontinued,
                    COUNT(od.order_id) AS orders_count
                FROM products p
                JOIN order_details od ON p.product_id = od.product_id
                WHERE p.category_id = :category_id
                GROUP BY p.product_id
                ORDER BY p.product_id
                LIMIT :limit
                OFFSET :offset
                """).bindparams(category_id=category_id, limit=limit, offset=offset)
    stmt = select(ProductCategory).from_statement(query)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_orders(db: AsyncSession, limit: int, offset: int) -> Sequence[Order]:
    query = text("""
                SELECT
                    o.order_id,
                    o.employee_id,
                    e.last_name || ' ' || e.first_name AS employee_full_name,
                    o.order_date,
                    o.required_date,
                    o.shipped_date,
                    o.ship_via,
                    s.company_name AS ship_company_name,
                    o.ship_name,
                    o.ship_address,
                    o.ship_city,
                    o.ship_region,
                    o.ship_postal_code,
                    o.ship_country,
                    o.customer_id,
                    c.company_name AS customer_company_name
                FROM orders o
                JOIN employees e ON o.employee_id = e.employee_id
                JOIN shippers s ON o.ship_via = s.shipper_id
                JOIN customers c ON o.customer_id = c.customer_id
                LIMIT :limit
                OFFSET :offset
                """).bindparams(limit=limit, offset=offset)
    stmt = select(Order).from_statement(query)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_order(db: AsyncSession, order_id: int) -> Optional[Order]:
    query = text("""
                SELECT
                    o.order_id,
                    o.employee_id,
                    e.last_name || ' ' || e.first_name AS employee_full_name,
                    o.order_date,
                    o.required_date,
                    o.shipped_date,
                    o.ship_via,
                    s.company_name AS ship_company_name,
                    o.ship_name,
                    o.ship_address,
                    o.ship_city,
                    o.ship_region,
                    o.ship_postal_code,
                    o.ship_country,
                    o.customer_id,
                    c.company_name AS customer_company_name
                FROM orders o
                JOIN employees e ON o.employee_id = e.employee_id
                JOIN shippers s ON o.ship_via = s.shipper_id
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE o.order_id = :order_id
                """).bindparams(order_id=order_id)
    stmt = select(Order).from_statement(query)
    result = await db.execute(stmt)
    return result.scalars().one_or_none()

async def get_order_products(db: AsyncSession, order_id: int, limit: int, offset: int) -> Sequence[ProductOrder]:
    query = text("""
                SELECT
                    p.product_id,
                    p.product_name,
                    od.quantity,
                    od.unit_price,
                    od.discount,
                    ((od.quantity * od.unit_price) * (1 - od.discount))::numeric(10,2) AS total_price
                FROM order_details od
                JOIN products p ON od.product_id = p.product_id
                WHERE order_id = :order_id
                ORDER BY p.product_id
                LIMIT :limit
                OFFSET :offset
                """).bindparams(order_id=order_id, limit=limit, offset=offset)
    stmt = select(ProductOrder).from_statement(query)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_employees(db: AsyncSession, limit: int, offset: int) -> Sequence[Employee]:
    query = text("""
                SELECT
                    e.employee_id,
                    e.last_name || ' ' || e.first_name AS employee_full_name,
                    e.title,
                    e.birth_date,
                    e.hire_date,
                    e.address,
                    e.city,
                    e.postal_code,
                    e.country,
                    e.notes,
                    e.reports_to,
                    er.last_name || ' ' || er.first_name AS reports_to_full_name
                FROM employees e
                LEFT JOIN employees er ON e.reports_to = er.employee_id
                ORDER BY e.employee_id
                LIMIT :limit
                OFFSET :offset
                """).bindparams(limit=limit, offset=offset)
    stmt = select(Employee).from_statement(query)
    result = await db.execute(stmt)
    return result.scalars().all()