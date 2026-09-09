import pandas as pd

def analisar_sentimento(df):
    positivas = ["amei", "excelente", "ótimo", "perfeito", "maravilhoso", "incrível", "rápid", "recomendo", "bom", "adorei", "fiel", "funciona", "impecável", "surpreendente", "atenciosos", "protegido", "original"]
    negativas = ["péssimo", "horrível", "ruim", "defeito", "quebrado", "amassad", "arranhad", "atrasou", "demorou", "lesado", "enganosa", "lixo", "pior", "ignorar", "trocar", "taxa", "propaganda", "for a", "não querem", "não funciona"]

    def classificar(texto):
        t = texto.lower()
        score_pos = sum(1 for p in positivas if p in t)
        score_neg = sum(1 for n in negativas if n in t)

        if score_neg > score_pos:
            return "Negativo"
        if score_pos > score_neg:
            return "Positivo"
        return "Neutro"

    df['sentimento'] = df['texto'].apply(classificar)
    return df

def gerar_insights_ia(df, api_key=None):
    total = len(df)
    pos = len(df[df['sentimento'] == 'Positivo'])
    neg = len(df[df['sentimento'] == 'Negativo'])
    neu = len(df[df['sentimento'] == 'Neutro'])

    if neg > pos:
        return f"ALERTA: De {total} avaliações, {neg} são negativas ({neg/total:.0%}) vs {pos} positivas. Crise em: logística e produto com defeito. Ação urgente necessária."
    else:
        return f"De {total} avaliações, {pos} positivas ({pos/total:.0%}), {neg} negativas e {neu} neutras. Ponto forte: satisfação do cliente. Ponto a melhorar: reduzir neutras para positivas."