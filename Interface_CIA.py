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
@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(r"Notes.csv", sep = ";")

notes = load_data()

# ===== HEADER =====
st.title("🎓 CIA-FA - Tableau de Bord Notes")
st.markdown("*Suivi des performances 2025*")
st.markdown("---")

# ===== SIDEBAR =====
with st.sidebar:
    st.header("🔐 Connexion")
    
    code = st.text_input(
        "Code étudiant",
        type="password",
        placeholder="Ex: JEAN2025"
    )
    
    st.markdown("---")
    st.caption("💡 Format : NOM2025")
    
    if st.button("🔄 Actualiser"):
        st.cache_data.clear()
        st.rerun()

# ===== LOGIQUE PRINCIPALE =====
if code:
    etudiant = notes[notes['code_etudiant'] == code.upper()]
    
    if not etudiant.empty:
        # ===== INFOS ETUDIANT =====
        nom = etudiant['nom'].values[0]
        total = etudiant['total'].values[0]
        rang = (notes['total'] > total).sum() + 1
        
        # ===== BIENVENUE =====
        st.success(f"👋 Bienvenue **{nom}** !")
        
        # ===== METRIQUES =====
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
        
        # ===== LAYOUT =====
        col_left, col_right = st.columns(2)
        
        # ===== TOP 5 =====
        with col_left:
            st.subheader("🏆 Top 5 CIA-FA")
            
            top5 = notes.nlargest(5, 'total')[['nom', 'total']].copy()
            top5 = top5.reset_index(drop=True)
            top5.index = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
            top5.columns = ['Nom', 'Total']
            
            def highlight_user(row):
                if row['Nom'] == nom:
                    return ['background-color: #90EE90'] * len(row)
                return [''] * len(row)
            
            st.dataframe(top5.style.apply(highlight_user, axis=1),
                         use_container_width=True, height=220)
            
            # Feedback classement
            if rang <= 3:
                st.success("🔥 Tu es sur le podium ! Bravo !")
            elif rang <= 5:
                st.info("⭐ Top 5 ! Encore un effort !")
            else:
                ecart = top5.iloc[4]['Total'] - total
                st.info(f"💡 À {ecart} pts du Top 5 !")
        
        # ===== VISUALISATION =====
        with col_right:
            st.subheader("📊 Ta Position")
            
            fig = px.histogram(
                notes,
                x='total',
                nbins=8,
                labels={'total': 'Total Points'},
            )
            
            fig.add_vline(
                x=total,
                line_dash="dash",
                line_width=3,
                annotation_text=f"TOI ({total})"
            )
            
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # ===== COMPARAISON =====
            st.subheader("📈 Comparaison Classe")
            
            col_a, col_b = st.columns(2)
            
            moyenne = notes['total'].mean()
            delta = total - moyenne
            
            with col_a:
                st.metric("Moyenne Classe",
                          f"{moyenne:.0f} pts",
                          delta=f"{delta:+.0f}")
            
            with col_b:
                ecart = notes['total'].max() - total
                st.metric("Écart avec 1er", f"{ecart} pts")
        
        # ===== FEEDBACK FINAL =====
        st.markdown("---")
        
        if total >= 450:
            st.balloons()
            st.success("🏆 EXCELLENCE ! Tu domines complètement ! 🔥")
        elif total >= 400:
            st.success("💪 Très forte performance ! Continue !")
        elif total >= 350:
            st.info("👍 Bon niveau, continue !")
        else:
            st.warning("💡 Accroche-toi ! 🚀")
    
    else:
        st.error("❌ Code invalide !")
        st.info("💡 Format : NOM2025 (ex: JEAN2025)")

# ===== PAGE ACCUEIL =====
else:
    st.info("👈 Entre ton code étudiant dans la barre latérale")
    
    st.markdown("---")
    
    st.subheader("📊 Statistiques Générales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Membres", len(notes))
    
    with col2:
        st.metric("📈 Moyenne", f"{notes['total'].mean():.0f} pts")
    
    with col3:
        st.metric("🥇 Meilleur", f"{notes['total'].max()} pts")
    
    with col4:
        st.metric("📊 Médiane", f"{notes['total'].median():.0f} pts")
    
    # ===== BOXPLOT =====
    st.subheader("📊 Distribution des Notes")
    
    fig = px.box(notes, y='total')
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ===== TOP 3 =====
    st.subheader("👀 Aperçu Top 3")
    
    top3 = notes.nlargest(3, 'total')[['nom', 'total']]
    top3.index = ['🥇', '🥈', '🥉']
    top3.columns = ['Champion', 'Score']
    
    st.dataframe(top3, use_container_width=True)
    
    st.caption("🔐 Connecte-toi pour voir plus !")

# ===== FOOTER =====
st.markdown("---")
st.caption("🤖 CIA-FA Dashboard • Développé par Boris Camille FAGBEDJI")
