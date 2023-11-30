from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder


class MainApp(App):
    """Classe com o aplicativo."""

    def build(self):
        """Método que gera o aplicativo com base no widget principal."""
        self._widget = MainWidget(scan_time=1000, server_ip='10.15.20.17', server_port=10011,
        modbus_addrs={
            'es.torque': {
                'addr': 1420,
                'tipo':'FP',
                'div':100.0,
            },
            'es.habilita': {
                'addr':1330,
                'tipo': '4X',
                'div': 1
            },
            'es.indica_driver':{
                'addr':  1216,      
                'tipo': '4X',
                'div':1
            },
            'es.tipo_motor': {
                'addr':708,
                'tipo':'4X',
                'div':1
            },
            'es.temp_carc': {
                'addr':706,
                'tipo':'FP',
                'div': 10
            }
        }
        )

        return self._widget
    
if __name__ == '__main__':
    Builder.load_string(open("mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("popups.kv",encoding="utf-8").read(),rulesonly=True)
    MainApp().run()