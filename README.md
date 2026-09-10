# 📊 Sentiment Insights - Análise de Sentimentos Universal

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Status](https://img.shields.io/badge/Status-Funcionando-00CC96)

> Arraste **QUALQUER CSV** e veja a análise em segundos. O app detecta automaticamente a coluna de texto e a nota, sem precisar renomear nada.

**🔗 Demo ao vivo:** https://sentiment-insight-app.streamlit.app/

### 🎯 O que esse projeto faz?

Dashboard interativo que resolve um problema real de e-commerce e atendimento:

1.  **Detector Universal de Colunas:** Funciona com `texto`, `comentario`, `review`, `feedback_cliente`, `mensagem`... qualquer nome.
2.  **Análise Híbrida:** Usa a NOTA (1 a 5) + palavras-chave para classificar. Nota 3 = Neutro, não Positivo falso.
3.  **Visual Profissional:** Gráfico de donut com tema escuro, % em branco legível e tabela com cores (verde/vermelho/azul).
4.  **Resumo de IA:** Gera insights automáticos: "ALERTA: 40% negativas, foco em logística".

Testado com sucesso com 12, 15 e 30 linhas, em 3 formatos diferentes de CSV.

### 🛠️ Tecnologias
- **Python + Pandas:** Limpeza e tratamento de CSVs sujos
- **Streamlit:** Dashboard interativo
- **Plotly:** Gráfico de donut com fonte branca no tema escuro
- **Lógica de Negócio:** Classificação que prioriza nota sobre palavra para evitar falso positivo (ex: "funciona mas é frágil" + nota 2 = Negativo)

### 📸 Screenshots

![Gráfico](docs/INSIGHT%205.png)

![Avaliações](docs/INSIGHT%204.png)

Feito por **Jairo Andrade**