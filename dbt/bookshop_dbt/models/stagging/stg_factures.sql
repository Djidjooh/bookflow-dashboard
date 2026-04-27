{{ config(materialized='table', schema='STAGGING') }}

SELECT
    ID,
    CODE,
    CUSTOMER_ID,
    TO_DATE(DATE_EDIT, 'YYYYMMDD') AS DATE_EDIT,
    QTE_TOTALE,
    TOTAL_AMOUNT,
    TOTAL_PAID
FROM {{ source('raw', 'FACTURES') }}
