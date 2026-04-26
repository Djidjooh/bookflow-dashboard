import os
import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

st.set_page_config(
    page_title="BookFlow Dashboard",
    page_icon="📚",
    layout="wide",
)

@st.cache_resource
def get_snowflake_conn():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "BOOKSHOP"),
        role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    )

@st.cache_data(ttl=300)
def run_query(sql):
    conn = get_snowflake_conn()
    return pd.read_sql(sql, conn)

st.sidebar.title("📚 BookFlow")
st.sidebar.markdown("Projet M2 - Architecture Big Data")

page = st.sidebar.radio(
    "Navigation",
    ["Vue Globale", "Ventes par Période", "Top Livres", "Clients", "Détail OBT"],
)

st.title("📚 BookFlow — Tableau de bord des ventes de livres")

if page == "Vue Globale":
    st.header("Vue globale des ventes")

    df = run_query("SELECT * FROM BOOKSHOP.RAW_MARTS.OBT_SALES")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nombre de ventes", f"{df['SALE_ID'].nunique():,}")
    col2.metric("Chiffre d'affaires", f"{df['TOTAL_LINE'].sum():,.0f} FCFA")
    col3.metric("Quantité vendue", f"{df['QTE'].sum():,.0f}")
    col4.metric("Nombre de clients", f"{df['CUSTOMER_ID'].nunique():,}")

    st.divider()

    df_cat = df.groupby("CATEGORY_NAME", as_index=False)["TOTAL_LINE"].sum()
    fig = px.pie(
        df_cat,
        values="TOTAL_LINE",
        names="CATEGORY_NAME",
        title="Chiffre d'affaires par catégorie"
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Ventes par Période":
    st.header("Analyse des ventes par période")

    df = run_query("SELECT * FROM BOOKSHOP.RAW_MARTS.OBT_SALES")

    df_an = df.groupby("ANNEE", as_index=False).agg(
        TOTAL_QTE=("QTE", "sum"),
        TOTAL_CA=("TOTAL_LINE", "sum")
    )

    fig_an = px.bar(
        df_an,
        x="ANNEE",
        y="TOTAL_CA",
        title="Chiffre d'affaires par année"
    )
    st.plotly_chart(fig_an, use_container_width=True)

    df_mois = df.groupby("MOIS", as_index=False).agg(
        TOTAL_QTE=("QTE", "sum"),
        TOTAL_CA=("TOTAL_LINE", "sum")
    )

    fig_mois = px.bar(
        df_mois,
        x="MOIS",
        y="TOTAL_CA",
        title="Chiffre d'affaires par mois"
    )
    st.plotly_chart(fig_mois, use_container_width=True)

    df_jour = df.groupby("JOUR", as_index=False)["QTE"].sum()

    fig_jour = px.bar(
        df_jour,
        x="JOUR",
        y="QTE",
        title="Quantité vendue par jour de la semaine"
    )
    st.plotly_chart(fig_jour, use_container_width=True)

elif page == "Top Livres":
    st.header("Top livres vendus")

    df = run_query("""
        SELECT
            BOOK_CODE,
            BOOK_TITLE,
            CATEGORY_NAME,
            SUM(QTE) AS TOTAL_QTE,
            SUM(TOTAL_LINE) AS TOTAL_CA
        FROM BOOKSHOP.RAW_MARTS.OBT_SALES
        GROUP BY BOOK_CODE, BOOK_TITLE, CATEGORY_NAME
        ORDER BY TOTAL_QTE DESC
    """)

    top_n = st.slider("Nombre de livres à afficher", 5, 20, 10)
    df_top = df.head(top_n)

    fig1 = px.bar(
        df_top,
        x="BOOK_TITLE",
        y="TOTAL_QTE",
        color="CATEGORY_NAME",
        title=f"Top {top_n} livres par quantité vendue"
    )
    fig1.update_xaxes(tickangle=45)
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        df_top,
        x="BOOK_TITLE",
        y="TOTAL_CA",
        color="CATEGORY_NAME",
        title=f"Top {top_n} livres par chiffre d'affaires"
    )
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df, use_container_width=True)

elif page == "Clients":
    st.header("Analyse des clients")

    df = run_query("""
        SELECT
            CUSTOMER_CODE,
            CUSTOMER_NAME,
            COUNT(DISTINCT SALE_ID) AS NB_VENTES,
            SUM(QTE) AS TOTAL_QTE_ACHETEE,
            SUM(TOTAL_LINE) AS TOTAL_DEPENSE
        FROM BOOKSHOP.RAW_MARTS.OBT_SALES
        GROUP BY CUSTOMER_CODE, CUSTOMER_NAME
        ORDER BY TOTAL_DEPENSE DESC
    """)

    fig1 = px.bar(
        df.head(20),
        x="CUSTOMER_NAME",
        y="TOTAL_DEPENSE",
        title="Top clients par dépense totale"
    )
    fig1.update_xaxes(tickangle=45)
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        df.head(20),
        x="CUSTOMER_NAME",
        y="NB_VENTES",
        title="Nombre de ventes par client"
    )
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df, use_container_width=True)

elif page == "Détail OBT":
    st.header("Table finale OBT Sales")

    df = run_query("""
        SELECT *
        FROM BOOKSHOP.RAW_MARTS.OBT_SALES
        ORDER BY SALE_ID
    """)

    st.write(f"{len(df)} lignes disponibles")
    st.dataframe(df, use_container_width=True)
