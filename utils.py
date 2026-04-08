import streamlit as st
from pathlib import Path

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c9d1d9", family="monospace", size=12),
    title_font=dict(color="#f0f6fc", size=18),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c9d1d9")),
)

def apply_axes(fig):
    fig.update_xaxes(showgrid=False, color="#8b949e", tickfont=dict(color="#8b949e"), title_font=dict(color="#8b949e"))
    fig.update_yaxes(gridcolor="#21262d", color="#8b949e", tickfont=dict(color="#8b949e"), title_font=dict(color="#8b949e"))
    return fig

def load_css():
    css = Path("style.css").read_text()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def section_header(titulo):
    st.markdown(f"<div class='section-header'>{titulo}</div>", unsafe_allow_html=True)

def insight_box(texto):
    st.markdown(f"<div class='insight-box'>{texto}</div>", unsafe_allow_html=True)

def metric_card(col, label, value, delta="", delta_class="delta-neu"):
    col.markdown(
        f"<div class='metric-card'>"
        f"<div class='label'>{label}</div>"
        f"<div class='value'>{value}</div>"
        f"<div class='{delta_class}'>{delta or '&nbsp;'}</div>"
        f"</div>",
        unsafe_allow_html=True
    )