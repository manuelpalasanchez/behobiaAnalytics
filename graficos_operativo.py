import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import PLOT_LAYOUT, apply_axes, insight_box


def grafico_abandonos(df):
    dnf = df[
        (df['Resultado'] == 'DNF') &
        df['Punto_Abandono'].notna() &
        (df['Punto_Abandono'] != '')
    ]
    counts = dnf['Punto_Abandono'].value_counts().reset_index()
    counts.columns = ['Tramo', 'Abandonos']
    orden = ['0-5', '5-10', '10-15', '15-20']
    counts['Tramo'] = pd.Categorical(counts['Tramo'], categories=orden, ordered=True)
    counts = counts.sort_values('Tramo')
    total = counts['Abandonos'].sum()
    counts['Pct'] = (counts['Abandonos'] / total * 100).round(1)

    fig = px.bar(
        counts, x='Tramo', y='Abandonos',
        text=counts.apply(lambda r: f"{r['Abandonos']} ({r['Pct']}%)", axis=1),
        title="Distribución de Abandonos por Tramo (km)",
        color_discrete_sequence=['#e8463a']
    )
    fig.update_traces(textposition='outside', textfont=dict(color="#c9d1d9"))
    fig.update_layout(**PLOT_LAYOUT, xaxis_title="Tramo (km)", yaxis_title="Corredores DNF")
    apply_axes(fig)
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "Los tramos <b>0-5 km</b> y <b>10-15 km</b> concentran la mayor tasa de abandono."
        "Se recomienda refuerzo de personal médico y asistencial en estos puntos de máxima fatiga."
    )


def grafico_afluencia(df):
    tiempos = df[(df['Resultado'] == 'F') & (df['Tiempo_Oficial_s'] > 0)]['Tiempo_Oficial_s']
    por_minuto = (tiempos // 60).astype(int).value_counts().sort_index().reset_index()
    por_minuto.columns = ['Minuto', 'Corredores']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=por_minuto['Minuto'], y=por_minuto['Corredores'],
        mode='lines', fill='tozeroy',
        line=dict(color='#1f6feb', width=2),
        fillcolor='rgba(31,111,235,0.15)'
    ))
    
    fig.update_layout(
    **PLOT_LAYOUT,
    title=dict(text="Curva de Afluencia en Meta (corredores/minuto)", font=dict(color="#f0f6fc", size=18)),
    xaxis_title="Minuto de carrera",
    yaxis_title="Corredores/min"
)
    apply_axes(fig)
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "El pico de llegadas se concentra en torno al <b>minuto 100-120</b>. "
        "Dimensionar la entrega de medallas y avituallamiento en esta ventana evita "
        "cuellos de botella en meta."
    )


def render(df):
    col1, col2 = st.columns(2)
    with col1:
        grafico_abandonos(df)
    with col2:
        grafico_afluencia(df)