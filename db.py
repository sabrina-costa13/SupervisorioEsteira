"""
    Objetos do sqlalchemy core para a realização da conexão e operação do Banco de Dados
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base


DB_CONNECTION = 'sqlite:///data\data.db?check_same_thread=False'
engine = create_engine(DB_CONNECTION, echo=False) #mecanismo que possibilita a comunicação com o SGBD.
Session = sessionmaker(bind=engine) 
Base = declarative_base() 