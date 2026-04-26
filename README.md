# 📚 BookFlow Dashboard

## 🚀 Présentation du projet

BookFlow Dashboard est une plateforme décisionnelle moderne développée dans le cadre d’un projet Big Data / Data Engineering.

L’objectif principal est de concevoir un pipeline complet de traitement et de valorisation de données de ventes d’une librairie, depuis une base transactionnelle PostgreSQL jusqu’à un tableau de bord analytique interactif accessible en ligne.

Le projet met en œuvre une architecture moderne de données basée sur :

- PostgreSQL (source transactionnelle)
- Snowflake (Data Warehouse Cloud)
- dbt (transformations ELT)
- Streamlit (visualisation interactive)
- Docker (conteneurisation)
- GitHub (versioning & déploiement)

---

## 🏗️ Architecture du projet

```text
PostgreSQL
   ↓
Snowflake RAW
   ↓
dbt STAGGING
   ↓
dbt WAREHOUSE
   ↓
dbt MARTS
   ↓
Streamlit Dashboard Public

📊 Fonctionnalités principales
Dashboard interactif :
Vue globale des ventes
Chiffre d'affaires total
Nombre de ventes
Quantité vendue
Nombre de clients
Analyse par période
Top livres vendus
Analyse clients
Table finale analytique (OBT)
Pipeline Data :
Ingestion PostgreSQL → Snowflake
Modélisation dimensionnelle
Création des couches RAW / STAGGING / WAREHOUSE / MARTS
Déploiement cloud public


🛠️ Technologies utilisées

| Outil      | Rôle                  |
| ---------- | --------------------- |
| PostgreSQL | Base transactionnelle |
| Snowflake  | Data Warehouse Cloud  |
| dbt        | Transformation ELT    |
| Streamlit  | Dashboard interactif  |
| Docker     | Conteneurisation      |
| GitHub     | Versioning            |



📁 Structure du projet
bookflow-dashboard/
│── dashboard/
│   └── app.py
│── scripts/
│   ├── 01_setup_snowflake.py
│   └── 02_ingest_postgres_to_snowflake.py
│── models/
│── docker-compose.yml
│── requirements.txt
│── README.md


⚙️ Installation locale

git clone https://github.com/Djidjooh/bookflow-dashboard.git
cd bookflow-dashboard
docker-compose up -d


🔐 Variables d’environnement

SNOWFLAKE_ACCOUNT=xxxx
SNOWFLAKE_USER=xxxx
SNOWFLAKE_PASSWORD=xxxx
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=BOOKSHOP

▶️ Lancer l’application

streamlit run dashboard/app.py

🌍 Déploiement public

Application disponible en ligne via Streamlit Cloud :https://bookflow-dashboard.streamlit.app


