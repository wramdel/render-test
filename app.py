import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Configuración de página
st.set_page_config(
    page_title="Dashboard Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizado para un dashboard profesional
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
    .main { background: linear-gradient(180deg, #0f0f12 0%, #18181c 100%); }
    
    .stMetric {
        background: rgba(24, 24, 28, 0.9);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #27272a;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
    }
    .stMetric label { color: #a1a1aa !important; font-size: 0.875rem !important; }
    .stMetric [data-testid="stMetricValue"] { color: #f4f4f5 !important; font-weight: 700 !important; font-size: 1.75rem !important; }
    
    h1, h2, h3 { font-family: 'DM Sans', sans-serif !important; color: #f4f4f5 !important; }
    .stApp header { background: rgba(15, 15, 18, 0.95) !important; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #18181c 0%, #0f0f12 100%);
        border-right: 1px solid #27272a;
    }
    [data-testid="stSidebar"] .stMarkdown { color: #a1a1aa !important; }
    
    div[data-testid="stVerticalBlock"] > div {
        border-radius: 12px;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(99, 102, 241, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .kpi-value { font-size: 1.75rem; font-weight: 700; color: #818cf8; }
    .kpi-label { font-size: 0.8125rem; color: #a1a1aa; margin-top: 0.25rem; }
    
    .section-header {
        font-size: 1.125rem;
        font-weight: 600;
        color: #f4f4f5;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #27272a;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_datos():
    """Genera datos de ejemplo realistas para el dashboard."""
    np.random.seed(42)
    fechas = pd.date_range(end=datetime.now(), periods=90, freq="D")
    
    # Ventas con tendencia y estacionalidad
    tendencia = np.linspace(100, 180, 90)
    estacional = 30 * np.sin(np.arange(90) * 2 * np.pi / 30)
    ruido = np.random.normal(0, 12, 90)
    ventas = np.maximum(tendencia + estacional + ruido, 50)
    
    df_ventas = pd.DataFrame({
        "fecha": fechas,
        "ventas": np.round(ventas, 2),
        "usuarios": np.random.poisson(120, 90) + np.arange(90) // 7 * 5,
        "ticket_promedio": np.round(np.random.uniform(45, 85, 90), 2),
    })
    
    categorias = ["Electrónica", "Ropa", "Hogar", "Deportes", "Alimentación"]
    df_cat = pd.DataFrame({
        "categoria": np.random.choice(categorias, 200),
        "monto": np.round(np.random.exponential(150, 200), 2),
    }).groupby("categoria", as_index=False).agg({"monto": "sum"})
    
    canales = ["Directo", "Orgánico", "Paid", "Referidos", "Email"]
    df_canales = pd.DataFrame({
        "canal": canales,
        "conversiones": [420, 380, 290, 180, 130],
        "porcentaje": [29.5, 26.7, 20.4, 12.6, 9.1],
    })
    
    regiones = ["Norte", "Sur", "Centro", "Este", "Oeste"]
    df_regiones = pd.DataFrame({
        "region": regiones * 18,
        "mes": sorted([f"2024-{m:02d}" for m in range(1, 7)] * 15),
        "ingresos": np.round(np.random.gamma(2, 500, 90), 2),
    }).groupby(["region", "mes"], as_index=False).agg({"ingresos": "sum"})
    
    return df_ventas, df_cat, df_canales, df_regiones


def main():
    df_ventas, df_cat, df_canales, df_regiones = cargar_datos()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Controles")
        st.markdown("---")
        rango = st.select_slider(
            "Período (días)",
            options=[7, 14, 30, 60, 90],
            value=30,
            format_func=lambda x: f"{x} días",
        )
        st.markdown("---")
        st.markdown("**Filtros**")
        mostrar_usuarios = st.checkbox("Incluir gráfica de usuarios", value=True)
        tema_graficas = st.radio("Tema gráficas", ["Plotly Dark", "Plotly White"], index=0)
    
    template = "plotly_dark" if tema_graficas == "Plotly Dark" else "plotly_white"
    df = df_ventas.tail(rango).copy()
    
    # Título
    st.title("📊 Dashboard Analytics")
    st.markdown("Vista general de rendimiento y métricas clave.")
    st.markdown("---")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Ventas totales",
            f"${df['ventas'].sum():,.0f}",
            f"+{(df['ventas'].iloc[-1] - df['ventas'].iloc[0]):.0f} vs inicio",
        )
    with col2:
        st.metric(
            "Promedio diario",
            f"${df['ventas'].mean():,.0f}",
            f"{(df['ventas'].mean() / df_ventas['ventas'].mean() - 1) * 100:.1f}% vs histórico",
        )
    with col3:
        st.metric(
            "Usuarios (total)",
            f"{df['usuarios'].sum():,}",
            f"+{df['usuarios'].iloc[-1] - df['usuarios'].iloc[0]} vs inicio",
        )
    with col4:
        st.metric(
            "Ticket promedio",
            f"${df['ticket_promedio'].mean():.1f}",
            f"{((df['ticket_promedio'].iloc[-1] / df['ticket_promedio'].iloc[0]) - 1) * 100:.1f}%",
        )
    
    st.markdown("---")
    
    # Primera fila: línea + área
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<p class="section-header">📈 Tendencia de ventas</p>', unsafe_allow_html=True)
        fig_ventas = go.Figure()
        fig_ventas.add_trace(
            go.Scatter(
                x=df["fecha"],
                y=df["ventas"],
                mode="lines+markers",
                name="Ventas",
                line=dict(color="#6366f1", width=2),
                marker=dict(size=6),
            )
        )
        if mostrar_usuarios:
            fig_ventas.add_trace(
                go.Scatter(
                    x=df["fecha"],
                    y=df["usuarios"],
                    mode="lines",
                    name="Usuarios",
                    yaxis="y2",
                    line=dict(color="#22c55e", width=2, dash="dot"),
                )
            )
            fig_ventas.update_layout(
                yaxis2=dict(title="Usuarios", overlaying="y", side="right", gridcolor="rgba(255,255,255,0.05)"),
            )
        fig_ventas.update_layout(
            template=template,
            margin=dict(l=50, r=50, t=40, b=40),
            height=340,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)" if template == "plotly_dark" else "rgba(0,0,0,0.08)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)" if template == "plotly_dark" else "rgba(0,0,0,0.08)"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_ventas, use_container_width=True)
    
    with c2:
        st.markdown('<p class="section-header">🥧 Por canal</p>', unsafe_allow_html=True)
        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=df_canales["canal"],
                    values=df_canales["conversiones"],
                    hole=0.6,
                    marker=dict(colors=px.colors.qualitative.Set2),
                    textinfo="label+percent",
                    textposition="outside",
                    hovertemplate="%{label}<br>%{value} conv.<br>%{percent}<extra></extra>",
                )
            ]
        )
        fig_donut.update_layout(
            template=template,
            margin=dict(l=20, r=20, t=30, b=20),
            height=340,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text="Canales", x=0.5, y=0.5, font_size=14, showarrow=False)],
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    # Segunda fila: barras + área acumulada
    c3, c4 = st.columns(2)
    
    with c3:
        st.markdown('<p class="section-header">📦 Ventas por categoría</p>', unsafe_allow_html=True)
        fig_barras = px.bar(
            df_cat.sort_values("monto", ascending=True),
            x="monto",
            y="categoria",
            orientation="h",
            color="monto",
            color_continuous_scale="Viridis",
            text_auto=",.0f",
        )
        fig_barras.update_layout(
            template=template,
            margin=dict(l=50, r=30, t=40, b=40),
            height=320,
            showlegend=False,
            xaxis_title="Monto ($)",
            yaxis_title="",
            coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with c4:
        st.markdown('<p class="section-header">📊 Ventas acumuladas</p>', unsafe_allow_html=True)
        df["acumulado"] = df["ventas"].cumsum()
        fig_area = go.Figure()
        fig_area.add_trace(
            go.Scatter(
                x=df["fecha"],
                y=df["acumulado"],
                fill="tozeroy",
                mode="lines",
                name="Ventas acumuladas",
                line=dict(color="#6366f1", width=2),
                fillcolor="rgba(99, 102, 241, 0.3)",
            )
        )
        fig_area.update_layout(
            template=template,
            margin=dict(l=50, r=30, t=40, b=40),
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_area, use_container_width=True)
    
    # Tercera fila: heatmap por región/mes
    st.markdown('<p class="section-header">🗺️ Ingresos por región y mes</p>', unsafe_allow_html=True)
    pivot = df_regiones.pivot(index="region", columns="mes", values="ingresos").fillna(0)
    fig_heat = px.imshow(
        pivot,
        labels=dict(x="Mes", y="Región", color="Ingresos"),
        color_continuous_scale="Plasma",
        aspect="auto",
        text_auto=",.0f",
    )
    fig_heat.update_layout(
        template=template,
        height=280,
        margin=dict(l=80, r=30, t=40, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
    # Tabla resumen
    with st.expander("Ver datos de ventas (últimos 7 días)"):
        tabla = df.tail(7)[["fecha", "ventas", "usuarios", "ticket_promedio"]].copy()
        tabla["ventas"] = tabla["ventas"].map(lambda x: f"${x:,.2f}")
        tabla["ticket_promedio"] = tabla["ticket_promedio"].map(lambda x: f"${x:,.2f}")
        st.dataframe(tabla, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
