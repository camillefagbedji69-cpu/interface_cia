## importation des packages 
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

## titre 
st.title("📊 Club IA - Faculté d'Agronomie - Tableau de bord de l'étudiant")

## upload du fichier
notes = pd.read_excel('Notes.xlsx')

## Data cleaning 
notes.columns = notes.columns.str.strip().str.lower()
notes['code_etudiant'] = notes['code_etudiant'].str.strip().str.upper()
notes['nom'] = notes['nom'].str.strip()
notes['total'] = pd.to_numeric(notes['total'], errors='coerce')
notes = notes.dropna(subset=['code_etudiant', 'total'])

## Enter code 
st.header("Connectez vous")
user_text = st.text_input("Entrez votre code étudiant", placeholder="JOHN2025")
if user_text:
        etudiant = notes[notes['code_etudiant']==user_text]
        nom = etudiant['nom'].values[0]
        total = etudiant['total'].values[0]
        rang = (notes['total'] > total).sum() + 1
        max_total = notes['total'].max()
        moyenne = notes['total'].mean()
        percentile = (notes['total'] <= total).mean() * 100
        fig = px.histogram(
                        notes, x='total', nbins=8, labels={'total':'Total Points'}, color_discrete_sequence=['#1f77b4'])
        fig.add_vline(x=total, line_dash="dash", line_color="red",
                  annotation_text=f"TOI ({total})", annotation_position="top")
        fig.update_layout(height=300, showlegend=False)
        top5 = notes.nlargest(5,'total')[['nom','total']].copy().reset_index(drop=True)
        top5.index = ['🥇','🥈','🥉','4️⃣','5️⃣']
        top5.columns = ['Nom','Total']
        top5_html = top5.to_html(index=True)
        metrics = f"""{nom} vous avez un total de {total} pts. Vous êtes {rang} ème sur {len(notes)} étudiants. 
        Vous faites mieux que {percentile:.1f} % des étudiants."""
        st.write("Résumé : ", metrics)
        st.write("Distribution des notes", fig)
        st.write('Top 5', top5)
st.markdown("---")

st.caption("🤖 CIA-FA Dashboard • Développé avec ❤️ par Club IA - Faculté d'Agronomie. \n Dernière mise à jour le 05/04/2026.")


