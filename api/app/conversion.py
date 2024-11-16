import schemas
import models


def map_order_to_schema(order: models.Order) -> schemas.Order:
    return schemas.Order(
        id=order.order_id,
        employee=schemas.EmployeeBase(id=order.employee_id, name=order.employee_full_name),
        customer=schemas.Customer(id=order.customer_id, name=order.customer_company_name),
        order_date=order.order_date,
        shipment=schemas.Shipment(
            ship_via=schemas.Shipper(id=order.ship_via, name=order.ship_company_name),
            name=order.ship_name,
            address=order.ship_address,
            city=order.ship_city,
            postal_code=order.ship_postal_code,
            country=order.ship_country,
            required_date=order.required_date,
            shipped_date=order.shipped_date
        )
    )

def map_employee_to_schema(employee: models.Employee) -> schemas.Employee:
    return schemas.Employee(
        id=employee.employee_id,
        name=employee.employee_full_name,
        title=employee.title,
        birth_date=employee.birth_date,
        hire_date=employee.hire_date,
        address=employee.address,
        city=employee.city,
        postal_code=employee.postal_code,
        country=employee.country,
        notes=employee.notes,
        reports_to=schemas.EmployeeBase(id=employee.reports_to, name=employee.reports_to_full_name),
        total_sales=employee.total_sales
    )

def map_largest_order_to_schema(order: models.LargestOrder) -> schemas.LargestOrder:
    return schemas.LargestOrder(
        id=order.order_id,
        employee=schemas.EmployeeBase(id=order.employee_id, name=order.employee_full_name),
        customer=schemas.Customer(id=order.customer_id, name=order.customer_company_name),
        order_date=order.order_date,
        shipment=schemas.Shipment(
            ship_via=schemas.Shipper(id=order.ship_via, name=order.ship_company_name),
            name=order.ship_name,
            address=order.ship_address,
            city=order.ship_city,
            postal_code=order.ship_postal_code,
            country=order.ship_country,
            required_date=order.required_date,
            shipped_date=order.shipped_date
        ),
        product=schemas.ProductOrder(
            product_id=order.product_id,
            product_name=order.product_name,
            unit_price=order.unit_price,
            quantity=order.quantity,
            discount=order.discount,
            total_price=order.total_price,
        )
    )