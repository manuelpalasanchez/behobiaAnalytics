import streamlit as st
import pandas as pd
from utils import load_css, section_header, metric_card
import graficos_operativo
import graficos_mercado
import graficos_deportivo


st.set_page_config(
    page_title="Behobia-San Sebastián Analytics",
    page_icon="🏃",
    layout="wide"
)
load_css()

@st.cache_data
def cargar_datos():
    df = pd.read_csv("behobia_maestro.csv")
    sexo_map = {
        'Junior F': 'F', 'Promesa F': 'F', 'Senior F': 'F',
        'Veterana': 'F', 'Veterana Ii': 'F', 'Veterana Iii': 'F', 'Veterana Iv': 'F',
        'Invidentes F': 'F',
        'Junior M': 'M', 'Promesa M': 'M', 'Senior M': 'M',
        'Veterano': 'M', 'Veterano Ii': 'M', 'Veterano Iii': 'M', 'Veterano Iv': 'M',
        'Invidentes M': 'M',
        'Discapacitados': 'X', 'Apoyo Discapacitado': 'X',
    }
    df['Sexo'] = df['Categoria'].map(sexo_map).fillna('X')
    return df

df_full = cargar_datos()
años = sorted(df_full['Año'].dropna().unique().astype(int))


st.markdown(
    "<div style='text-align:center'>"
    "<h1>🏃 Behobia – San Sebastián</h1>"
    "<p style='color:#8b949e;margin-top:-10px;margin-bottom:16px;font-size:1.5rem'>Auditoría y oportunidades comerciales - Ediciones 2021–2025 - ~123k registros</p>"
    "</div>",
    unsafe_allow_html=True
)


años_str = [str(a) for a in años]
seleccion = st.pills(
    label="Edición",
    options=años_str,
    selection_mode="multi",
    label_visibility="collapsed"
)

años_seleccionados = [int(a) for a in seleccion] if seleccion else años
df = df_full[df_full['Año'].isin(años_seleccionados)]

total = len(df)
finishers = len(df[df['Resultado'] == 'F'])
pct_femenino = len(df[df['Sexo'] == 'F']) / total * 100 if total > 0 else 0
tasa_finish = finishers / total * 100 if total > 0 else 0

if not seleccion:
    v2021 = len(df_full[df_full['Año'] == 2021])
    v2025 = len(df_full[df_full['Año'] == 2025])
    crecimiento = (v2025 - v2021) / v2021 * 100
    delta_part = (f"+{crecimiento:.1f}% vs 2021", "delta-pos")
else:
    delta_part = ("", "delta-neu")

ediciones = len(años_seleccionados)

cols = st.columns(4)
metric_card(cols[0], "Participantes",          f"{total:,}",           *delta_part)
metric_card(cols[1], "Finishers",              f"{finishers:,}",        f"{tasa_finish:.1f}% tasa", "delta-pos")
metric_card(cols[2], "Participación femenina", f"{pct_femenino:.1f}%", "", "delta-neu")
metric_card(cols[3], "Ediciones analizadas",   str(ediciones),         "", "delta-neu")


section_header("1 · Optimización Operativa")
graficos_operativo.render(df)

section_header("2 · Inteligencia de Mercado")
graficos_mercado.render(df, df_full)

section_header("3 · Inteligencia Deportiva")
graficos_deportivo.render(df)


st.markdown("<hr style='border-color:#21262d;margin-top:32px'>", unsafe_allow_html=True)
st.markdown(
    "<div class='footer'>Manuel Palacios Sánchez · "
    "<a href='https://github.com/manuelpalasanchez'>github.com/manuelpalasanchez</a>"
    "</div>",
    unsafe_allow_html=True
)

