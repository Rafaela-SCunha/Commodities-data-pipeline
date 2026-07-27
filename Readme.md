# 📈 Commodity Monitoring Data Pipeline

> Automated data collection and processing pipeline for financial and macroeconomic commodity monitoring.

---

## Project Overview

This project implements an automated pipeline to collect, process, and update historical and current data from **14 commodity markets**.

The system integrates financial and economic APIs, performs incremental data updates, processes time series data, and automatically executes scheduled workflows using GitHub Actions.

The main goal is to create a reliable and scalable data pipeline for commodity market monitoring.

---

## Pipeline Architecture

Financial APIs
↓
Python Data Extraction
↓
Data Validation & Processing
↓
Incremental CSV Storage
↓
Automated Scheduled Updates


---

## Main Features

### Automated Data Collection

✔ Hybrid extraction using:

- **FRED API** (Federal Reserve Economic Data)
- **Alpha Vantage API**

---

### Incremental Data Updates

The pipeline automatically:

- Checks the latest available date
- Downloads only new records
- Prevents duplicated data
- Maintains historical continuity

---

### Automated Workflow

Using **GitHub Actions**, the pipeline runs automatically every Friday night, ensuring that datasets remain updated without manual intervention.

---

### Data Processing

The system performs:

- Time series cleaning
- Frequency conversion (daily/weekly to monthly averages)
- Data consolidation
- Historical dataset maintenance

---

## Monitored Assets

The pipeline collects data from multiple commodity categories:

### Energy

- WTI Crude Oil
- Natural Gas

### Industrial Metals

- Copper
- Aluminum
- Zinc
- Tin

### Precious Metals

- Gold
- Platinum
- Palladium (via ETFs)

### Agriculture

- Soybeans
- Corn
- Wheat
- Cotton

### Macroeconomic Indicator

- US Dollar Index (DXY)

---

## Technologies Used

- Python 3.10+
- Pandas
- FRED API
- Alpha Vantage API
- GitHub Actions
- Time Series Processing

---

## Skills Demonstrated

- Python Automation
- API Integration
- Data Extraction
- Data Processing
- ETL Pipelines
- Workflow Automation
- Financial Data Engineering

#### versão em português
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