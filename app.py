## importation des packages 
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

## titre 
st.title("📊 Club IA - Faculté d'Agronomie")
st.subheader("Tableau de bord de l'étudiant")

## upload du fichier
notes = pd.read_excel('Notes.xlsx')

## Data cleaning 
notes.columns = notes.columns.str.strip().str.lower()
notes['code_etudiant'] = notes['code_etudiant'].str.strip().str.upper()
notes['nom'] = notes['nom'].str.strip()
notes[["exo", "presence", "total"]] = notes[["exo", "presence", "total"]].apply(pd.to_numeric, errors = "coerce")

## Enter code 
st.info("""Entrez votre code étudiant ci-dessous. Votre code est au format : NOM2025.
Ex: FAGBEDJI2025 ou FAGBEDJI-AVITIKPAMBA2025 ou FAGBEDJICHABI2025""")

user_text = st.text_input("Entrez votre code étudiant", placeholder="Ex: JOHN2025")
if user_text:
        etudiant = notes[notes['code_etudiant']==user_text]
        nom = etudiant['nom'].values[0]
        note = etudiant['total'].values[0]
        rang = (notes['total'] > note).sum() + 1
        max_total = notes['total'].max()
        exo = etudiant['exo'].values[0]
        contribution_exo = (exo * 100) / note
        percentile = (notes['total'] <= note).mean() * 100
        fig = px.histogram(
                        notes, x='total', nbins=8, labels={'total':'Total des points'}, color_discrete_sequence=['#1f77b4'])
        fig.add_vline(x=note, line_dash="dash", line_color="red",
                  annotation_text=f"VOUS ({note})", annotation_position="top")
        fig.update_layout(height=300, showlegend=False)

        ## Leaderboard table conception
        top5 = notes.nlargest(5,'total')[['nom','total']].copy().reset_index(drop=True)
        top5.index = ['🥇','🥈','🥉','4️⃣','5️⃣']
        top5.columns = ['nom','total']
        top5_html = top5.to_html(index=True)

        ## Performance 
        st.subheader("Vos performances")
        col1, col2, col3 = st.columns(3)
        col1.metric("Note Totale", f"{note} pts")
        col2.metric("Rang", f"{rang}e / {len(notes)}")
        col3.metric("Percentile", f"{percentile:.1f}%")

        ## Summary for student 
        st.subheader("Résumé")
        metrics = f"""{nom}, vous avez un total de {note} pts. Vous êtes {rang} ème sur {len(notes)} étudiants. 
        Les exercices représentent {float(contribution_exo):.2f} % de votre note (soit {exo}/{note}).
        Vous faites mieux que {percentile:.1f} % des étudiants."""
        st.write(metrics)

        ## Histogram for notes distributions 
        st.subheader("Distribution des notes")
        st.write(fig)

        ## Leaderboard table 
        st.subheader("Leaderboard (Top 5)")
        st.write(top5)
        
st.markdown("---")
st.caption("🤖 CIA-FA Dashboard • Développé avec ❤️ par Club IA - Faculté d'Agronomie. \n Dernière mise à jour le 05/04/2026.")


