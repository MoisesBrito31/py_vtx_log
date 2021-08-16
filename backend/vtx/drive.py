
from pymodbus.client.sync import ModbusSerialClient as Modbus
from .models import Gateway, Hist, Node, NodeSetup
from time import sleep
from threading import Thread
from datetime import datetime, timedelta

try:
    gate = Gateway.objects.all()
    print(gate[0])
    devices = Node.objects.all()
    print(devices[0])

except Exception as ex:
    print(f'falha: {str(ex)}')

class Servico():
    __controleRead = True
    statusTcp = 'OffLine'
    statusScript = 'ok'
    execSetup = False
    lendo = False

    def __init__(self, gateway, nodes,):
        self.gate = gateway
        self.nodes = nodes

    def ler(self):
        try:
            for n in self.nodes:
                setup = NodeSetup.objects.get(id=n.id)
                n.vibraX = self.dxm.read_holding_registers(setup.addrVibraX-1,1,unit=setup.address).registers[0]/1000
                n.vibraZ = self.dxm.read_holding_registers(setup.addrVibraZ-1,1,unit=setup.address).registers[0]/1000
                n.temp = self.dxm.read_holding_registers(setup.addrTemp-1,1,unit=setup.address).registers[0]/20
                if n.vibraX==0.000 and n.vibraZ==0.000 and n.temp==0.0:
                    n.online = False
                else:
                    n.online = True
                n.save()
            self.gate.online = True
            self.gate.save()
            sleep(1)
            return True
        except Exception as ex:
            print(f'falha na leitura 2 - {str(ex)}')
            self.gate.online = False
            self.gate.save()
            sleep(2)
            return False

    def _readTCP(self):
        while self.__controleRead== True:
            if self.ler():
                self.statusTcp = 'dxm OnLine'
            else:
                self.statusTcp = 'dxm OffLine'
                sleep(3)
       
    def _setupTCP(self):
        print('setupTcp...')
        self.__controleRead = False
        sleep(4)
        try:
            self.dxm = Modbus(method="rtu", port=self.gate.port, timeout=1, boudrate=self.gate.boudrate)
            self.dxm.connect()
            retorno = self.dxm.read_holding_registers(0,1,unit=1)
            if retorno:
                self.statusTcp = 'dxm OnLine'
                self.__controleRead = True
                self.th = Thread(target=self._readTCP)
                self.th.start()    
            else:
                self.statusTcp = 'dxm OffLine'
                sleep(3)
                #if not self.lendo:
                self.__controleRead = True
                self.th = Thread(target=self._readTCP)
                self.th.start()
        except Exception as ex:
            self.statusTcp = 'dxm OffLine'
            print(f'falha no setup:  {str(ex)}')
            sleep(3)
            #if not self.lendo:
            self.__controleRead = True
            self.th = Thread(target=self._readTCP)
            self.th.start()
                
    
    def close(self):
        self.__controleRead = False 
        self.dxm.close()

class Ciclo():
    def __init__(self,node):
        self.ctl_log = True
        self.node = node
        self.Th = Thread(target=self.cicloLog)
    
    def cicloLog(self):
        sleep(10)
        time = 0
        while self.ctl_log:
            setup = NodeSetup.objects.get(id=self.node.id)
            print(f'time: {time}, alvo:{setup.ciclo}')
            if time > setup.ciclo:
                h = Hist(
                    node=self.node,vibraX=self.node.vibraX,
                    vibraZ= self.node.vibraZ, temp= self.node.temp,
                    alertVibraX= setup.alertVibraX, alertVibraZ= setup.alertVibraZ,
                    alertTemp= setup.alertTemp
                )
                h.save()
                time=0 
            time+=1
            sleep(1)

    def start(self):
        self.Th.start()

    def close(self):
        self.ctl_log=False

servico = Servico(gate[0],devices)

ciclos = []
for n in devices:
    ciclos.append(Ciclo(n))

def leitu():
    servico._setupTCP()
    for c in ciclos:
        c.start()
    controle = True
    while controle:
        cmd = input()
        if cmd == 'exit':
            for c in ciclos:
                c.close()
            servico.close()
            controle = False
        if cmd == 'sts':
            print(servico.statusTcp)
    print('fim...')




l = Thread(target=leitu)
l.start()