{{ config(materialized='table', schema='WAREHOUSE') }}

SELECT
    ID AS FACTURE_ID,
    CODE AS FACTURE_CODE,
    CUSTOMER_ID,
    DATE_EDIT,
    YEAR(DATE_EDIT) AS ANNEES,
    MONTHNAME(DATE_EDIT) AS MOIS,
    DAYNAME(DATE_EDIT) AS JOUR,
    QTE_TOTALE,
    TOTAL_AMOUNT,
    TOTAL_PAID
FROM {{ ref('stg_factures') }}
