{{ config(materialized='table', schema='MARTS') }}

SELECT
    fs.SALE_ID,
    fs.DATE_EDIT,
    YEAR(fs.DATE_EDIT) AS ANNEE,
    MONTHNAME(fs.DATE_EDIT) AS MOIS,
    DAYNAME(fs.DATE_EDIT) AS JOUR,

    fs.PU,
    fs.QTE,
    fs.TOTAL_LINE,

    dc.CUSTOMER_ID,
    dc.CODE AS CUSTOMER_CODE,
    dc.FIRST_NAME,
    dc.LAST_NAME,
    dc.FIRST_NAME || ' ' || dc.LAST_NAME AS CUSTOMER_NAME,
    dc.EMAIL,

    db.BOOK_ID,
    db.CODE AS BOOK_CODE,
    db.INTITULE AS BOOK_TITLE,
    db.ISBN_10,
    db.ISBN_13,
    db.CATEGORY_NAME

FROM {{ ref('fact_sales') }} fs
LEFT JOIN {{ ref('dim_customers') }} dc
    ON fs.CUSTOMER_ID = dc.CUSTOMER_ID
LEFT JOIN {{ ref('dim_books') }} db
    ON fs.BOOK_ID = db.BOOK_ID
