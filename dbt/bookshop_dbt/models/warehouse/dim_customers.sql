{{ config(materialized='table', schema='WAREHOUSE') }}

SELECT
    ID AS CUSTOMER_ID,
    CODE AS CUSTOMER_CODE,
    FIRST_NAME,
    LAST_NAME,
    FIRST_NAME || ' ' || LAST_NAME AS NOM,
    EMAIL
FROM {{ ref('stg_customers') }}
