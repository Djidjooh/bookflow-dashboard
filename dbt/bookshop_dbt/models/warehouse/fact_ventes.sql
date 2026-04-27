{{ config(materialized='table', schema='WAREHOUSE') }}

SELECT
    ID AS VENTE_ID,
    FACTURE_ID,
    BOOK_ID,
    DATE_EDIT,
    YEAR(DATE_EDIT) AS ANNEES,
    MONTHNAME(DATE_EDIT) AS MOIS,
    DAYNAME(DATE_EDIT) AS JOUR,
    PU,
    QTE,
    PU * QTE AS MONTANT_LIGNE
FROM {{ ref('stg_ventes') }}
