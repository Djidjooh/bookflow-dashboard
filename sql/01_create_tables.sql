CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50),
    intitule VARCHAR(255)
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50),
    intitule VARCHAR(255),
    isbn_10 VARCHAR(20),
    isbn_13 VARCHAR(20),
    category_id INT REFERENCES category(id)
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150)
);

CREATE TABLE factures (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50),
    customer_id INT REFERENCES customers(id),
    date_edit VARCHAR(8),
    qte_totale INT,
    total_amount NUMERIC(12,2),
    total_paid NUMERIC(12,2)
);

CREATE TABLE ventes (
    id SERIAL PRIMARY KEY,
    facture_id INT REFERENCES factures(id),
    book_id INT REFERENCES books(id),
    date_edit VARCHAR(8),
    pu NUMERIC(12,2),
    qte INT
);
