import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Élections Québec DGEQ", page_icon="🗳️", layout="wide")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    # Ici, tu pourras plus tard mettre : pd.read_csv("ton_fichier.csv")
    data = {
        "Circonscription": ["Laval-des-Rapides", "Sainte-Rose", "Vimont", "Mille-Îles", "Fabre", "Chomedey"],
        "Participation (%)": [68.5, 72.1, 70.3, 69.8, 65.4, 60.2],
        "CAQ (%)": [35.2, 42.1, 38.5, 36.0, 30.1, 25.4],
        "PLQ (%)": [28.4, 22.0, 25.1, 29.5, 45.2, 55.1],
        "QS (%)": [18.1, 15.3, 14.8, 13.2, 10.5, 8.2],
        "PQ (%)": [11.3, 15.6, 13.6, 13.3, 8.2, 6.3],
        "PCQ (%)": [7.0, 5.0, 8.0, 8.0, 6.0, 5.0]
    }
    return pd.DataFrame(data)

df = load_data()

# --- INTERFACE UTILISATEUR ---
st.title("🗳️ Tableau de Bord - Élections Québec")
st.markdown("Comparez les résultats électoraux et analysez la répartition des votes.")

# --- BARRE LATÉRALE ---
st.sidebar.header("Paramètres de comparaison")
liste_circos = df["Circonscription"].tolist()

circo1 = st.sidebar.selectbox("Circonscription 1", liste_circos, index=0)
circo2 = st.sidebar.selectbox("Circonscription 2", liste_circos, index=1)

# --- EXTRACTION DES DONNÉES ---
data_circo1 = df[df["Circonscription"] == circo1].iloc[0]
data_circo2 = df[df["Circonscription"] == circo2].iloc[0]

# --- AFFICHAGE DES INDICATEURS ---
st.subheader("📊 Aperçu de la participation")
col1, col2 = st.columns(2)

col1.metric(label=f"Participation - {circo1}", value=f"{data_circo1['Participation (%)']}%")
col2.metric(label=f"Participation - {circo2}", value=f"{data_circo2['Participation (%)']}%",
              delta=f"{(data_circo2['Participation (%)'] - data_circo1['Participation (%)']):.1f}%")

st.markdown("---")

# --- GRAPHIQUES ---
st.subheader("📈 Répartition des votes")

partis = ["CAQ (%)", "PLQ (%)", "QS (%)", "PQ (%)", "PCQ (%)"]
df_graphique = pd.DataFrame({
    "Parti": partis * 2,
    "Pourcentage": [data_circo1[p] for p in partis] + [data_circo2[p] for p in partis],
    "Circonscription": [circo1] * 5 + [circo2] * 5
})

fig = px.bar(df_graphique, x="Parti", y="Pourcentage", color="Circonscription",
             barmode="group", title=f"Comparaison : {circo1} vs {circo2}")

st.plotly_chart(fig, use_container_width=True)

# --- VUE DONNÉES ---
st.subheader("📋 Base de données complète")
with st.expander("Voir les données brutes"):
    st.dataframe(df, use_container_width=True)

