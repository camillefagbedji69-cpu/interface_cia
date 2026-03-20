import streamlit as st
import pandas as pd
import plotly.express as px

import os
st.write("Fichiers dispo dans l’app :", os.listdir())

# ===== CONFIG =====
st.set_page_config(
    page_title="Notes CIA-FA",
    page_icon="🎓",
    layout="wide"
)
