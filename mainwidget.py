from kivy.uix.boxlayout import BoxLayout    
from popups import ModbusPopup,ScanPopup, DataGraphPopup, PidPopup, MotorPopup , VarEltPopup, HistGraphPopup, SelectDataGraphPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random
from pymodbus import payload as pl
from timeseriesgraph import TimeSeriesGraph
from kivy.uix.boxlayout import BoxLayout 
from db import Base,Session,engine
from models import DadosEsteira
from kivy_garden.graph import LinePlot
from threading import Lock

class MainWidget(BoxLayout):
    """Classe que representa o widget principal."""
    
    _tags={'modbus_addrs':{}}
    _updateThread = None
    #_decoder = None
    _updateWidgets = True
    _dados={}
    _max_points = 20
    new_ymax = 100
    
    def __init__(self,**kwargs):
        """Construtor do widget principal."""
        
        super().__init__()
        self._scan_time = kwargs.get('scan_time')
        self._serverIP=kwargs.get('server_ip')
        self._serverPort=kwargs.get('server_port')
        self._modbusPopup= ModbusPopup(self._serverIP,self._serverPort)
        self._scanPopup = ScanPopup(self._scan_time)
        self._modbusClient = ModbusClient(host=self._serverIP,port=self._serverPort)
        self._pidPopup = PidPopup()
        self._motorPopup = MotorPopup()
        self._vareltPopup = VarEltPopup()
        self._selection='es.tensao_st'
        self._selectData= SelectDataGraphPopup()
        self._tags['modbus_addrs'] = kwargs.get('modbus_addrs')
        
        self._hgraph= HistGraphPopup(tags=self._tags)
        
        self._meas={}
        self._meas['timestamp']= None
        self._meas['values']={}
        
        #self._session=Session()   
        # Base.metadata.create_all(engine)  #
        self._lock=Lock()   #
        
        for key,value in self._tags['modbus_addrs'].items():
            if key== 'es.torque':
                plot_color = (1,0,0,1)
            else:
                plot_color = (random.random(),random.random(),random.random(),1)
            self._tags['modbus_addrs'][key]={'addr':value['addr'],'color':plot_color,'tipo':value['tipo'],'div':value['div'],'atuador':value['atuador']}
        print(self._tags)
        for key,value in self._tags['modbus_addrs'].items():
            if self._selection == key:
                self._graph=DataGraphPopup(self._max_points,self._tags['modbus_addrs'][key]['color'])


    def startDataRead(self,ip,port):
        """
        Método utilizado para a configuração do IP e porta do servidor Modbus e 
        inicialização da thread de leitura dos dados e atualização da interface gráfica
        """
        self._serverIp = ip
        self._serverPort = port
        self._modbusClient.host = self._serverIp
        self._modbusClient.port = self._serverPort
        try:
            Window.set_system_cursor('wait')
            self._modbusClient.open() 
            Window.set_system_cursor('arrow')
            if self._modbusClient.is_open: #conectar ao servidor modbus
                self._updateThread = Thread(target=self.updater) #se conectado, iniciar a thread de atualização
                self._updateThread.start()
                self.ids.img_con.source= 'imgs/conectado.png'
                self._modbusPopup.dismiss()
            else:
                self._modbusPopup.setInfo('Falha na conexão com o servidor')
        except Exception as e:
            print("Erro start Data read:",e.args)
            
    def updater(self):
        """
        Método que invoca as rotinas de leitura de dados, 
        atualização da interface e inserção dos dados no Banco de dados
        """
        try: #criando uma thread secundária
            while self._updateWidgets: 
                self.readData()
                self.updateGUI()
                #Inserir os dados no banco de dados
                sleep(self._scan_time/1000)
        except Exception as e:
            self._modbusClient.close()
            print("Erro updater:",e.args)
    
    def updateDataBank(self):
        """
        Método para a inserção dos dados no Banco de dados
        """
        try:
            self._dados = {
                'timestamp': self._meas['timestamp'],
                'tempCarc': self._meas['values']['es.temp_carc'],
                'velEsteira': self._meas['values']['es.esteira'],
                'cargaPV': self._meas['values']['es.le_carga'],
                'tensaoRS': self._meas['values']['es.tensao_rs'],
                'statusPID': self._meas['values']['es.status_pid'],
                'frequencia': self._meas['values']['es.frequencia'],
                'correnter': self._meas['values']['es.corrente_r'],
                'correntes': self._meas['values']['es.corrente_s'],
                'correntet': self._meas['values']['es.corrente_t'],
                'correnten': self._meas['values']['es.corrente_n'],
                'correnteMedia': self._meas['values']['es.corrente_media'],
                'tensaors': self._meas['values']['es.tensao_rs'],
                'tensaost': self._meas['values']['es.tensao_st'],
                'tensaotr': self._meas['values']['es.tensao_tr'],
                'potAtivar': self._meas['values']['es.ativa_r'],
                'potAtivas': self._meas['values']['es.ativa_s'],
                'potAtivat': self._meas['values']['es.ativa_t'],
                'potAtivaTotal': self._meas['values']['es.ativa_total'],
                'fatorPot': self._meas['values']['es.fp_total'],
                'rotmotor': self._meas['values']['es.encoder'],
                'indicaPartida': self._meas['values']['es.indica_driver'],
                'torque': self._meas['values']['es.torque'],
                'tipoMotor': self._meas['values']['es.tipo_motor']
            }
            dado=DadosEsteira(**self._dados)
            self._lock.acquire()
            self._session.add(dado)
            self._session.commit()
            self._lock.release()
        except Exception as e:
            print("Erro :",e.args)
            
    def getDataDB(self):
        """
        Método para busca no Banco de dados
        """
        try:
            init_t=self._hgraph.ids.txt_init_time.text
            final_t=self._hgraph.ids.txt_final_time.text
            init_t=datetime.strptime(init_t,'%d/%m/%Y %H:%M:%S')
            final_t=datetime.strptime(final_t,'%d/%m/%Y %H:%M:%S')
                
            if init_t is None or final_t is None:
                return
            self._lock.acquire()
            results=self._session.query(DadosEsteira).filter(DadosEsteira.timestamp.between(init_t,final_t)).all()
            self._lock.release()
            results = [reg.get_resultsdic() for reg in results]
            sensorAtivo=[]
            for sensor in self._hgraph.ids.sensores.children:
                if sensor.ids.checkbox.active:
                    sensorAtivo.append(sensor.ids.label.text)
            if results is None or len(results)==0:
                return
            self._hgraph.ids.graph.clearPlots()
            tempo=[]
            for i in results:
                for key,value in i.items():
                    if key=='timestamp':
                        tempo.append(value)
                        continue
                    elif key=='id':
                        continue
                    for s in sensorAtivo:
                        if key==s:
                            p= LinePlot(line_width=1)
                            p.points = [(x, results[x][key]) for x in range(0,len(results))]
                            self._hgraph.ids.graph.add_plot(p)
                            self._hgraph.ids.graph.ymax=self._tags['modbus_addrs'][s]['escalamax']
                            self._hgraph.ids.graph.y_ticks_major=self._tags['modbus_addrs'][s]['escalamax']/5
                            self._hgraph.ids.graph.ylabel= self._tags['modbus_addrs'][s]['legenda']
            self._hgraph.ids.graph.xmax=len(results)
            self._hgraph.ids.update_x_labels(tempo)
            

        except Exception as e:
            print("Erro na busca no banco:",e.args)
    
    def readData(self):
        """
        Método que realiza a leitura dos dados por meio do protocolo Modbus
        """
        try:
            self._meas['timestamp']=datetime.now() 
            
            for key,value in self._tags['modbus_addrs'].items():
                if value['atuador']==0:
                    if value['tipo']=='4X': #Holding Register 16bits
                        self._lock.acquire()
                        self._meas['values'][key]=(self._modbusClient.read_holding_registers(value['addr'],1)[0])/value['div']      
                        self._lock.release()
                    elif value['tipo']=='FP': #Floating Point
                        self._meas['values'][key]=(self.lerFloat(value['addr']))/value['div']
            
        except Exception as e:
            print("read data: ",e.args)
    
    def set_motor(self):
        if self._motorPopup.partida == 'Direta':
            self.writeData(1319,'4X',1,self._motorPopup.operacao)
        if self._motorPopup.partida == 'Inversor':
            self.writeData(1312,'4X',1,self._motorPopup.operacao)
        if self._motorPopup.partida == 'Soft-Start':
            self.writeData(1316,'4X',1,self._motorPopup.operacao)
        pass    
        
    def writeData(self,addr,tipo,div,value):
        """
        Método para a escrita de dados por meio do protocolo MODBUS
        """
        
        if tipo=='4X':
            self._lock.acquire()
            self._modbusClient.write_single_register(addr,int(value*div))
            self._lock.release()
        elif tipo=='FP':
            print(self.escreveFloat(addr,float(value*div)))

    def lerFloat(self, addr):
        self._lock.acquire()
        self._decoder = pl.BinaryPayloadDecoder.fromRegisters(self._modbusClient.read_holding_registers(addr,2),byteorder=pl.Endian.BIG,wordorder=pl.Endian.LITTLE)
        self._lock.release()
        return self._decoder.decode_32bit_float()
    
    def escreveFloat(self, addr, value):
        """
        Método para escrever um dado float utilizando o protocolo MODBUS
        """
        builder = pl.BinaryPayloadBuilder(byteorder=pl.Endian.BIG, wordorder=pl.Endian.LITTLE)
        builder.add_32bit_float(value)
        payload = builder.to_registers()
        return self._modbusClient.write_multiple_registers(addr,payload)
    
    def updateGUI(self):
        """
        Metodo para atualizar a interface grafica a partir dos dados lidos
        """
        # atualização do nível da velociade
        try:
            print(self._meas)
            self.ids.lb_velocidade.size[1] = (self.ids.velocidade.size[1])*(self._meas['values']['es.esteira'])/(20)  #(self._meas['values']['es.esteira']/100*self.ids.velocidade.size[1])#provavelmente o dado esteira esta errado, conferir no teste
            
            # atualização do gráfico
            self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values']['es.esteira']),0)
            # atualização dos labels da pagina principal
            self.ids['es.esteira'].text=str(round(self._meas['values']['es.esteira'],2))+' m/min'
            self.ids['es.le_carga'].text=str(round(self._meas['values']['es.le_carga'],2))+' kgf/cm²'
            
            self._pidPopup.update(self._meas)
            self._vareltPopup.update(self._meas) #conferir o endereço passado vareltPopup
            self._motorPopup.update(self._meas)
            self.updateGraph() 
            print(self._meas)
        except Exception as e:
            print("e1: ",e.args)


    def updateGraph(self):
        '''
        Método para a atualização do gráfico
        '''
        self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values'][self._selection]),0)
        self._graph.ids.graph.ymax = self.new_ymax
        self._graph.ids.graph.ylabel = self._selection
        self._graph.ids.graph.y_ticks_major = self.new_ymax/10
        # self._graph.ids.graph.ylabel= str(self._tags['modbus_addrs'])
        # self._graph.ids.graph.ymax=self._tags['modbus_addrs']
        # self._graph.ids.graph.y_ticks_major=self._tags['modbus_addrs']           
        
    def stopRefresh(self):
        self._updateWidgets = False