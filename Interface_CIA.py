import streamlit as st
import pandas as pd
import plotly.express as px

# ===== CONFIG =====
st.set_page_config(
    page_title="Notes CIA-FA",
    page_icon="🎓",
    layout="wide"
)

# ===== CHARGEMENT & NETTOYAGE =====
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv("Notes.csv", sep=";", encoding="utf-8")

        # Nettoyage colonnes
        df.columns = df.columns.str.strip().str.lower()

        # Nettoyage codes étudiants
        df['code_etudiant'] = (
            df['code_etudiant']
            .astype(str)
            .str.strip()
            .str.replace(" ", "", regex=False)
            .str.upper()
        )

        # Nettoyage noms
        df['nom'] = df['nom'].astype(str).str.strip()

        # Conversion total
        df['total'] = pd.to_numeric(df['total'], errors='coerce')

        # Supprimer lignes invalides
        df = df.dropna(subset=['code_etudiant', 'total'])

        return df

    except Exception as e:
        st.error(f"Erreur chargement données : {e}")
        st.stop()

notes = load_data()

# ===== HEADER =====
st.title("🎓 CIA-FA - Tableau de Bord Notes")
st.markdown("*Suivi des performances 2025*")
st.markdown("---")

# ===== SIDEBAR =====
with st.sidebar:
    st.header("🔐 Connexion")

    code_input = st.text_input(
        "Code étudiant",
        type="password",
        placeholder="Ex: JEAN2025"
    )

    code = code_input.strip().replace(" ", "").upper()

    st.markdown("---")

    if st.button("🔄 Actualiser"):
        st.cache_data.clear()
        st.rerun()

# ===== LOGIQUE PRINCIPALE =====
if code:
    etudiant = notes[notes['code_etudiant'] == code]

    if not etudiant.empty:
        nom = etudiant['nom'].iloc[0]
        total = etudiant['total'].iloc[0]

        rang = (notes['total'] > total).sum() + 1
        max_total = notes['total'].max()
        moyenne = notes['total'].mean()

        # Percentile
        percentile = (notes['total'] < total).mean() * 100

        # ===== BIENVENUE =====
        st.success(f"👋 Bienvenue **{nom}** !")

        # ===== METRIQUES =====
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📊 Total", f"{total:.0f} pts")

        with col2:
            medal = "🥇" if rang == 1 else "🥈" if rang == 2 else "🥉" if rang == 3 else "🏅"
            st.metric("Classement", f"{medal} {rang}/{len(notes)}")

        with col3:
            progression = (total / max_total) * 100
            st.metric("Progression", f"{progression:.1f}%")

        with col4:
            st.metric("📈 Percentile", f"{percentile:.0f}%")

        st.markdown("---")

        # ===== LAYOUT =====
        col_left, col_right = st.columns(2)

        # ===== TOP 5 =====
        with col_left:
            st.subheader("🏆 Top 5 CIA-FA")

            top5 = notes.nlargest(5, 'total')[['nom', 'total']].copy()
            top5.index = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
            top5.columns = ['Nom', 'Total']

            def highlight(row):
                return ['background-color: #90EE90']*len(row) if row['Nom'] == nom else ['']*len(row)

            st.dataframe(top5.style.apply(highlight, axis=1),
                         use_container_width=True)

            # Feedback
            if percentile >= 90:
                st.success("🔥 Top 10% de la classe !")
            elif percentile >= 75:
                st.info("💪 Top 25% ! Très bon niveau")
            elif percentile >= 50:
                st.info("👍 Au-dessus de la moyenne")
            else:
                st.warning("💡 Continue tes efforts !")

        # ===== VISUALISATION =====
        with col_right:
            st.subheader("📊 Distribution")

            fig = px.histogram(notes, x='total', nbins=8)

            fig.add_vline(
                x=total,
                line_dash="dash",
                line_width=3,
                annotation_text=f"TOI ({total:.0f})"
            )

            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            # Comparaison
            st.subheader("📈 Comparaison")

            col_a, col_b = st.columns(2)

            with col_a:
                delta = total - moyenne
                st.metric("Moyenne classe",
                          f"{moyenne:.0f}",
                          delta=f"{delta:+.0f}")

            with col_b:
                ecart = max_total - total
                st.metric("Écart avec 1er", f"{ecart:.0f} pts")

        # ===== FEEDBACK FINAL =====
        st.markdown("---")

        if total >= 450:
            st.balloons()
            st.success("🏆 EXCELLENCE ! Niveau élite 🔥")
        elif total >= 400:
            st.success("💪 Très forte performance !")
        elif total >= 350:
            st.info("👍 Bon niveau")
        else:
            st.warning("💡 Continue tes efforts !")

    else:
        st.error("❌ Code invalide")
        st.info("💡 Vérifie ton code étudiant")

# ===== PAGE ACCUEIL =====
else:
    st.info("👈 Entre ton code étudiant dans la barre latérale")

    st.markdown("---")

    st.subheader("📊 Statistiques générales")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Étudiants", len(notes))

    with col2:
        st.metric("📈 Moyenne", f"{notes['total'].mean():.0f}")

    with col3:
        st.metric("🥇 Max", f"{notes['total'].max():.0f}")

    with col4:
        st.metric("📊 Médiane", f"{notes['total'].median():.0f}")

    # Graph
    fig = px.box(notes, y='total')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Top 3
    st.subheader("👀 Top 3")

    top3 = notes.nlargest(3, 'total')[['nom', 'total']]
    top3.index = ['🥇', '🥈', '🥉']
    top3.columns = ['Nom', 'Score']

    st.dataframe(top3, use_container_width=True)

# ===== FOOTER =====
st.markdown("---")
st.caption("Dernière mise à jour le 20/03/2026")
st.caption("🤖 CIA-FA Dashboard • Développé par Boris Camille FAGBEDJI")
