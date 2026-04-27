{{ config(materialized='table', schema='WAREHOUSE') }}

SELECT
    ID AS CATEGORY_ID,
    CODE AS CATEGORY_CODE,
    INTITULE AS CATEGORY_INTITULE
FROM {{ ref('stg_category') }}
