import pandas as pd
import os
from sqlalchemy import create_engine

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "csv", "IOT-temp.csv")

    try:
        df = pd.read_csv(file_path)
        print("Arquivo carregado com sucesso!")

        # 🔽 TRATAMENTO DOS DADOS
        df.columns = ["id", "device_id", "timestamp", "temperature", "location"]

        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d-%m-%Y %H:%M")

        # 🔽 CONEXÃO COM POSTGRES (DOCKER)
        engine = create_engine("postgresql://postgres:1234@localhost:5432/iot_db")

        # 🔽 ENVIA PARA O BANCO
        df.to_sql("temperature_readings", engine, if_exists="replace", index=False)

        print("✅ Dados enviados para o PostgreSQL!")

        return df

    except FileNotFoundError:
        print(f"Erro: O arquivo não foi encontrado em: {file_path}")
        return None


if __name__ == "__main__":
    load_data()