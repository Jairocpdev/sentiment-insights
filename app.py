import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils import analisar_sentimento, gerar_insights_ia

st.set_page_config(page_title="Sentiment Insights", page_icon="📊", layout="centered")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;}.block-container {padding-top: 2rem;}</style>", unsafe_allow_html=True)

st.title("📊 Sentiment Insights")
st.caption("Arraste QUALQUER CSV - o app encontra o texto sozinho")

def achar_coluna_texto(df):
    possiveis = ["texto", "comentario", "comentário", "review", "mensagem", "feedback", "feedback_cliente", "avaliacao", "avaliação", "descricao", "descrição", "opiniao", "opinião", "content", "text", "coment", "avaliacoes"]

    for col in df.columns:
        if col.lower().strip() in possiveis:
            return col

    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                if df[col].astype(str).str.len().mean() > 15:
                    return col
            except:
                pass
    return None

uploaded_file = st.file_uploader("Arraste seu CSV aqui (aceita coluna comentario, review, texto...)", type=["csv", "xlsx"])

if not uploaded_file:
    st.info("👆 Arraste seu CSV acima para ver a análise.")
    st.stop()

try:
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='latin1')
    if df.empty:
        st.error("O CSV está vazio.")
        st.stop()
except Exception as e:
    st.error(f"Erro ao ler: {e}")
    st.stop()

col_texto = achar_coluna_texto(df)

if not col_texto:
    st.error(f"Não encontrei coluna de texto. Colunas encontradas: {list(df.columns)}")
    st.dataframe(df.head())
    st.stop()
else:
    if col_texto != "texto":
        st.success(f"Detectei coluna '{col_texto}' como texto ✓")
        df = df.rename(columns={col_texto: "texto"})

df = analisar_sentimento(df)

c1, c2, c3 = st.columns(3)
c1.metric("Total", len(df))
c2.metric("Positivas", int(len(df[df.sentimento=='Positivo'])))
c3.metric("Negativas", int(len(df[df.sentimento=='Negativo'])))

fig = px.pie(df, names='sentimento', hole=0.5, color='sentimento',
             color_discrete_map={'Positivo':'#00CC96','Negativo':'#EF553B','Neutro':'#636EFA'})

fig.update_traces(
    textinfo='percent',
    textfont=dict(color='white', size=15, family='Arial Black'),
    textposition='inside'
)
fig.update_layout(
    showlegend=True,
    height=350,
    margin=dict(t=0,b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    legend=dict(font=dict(color='white', size=14))
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🤖 Resumo da IA")
with st.spinner("Gerando..."):
    resumo = gerar_insights_ia(df)
st.info(resumo)

with st.expander("Ver tabela completa"):
    try:
        def color_sentimento(val):
            if val == 'Positivo':
                return 'background-color: #00CC96; color: white; font-weight: bold'
            elif val == 'Negativo':
                return 'background-color: #EF553B; color: white; font-weight: bold'
            else:
                return 'background-color: #636EFA; color: white; font-weight: bold'
            
        styled_df = df.style.map(color_sentimento, subset=['sentimento'])
        st.dataframe(styled_df, use_container_width=True)

    except Exception:
        st.dataframe(df, use_container_width=True)

st.caption("Feito por Jairo Andrade")