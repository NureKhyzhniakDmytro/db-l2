CREATE TYPE order_result AS (
    product_id smallint,
    product_name varchar(40),
    order_id smallint,
    unit_price real,
    quantity smallint,
    discount real,
    total_price real,
    employee_id smallint,
    employee_full_name varchar(31),
    order_date date,
    required_date date,
    shipped_date date,
    ship_via smallint,
    ship_company_name varchar(40),
    ship_name varchar(40),
    ship_address varchar(60),
    ship_city varchar(15),
    ship_postal_code varchar(10),
    ship_country varchar(15),
    customer_id varchar(5),
    customer_company_name varchar(40)
);

CREATE OR REPLACE FUNCTION get_largest_order(name varchar)
RETURNS order_result
LANGUAGE plpgsql
AS $$
    DECLARE _product_id integer;
    DECLARE result order_result;
    BEGIN
        SELECT p.product_id INTO _product_id
        FROM products p
        WHERE p.product_name = name;

        IF NOT FOUND THEN
            RAISE NOTICE 'Відсутні замовлення товару «%»', name;
            RETURN NULL;
        END IF;

        SELECT
            _product_id,
            name,
            od.order_id,
            od.unit_price,
            od.quantity,
            od.discount,
            ((od.quantity * od.unit_price) * (1 - od.discount))::numeric(10,2) AS total_price,
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
        INTO result
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN employees e ON o.employee_id = e.employee_id
        JOIN shippers s ON o.ship_via = s.shipper_id
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE od.product_id = _product_id
        ORDER BY od.quantity DESC;

        IF NOT FOUND THEN
            RAISE NOTICE 'Відсутні замовлення товару «%»', name;
            RETURN NULL;
        END IF;

        RETURN result;
    END;
$$;
