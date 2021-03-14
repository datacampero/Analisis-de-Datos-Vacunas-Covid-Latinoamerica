import streamlit as st
import time
import io
import csv
import sys
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import numpy as np 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sidebar and main screen text and title.
st.title("💉 Análisis de Vacunas en Latinoamérica")
st.markdown(""" 
Esta aplicación muestra las estadísticas de personas vacunadas!
* **Fuente de Extracción de los Datos:**

Los datos son recolectados del repositorio de Github www.ourworldindata.org/(https://ourworldindata.org/covid-vaccinations).
Este repositorio es actualizado diariamente con los datos mundiales de las vacunas.

Link del dataset https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations
""")

author_pic = Image.open('assets/alep.png')
st.sidebar.image(author_pic, "[www.alejandromarcano.com]")

st.sidebar.title("Vacunas Datacampero:")
st.sidebar.markdown("Analizaremos del dataset de sobre los reportes de las vacunas. Esta página se actualiza con los datos actuales 📁.")





st.sidebar.header('Clasificar por País')


#leyendo el archivo que tiene toda la informacion
df = pd.read_csv("https://docs.google.com/spreadsheets/d/1MlLL19lch5UGJkTtiiKf_yMDJRhzBpfF4ngSOuFVzPk/export?format=csv")

#limpiando los datos
df_cl = df.fillna(0)

#clasificando la informacion
data_fr = df_cl[(df_cl["total_vaccinations"] != 0)]

#seleccionando paises de Latam
data_fr_ = data_fr[(data_fr["country"].str.contains("Ecuador")) |
                   (data_fr["country"].str.contains("Colombia")) | 
                   (data_fr["country"].str.contains("Chile")) | 
                   (data_fr["country"].str.contains("Argentina")) | 
                   (data_fr["country"].str.contains("Brazil")) |
                   (data_fr["country"].str.contains("Bolivia")) |
                   (data_fr["country"].str.contains("Paraguay")) | 
                   (data_fr["country"].str.contains("Venezuela")) |
                   (data_fr["country"].str.contains("Uruguay")) |
                   (data_fr["country"].str.contains("Peru"))]


# Barra Lateral - Seleccionar Pais
pais_unico = sorted(data_fr_.country.unique())
seleccion_pais = st.sidebar.multiselect('Pais', pais_unico, pais_unico)

# Filtrando datos
df_seleccion_pais = data_fr_[(data_fr_.country.isin(seleccion_pais))] # & (data_fr_.Pos.isin(seleccion_mes))

st.header('Mostrar información del país seleccionado')
st.write('Dimensión de Datos: ' + str(df_seleccion_pais.shape[0]) + ' filas y ' + str(df_seleccion_pais.shape[1]) + ' columnas.')
st.dataframe(df_seleccion_pais)

#st.line_chart(data_fr_)   dato visualizable

#Vacunas que se estan usando en latam
vacuna2 = df_seleccion_pais.vaccines.value_counts()
#vacuna2.plot.pie()

#st.pyplot(vacuna2) dato no visualizable
#st.plotly_chart(df_seleccion_pais.vaccines)
#st.

#personas vacunadas
#total = df_seleccion_pais.people_vaccinated.sum()
st.write('Tipos de vacunas que estan usando en la region')
vacuna = pd.DataFrame(df_seleccion_pais.vaccines.value_counts())
st.bar_chart(vacuna)

#st.pyplot(plt.plot(df_seleccion_pais.vaccines))


df_vacunas = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')
df_vacunas_filter = df_vacunas[['location', 'iso_code', 'date', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated' ]]
df_paises = df_vacunas_filter[df_vacunas_filter.location.isin(seleccion_pais)]
df_paises2 = df_paises.dropna(subset=['total_vaccinations'])
df_paises2 = df_paises2.sort_values("date",ascending=True)
data_over_time= df_paises2.groupby(["date", "location"])[["total_vaccinations","people_vaccinated","people_fully_vaccinated"]].sum().reset_index().sort_values("date",ascending=True)


fig = px.line(data_over_time, x="date", y="total_vaccinations", color='location')


fig.update_traces(mode='lines+markers')
fig.update_xaxes(
        rangeslider_visible=True,
)
fig.update_layout(
    title=' Evolución de las personas total vacunadas a lo largo del tiempo en el mundo',
        template='plotly_white',
      yaxis_title="Casos Confirmados",
    xaxis_title="Días",

)

st.write(fig)

df_paises2['date_str'] = df_paises2['date'].astype(str)
fig_map = px.choropleth(df_paises2,                            # Input Dataframe
                     locations="iso_code",           # identify country code column
                     color="total_vaccinations",                     # identify representing column
                     hover_name="location",              # identify hover name
                     animation_frame="date_str",        # identify date column
                     scope='south america',        # select projection
                     color_continuous_scale = 'Peach',  # select prefer color scale
                     range_color=[0,11149530.0]              # select range of dataset
                     )  

st.write(fig_map)



if st.button('Total de Personas Vacunadas'):
    primer_dosis = (df_seleccion_pais.people_vaccinated.sum())
    st.write('Personas que recibieron la primera dosis son: '+str(primer_dosis))
    segunda_dosis =(df_seleccion_pais.people_fully_vaccinated.sum())
    st.write('Personas que recibieron la segunda dosis son: '+str(segunda_dosis))
    total_vacunados =(df_seleccion_pais.total_vaccinations.sum())
    st.write('Total de personas vacunadas en la region: '+str(total_vacunados))



st.sidebar.write("""Creado con 💖 por *datacampero* """)
