import pandas as pd

def analisar_sentimento(df):
    positivas = ["amei", "excelente", "ótimo", "perfeito", "maravilhoso", "incrível", "recomendo", "adorei", "impecável", "surpreendente", "atenciosos", "original"]
    negativas = ["péssimo", "horrível", "ruim", "defeito", "quebrado", "amassad", "arranhad", "atrasou", "demorou", "lesado", "enganosa", "lixo", "pior", "ignorar", "taxa", "propaganda", "não compraria", "nunca mais"]

    neutras_neg = ["frágil", "medo", "receio", "mediano"]

    def classificar(row):
        texto = str(row['texto']).lower()

        nota = None
        for col in ['nota', 'estrelas', 'estrelas', 'rating', 'stars']:
            if col in row and pd.notna(row[col]):
                try:
                    nota = int(row[col])
                    break
                except:
                    pass

        if nota is not None:
            if nota >= 4:
                return "Positivo"
            if nota <= 2:
                return "Negativo"
            if nota == 3:
                # Nota 3 = neutro, a menos que tenha palavra muito forte
                score_neg = sum(1 for n in negativas if n in texto)
                if score_neg >= 1:
                    return "Negativo"
                return "Neutro"

        score_pos = sum(1 for p in positivas if p in texto)
        score_neg = sum(1 for n in negativas if n in texto)

        if any(x in texto for x in neutras_neg):
            if score_pos <= 1: # se só tem "funciona" mas tem "frágil"
                return "Neutro" if score_neg == 0 else "Negativo"

        if score_neg > score_pos:
            return "Negativo"
        if score_pos > score_neg:
            return "Positivo"
        return "Neutro"

    df['sentimento'] = df.apply(classificar, axis=1)
    return df

def gerar_insights_ia(df, api_key=None):
    total = len(df)
    pos = len(df[df['sentimento'] == 'Positivo'])
    neg = len(df[df['sentimento'] == 'Negativo'])
    neu = len(df[df['sentimento'] == 'Neutro'])

    if total == 0:
        return "Sem dados."

    if neg > pos:
        return f"ALERTA: De {total} avaliações, {neg} negativas ({neg/total:.0%}) vs {pos} positivas. Foco urgente em logística e qualidade."
    elif pos >= total * 0.6:
        return f"ÓTIMO: De {total} avaliações, {pos} positivas ({pos/total:.0%}). Cliente satisfeito, mantenha o padrão!"
    else:
        return f"De {total} avaliações, {pos} positivas ({pos/total:.0%}), {neg} negativas e {neu} neutras. Ponto forte: satisfação. Oportunidade: converter neutras em positivas."