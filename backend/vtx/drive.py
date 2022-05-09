
from pymodbus.client.sync import ModbusSerialClient as ModbusSerial
from pymodbus.client.sync import ModbusTcpClient as ModbusTcp
from .models import Gateway, Hist, Node, NodeSetup, Evento
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
                n.vibraX = self.dxm.read_holding_registers(setup.addrVibraX-1,1,unit=setup.address).registers[0]
                n.vibraZ = self.dxm.read_holding_registers(setup.addrVibraZ-1,1,unit=setup.address).registers[0]
                n.temp = self.dxm.read_holding_registers(setup.addrTemp-1,1,unit=setup.address).registers[0]
                if n.vibraX == None:
                    e = Evento(node=n,descricao="Gateway OffLine", tipo="Falha")
                    e.save()
                else:
                    if n.vibraX==65535:
                        n.estado = "Desconectado"
                        if n.online:
                            e = Evento(node=n,descricao="Node OffLine", tipo="Falha")
                            e.save()
                        n.online = False
                    else:
                        n.estado = "OK"
                        if n.online == False:
                            e = Evento(node=n,descricao="Node Restabelecido", tipo="Evento")
                            e.save()
                        n.online = True
                    if n.estado!="falha":     
                        alertaVX = setup.alertVibraX*1000   
                        alertaVZ = setup.alertVibraZ*1000  
                        alertaT = setup.alertTemp*20
                        if n.vibraX>alertaVX or n.vibraZ>alertaVZ or n.temp>alertaT:
                            n.estado = "alerta"
                        else:
                            n.estado = "OK"
                        n.save()
            self.gate = Gateway.objects.all()[0]
            self.gate.online = True
            self.gate.save()
            sleep(1)
            return True
        except Exception as ex:
            print(f'falha na leitura 2 - {str(ex)}')
            self.gate = Gateway.objects.all()[0]
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
                sleep(5)
       
    def _setupTCP(self):
        print('setupTcp...')
        self.__controleRead = False
        sleep(4)
        try:
            if self.gate.port.find(".")>0:
                self.dxm = ModbusTcp(host=self.gate.port, port=502)
            else:
                self.dxm = ModbusSerial(method="rtu", port=self.gate.port, timeout=1, boudrate=self.gate.boudrate)
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
        lastEvenX = False
        lastEvenZ = False
        lastEvenTemp = False
        score = 0
        while self.ctl_log:
            n = self.node
            setup = NodeSetup.objects.get(id=n.id)
            print(f'time: {time}, alvo:{setup.ciclo}')
            print(f'lastX: {lastEvenX}, lastZ: {lastEvenZ}, lastT: {lastEvenTemp}')
            if time > setup.ciclo and self.node.temp<3000:
                h = Hist(
                    node=self.node,vibraX=self.node.vibraX,
                    vibraZ= self.node.vibraZ, temp= self.node.temp,
                    alertVibraX= setup.alertVibraX, alertVibraZ= setup.alertVibraZ,
                    alertTemp= setup.alertTemp
                )      
                h.save()
                if n.vibraX>setup.alertVibraX*1000 and n.estado != "Desconectado":
                    print("alerta x")
                    score+=1
                    if not lastEvenX:
                        e = Evento(node=n,descricao="Vibração eixo X Alta", tipo="Alerta")
                        e.save()
                        lastEvenX=True
                        score+=10
                else:
                    if lastEvenX:
                        e = Evento(node=n,descricao="Vibração eixo X Normalizada", tipo="Evento")
                        e.save()
                    lastEvenX=False
                    score-=1
                if n.vibraZ>setup.alertVibraZ*1000 and n.estado != "Desconectado": 
                    score+=3
                    print("alerta z")
                    if not lastEvenZ:
                        e = Evento(node=n,descricao="Vibração eixo Z Alta", tipo="Alerta")
                        e.save()
                        lastEvenZ=True
                        score+=10
                else:
                    if lastEvenZ:
                        e = Evento(node=n,descricao="Vibração eixo Z Normalizada", tipo="Evento")
                        e.save()
                    lastEvenZ=False
                    score-=1
                if n.temp>setup.alertTemp*20 and n.estado != "Desconectado":
                    score+=3
                    print("alerta t")
                    if not lastEvenTemp:
                        e = Evento(node=n,descricao="Temperatura Alta", tipo="Alerta")
                        e.save()
                        lastEvenTemp=True
                        score+=10
                else:
                    if lastEvenTemp:
                        e = Evento(node=n,descricao="Temperatura Normalizada", tipo="Evento")
                        e.save()
                    lastEvenTemp=False
                    score-=3  
                time=0 
            #print(f'score: {score}')
            if score>=20:
                n.estado = "falha"
                n.save()
                score=20
            if score<0:
                score=0
                if n.estado == "falha":
                    n.estado = "alerta"
                    n.save()
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