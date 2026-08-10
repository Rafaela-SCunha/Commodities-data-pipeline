# Pipeline de Monitoramento de Commodities

O objetivo deste repositório é automatizar a extração de dados históricos e atuais de 14 commodities 

## Funcionalidades
- **Extração Híbrida**: Coleta de dados via API do **FRED** (Federal Reserve Economic Data) e **Alpha Vantage**.
- **Atualização Incremental**: O script verifica a última data no arquivo CSV e faz o download apenas dos dados novos, evitando duplicados.
- **Automação via GitHub Actions**: O pipeline é executado de forma autónoma todas as sextas-feiras à noite.
- **Tratamento de Dados**: Conversão automática de frequências (diário/semanal) para média mensal consolidada.

##  Ativos Monitorizados
O pipeline consolida dados de:
- **Energia**: Petróleo WTI e Gás Natural.
- **Metais Industriais**: Cobre, Alumínio, Zinco e Estanho.
- **Metais Preciosos**: Ouro, Platina e Paládio (via ETFs).
- **Agricultura**: Soja, Milho, Trigo e Algodão.
- **Macro**: Dólar Index (DXY).

## Tecnologias Utilizadas
- **Python 3.10+**
- **Pandas**: Manipulação e tratamento de séries temporais.
- **FRED API**: Dados macroeconómicos oficiais.
- **Alpha Vantage API**: Dados de mercado financeiro (ETFs).
- **GitHub Actions**: Orquestração e automação em nuvem.