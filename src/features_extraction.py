import pandas as pd
from tsfresh import extract_features
from tsfresh.feature_extraction import ComprehensiveFCParameters

# O Windows EXIGE esse bloco para não dar erro no processamento paralelo
if __name__ == '__main__':

    # ==============================================================
    # FASE 1: TRATAMENTO MATEMÁTICO DA SÉRIE TEMPORAL
    # ==============================================================
    df = pd.read_csv('../data/monthly_commodities.csv')
    df['data'] = pd.to_datetime(df['data'])
    df.set_index('data', inplace=True)

    df = df.interpolate(method='time')
    df = df.dropna()

    # ==============================================================
    # FASE 2: RECRIANDO AS JANELAS DESLIZANTES
    # ==============================================================
    window_size = 36
    stride = 1
    windows_list = []

    for i in range(0, len(df) - window_size + 1, stride):
        window_df = df.iloc[i : i + window_size].copy()
        window_df['window_id'] = i 
        window_df['time_step'] = range(window_size)
        windows_list.append(window_df)

    df_rolling = pd.concat(windows_list, ignore_index=True)
    print(f"Total de janelas prontas para extração: {len(windows_list)}")

    # ==============================================================
    # FASE 3: EXTRAÇÃO PARALELA (TSFresh) SEGURA PARA WINDOWS
    # ==============================================================
    print("Iniciando TSFresh (Utilizando 4 núcleos da CPU)...")

    settings = ComprehensiveFCParameters()

    extracted_features = extract_features(
        df_rolling, 
        column_id='window_id', 
        column_sort='time_step',
        default_fc_parameters=settings,
        n_jobs=4,         
        disable_progressbar=False
    )

    print(f"✅ Extração concluída com sucesso! Matriz gerada: {extracted_features.shape}")
    extracted_features.to_csv('../data/raw_features.csv')