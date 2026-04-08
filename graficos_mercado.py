import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import PLOT_LAYOUT, apply_axes, insight_box


def grafico_genero(df_full):
    genero_año = (
        df_full[df_full['Sexo'].isin(['M', 'F'])]
        .groupby(['Año', 'Sexo']).size().reset_index(name='Participantes')
    )
    fig = px.line(
        genero_año, x='Año', y='Participantes', color='Sexo',
        markers=True,
        color_discrete_map={'M': '#1f6feb', 'F': '#e8463a'},
        title="Evolución de Inscripciones por Género (2021-2025)",
    )
    fig.update_layout(**PLOT_LAYOUT)
    fig.update_xaxes(dtick=1)
    apply_axes(fig)
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "La participación femenina creció un <b>+71% en términos absolutos</b> desde 2021, "
        "incrementando su cuota del <b>25,5% al 34%</b> en cinco ediciones."
    )


def grafico_fidelizacion(df_full):
    personas = df_full.groupby(['Nombre', 'Apellido1', 'Apellido2'])['Año'].nunique().reset_index()
    personas.columns = ['Nombre', 'Apellido1', 'Apellido2', 'Ediciones']
    fidelizados = len(personas[personas['Ediciones'] > 1])
    unicos = len(personas[personas['Ediciones'] == 1])

    fig = go.Figure(go.Pie(
        labels=[f'Fidelizados ({fidelizados:,})', f'Únicos ({unicos:,})'],
        values=[fidelizados, unicos],
        hole=0.4,
        marker=dict(colors=['#4C53AF', '#FFC107'], line=dict(color='#0f1117', width=2)),
        textfont=dict(color="#f0f6fc")
    ))
    fig.update_layout(
    **PLOT_LAYOUT,
    title=dict(text="Fidelización de Corredores (2021–2025)", font=dict(color="#f0f6fc", size=18))
    )
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "El <b>27,7% de los participantes</b> han repetido en más de una edición. "
        "Programas de incentivos como descuentos o beneficios para veteranos "
        "pueden elevar esta cifra significativamente."
    )


def grafico_localidades(df):
    top_loc = (
        df[df['Localidad'].notna() & (df['Localidad'] != 'Nan')]
        .groupby('Localidad').size()
        .nlargest(10).reset_index(name='Corredores')
        .sort_values('Corredores')
    )
    fig = px.bar(
        top_loc, x='Corredores', y='Localidad', orientation='h',
        text='Corredores',
        title="Top 10 Localidades (Participación Acumulada)",
        color_discrete_sequence=['#3498db']
    )
    fig.update_traces(textposition='outside', textfont=dict(color="#c9d1d9"))
    fig.update_layout(**PLOT_LAYOUT, xaxis_title="Número de Corredores", yaxis_title="")
    apply_axes(fig)
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "<b>Donostia-San Sebastián</b> lidera la participación acumulada, seguida de "
        "Madrid, Barcelona y Zaragoza. Ampliar campañas en estos núcleos representa "
        "el mayor ROI potencial para 2026."
    )


def grafico_inclusion(df):
    cats_inclusion = ['Discapacitados', 'Invidentes M', 'Apoyo Discapacitado', 'Invidentes F']
    counts = (
        df[df['Categoria'].isin(cats_inclusion)]
        .groupby('Categoria').size().reset_index(name='Atletas')
        .sort_values('Atletas')
    )
    total = len(df)
    counts['Pct'] = (counts['Atletas'] / total * 100).round(3)

    fig = px.bar(
        counts, x='Atletas', y='Categoria', orientation='h',
        text=counts.apply(lambda r: f"{r['Atletas']} ({r['Pct']}%)", axis=1),
        title="Participación en Categorías Inclusivas",
        color_discrete_sequence=['#00897b']
    )
    fig.update_traces(textposition='outside', textfont=dict(color="#c9d1d9"))
    fig.update_layout(**PLOT_LAYOUT, xaxis_title="Número de Atletas", yaxis_title="")
    apply_axes(fig)
    st.plotly_chart(fig, use_container_width=True)
    insight_box(
        "Solo <b>230 atletas (0,19%)</b> participan en categorías adaptadas. "
        "Estrategias proactivas de captación posicionarían a la Behobia-SS "
        "como referente europeo en deporte inclusivo."
    )


def render(df, df_full):
    col1, col2 = st.columns(2)
    with col1:
        grafico_genero(df_full)
    with col2:
        grafico_fidelizacion(df_full)

    col3, col4 = st.columns(2)
    with col3:
        grafico_localidades(df)
    with col4:
        grafico_inclusion(df)