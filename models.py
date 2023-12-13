from db import Base
from sqlalchemy import Column, Integer, DateTime, Float

class DadosEsteira(Base):
    """
    Modelo dos dados
    """
    __tablename__ = 'dadosesteira'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    tempCarc = Column(Float)
    velEsteira = Column(Float)
    cargaPV = Column(Float)
    tensaoRS = Column(Integer)
    statusPID = Column(Integer)
    frequencia=Column(Integer)
    corenter=Column(Integer)
    correntes=Column(Integer)
    correntet=Column(Integer)
    correnten=Column(Integer)
    correnteMedia = Column(Integer)
    tensaors = Column(Integer)
    tensaost = Column(Integer)
    tensaotr = Column(Integer)
    potAtivar = Column(Integer)
    potAtivas = Column(Integer)
    potAtivat = Column(Integer)
    potAtivaTotal = Column(Integer)
    fatorPot = Column(Integer)
    rotmotor = Column(Float)
    indicaPartida = Column(Integer)
    torque = Column(Float)
    tipoMotor = Column(Integer)

    def get_resultsdic(self):
        return {'id':self.id,
        'es.timestamp':self.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
        'es.status_pid':self.statusPID,
        'es.temp_carc':self.tempCarc,
        'es.le_carga':self.cargaPV,
        'es.esteira':self.velEsteira,
        'es.frequencia':self.frequencia,
        'es.corrente_r':self.correnter,
        'es.corrente_s':self.correntes,
        'es.corrente_t':self.correntet,
        'es.corrente_n':self.correnten,
        'es.corrente_media':self.correnteMedia,
        'es.tensao_rs':self.indicaPartida,
        'es.tensao_st':self.torque,
        'es.tensao_tr':self.tipoMotor,
        'es.ativa_r':self.potAtivar,
        'es.ativa_s':self.potAtivas,
        'es.ativa_t':self.potAtivat,
        'es.ativa_total':self.potAtivatotal,
        'es.fp_total':self.fatorPot,
        'es.encoder':self.rotmotor,
        'es.carga':self.cargapid,
        'es.habilita':self.indicaPartida,
        'es.torque':self.torque
        'es.tipo_motor':self.tipoMotor
        
        
        }