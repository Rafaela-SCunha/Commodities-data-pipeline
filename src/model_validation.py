import pandas as pd

# 1. Carregar o dataset original consolidado para resgatar as datas
df_original = pd.read_csv('../data/monthly_commodities.csv')
df_original['data'] = pd.to_datetime(df_original['data'])

# 2. Carregar os resultados dos regimes gerados pelo modelo
df_regimes = pd.read_csv('../data/crisis_regimes.csv', index_col=0)

# 3. Filtrar apenas os pontos vermelhos (Anomaly_Label == -1)
crises = df_regimes[df_regimes['Anomaly_Label'] == -1].copy()

# 4. Ordenar da crise mais severa (score mais negativo) para a mais branda
crises = crises.sort_values(by='Anomaly_Score')

# 5. Mapear o Window_ID para as datas reais
# O Window_ID é a linha onde a janela de 3 anos começa. A data final é ID + 35 meses.
window_size = 36

datas_inicio = []
datas_fim = []

for window_id in crises.index:
    # Captura a data da primeira e da última linha daquela janela específica
    data_inicio = df_original.iloc[window_id]['data'].date()
    data_fim = df_original.iloc[window_id + window_size - 1]['data'].date()
    
    datas_inicio.append(data_inicio)
    datas_fim.append(data_fim)

# Adiciona as datas ao DataFrame de resultados
crises['Data_Inicio (Mes 1)'] = datas_inicio
crises['Data_Fim (Mes 36)'] = datas_fim

# 6. Exibir as Top 15 janelas mais severas
print("TOP 15 JANELAS DE CRISE DETECTADAS PELO MODELO:")
colunas_para_exibir = ['Data_Inicio (Mes 1)', 'Data_Fim (Mes 36)', 'Anomaly_Score']
print(crises[colunas_para_exibir].head(15).to_string(index=False))