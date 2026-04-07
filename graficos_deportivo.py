import streamlit as st
import plotly.express as px
from utils import PLOT_LAYOUT, apply_axes, insight_box


def grafico_muro(df):
    muro_df = df[
        (df['Resultado'] == 'F') &
        df['Tiempo_Oficial_s'].notna() &
        df['Parcial_15K_s'].notna()
    ].copy()

    muro_df['ritmo_inicio'] = muro_df['Parcial_15K_s'] / 15.0
    muro_df['ritmo_final'] = (muro_df['Tiempo_Oficial_s'] - muro_df['Parcial_15K_s']) / 5.0
    muro_df['perdida'] = muro_df['ritmo_final'] - muro_df['ritmo_inicio']

    muro_cat = (
        muro_df.groupby('Categoria')['perdida'].mean()
        .reset_index(name='Perdida_s_km')
        .nlargest(10, 'Perdida_s_km')
        .sort_values('Perdida_s_km')
    )

    fig = px.bar(
        muro_cat, x='Perdida_s_km', y='Categoria', orientation='h',
        title='El "Muro": Pérdida media de seg/km (km 15 → meta)',
        color='Perdida_s_km',
        color_continuous_scale=[[0, '#fbc02d'], [1, '#d32f2f']],
    )
    fig.update_layout(**PLOT_LAYOUT, xaxis_title="Segundos perdidos por km", yaxis_title="", coloraxis_showscale=False)
    apply_axes(fig)
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "La pérdida de velocidad se agudiza a partir del <b>km 15</b> en todas las categorías. "
        "Oportunidad de patrocinio para marcas de suplementación energética "
        "en este punto crítico de la carrera."
    )


def grafico_segmentacion(df):
    seg_df = df[(df['Ritmo (min/km)'] > 2) & (df['Ritmo (min/km)'] < 10)].copy()

    def segmentar(ritmo):
        if ritmo < 4.0:   return 'Pro (<4:00)'
        elif ritmo < 5.0: return 'Avanzado (4-5)'
        elif ritmo < 6.0: return 'Popular (5-6)'
        else:             return 'Recreativo (>6:00)'

    seg_df['Segmento'] = seg_df['Ritmo (min/km)'].apply(segmentar)
    seg_counts = seg_df.groupby(['Categoria', 'Segmento']).size().reset_index(name='N')
    seg_totales = seg_counts.groupby('Categoria')['N'].transform('sum')
    seg_counts['Pct'] = (seg_counts['N'] / seg_totales * 100).round(1)

    cats_validas = seg_counts.groupby('Categoria')['N'].sum()
    cats_validas = cats_validas[cats_validas > 100].index
    seg_counts = seg_counts[seg_counts['Categoria'].isin(cats_validas)]

    orden_seg = ['Pro (<4:00)', 'Avanzado (4-5)', 'Popular (5-6)', 'Recreativo (>6:00)']
    colores_seg = {
        'Pro (<4:00)': '#d32f2f',
        'Avanzado (4-5)': '#fb8c00',
        'Popular (5-6)': '#1976d2',
        'Recreativo (>6:00)': '#388e3c'
    }

    fig = px.bar(
        seg_counts, x='Pct', y='Categoria', color='Segmento',
        orientation='h', barmode='stack', text='Pct',
        title="Segmentación por Ritmo (Target para Marcas)",
        category_orders={'Segmento': orden_seg},
        color_discrete_map=colores_seg
    )
    fig.update_traces(texttemplate='%{text:.0f}%', textposition='inside', textfont=dict(color="white"))
    fig.update_layout(**PLOT_LAYOUT, xaxis_title="Distribución (%)", yaxis_title="", xaxis_range=[0, 100])
    apply_axes(fig)
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "<b>Senior M y Promesa M</b> concentran mayor densidad de perfiles Pro/Avanzado. "
        "Las categorías femeninas y veteranas tienen masa crítica en Popular/Recreativo — "
        "públicos objetivo diferenciados para marcas técnicas vs. de confort."
    )


def render(df):
    col1, col2 = st.columns(2)
    with col1:
        grafico_muro(df)
    with col2:
        grafico_segmentacion(df)