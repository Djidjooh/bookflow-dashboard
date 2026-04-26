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

    df = run_query("SELECT * FROM BOOKSHOP.MARTS.OBT_SALES")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nombre de ventes", f"{df['ID'].nunique():,}")
    col2.metric("Chiffre d'affaires", f"{df['MONTANT_LIGNE'].sum():,.0f} FCFA")
    col3.metric("Quantité vendue", f"{df['QTE'].sum():,.0f}")
    col4.metric("Nombre de clients", f"{df['ID'].nunique():,}")

    st.divider()

    df_cat = df.groupby("CATEGORY_INTITULE", as_index=False)["MONTANT_LIGNE"].sum()
    fig = px.pie(
        df_cat,
        values="MONTANT_LIGNE",
        names="CATEGORY_INTITULE",
        title="Chiffre d'affaires par catégorie"
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Ventes par Période":
    st.header("Analyse des ventes par période")

    df = run_query("SELECT * FROM BOOKSHOP.MARTS.OBT_SALES")

    df_an = df.groupby("ANNEES", as_index=False).agg(
        TOTAL_QTE=("QTE", "sum"),
        TOTAL_CA=("MONTANT_LIGNE", "sum")
    )

    fig_an = px.bar(
    df_an,
    x="ANNEES",
    y="TOTAL_CA",
    color="ANNEES",
    color_discrete_sequence=["#1f77b4","#2ca02c","#d62728","#ff7f0e","#9467bd","#17becf","#e377c2"],
    text="TOTAL_CA",
    title="Chiffre d'affaires par année"
    )
    st.plotly_chart(fig_an, use_container_width=True)

    df_mois = df.groupby("MOIS", as_index=False).agg(
        TOTAL_QTE=("QTE", "sum"),
        TOTAL_CA=("MONTANT_LIGNE", "sum")
    )

    fig_mois_line = px.line(
    df_mois,
    x="MOIS",
    y="TOTAL_CA",
    markers=True,
    title="Évolution mensuelle du chiffre d'affaires"
    )
    st.plotly_chart(fig_mois_line, use_container_width=True)
    
    fig_area = px.area(
    df_mois,
    x="MOIS",
    y="TOTAL_CA",
    title="Tendance cumulée du chiffre d'affaires mensuel"
    )
    st.plotly_chart(fig_area, use_container_width=True)

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
            BOOK_INTITULE,
            CATEGORY_INTITULE,
            SUM(QTE) AS TOTAL_QTE,
            SUM(MONTANT_LIGNE) AS TOTAL_CA
        FROM BOOKSHOP.MARTS.OBT_SALES
        GROUP BY BOOK_CODE, BOOK_INTITULE, CATEGORY_INTITULE
        ORDER BY TOTAL_QTE DESC
    """)

    top_n = st.slider("Nombre de livres à afficher", 5, 20, 10)
    df_top = df.head(top_n)

    fig_books = px.bar(
    df_top,
    x="TOTAL_QTE",
    y="BOOK_INTITULE",
    color="CATEGORY_INTITULE",
    orientation="h",
    title="Top livres vendus"
    )
    fig_books.update_traces(marker_color="purple")
    st.plotly_chart(fig_books, use_container_width=True)

    fig2 = px.bar(
        df_top,
        x="BOOK_INTITULE",
        y="TOTAL_CA",
        color="CATEGORY_INTITULE",
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
            NOM,
            COUNT(DISTINCT ID) AS NB_VENTES,
            SUM(QTE) AS TOTAL_QTE_ACHETEE,
            SUM(MONTANT_LIGNE) AS TOTAL_DEPENSE
        FROM BOOKSHOP.MARTS.OBT_SALES
        GROUP BY CUSTOMER_CODE, NOM
        ORDER BY TOTAL_DEPENSE DESC
    """)

    fig1 = px.bar(
        df.head(20),
        x="NOM",
        y="TOTAL_DEPENSE",
        title="Top clients par dépense totale"
    )
    fig1.update_xaxes(tickangle=45)
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        df.head(20),
        x="NOM",
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
        FROM BOOKSHOP.MARTS.OBT_SALES
        ORDER BY ID
    """)

    st.write(f"{len(df)} lignes disponibles")
    st.dataframe(df, use_container_width=True)
