{{ config(materialized='table', schema='WAREHOUSE') }}

SELECT
    ID AS CUSTOMER_ID,
    CODE,
    FIRST_NAME,
    LAST_NAME,
    EMAIL
FROM {{ ref('stg_customers') }}
