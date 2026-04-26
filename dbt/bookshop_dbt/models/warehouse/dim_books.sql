{{ config(materialized='table', schema='WAREHOUSE') }}

SELECT
    b.ID AS BOOK_ID,
    b.CODE,
    b.INTITULE,
    b.ISBN_10,
    b.ISBN_13,
    c.INTITULE AS CATEGORY_NAME
FROM {{ ref('stg_books') }} b
LEFT JOIN {{ ref('stg_category') }} c
ON b.CATEGORY_ID = c.ID
