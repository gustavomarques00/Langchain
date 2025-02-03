import os
import psycopg2
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# API Key da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Função para conectar ao banco de dados PostgreSQL
def conectar_db():
    try:
        # Obtém as variáveis de ambiente para conectar ao banco de dados
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),  # Nome do banco de dados
            user=os.getenv("USER"),  # Seu usuário PostgreSQL
            password=os.getenv("PASSWORD_DB"),  # Sua senha do PostgreSQL
            host=os.getenv("DB_HOST", "localhost"),  # Host do banco de dados (localhost por padrão)
            port=os.getenv("DB_PORT", "5432")  # Porta do PostgreSQL (5432 por padrão)
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

