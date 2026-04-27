{{ config(materialized='table', schema='WAREHOUSE') }}

SELECT
    v.ID AS SALE_ID,
    v.DATE_EDIT,
    v.FACTURE_ID,
    f.CUSTOMER_ID,
    v.BOOK_ID,
    v.PU,
    v.QTE,
    v.PU * v.QTE AS TOTAL_LINE
FROM {{ ref('stg_ventes') }} v
LEFT JOIN {{ ref('stg_factures') }} f
ON v.FACTURE_ID = f.ID
