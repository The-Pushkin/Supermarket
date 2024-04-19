CREATE TABLE IF NOT EXISTS Products (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_price REAL NOT NULL,
    product_stock INTEGER NOT NULL
);
