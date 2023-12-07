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
        
class LabeledCheckBoxDataGraph(BoxLayout):
    pass

class HistGraphPopup(Popup):
    def __init__(self,**kwargs):
        super().__init__()
        for key,value in kwargs.get('tags').itens():
            cb = LabeledCheckBoxHistGraph()
            
            
class LabeledCheckBoxHistGraph(BoxLayout):
    pass