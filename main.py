from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder

# Comentario teste ppiara commit/push
class MainApp(App):
    """
    Classe com o aplicativo
    """

    def build(self):
        """
        Método que gera o aplicativo com base no widget principal
        """
        self._widget = MainWidget(scan_time=1000, server_ip='10.15.20.17', server_port=10011,
        modbus_addrs={
            'es.status_pid':{
                'addr':722,
                'tipo':'4X',
                'div':1 ,
                'atuador':0
            },
            'es.temp_carc':{
                'addr':706,
                'tipo':'FP',
                'div':10,
                'atuador':0
            },
            'es.le_carga':{
                'addr':710,
                'tipo':'FP',
                'div':1,
                'atuador':0
            },
            'es.esteira':{
                'addr':724,
                'tipo':'FP',
                'div':1,
                'atuador':0
            },
            'es.frequencia':{
                'addr':830,
                'tipo':'4X',
                'div':100,
                'atuador':0
            },
            'es.corrente_r':{
                'addr':840,
                'tipo':'4X',
                'div':100,
                'atuador':0
            },
            'es.corrente_s':{
                'addr':841,
                'tipo':'4X',
                'div':100,
                'atuador':0
            },
            'es.corrente_t':{
                'addr':842,
                'tipo':'4X',
                'div':100,
                'atuador':0
            },
            'es.corrente_n':{
                'addr':843,
                'tipo':'4X',
                'div':100,
                'atuador':0
            },
            'es.corrente_media':{
                'addr':845,
                'tipo':'4X',
                'div':100,
                'atuador':0
            },
            'es.tensao_rs':{
                'addr':847,
                'tipo':'4X',
                'div':10,
                'atuador':0
            },
            'es.tensao_st':{
                'addr':848,
                'tipo':'4X',
                'div':10,
                'atuador':0
            },
            'es.tensao_tr':{
                'addr':849,
                'tipo':'4X',
                'div':10,
                'atuador':0
            },
            'es.ativa_r':{
                'addr':852,
                'tipo':'4X',
                'div':1,
                'atuador':0
            },
            'es.ativa_s':{
                'addr':853,
                'tipo':'4X',
                'div':1,
                'atuador':0
            },
            'es.ativa_t':{
                'addr':854,
                'tipo':'4X',
                'div':1,
                'atuador':0
            },
            'es.ativa_total':{
                'addr':855,
                'tipo':'4X',
                'div':1,
                'atuador':0
            },
            'es.fp_total':{
                'addr':871,
                'tipo':'4X',
                'div':1000,
                'atuador':0
            },
            'es.encoder':{
                'addr':884,
                'tipo':'FP',
                'div':1,
                'atuador':0
            },
            'es.torque':{
                'addr':1420,
                'tipo':'4X',
                'div':100,
                'atuador':0
            },
            'es.tipo_motor':{
                'addr':708,
                'tipo':'4X',
                'div':1,
                'atuador':0
            },
            'es.indica_driver':{
                'addr':1216,
                'tipo':'4X',
                'div':1,
                'atuador':1
            },
            'es.atv31':{
                'addr':1312,
                'tipo':'4X',
                'div':1,
                'atuador':1
            },
            'es.atv31_velocidade':{
                'addr':1313,
                'tipo':'4X',
                'div':10,
                'atuador':1
            },
            'es.atv31_acc':{
                'addr':1314,
                'tipo':'4X',
                'div':10,
                'atuador':1
            },
            'es.atv31_dcc':{
                'addr':1315,
                'tipo':'4X',
                'div':10,
                'atuador':1
            },
            'es.ats48':{
                'addr':1316,
                'tipo':'4X',
                'div':1,
                'atuador':1
            },
            'es.ats48_acc':{
                'addr':1317,
                'tipo':'4X',
                'div':1,
                'atuador':1
            },
            'es.ats48_dcc':{
                'addr':1318,
                'tipo':'4X',
                'div':1,
                'atuador':1
            },
            'es.tesys':{
                'addr':1319,
                'tipo':'4X',
                'div':1,
                'atuador':1
            },
            'es.sel_driver':{
                'addr':1324,
                'tipo':'4X',
                'div':1,
                'atuador':1
            },
            'es.sel_pid':{
                'addr':1332,
                'tipo':'4X',
                'div':1,
                'atuador':1
            },
            'es.habilita':{
                'addr':1330,
                'tipo':'4X',
                'div':1,
                'atuador':1
            },
            'es.carga':{
                'addr':1302,
                'tipo':'FP',
                'div':1,
                'atuador':1
            },
            'es.p':{
                'addr':1304,
                'tipo':'FP',
                'div':1,
                'atuador':1
            },
            'es.i':{
                'addr':1306,
                'tipo':'FP',
                'div':1,
                'atuador':1
            },
            'es.d':{
                'addr':1308,
                'tipo':'FP',
                'div':1,
                'atuador':1
            },
            'es.mv_escreve':{
                'addr':1310,
                'tipo':'FP',
                'div':1,
                'atuador':1
            }
        }
        )

        return self._widget
    
    def on_stop(self):
        """
        Método que é executado ao fechar a aplicação
        """
        self._widget.stopRefresh()

if __name__ == '__main__':
    Builder.load_string(open("mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv",encoding="utf-8").read(),rulesonly=True)
    MainApp().run()
    
    
"""
    {'timestamp': datetime.datetime(2023, 12, 14, 9, 58, 59, 916366), 'values': 
    {'es.status_pid': 1.0, 'es.temp_carc': 26.5, 'es.le_carga': 0.0, 'es.esteira': 0.0, 'es.frequencia': 60.03, 'es.corrente_r': 0.0, 'es.corrente_s': 0.0, 'es.corrente_t': 0.0, 'es.corrente_n': 0.0, 'es.corrente_media': 0.0, 'es.tensao_rs': 224.6, 'es.tensao_st': 224.1, 'es.tensao_tr': 226.1, 'es.ativa_r': 0.0, 'es.ativa_s': 0.0, 'es.ativa_t': 0.0, 'es.ativa_total': 0.0, 'es.fp_total': 32.768, 'es.encoder': 0.0, 'es.torque': 0.0, 'es.tipo_motor': 1.0, 'es.sel_pid': 1, 'es.mv_escreve': 0.0, 'es.carga': 0.0, 'es.p': 8.0, 'es.i': 5.0, 'es.d': 2.0, 'es.tesys': None, 'es.ats48': None, 'es.ats48_acc': None, 'es.ats48_dcc': None, 'es.atv31': 0, 'es.atv31_acc': 10.0, 'es.atv31_dcc': 10.0, 'es.atv31_velocidade': 60.0, 'es.sel_driver': 2}}

    {'timestamp': datetime.datetime(2023, 12, 14, 9, 58, 59, 916366), 'values': 
    {'es.status_pid': 1.0, 'es.temp_carc': 26.5, 'es.le_carga': 0.0, 'es.esteira': 0.0, 'es.frequencia': 60.03, 'es.corrente_r': 0.0, 'es.corrente_s': 0.0, 'es.corrente_t': 0.0, 'es.corrente_n': 0.0, 'es.corrente_media': 0.0, 'es.tensao_rs': 224.6, 'es.tensao_st': 224.1, 'es.tensao_tr': 226.1, 'es.ativa_r': 0.0, 'es.ativa_s': 0.0, 'es.ativa_t': 0.0, 'es.ativa_total': 0.0, 'es.fp_total': 32.768, 'es.encoder': 0.0, 'es.torque': 0.0, 'es.tipo_motor': 1.0, 'es.sel_pid': 1, 'es.mv_escreve': 0.0, 'es.carga': 0.0, 'es.p': 8.0, 'es.i': 5.0, 'es.d': 2.0, 'es.tesys': None, 'es.ats48': None, 'es.ats48_acc': None, 'es.ats48_dcc': None, 'es.atv31': 0, 'es.atv31_acc': 10.0, 'es.atv31_dcc': 10.0, 'es.atv31_velocidade': 60.0, 'es.sel_driver': 2}}"""