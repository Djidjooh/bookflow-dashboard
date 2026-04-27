{{ config(materialized='table', schema='WAREHOUSE') }}

SELECT
    b.BOOK_ID,
    b.CODE AS BOOK_CODE,
    b.INTITULE AS BOOK_INTITULE,
    v.ANNEES,
    v.MOIS,
    v.JOUR,
    SUM(v.QTE) AS TOTAL_QTE,
    SUM(v.MONTANT_LIGNE) AS TOTAL_CA
FROM {{ ref('fact_ventes') }} v
JOIN {{ ref('dim_books') }} b
    ON v.BOOK_ID = b.BOOK_ID
GROUP BY b.BOOK_ID, b.CODE, b.INTITULE, v.ANNEES, v.MOIS, v.JOUR
