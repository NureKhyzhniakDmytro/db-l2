from conversion import map_order_to_schema, map_employee_to_schema, map_largest_order_to_schema
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas
import crud

app = FastAPI()


@app.get("/categories", response_model=schemas.PaginatedCategories)
async def read_categories(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    categories = await crud.get_categories(db, limit, offset)
    total_items = await crud.get_categories_count(db)
    response = schemas.PaginatedCategories(
        data=categories,
        metadata=schemas.PaginationMetadata(
            total_items=total_items,
            limit=limit,
            offset=offset
        )
    )
    return response

@app.get("/categories/{category_id}", response_model=schemas.Category)
async def read_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    category = await crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.get("/categories/{category_id}/products", response_model=schemas.PaginatedCategoryProducts)
async def read_category_products(
    category_id: int,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    category = await crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    products = await crud.get_category_products(db, category_id, limit, offset)
    total_items = await crud.get_category_products_count(db, category_id)
    response = schemas.PaginatedCategoryProducts(
        data=products,
        metadata=schemas.PaginationMetadata(
            total_items=total_items,
            limit=limit,
            offset=offset
        )
    )
    return response

@app.get("/orders", response_model=schemas.PaginatedOrders)
async def read_orders(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    orders = await crud.get_orders(db, limit, offset)
    total_items = await crud.get_orders_count(db)
    response = schemas.PaginatedOrders(
        data=[map_order_to_schema(order) for order in orders],
        metadata=schemas.PaginationMetadata(
            total_items=total_items,
            limit=limit,
            offset=offset
        )
    )
    return response

@app.get("/orders/{order_id}", response_model=schemas.Order)
async def read_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    order = await crud.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return map_order_to_schema(order)

@app.get("/orders/{order_id}/products", response_model=schemas.PaginatedOrderProducts)
async def read_order_products(
    order_id: int,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    order = await crud.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    products = await crud.get_order_products(db, order_id, limit, offset)
    total_items = await crud.get_orders_products_count(db, order_id)
    response = schemas.PaginatedOrderProducts(
        data=products,
        metadata=schemas.PaginationMetadata(
            total_items=total_items,
            limit=limit,
            offset=offset
        )
    )
    return response

@app.get("/orders/{order_id}/price")
async def read_order_price(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await crud.get_order_price(db, order_id)
    return {"result": result}

@app.get("/employees", response_model=schemas.PaginatedEmployees)
async def read_employees(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    employees = await crud.get_employees(db, limit, offset)
    total_items = await crud.get_employees_count(db)
    response = schemas.PaginatedEmployees(
        data=[map_employee_to_schema(employee) for employee in employees],
        metadata=schemas.PaginationMetadata(
            total_items=total_items,
            limit=limit,
            offset=offset
        )
    )
    return response

@app.get("/product/{product_name}/largest", response_model=schemas.LargestOrder)
async def read_largest_order(
    product_name: str,
    db: AsyncSession = Depends(get_db)
):
    order = await crud.get_largest_order(db, product_name)
    if order is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return map_largest_order_to_schema(order)

@app.delete("/employees")
async def delete_employee(
    threshold: float,
    db: AsyncSession = Depends(get_db)
):
    result = await crud.delete_employee(db, threshold)
    return {'status': result}
