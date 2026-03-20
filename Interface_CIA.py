# 💻 CODE STREAMLIT ULTRA-SIMPLE
import streamlit as st
import pandas as pd
import plotly.express as px

# ===== CONFIG =====
st.set_page_config(
    page_title="Notes CIA-FA",
    page_icon="🎓",
    layout="wide"
)

# ===== CHARGEMENT DONNÉES =====
@st.cache_data
def load_data():
    return pd.read_csv("notes_cia.csv")

notes = load_data()

# ===== HEADER =====
st.title("🎓 CIA-FA - Tableau de Bord Notes")
st.markdown("*Suivi des performances 2025*")
st.markdown("---")

# ===== SIDEBAR : LOGIN =====
with st.sidebar:
    st.header("🔐 Connexion")
    code = st.text_input(
        "Code étudiant", 
        type="password",
        placeholder="Ex: JEAN2025"
    )
    
    st.markdown("---")
    st.caption("💡 Ton code est au format : NOM2025")
    
    if st.button("🔄 Actualiser"):
        st.cache_data.clear()
        st.rerun()

# ===== SI CODE ENTRÉ =====
if code:
    etudiant = notes[notes['code_etudiant'] == code.upper()]
    
    if not etudiant.empty:
        nom = etudiant['nom'].values[0]
        total = etudiant['total'].values[0]
        rang = (notes['total'] > total).sum() + 1
        
        # ===== BIENVENUE =====
        st.success(f"👋 Bienvenue **{nom}** !")
        
        # ===== MÉTRIQUES =====
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Ton Total", f"{total} pts")
        
        with col2:
            medaille = "🥇" if rang == 1 else "🥈" if rang == 2 else "🥉" if rang == 3 else "🏅"
            st.metric("Classement", f"{medaille} {rang}/{len(notes)}")
        
        with col3:
            max_total = notes['total'].max()
            progression = (total / max_total) * 100
            st.metric("Progression", f"{progression:.1f}%")
        
        st.markdown("---")
        
        # ===== DEUX COLONNES =====
        col_left, col_right = st.columns([1, 1])
        
        # ===== TOP 5 =====
        with col_left:
            st.subheader("🏆 Top 5 CIA-FA")
            
            top5 = notes.nlargest(5, 'total')[['nom', 'total']].copy()
            top5 = top5.reset_index(drop=True)
            top5.index = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
            top5.columns = ['Nom', 'Total']
            
            # Highlighting si user dans top 5
            def highlight_user(row):
                if row['Nom'] == nom:
                    return ['background-color: #90EE90'] * len(row)
                return [''] * len(row)
            
            styled_top5 = top5.style.apply(highlight_user, axis=1)
            st.dataframe(styled_top5, use_container_width=True, height=220)
            
            # Feedback contextuel
            if rang <= 3:
                st.success("🔥 Tu es sur le podium ! Bravo champion ! 💪")
            elif rang <= 5:
                st.info("⭐ Top 5 ! Encore un effort pour le podium ! 🚀")
            else:
                ecart = top5.iloc[4]['Total'] - total
                st.info(f"💡 À {ecart} pts du Top 5 ! Continue ! 💪")
        
        # ===== VISUALISATIONS =====
        with col_right:
            st.subheader("📊 Ta Position")
            
            # Graphique distribution avec position user
            fig = px.histogram(
                notes, 
                x='total',
                nbins=8,
                labels={'total': 'Total Points', 'count': 'Nombre étudiants'},
                color_discrete_sequence=['#1f77b4']
            )
            
            # Ligne verticale position user
            fig.add_vline(
                x=total, 
                line_dash="dash", 
                line_color="red",
                line_width=3,
                annotation_text=f"TOI ({total} pts)",
                annotation_position="top"
            )
            
            fig.update_layout(
                showlegend=False,
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Stats comparatives
            st.subheader("📈 Comparaison Classe")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                moyenne_classe = notes['total'].mean()
                delta = total - moyenne_classe
                st.metric(
                    "Moyenne Classe", 
                    f"{moyenne_classe:.0f} pts",
                    delta=f"{delta:+.0f} pts (toi)"
                )
            
            with col_b:
                ecart_premier = notes['total'].max() - total
                st.metric(
                    "Écart avec 1er",
                    f"{ecart_premier} pts"
                )
    
    else:
        st.error("❌ Code invalide ! Vérifie ton code étudiant.")
        st.info("💡 Format attendu : NOM2025 (ex: JEAN2025)")

else:
    # ===== PAGE ACCUEIL =====
    st.info("👈 **Entre ton code étudiant dans la barre latérale** pour voir tes notes")
    
    st.markdown("---")
    
    # Stats globales
    st.subheader("📊 Statistiques Générales CIA-FA")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Membres actifs", len(notes))
    
    with col2:
        st.metric("📈 Moyenne générale", f"{notes['total'].mean():.0f} pts")
    
    with col3:
        st.metric("🥇 Meilleur score", f"{notes['total'].max()} pts")
    
    with col4:
        st.metric("📊 Score médian", f"{notes['total'].median():.0f} pts")
    
    # Distribution globale
    st.subheader("📊 Distribution des Notes")
    
    fig_global = px.box(
        notes,
        y='total',
        labels={'total': 'Total Points'},
        color_discrete_sequence=['#2ecc71']
    )
    
    fig_global.update_layout(height=400)
    
    st.plotly_chart(fig_global, use_container_width=True)
    
    # Leaderboard partiel (juste top 3 pour teaser)
    st.subheader("👀 Aperçu Top 3")
    top3 = notes.nlargest(3, 'total')[['nom', 'total']]
    top3.index = ['🥇', '🥈', '🥉']
    top3.columns = ['Champion', 'Score']
    st.dataframe(top3, use_container_width=True)
    
    st.caption("🔐 Connecte-toi pour voir le Top 5 complet et ta position !")

# Après métriques
if total >= 450:
    st.balloons()
    st.success("🏆 EXCELLENCE ! Tu domines complètement ! 🔥")
elif total >= 400:
    st.success("💪 Très forte performance ! Continue !")
elif total >= 350:
    st.info("👍 Bon niveau général, continue l'effort !")
else:
    st.warning("💡 Accroche-toi ! Le meilleur reste à venir ! 🚀")

# ===== FOOTER =====
st.markdown("---")
st.caption("🤖 CIA-FA Dashboard • Développé avec ❤️ par Boris Camille FAGBEDJI")