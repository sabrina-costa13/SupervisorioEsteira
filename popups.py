from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy_garden.graph import LinePlot
from timeseriesgraph import TimeSeriesGraph
from kivy.uix.boxlayout import BoxLayout

class ModbusPopup(Popup):
    """Classe que gera o popup de configuração do Modbus"""
    
    _info_lb=None
    
    def __init__(self,server_ip,server_port,**kwargs):
        """
        Construtor da classe ModbusPopup
        """
        super().__init__(**kwargs)
        self.ids.txt_ip.text = str(server_ip)
        self.ids.txt_port.text = str(server_port)
        
    def setInfo(self,message):
        self._info_lb=Label(text=message)
        self.ids.layout.add_widget(self._info_lb)
        
    def clearInfo(self):
        if self._info_lb is not None:
            self.ids.layout.remove_widget(self._info_lb)

class ScanPopup(Popup):
    """
    Popup para a configuração do tempo de varredura
    """
    def __init__(self,scantime,**kwargs):
        """
        Construtor da classe ScanPopup
        """
        super().__init__(**kwargs)
        self.ids.txt_st.text = str(scantime)

class DataGraphPopup(Popup): #gráfico 
    def __init__(self,xmax,plot_color, **kwargs):
        super().__init__(**kwargs)
        self.plot = LinePlot(line_width=1.5, color=plot_color)
        self.ids.graph.add_plot(self.plot)
        self.ids.graph.xmax = xmax
class HistGraphPopup(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        print(teste)
        for key,value in kwargs.get('tags').items():
            print(f'teste: {key}')
            cb = LabeledCheckBoxHistGraph()
            cb.ids.label.text = key
            cb.id= key
            self.ids.sensores.add_widget(cb)
            
class PidPopup(Popup):
    """
    Popup para a configuração do PID
    """
    _SP=None
    _MV=None
    _P=None
    _I=None
    _D=None
    def __init__(self,**kwargs):
        """
        Construtor da classe PidPopup
        """
        super().__init__(**kwargs)
        self._MV=0.0
        self._SP=0.0
        self._P=8.0
        self._I=5.0
        self._D=2.0
    def update(self,medida):    #medida = meas
        """
        Método utilizado para atualizar os valores do PID
        """
        self.ids.es.le_carga.text = str(medida['values']['es.le_carga'])
        statusPID=medida['values']['es.status_pid']
        if statusPID == 0:
            self.ids.statusPID.text = 'Automático'
        elif statusPID == 1:
            self.ids.statusPID.text = 'Manual'
        #Atuadores
        AutomaticoPid=self.ids.AutomaticoOn.active
        if AutomaticoPid:
            medida['values']['es.sel_pid']=0
        else:
            medida['values']['es.sel_pid']=1
        medida['values']['es.mv_escreve']=self._MV
        medida['values']['es.carga']=self._SP
        medida['values']['es.p']=self._P
        medida['values']['es.i']=self._I
        medida['values']['es.d']=self._D
    def setSetPoint(self):
        self._SP= float(self.ids.es.carga.text) 
    def setMV(self):
        self._MV= float(self.ids.es.mv_escreve.text)
    def setP(self):
        self._P= float(self.ids.es.p.text)
    def setI(self):
        self._I= float(self.ids.es.i.text)
    def setD(self):
        self._D= float(self.ids.es.d.text)

class MotorPopup(Popup):
    """
    Popup para a configuração do motor
    """
    _partida=None
    _operacao=None
    _velInversor=None
    _aceleracao=None
    _desaceleracao=None
    def __init__(self,**kwargs):
        """
        Construtor da classe ComandoPopup
        """
        super().__init__(**kwargs)
        self._partida= 'Inversor' #Partida padrão como inversor
        self._operacao= 0 #Operação padrão como parado
        self._velInversor=float(self.ids["es.atv31_velocidade"].text)
        self._aceleracao=float(self.ids["es.atv31_acc"].text)
        self._desaceleracao=float(self.ids["es.atv31_dcc"].text)
    def update(self,medida):
        medida['values']['es.tesys']=None

        medida['values']['es.ats48']=None
        medida['values']['es.ats48_acc']=None
        medida['values']['es.ats48_dcc']=None

        medida['values']['es.atv31']=None
        medida['values']['es.atv31_acc']=None
        medida['values']['es.atv31_dcc']= None
        medida['values']['es.atv31_velocidade']=None

        if self._partida is not None:
            if self._partida== 'Direta':
                medida['values']['es.tesys']=self._operacao
                medida['values']['es.sel_driver']=3


            elif self._partida == 'Soft-Start':
                medida['values']['es.ats48']=self._operacao
                medida['values']['es.ats48_acc']=self._aceleracao
                medida['values']['es.ats48_dcc']=self._desaceleracao
                medida['values']['es.sel_driver']=1

            elif self._partida == 'Inversor':
                medida['values']['es.atv31']=self._operacao
                medida['values']['es.atv31_acc']=self._aceleracao
                medida['values']['es.atv31_dcc']=self._desaceleracao
                medida['values']['es.atv31_velocidade']=self._velInversor
                medida['values']['es.sel_driver']=2

class VarEltPopup(Popup):
    """
    Popup para a configuração das variáveis elétricas 
    """
    def __init__(self,**kwargs):
        """
        Construtor da classe VarEltPopup
        """
        super().__init__(**kwargs)
    def update(self,medida):
        """
        Método utilizado para atualizar os valores das medições
        """
        self.ids["es.corrente_media"].text = str(medida['values']['es.corrente_media'])
        self.ids["es.ativa_total"].text = str(medida['values']['es.ativa_total'])
        self.ids["es.frequencia"].text = str(medida['values']['es.frequencia'])
        self.ids["es.fp_total"].text = str(medida['values']['es.fp_total'])
        self.ids["es.tensao_rs"].text = str(medida['values']['es.tensao_rs'])  
        self.ids["es.tensao_st"].text = str(medida['values']['es.tensao_st'])   
        self.ids["es.tensao_tr"].text = str(medida['values']['es.tensao_tr']) 

    def setPartida(self,partida):
        self._partida=partida
    def setOperacao(self,operacao):
        self._operacao=operacao
    def setAcc(self):
        self._aceleracao=float(self.ids["es.atv31_acc"].text)
    def setDcc(self):
        self._desaceleracao=float(self.ids["es.atv31_dcc"].text)
    def setVelInversor(self):
        self._velInversor=int(self.ids["es.atv31_velocidade"].text)
    def setVelInversorSlider(self,vel):
        self._velInversor=vel

class HistGraphPopup(Popup):
    def __init__(self,**kwargs):
        super().__init__()
        for key,value in kwargs.get('tags').items():
            cb = LabeledCheckBoxHistGraph()
            cb.ids.label.text = key
            cb.id= key
            self.ids.sensores.add_widget(cb)
            
class LabeledCheckBoxHistGraph(BoxLayout):
    pass

class SelectDataGraphPopup(Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
class LabeledCheckBoxDataGraph(BoxLayout):
    pass