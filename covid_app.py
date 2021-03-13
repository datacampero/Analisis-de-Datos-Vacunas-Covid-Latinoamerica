import streamlit as st
import time
import io
import csv
import sys
from PIL import Image


# Sidebar and main screen text and title.
st.title("💉 Análisis de Vacunas en Latinoamérica")
st.markdown("Analizaremos del dataset de sobre los reportes de las vacunas. Esta página se actualiza con los datos actuales")

author_pic = Image.open('assets/alep.png')
st.sidebar.image(author_pic, "[www.alejandromarcano.com]")

st.sidebar.title("Vacunas Datacampero:")
st.sidebar.markdown("Analizaremos del dataset de sobre los reportes de las vacunas. Esta página se actualiza con los datos actuales 📁.")


st.sidebar.write("""Creado con 💖 por *datacampero* """)
