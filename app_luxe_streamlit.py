
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Social Listening - Luxe", layout="wide")

st.title("💬 Social Listening – Marques de Luxe (Projet We Are Social)")

@st.cache_data
def load_data():
    df = pd.read_csv("social_listening_luxe_enriched.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# Sélecteurs
brands = df["brand"].unique()
sentiments = df["sentiment"].unique()

col1, col2 = st.columns(2)
with col1:
    selected_brand = st.selectbox("Choisir une marque :", brands)
with col2:
    selected_sentiment = st.selectbox("Filtrer par sentiment :", ["Tous"] + list(sentiments))

# Filtrage
filtered_df = df[df["brand"] == selected_brand]
if selected_sentiment != "Tous":
    filtered_df = filtered_df[filtered_df["sentiment"] == selected_sentiment]

# Graphiques
st.subheader("📊 Tonalité par mois")
monthly = filtered_df.groupby(["month", "sentiment"]).size().reset_index(name="count")
fig1 = px.bar(monthly, x="month", y="count", color="sentiment", barmode="group",
              title=f"Sentiments mensuels pour {selected_brand}")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🔥 Top posts les plus viraux")
filtered_df["engagement"] = filtered_df["likes"] + filtered_df["shares"]
top_posts = filtered_df.sort_values(by="engagement", ascending=False).head(5)
st.dataframe(top_posts[["date", "text", "sentiment", "source", "likes", "shares"]])

st.caption("Projet réalisé par Samadou Kodon – 2025")
