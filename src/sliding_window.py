import pandas as pd

# 1. Carregar o dataset consolidado
df = pd.read_csv('data/monthly_commodities.csv')
df['data'] = pd.to_datetime(df['data'])
df.set_index('data', inplace=True)

# 2. Configurações da Janela (conforme o artigo)
window_size = 36  # 36 meses (3 anos)
stride = 1        # Avanço de 1 mês por vez

windows_list = []

# 3. Loop de fatiamento deslizante
for i in range(0, len(df) - window_size + 1, stride):
    # Recorta a janela de 36 meses
    window_df = df.iloc[i : i + window_size].copy()
    
    # Identificador único da janela (exigido para associar os blocos)
    window_df['window_id'] = i 
    
    # Eixo de tempo interno para cada janela (0 a 35)
    window_df['time_step'] = range(window_size)
    
    windows_list.append(window_df)

# 4. Concatena todas as janelas em um único DataFrame expandido
df_rolling_ready = pd.concat(windows_list, ignore_index=True)

# 5. Salva o resultado pronto para a extração de features
df_rolling_ready.to_csv('data/rolling_windows.csv', index=False)

print("✅ Janelas deslizantes geradas com sucesso!")
print(f"Total de janelas de análise criadas: {len(windows_list)}")
print(f"Formato do DataFrame final de janelas: {df_rolling_ready.shape}")
print(df_rolling_ready.head())