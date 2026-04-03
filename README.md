# Monitoramento e Análise de Temperatura IoT

## Visão Geral

Este projeto implementa um pipeline completo de dados para monitoramento e análise de temperatura em dispositivos IoT.

A solução cobre todas as etapas:
- Ingestão de dados
- Processamento
- Armazenamento
- Visualização interativa

Tecnologias utilizadas:
- Python para processamento
- PostgreSQL para armazenamento
- Streamlit para dashboard

---

## Arquitetura

```text
Dataset CSV
   ↓
Processamento (Pandas)
   ↓
PostgreSQL
   ↓
Views SQL
   ↓
Dashboard (Streamlit)
```

---

## Tecnologias Utilizadas

- Python
- Pandas
- SQLAlchemy
- PostgreSQL (Docker)
- Streamlit
- Plotly

---

## Estrutura do Projeto

```text
machine/
│
├── machine_prediction/
│   ├── streamlit_app.py       # Dashboard interativo
│   ├── data_loader.py         # Ingestão e limpeza dos dados
│
├── csv/
│   └── IOT-temp.csv           # Dataset original
│
└── README.md
```

---

## Configuração e Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/AlanADS753/Iot
cd machine
```

---

### 2. Instalar dependências

```bash
pip install pandas sqlalchemy psycopg2-binary streamlit plotly
```

---

### 3. Subir o PostgreSQL com Docker

```bash
docker run --name postgres-iot \
-e POSTGRES_PASSWORD=1234 \
-p 5432:5432 \
-d postgres
```

---

### 4. Criar o banco de dados

Acesse o terminal do PostgreSQL:

```bash
psql -U postgres -h localhost
```

Execute:

```sql
CREATE DATABASE iot_db;
```

---

## Ingestão de Dados

Execute o script:

```bash
python machine_prediction/data_loader.py
```

### O que o script faz:
- Carrega o CSV
- Limpa os dados
- Padroniza colunas
- Converte datas
- Insere na tabela temperature_readings

---

## Views SQL e Objetivos

### 1. Média de Temperatura por Dispositivo

```sql
CREATE VIEW avg_temp_por_dispositivo AS
SELECT device_id, AVG(temperature) AS avg_temp
FROM temperature_readings
GROUP BY device_id;
```

Identifica dispositivos com possível superaquecimento.

---

### 2. Leituras por Hora

```sql
CREATE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM timestamp) AS hora,
       COUNT(*) AS contagem
FROM temperature_readings
GROUP BY hora
ORDER BY hora;
```

Mostra horários de maior atividade.

---

### 3. Temperatura Máxima e Mínima por Dia

```sql
CREATE VIEW temp_max_min_por_dia AS
SELECT DATE(timestamp) AS data,
       MAX(temperature) AS temp_max,
       MIN(temperature) AS temp_min
FROM temperature_readings
GROUP BY data
ORDER BY data;
```

Analisa variações térmicas ao longo do tempo.

---

## Executando o Dashboard

```bash
cd machine_prediction
streamlit run streamlit_app.py
```

---

## Insights e Análises

Com o dashboard, é possível:

- Identificar dispositivos fora da temperatura ideal  
- Detectar horários de pico  
- Analisar tendências para manutenção preditiva  
- Encontrar anomalias ou falhas  

---

## Conclusão

Este projeto demonstra, na prática, a construção de um pipeline de dados para IoT, com foco em:

- Escalabilidade (uso de SQL)
- Organização de dados
- Visualização eficiente