{{ config(materialized='table', schema='STAGGING') }}

SELECT *
FROM {{ source('raw', 'BOOKS') }}
