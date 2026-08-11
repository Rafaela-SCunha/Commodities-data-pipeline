import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from tsfresh.utilities.dataframe_functions import impute

# 1. Carregar a matriz de características gerada pelo TSFresh
features_df = pd.read_csv('../data/raw_features.csv', index_col=0)

# O TSFresh gera valores nulos se encontrar divisões por zero durante 
# as operações estatísticas. A função 'impute' trata isso instantaneamente.
impute(features_df)

print("Iniciando a Detecção de Anomalias (Isolation Forest)...")

# 2. Isolation Forest: Treinando com o conjunto completo (10.962 features)
# Contaminação de 5% e random_state=42 para reprodutibilidade rigorosa
iso_forest = IsolationForest(contamination=0.05, random_state=42)

# label: 1 (Normal) ou -1 (Anomalia/Crise)
anomaly_labels = iso_forest.fit_predict(features_df)
# score: Quanto mais negativo, mais grave é a anomalia
anomaly_scores = iso_forest.decision_function(features_df)


print("Iniciando a Redução de Dimensionalidade (PCA)...")

# 3. PCA: Reduzindo as características de alta dimensão para 3 Componentes Principais
pca = PCA(n_components=3, random_state=42)
pca_resultados = pca.fit_transform(features_df)


print("Consolidando os dados do Regime de Mercado...")

# 4. Juntar os componentes do PCA e os resultados do Isolation Forest em um único local
df_regimes = pd.DataFrame(pca_resultados, columns=['PC1', 'PC2', 'PC3'], index=features_df.index)
df_regimes['Anomaly_Label'] = anomaly_labels
df_regimes['Anomaly_Score'] = anomaly_scores

# 5. Salvar os resultados analíticos
df_regimes.to_csv('../data/crisis_regimes.csv')

print("✅ Modelagem concluída com sucesso! Matriz salva.")
print(df_regimes.head()) 