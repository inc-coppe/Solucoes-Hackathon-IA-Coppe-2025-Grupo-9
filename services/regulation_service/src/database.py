# Cole este código em services/regulation_service/src/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Carrega as variáveis de ambiente para conexão com o BD
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.getenv("POSTGRES_DB", "sus_hackathon_db")
DB_HOST = "db_postgres" # Usamos o nome do serviço do docker-compose
DB_PORT = "5432"

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

# Cria a "engine" de conexão do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma fábrica de sessões (SessionLocal) para interagir com o BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa que será usada pelos nossos modelos de tabela
Base = declarative_base()