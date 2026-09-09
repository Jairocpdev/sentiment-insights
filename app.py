import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils import analisar_sentimento, gerar_insights_ia

st.set_page_config(page_title="Sentiment Insights", page_icon="📊", layout="centered")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;}.block-container {padding-top: 2rem;}</style>", unsafe_allow_html=True)

st.title("📊 Sentiment Insights")
st.caption("Arraste QUALQUER CSV - o app encontra o texto sozinho")

uploaded_file = st.file_uploader("Arraste seu CSV aqui (aceita coluna comentario, review, texto...)", type=["csv", "xlsx"])

if not uploaded_file:
    st.info("👆 Arraste seu CSV acima para ver a análise. Use o arquivo que te mandei de exemplo se quiser testar.")
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
            st.error("O CSV está vazio. Baixa o arquivo de exemplo que te mandei.")
            st.stop()
            
except pd.errors.EmptyDataError:
    st.error("O arquivo está vazio ou corrompido. Tenta baixar de novo o CSV que gerei.")
    st.stop()

except Exception as e:
    st.error(f"Erro ao ler: {e}")
    st.stop()

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except:
                df = pd.read_csv(uploaded_file, encoding='latin1')
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
        st.stop()
else:
    if os.path.exists("data/avaliacoes_exemplo.csv"):
        df = pd.read_csv("data/avaliacoes_exemplo.csv")
    else:
        df = pd.DataFrame({"texto": ["Entrega super rápida, amei", "Péssimo atendimento", "Produto ok"]})

col_texto = achar_coluna_texto(df)

if not col_texto:
    st.error(f"Não encontrei coluna de texto. Seu CSV tem essas colunas: {list(df.columns)}. Renomeie uma para 'texto' ou 'comentario'")
    st.dataframe(df.head())
    st.stop()
else:
    if col_texto!= "texto":
        st.success(f"Detectei automaticamente a coluna '{col_texto}' como texto ✓")
        df = df.rename(columns={col_texto: "texto"})

df = analisar_sentimento(df)

c1, c2, c3 = st.columns(3)
c1.metric("Total", len(df))
c2.metric("Positivas", int(len(df[df.sentimento=='Positivo'])))
c3.metric("Negativas", int(len(df[df.sentimento=='Negativo'])))