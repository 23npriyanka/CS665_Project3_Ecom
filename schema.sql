-- schema.sql
-- CS665 Project 3 — Final 3NF Schema
-- Run this to create the schema from scratch (without seeded data)

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sellers;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    created_at  DATE         NOT NULL,
    created_by  VARCHAR(50)
);

CREATE TABLE sellers (
    seller_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_name VARCHAR(100) NOT NULL,
    join_date   DATE         NOT NULL,
    source      VARCHAR(50)
);

CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name VARCHAR(100)    NOT NULL,
    price        DECIMAL(10,2)   NOT NULL CHECK (price >= 0),
    seller_id    INTEGER         NOT NULL,
    note         VARCHAR(100),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER      NOT NULL,
    order_date  DATE         NOT NULL,
    status      VARCHAR(50)  NOT NULL DEFAULT 'pending'
                             CHECK (status IN ('pending','shipped','delivered','cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      INTEGER       NOT NULL,
    product_id    INTEGER       NOT NULL,
    quantity      INTEGER       NOT NULL CHECK (quantity > 0),
    total_price   DECIMAL(10,2),   -- stored computed: quantity × product.price
    flag          VARCHAR(50)   DEFAULT 'ok',
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
