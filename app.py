## importation des packages 
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

## titre 
st.title("📊 Dashboard des notes")

## upload du fichier
notes = pd.read_excel('Notes.xlsx')

## Data cleaning 
notes.columns = notes.columns.str.strip().str.lower()
notes['code_etudiant'] = notes['code_etudiant'].str.strip().str.upper()
notes['nom'] = notes['nom'].str.strip()
notes['total'] = pd.to_numeric(notes['total'], errors='coerce')
notes = notes.dropna(subset=['code_etudiant', 'total'])

## Enter code 
user_text = st.text_input("Entrez votre code étudiant", placeholder="JOHN2025")

st.markdown("---")

st.caption("🤖 CIA-FA Dashboard • Développé avec ❤️ par Club IA - Faculté d'Agronomie. \n Dernière mise à jour le 20/03/2026.")


