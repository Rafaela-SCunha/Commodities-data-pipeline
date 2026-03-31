
import pandas as pd
from fredapi import Fred
import time
import os
from datetime import timedelta
import requests

#=================================================
# 1. FUNÇÕES DE EXTRAÇÃO
#=================================================

def baixar_fred(api_key, lista_ativos, start_date, end_date=None):
    fred = Fred(api_key=api_key)
    df_novo = pd.DataFrame()
    
    print("\n--- A extrair dados do FRED (Economia Real) ---")
    for nome, ticker in lista_ativos.items():
        print(f" -> A procurar FRED: {nome} ({ticker})")
        try:
            kwargs = {'observation_start': start_date}
            if end_date and start_date == '2000-01-01':
                kwargs['observation_end'] = end_date
            
            serie = fred.get_series(ticker, **kwargs)
            if not serie.empty:
                df_temp = pd.DataFrame(serie, columns=[nome])
                if df_novo.empty:
                    df_novo = df_temp
                else:
                    df_novo = df_novo.join(df_temp, how='outer')
            time.sleep(0.5) # Pausa curta, FRED permite 120 req/min
        except Exception as e:
            print(f"Erro no FRED [{nome}]: {e}")
            
    if not df_novo.empty:
        # Tira a média mensal e preenche falhas (bfill resolve o primeiro mês)
        df_mensal = df_novo.resample('ME').mean().ffill().bfill()
        
        # GARANTIA: Remove horas, minutos e fuso horário
        df_mensal.index = df_mensal.index.normalize() 
        if df_mensal.index.tz is not None:
            df_mensal.index = df_mensal.index.tz_localize(None)
            
        return df_mensal
    return pd.DataFrame()

def baixar_alpha_vantage(api_key, lista_ativos, start_date):
    df_novo = pd.DataFrame()
    print("\n--- A extrair dados da Alpha Vantage (ETFs de Metais) ---")
    
    for nome, ticker in lista_ativos.items():
        print(f" -> A procurar Alpha Vantage: {nome} ({ticker})")
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={api_key}'
        try:
            r = requests.get(url)
            dados = r.json()
            
            if 'Monthly Time Series' in dados:
                df_temp = pd.DataFrame.from_dict(dados['Monthly Time Series'], orient='index')
                df_temp = df_temp[['4. close']].rename(columns={'4. close': nome})
                df_temp.index = pd.to_datetime(df_temp.index)
                df_temp[nome] = pd.to_numeric(df_temp[nome])
                
                # Filtra apenas os dados mais recentes que o nosso CSV
                if start_date != '2000-01-01':
                    df_temp = df_temp[df_temp.index >= start_date]
                    
                if df_novo.empty:
                    df_novo = df_temp
                else:
                    df_novo = df_novo.join(df_temp, how='outer')
            else:
                print(f"Aviso Alpha Vantage [{nome}]: Limite atingido ou erro retornado.")
            
            time.sleep(15) # Pausa OBRIGATÓRIA da Alpha Vantage (plano grátis)
        except Exception as e:
            print(f"Erro na Alpha Vantage [{nome}]: {e}")
            
    if not df_novo.empty:
        # Desloca a data para o FIM do mês, assim alinha perfeitamente com o FRED
        df_novo.index = df_novo.index + pd.offsets.MonthEnd(0)
        
        # GARANTIA: Remove horas, minutos e fuso horário
        df_novo.index = df_novo.index.normalize()
        if df_novo.index.tz is not None:
            df_novo.index = df_novo.index.tz_localize(None)
            
        return df_novo
    return pd.DataFrame()

#=================================================
# 2. FUNÇÃO DE UNIÃO
#=================================================

def atualizar_base_unificada(api_fred, api_alpha, fred_dict, alpha_dict, ficheiro, end_date=None):
    # Verifica o que já temos no CSV
    if os.path.exists(ficheiro):
        df_base = pd.read_csv(ficheiro, parse_dates=['data'])
        last_date = df_base['data'].max()
        start_date = last_date.replace(day=1).strftime('%Y-%m-%d')
        print(f"Base encontrada! Última atualização: {last_date.date()}.")
        print(f"A procurar novos dados a partir de: {start_date}...")      
    else:
        df_base = pd.DataFrame()
        start_date = '2000-01-01'
        print(f"Base não encontrada. A iniciar carga histórica a partir de {start_date}...")

    # 1. Puxa os dados das duas fontes
    df_fred = baixar_fred(api_fred, fred_dict, start_date, end_date)
    df_alpha = baixar_alpha_vantage(api_alpha, alpha_dict, start_date)

    # 2. Une as duas APIs pelo Índice (Data)
    df_novos = pd.DataFrame()
    if not df_fred.empty and not df_alpha.empty:
        df_novos = df_fred.join(df_alpha, how='outer') # A mágica da união perfeitamente alinhada
    elif not df_fred.empty:
        df_novos = df_fred
    elif not df_alpha.empty:
        df_novos = df_alpha

    # Se não baixou nada de novo, encerra
    if df_novos.empty:
        print("\nNenhum dado novo disponível. A base já está 100% atualizada!")
        return df_base

    # Formata a coluna de datas
    df_novos.reset_index(inplace=True)
    df_novos.rename(columns={'index': 'data'}, inplace=True)

    # 3. Junta com o histórico antigo (Upsert)
    if not df_base.empty:
        df_final = pd.concat([df_base, df_novos], ignore_index=True)
        df_final = df_final.drop_duplicates(subset=['data'], keep='last')
    else:
        df_final = df_novos

    # Ordena cronologicamente e guarda o CSV final
    df_final = df_final.sort_values('data').reset_index(drop=True)
    df_final.to_csv(ficheiro, index=False)

    print(f"\n✅ Base guardada com sucesso! Total de registos: {len(df_final)}")
    return df_final

#=================================================
# 3. EXECUÇÃO
#=================================================

if __name__ == "__main__":
    
    API_KEY_FRED = os.environ.get('FRED_API_KEY')
    API_KEY_ALPHA = os.environ.get('ALPHA_API_KEY')
    
    # 11 Commodities do FRED
    lista_fred = {
        'Petroleo_WTI': 'DCOILWTICO', 
        'Gas_Natural': 'DHHNGSP', 
        'Cobre': 'PCOPPUSDM', 
        'Aluminio': 'PALUMUSDM', 
        'Zinco': 'PZINCUSDM', 
        'Estanho': 'PTINUSDM', 
        'Soja': 'PSOYBUSDM', 
        'Milho': 'PMAIZMTUSDM', 
        'Trigo': 'PWHEAMTUSDM', 
        'Algodao': 'PCOTTINDUSDM', 
        'Dolar_Index': 'DTWEXBGS'
    }
    
    # 3 ETFs de Metais Preciosos da Alpha Vantage
    lista_alpha = {
        'Ouro': 'GLD',
        'Platina': 'PPLT',
        'Paladio': 'PALL'
    }
    
    #END_DATE = '2026-02-28'
    END_DATE = None
    NOME_FICHEIRO = 'commodities_mensal.csv'
    
    # Executa o Pipeline unificado
    df_final = atualizar_base_unificada(API_KEY_FRED, API_KEY_ALPHA, lista_fred, lista_alpha, NOME_FICHEIRO, END_DATE)

    if df_final is not None and not df_final.empty:
        print("\nÚltimos 5 meses de dados capturados:")
        print(df_final.tail())