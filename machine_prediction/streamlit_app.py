import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="IoT Dashboard", 
    page_icon="📡", 
    layout="wide"
)

# --- CONEXÃO COM O BANCO ---
# Usamos cache para não recriar a engine toda hora
@st.cache_resource
def get_engine():
    return create_engine("postgresql://postgres:1234@localhost:5432/iot_db")

engine = get_engine()

# --- CARREGAMENTO DE DADOS ---
# @st.cache_data evita que o app trave fazendo consultas ao banco a cada clique
@st.cache_data(ttl=600) # Atualiza a cada 10 minutos
def load_data(view):
    try:
        return pd.read_sql(f"SELECT * FROM {view}", engine)
    except Exception as e:
        st.error(f"Erro ao carregar a view {view}: {e}")
        return pd.DataFrame()

# --- TÍTULO E CABEÇALHO ---
st.title("📡 Dashboard de Temperaturas IoT")
st.markdown("---")

# --- LINHA 1: MÉTRICAS RÁPIDAS (OPCIONAL MAS RECOMENDADO) ---
# Aqui você pode carregar dados gerais para mostrar números grandes no topo
df_raw = load_data("avg_temp_por_dispositivo") # Exemplo
if not df_raw.empty:
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total de Dispositivos", len(df_raw['device_id'].unique()))
    col_m2.metric("Média Geral", f"{df_raw['avg_temp'].mean():.2f}°C")
    col_m3.metric("Status do Sistema", "Online", delta="Ativo")

st.markdown("### 📊 Análise por Dispositivo e Tempo")

# --- LINHA 2: DOIS GRÁFICOS LADO A LADO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Média de Temperatura / Dispositivo")
    df1 = load_data("avg_temp_por_dispositivo")
    if not df1.empty:
        fig1 = px.bar(
            df1, 
            x="device_id", 
            y="avg_temp", 
            text_auto='.2f',
            color="device_id",
            labels={"device_id": "Dispositivo", "avg_temp": "Média Temp (°C)"},
            template="plotly_dark"
        )
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Volume de Leituras por Hora")
    df2 = load_data("leituras_por_hora")
    if not df2.empty:
        fig2 = px.line(
            df2, 
            x="hora", 
            y="contagem",
            markers=True,
            labels={"hora": "Hora do Dia", "contagem": "Nº de Mensagens"},
            template="plotly_dark",
            color_discrete_sequence=["#00CC96"]
        )
        st.plotly_chart(fig2, use_container_width=True)


st.markdown("---")
st.subheader("🌡️ Histórico de Temperaturas Máximas e Mínimas")
df3 = load_data("temp_max_min_por_dia")

if not df3.empty:

    fig3 = px.line(
        df3, 
        x="data", 
        y=["temp_max", "temp_min"],
        labels={"value": "Temperatura (°C)", "data": "Data", "variable": "Tipo"},
        color_discrete_map={"temp_max": "#EF553B", "temp_min": "#636EFA"},
        template="plotly_dark"
    )
    fig3.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig3, use_container_width=True)