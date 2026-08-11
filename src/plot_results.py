import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

# 1. Carregar os dados modelados
df_regimes = pd.read_csv('../data/crisis_regimes.csv', index_col=0)

# 2. Transformação Matemática para Dados Composicionais
# O Plotly Ternary exige valores positivos. O MinMaxScaler ajusta as 3 componentes para um range de 0 a 1.
scaler = MinMaxScaler()
pca_scaled = scaler.fit_transform(df_regimes[['PC1', 'PC2', 'PC3']])
df_scaled = pd.DataFrame(pca_scaled, columns=['PC1_norm', 'PC2_norm', 'PC3_norm'], index=df_regimes.index)

# Normalização L1 (Soma = 1) para habilitar a interpretação geométrica em 3D
df_scaled['soma'] = df_scaled[['PC1_norm', 'PC2_norm', 'PC3_norm']].sum(axis=1)
df_scaled['PC1_comp'] = df_scaled['PC1_norm'] / df_scaled['soma']
df_scaled['PC2_comp'] = df_scaled['PC2_norm'] / df_scaled['soma']
df_scaled['PC3_comp'] = df_scaled['PC3_norm'] / df_scaled['soma']

# 3. Preparando os rótulos e mapeamento para o gráfico
# Transformando o -1 e 1 do Isolation Forest em nomes legíveis
df_scaled['Regime'] = df_regimes['Anomaly_Label'].map({1: 'Normal', -1: 'Crise/Anomalia'})

# Adicionando o eixo de tempo usando o ID da janela (ou pode mapear de volta para as datas reais)
df_scaled['Window_ID'] = df_regimes.index 

print("Gerando o Espaço de Regimes (Ternary Plot)...")

# 4. Plotagem do Gráfico Ternário Interativo
fig = px.scatter_ternary(
    df_scaled, 
    a="PC1_comp", 
    b="PC2_comp", 
    c="PC3_comp", 
    color="Regime",
    color_discrete_map={"Normal": "#1f77b4", "Crise/Anomalia": "#d62728"},
    title="Detecção de Crises: Mapa de Regimes em Espaço 3D (Ternary Plot)",
    hover_name="Window_ID",
    size_max=10
)

# Ajuste visual para deixar com cara de paper acadêmico
fig.update_layout(
    ternary=dict(
        sum=1,
        aaxis_title="PC1: Nível de Mercado",
        baxis_title="PC2: Volatilidade",
        caxis_title="PC3: Correlações"
    ),
    template="plotly_white"
)

fig.show()