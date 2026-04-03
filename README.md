# Monitoramento e Análise de Temperatura IoT

## Visão Geral

Este projeto implementa um pipeline de dados completo para monitorar e analisar dados de temperatura de dispositivos IoT. Ele abrange a ingestão, processamento, armazenamento e visualização de dados por meio de um dashboard interativo.

A solução utiliza **Python** para manipulação de dados, **PostgreSQL** para armazenamento e **Streamlit** para a construção de uma interface responsiva e amigável.

---

## Arquitetura

Dataset CSV → Processamento de Dados (Pandas) → PostgreSQL → Views SQL → Dashboard Streamlit

---

## Tecnologias Utilizadas

- **Python** (Linguagem principal)
- **Pandas** (Manipulação de dados)
- **SQLAlchemy** (ORM e conexão com banco)
- **PostgreSQL** (Armazenamento via Docker)
- **Streamlit** (Interface do Dashboard)
- **Plotly** (Gráficos interativos)

---

## Estrutura do Projeto

```text
machine/
│
├── machine_prediction/
│   ├── streamlit_app.py       # Aplicação principal do Dashboard
│   ├── data_loader.py         # Script de carga e limpeza de dados
│
├── csv/
│   └── IOT-temp.csv           # Dataset bruto
│
└── README.md

---
Configuração e Instalação
1. Clonar o repositório
Bash
git clone <https://github.com/AlanADS753/Iot>
cd machine
2. Instalar dependências
Bash
pip install pandas sqlalchemy psycopg2-binary streamlit plotly
3. Rodar PostgreSQL com Docker
Bash
docker run --name postgres-iot -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres
4. Criar o banco de dados
Acesse o terminal do Postgres:

Bash
psql -U postgres -h localhost
E execute o comando SQL:

SQL
CREATE DATABASE iot_db;
Ingestão de Dados
Execute o script de carga para processar o dataset e enviar para o banco:

Bash
python machine_prediction/data_loader.py
O que o script faz:

Carrega e limpa os dados do CSV.

Padroniza os nomes das colunas.

Converte os campos de data/hora para o formato correto.

Insere os dados na tabela temperature_readings.

---

## Views SQL e Seus Objetivos
1. Média de Temperatura por Dispositivo

SQL
CREATE VIEW avg_temp_por_dispositivo AS
SELECT device_id, AVG(temperature) AS avg_temp
FROM temperature_readings
GROUP BY device_id;
Ajuda a identificar equipamentos com tendência ao superaquecimento.

2. Distribuição de Leituras por Hora
SQL
CREATE VIEW leituras_por_hora AS
SELECT EXTRACT(HOUR FROM timestamp) AS hora, COUNT(*) AS contagem
FROM temperature_readings
GROUP BY hora
ORDER BY hora;
Mostra os períodos de maior atividade do sistema.

3. Extremos de Temperatura Diária
SQL
CREATE VIEW temp_max_min_por_dia AS
SELECT DATE(timestamp) AS data,
       MAX(temperature) AS temp_max,
       MIN(temperature) AS temp_min
FROM temperature_readings
GROUP BY data
ORDER BY data;
Permite observar oscilações térmicas ao longo dos dias.

Executando o Dashboard
Para iniciar a interface visual:

Bash
cd machine_prediction
streamlit run streamlit_app.py
Insights e Análise

---

A partir deste dashboard, é possível:

Identificar dispositivos que operam fora da temperatura média ideal.

Detectar horários de pico na coleta de dados dos sensores.

Observar tendências térmicas para manutenção preditiva.

Visualizar anomalias ou falhas de leitura em períodos específicos.

---

Conclusão
Este projeto demonstra a implementação prática de um pipeline de análise de dados aplicado a cenários de IoT, focando em escalabilidade (usando SQL) e visualização de dados eficiente.