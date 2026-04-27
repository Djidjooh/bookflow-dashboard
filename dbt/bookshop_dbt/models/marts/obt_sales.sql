{{ config(materialized='table', schema='MARTS') }}

SELECT
    v.VENTE_ID AS ID,
    v.ANNEES,
    v.MOIS,
    v.JOUR,
    v.PU,
    v.QTE,
    v.MONTANT_LIGNE,

    f.FACTURE_ID,
    f.FACTURE_CODE,
    f.QTE_TOTALE,
    f.TOTAL_AMOUNT,
    f.TOTAL_PAID,

    c.CATEGORY_INTITULE,

    b.CODE AS BOOK_CODE,
    b.INTITULE AS BOOK_INTITULE,
    b.ISBN_10,
    b.ISBN_13,

    dc.CUSTOMER_CODE,
    dc.NOM

FROM {{ ref('fact_ventes') }} v
LEFT JOIN {{ ref('fact_factures') }} f
    ON v.FACTURE_ID = f.FACTURE_ID
LEFT JOIN {{ ref('dim_books') }} b
    ON v.BOOK_ID = b.BOOK_ID
LEFT JOIN {{ ref('dim_category') }} c
    ON b.CATEGORY_NAME = c.CATEGORY_INTITULE
LEFT JOIN {{ ref('dim_customers') }} dc
    ON f.CUSTOMER_ID = dc.CUSTOMER_ID
