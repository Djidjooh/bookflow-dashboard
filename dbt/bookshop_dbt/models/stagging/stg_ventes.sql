{{ config(materialized='table', schema='STAGGING') }}

SELECT
    ID,
    FACTURE_ID,
    BOOK_ID,
    TO_DATE(DATE_EDIT, 'YYYYMMDD') AS DATE_EDIT,
    PU,
    QTE
FROM {{ source('raw', 'VENTES') }}
