from db import Base
from sqlalchemy import Column, Integer, Float, DataTime


class DadoEsteira(Base):
    """
    Modelo dos dados da esteira
    """
    _tablename_ = 'dadoesteira'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DataTime)
    status_pid = Column(Integer)
    temp_carc = Column(Float)
    le_carga = Column(Float)
    esteira = Column(Float)
    frequencia = Column(Integer)
    corrente_r = Column(Integer)
    corrente_s = Column(Integer)
    corrente_t = Column(Integer)
    corrente_n = Column(Integer)
    corrente_media = Column(Integer)
    tensao_rs = Column(Integer)
    tensao_st = Column(Integer)
    tensao_tr = Column(Integer)
    ativa_r = Column(Integer)
    ativa_s = Column(Integer)
    ativa_t = Column(Integer)
    ativa_total = Column(Integer)
    fp_total = Column(Integer)
    encoder = Column(Float)
    indica_driver = Column(Integer)
    atv31 = Column(Integer)
    atv31_velocidade = Column(Integer)
    atv31_acc = Column(Integer)
    atv31_dcc = Column(Integer)
    ats48 = Column(Integer)
    tesys = Column(Integer)
    sel_drive = Column(Integer)
    sel_pid = Column(Integer)
    demanda_anterior = Column(Integer)
    demanda_atual = Column(Integer)
    demanda_media = Column(Integer)
    demanda_pico = Column(Integer)
    demanda_prevista = Column(Integer)
    habilita = Column(Integer)
    torque = Column(Float)
    
    
    