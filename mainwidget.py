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

class MainWidget(BoxLayout):
    """Classe que representa o widget principal."""
    
    _tags={'modbusaddrs':{},'atuadores':{}}
    _updateThread = None
    #_decoder = None
    _updateWidgets = True
    _dados={}
    _max_points = 20
    
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
        self._motorPopup=MotorPopup()
        self._vareltPopup = VarEltPopup()
        self._selection='es.tensao_st'
        self._selectData= SelectDataGraphPopup()
        
        
        self._hgraph= HistGraphPopup(tags=self._tags['modbusaddrs'])
        
        self._meas={}
        self._meas['timestamp']= None
        self._meas['values']={}
        
        for key,value in kwargs.get('modbus_addrs').items():
            print(f'key: {key}, value: {value}')
            if key== 'es.torque':
                plot_color = (1,0,0,1)
            else:
                plot_color = (random.random(),random.random(),random.random(),1)
            self._tags['modbusaddrs'][key]={'addr':value['addr'],'color':plot_color,'tipo':value['tipo'],'div':value['div']}
            
        for key,value in kwargs.get('atuadores').items():
            self._tags['atuadores'][key]={'addr':value['addr'],'tipo':value['tipo'],'div':value['div']}

        for key,value in self._tags['modbusaddrs'].items():
            if self._selection == key:
                self._graph=DataGraphPopup(self._max_points,self._tags['modbusaddrs'][key]['color'])



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
            
    def readData(self):
        """
        Método que realiza a leitura dos dados por meio do protocolo Modbus
        """
        self._meas['timestamp']=datetime.now() 
        
        for key,value in self._tags.items():
            if value['tipo']=='4X': #Holding Register 16bits
                self._meas['values'][key]=(self._modbusClient.read_holding_registers(value['addr'],1)[0])/value['div']      
        
            elif value['tipo']=='FP': #Floating Point
                
                self._meas['values'][key]=(self.lerFloat(value['addr']))/value['div']
                print(value['div'])
   
    def writeData(self,addr,tipo,div,value):
        """
        Método para a escrita de dados por meio do protocolo MODBUS
        """
        
        if tipo=='4X':
            self._modbusClient.write_single_register(addr,int(value*div))
        elif tipo=='FP':
            print(self.escreveFloat(addr,float(value*div)))

    def lerFloat(self, addr):
        self._decoder = pl.BinaryPayloadDecoder.fromRegisters(self._modbusClient.read_holding_registers(addr,2),byteorder=pl.Endian.BIG,wordorder=pl.Endian.LITTLE)
        return self._decoder.decode_32bit_float()
    
    def escreveFloat(self, addr, value):
        """
        Método para escrever um dado float utilizando o protocolo MODBUS
        """
        builder = pl.BinaryPayloadBuilder(byteorder=pl.Endian.BIG, wordorder=pl.Endian.LITTLE)
        builder.add_32bit_float(value)
        payload = builder.to_registers()
        return self._modbusClient.write_multiple_registers(addr,payload)
    
    def updateGUI(self):  # thiago explicar
        """
        Metodo para atualizar a interface grafica a partir dos dados lidos
        """
        #atualização do nível da velociade
        #self.ids.lb_velocidade.size[1] = (self._meas['values']['es.esteira']/100*self.ids.velocidade.size[1])#provavelmente o dado esteira esta errado, conferir no teste
        
        #atualização do gráfico
        #self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values']['es.esteira']),0)

        # atualizacao dos labels
        #for key, value in self._tags.items():
            #self.ids[key].text = str(self._meas['values'][key])
            
        self.ids['es.esteira'].text=str(round(self._meas['values']['es.esteira'],2))+' m/min'
        self.ids['es.le_carga'].text=str(round(self._meas['values']['es.le_carga'],2))+' kgf/cm²'
        #self.ids['freqRotacao'].text=str(self._meas['values']['freqRotacao'])+' RPM'
        partida=self._meas['values']['indicaPartida']
        if partida==3:
            self.ids['indicaPartida'].text='Direta'
        elif partida==1:
            self.ids['indicaPartida'].text='Soft-Start'
        elif partida==2:
            self.ids['indicaPartida'].text='Inversor'
        self.ids['es.torque'].text=str(self._meas['values']['torque'])+' N.m' #conferir a tag
        tipoMotor=self._meas['values']['es.tipo_motor']
        if tipoMotor==1:
            self.ids['btnComando'].background_color=(0,1,0,1)
        elif tipoMotor==2:
            self.ids['btnComando'].background_color=(0,0,1,1)
        self._pidPopup.update(self._meas)
        self._vareltPopup.update(self._meas) #conferir o endereço passado vareltPopup
        self._motorPopup.update(self._meas)

        #self.updateAtuadores()
        self.updateGraph() 

    def updateGraph(self):
        '''
        Método para a atualização do gráfico
        '''
        self._graph.ids.graph.updateGraph((self._meas['timestamp'],self._meas['values'][self._selection]),0)
        self._graph.ids.graph.ylabel= self._tags['modbusaddrs'][self._selection]['legenda']
        self._graph.ids.graph.ymax=self._tags['modbusaddrs'][self._selection]['escalamax']
        self._graph.ids.graph.y_ticks_major=self._tags['modbusaddrs'][self._selection]['escalamax']/5            
        
    def stopRefresh(self):
        self._updateWidgets = False