"""
MédiaScope - Dashboard complet avec catégorisation
40 articles (10 par source : CNN, Al Jazeera, BBC News, Reuters)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import glob

# Configuration
st.set_page_config(page_title="MédiaScope", page_icon="📊", layout="wide")

# CSS
st.markdown("""
<style>
.stApp { background-color: #f5f7fb; }
.main-title { text-align: center; padding: 25px; background: white; border-radius: 15px; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.main-title h1 { font-size: 36px; margin: 0; color: #2c3e50; }
.main-title p { font-size: 14px; color: #6c757d; margin-top: 8px; }
.stat-card { background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.stat-number { font-size: 32px; font-weight: bold; color: #1a73e8; }
.stat-label { font-size: 13px; color: #5f6368; margin-top: 8px; }
.filter-box { background: white; padding: 20px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.article-card { background: white; border-radius: 10px; padding: 15px; margin-bottom: 12px; border: 1px solid #e0e4e8; transition: all 0.2s; }
.article-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-color: #1a73e8; }
.article-title { font-size: 15px; font-weight: 500; color: #202124; margin: 8px 0 0 0; }
.badge { padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; display: inline-block; }
.badge-cnn { background: #CC0000; color: white; }
.badge-aj { background: #1E3A5F; color: white; }
.badge-bbc { background: #000000; color: white; }
.badge-reuters { background: #FF8000; color: white; }
.badge-cat { background: #e9ecef; color: #495057; margin-left: 8px; }
.section-title { font-size: 18px; font-weight: 600; color: #2c3e50; margin: 20px 0 15px 0; }
.footer { text-align: center; padding: 20px; margin-top: 30px; border-top: 1px solid #e9ecef; color: #6c757d; font-size: 12px; }
hr { margin: 20px 0; border: none; border-top: 1px solid #e9ecef; }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("""
<div class="main-title">
    <h1>📊 MédiaScope</h1>
    <p>Plateforme d'analyse des tendances médiatiques | Scraping en temps réel</p>
    <p style="font-size: 13px;">📰 CNN | Al Jazeera | BBC News | Reuters</p>
</div>
""", unsafe_allow_html=True)

# =============================================================
# CHARGEMENT DES DONNÉES
# =============================================================
@st.cache_data
def load_data():
    silver_dir = "data/silver"
    
    if not os.path.exists(silver_dir):
        return pd.DataFrame()
    
    parquet_files = glob.glob(f"{silver_dir}/*.parquet")
    
    if not parquet_files:
        return pd.DataFrame()
    
    # Priorité au fichier complet
    complet_files = [f for f in parquet_files if "complet" in f]
    if complet_files:
        latest_file = complet_files[0]
    else:
        latest_file = max(parquet_files, key=os.path.getctime)
    
    df = pd.read_parquet(latest_file)
    return df

df = load_data()

if not df.empty:
    # =============================================================
    # MÉTRIQUES
    # =============================================================
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{len(df)}</div><div class="stat-label">📄 Articles</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{df["source"].nunique()}</div><div class="stat-label">📰 Sources</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{df["categorie_detectee"].nunique()}</div><div class="stat-label">🏷️ Thèmes</div></div>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # =============================================================
    # FILTRES INTERACTIFS
    # =============================================================
    st.markdown('<div class="filter-box">', unsafe_allow_html=True)
    st.markdown("### 🔍 Filtres interactifs")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        sources_list = df["source"].unique().tolist()
        selected_sources = st.multiselect("📰 Filtrer par source", sources_list, default=sources_list)
    with col_f2:
        categories_list = df["categorie_detectee"].unique().tolist()
        selected_categories = st.multiselect("🏷️ Filtrer par thème", categories_list, default=categories_list)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Application des filtres
    df_filtered = df[df["source"].isin(selected_sources)]
    df_filtered = df_filtered[df_filtered["categorie_detectee"].isin(selected_categories)]
    
    st.info(f"📊 **{len(df_filtered)} articles** correspondent à vos filtres (sur {len(df)} total)")
    
    # =============================================================
    # GRAPHIQUES
    # =============================================================
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown('<div class="section-title">📊 Articles par source</div>', unsafe_allow_html=True)
        if not df_filtered.empty:
            source_counts = df_filtered["source"].value_counts().reset_index()
            source_counts.columns = ["Source", "Nombre"]
            fig = px.bar(source_counts, x="Source", y="Nombre", color="Source",
                         color_discrete_sequence=['#CC0000', '#1E3A5F', '#000000', '#FF8000'],
                         text="Nombre")
            fig.update_layout(showlegend=False, height=350, plot_bgcolor='white')
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
    
    with col_g2:
        st.markdown('<div class="section-title">🏷️ Répartition par thème</div>', unsafe_allow_html=True)
        if not df_filtered.empty:
            cat_counts = df_filtered["categorie_detectee"].value_counts().reset_index()
            cat_counts.columns = ["Thème", "Nombre"]
            fig = px.pie(cat_counts, values="Nombre", names="Thème", hole=0.3,
                         color_discrete_sequence=px.colors.sequential.Plasma_r)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    # =============================================================
    # DERNIERS ARTICLES
    # =============================================================
    st.markdown('<div class="section-title">🆕 Derniers articles</div>', unsafe_allow_html=True)
    
    for _, row in df_filtered.head(40).iterrows():
        badge_class = {
            'CNN': 'badge-cnn',
            'Al Jazeera': 'badge-aj',
            'BBC News': 'badge-bbc',
            'Reuters': 'badge-reuters'
        }.get(row['source'], 'badge-cnn')
        
        st.markdown(f"""
        <div class="article-card">
            <div>
                <span class="{badge_class}">{row['source']}</span>
                <span class="badge badge-cat">{row['categorie_detectee']}</span>
                <span style="float: right; font-size: 12px; color: #6c757d;">📅 {row['date_publication']}</span>
            </div>
            <div class="article-title">{row['titre']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # =============================================================
    # STATISTIQUES DÉTAILLÉES
    # =============================================================
    st.markdown('<div class="section-title">📋 Récapitulatif</div>', unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("**📰 Par source :**")
        st.dataframe(df_filtered.groupby('source').size().reset_index(name='Nombre'), use_container_width=True)
    with col_r2:
        st.markdown("**🏷️ Par thème :**")
        st.dataframe(df_filtered.groupby('categorie_detectee').size().reset_index(name='Nombre'), use_container_width=True)

else:
    st.warning("⚠️ Aucune donnée trouvée.")

# Footer
st.markdown(f"""
<div class="footer">
    MédiaScope v2.0 | Dernière mise à jour : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""", unsafe_allow_html=True)