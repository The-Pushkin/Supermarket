DROP TABLE IF EXISTS products;

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT UNIQUE NOT NULL,
    product_price REAL NOT NULL,
    product_stock INTEGER NOT NULL
);

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    user_name TEXT UNIQUE NOT NULL,
    user_password TEXT NOT NULL,
    user_role TEXT NOT NULL
);