from django.db import models
from django.db.models.aggregates import Min

class Gateway(models.Model):
    name = models.CharField("dispositivo", max_length=20)
    address = models.IntegerField("endereço",unique=True, default=1)
    port = models.CharField("porta", max_length=20, default="COM4")
    boudrate = models.IntegerField("BoudRate", default=19200)
    online = models.BooleanField("Online")

    class Meta:
        verbose_name="Gateway"
        verbose_name_plural="Gateways"

    def __str__(self):
        return f'{self.name} id {self.address}'

class Node(models.Model):
    name = models.CharField("Equipamento", max_length=20)
    vibraX = models.DecimalField("eixo x", default=0.000, decimal_places=3,max_digits=12)
    vibraZ = models.DecimalField("eixo z", default=0.000, decimal_places=3,max_digits=12)
    temp = models.DecimalField("Temperatura", default=0.000, decimal_places=1,max_digits=12)
    estado = models.CharField("Estado",max_length=30)
    online = models.BooleanField("Online")

    class Meta:
        verbose_name="Node"
        verbose_name_plural="Nodes"

    def __str__(self):
        return f'{self.name}'

class NodeSetup(models.Model):
    node = models.ForeignKey(Node,on_delete=models.CASCADE)
    nodeId = models.IntegerField("Node", default=1)
    address = models.IntegerField("endereço", default=1)
    ciclo = models.IntegerField("ciclo de logs (s)", default=60,)
    addrVibraX = models.IntegerField("endereço eixo x", default=1)
    addrVibraZ = models.IntegerField("endereço eixo z", default=1)
    addrTemp = models.IntegerField("endereço Temperatura", default=1)
    alertVibraX = models.DecimalField("Alert eixo x", default=5.000, decimal_places=3,max_digits=12)
    alertVibraZ = models.DecimalField("Alert eixo z", default=5.000, decimal_places=3,max_digits=12)
    alertTemp = models.DecimalField("Alert Temperatura", default=50.0, decimal_places=1,max_digits=12)
    alertVibraX2 = models.DecimalField("Alert eixo x", default=15.000, decimal_places=3,max_digits=12)
    alertVibraZ2 = models.DecimalField("Alert eixo z", default=15.000, decimal_places=3,max_digits=12)
    alertTemp2 = models.DecimalField("Alert Temperatura", default=70.00, decimal_places=1,max_digits=12)

    class Meta:
        verbose_name="NodeSetup"
        verbose_name_plural="NodeSetups"

    def __str__(self):
        return f'setup do node: {self.node}'


class Hist(models.Model):
    date = models.DateTimeField('Data',auto_now_add=True)
    node = models.ForeignKey(Node,on_delete=models.CASCADE)
    alertVibraX = models.DecimalField("Alert eixo x", default=5.000, decimal_places=3,max_digits=12)
    alertVibraZ = models.DecimalField("Alert eixo z", default=5.000, decimal_places=3,max_digits=12)
    alertTemp = models.DecimalField("Alert Temperatura", default=60.0, decimal_places=1,max_digits=12)
    vibraX = models.DecimalField("eixo x", default=0.000, decimal_places=3,max_digits=12)
    vibraZ = models.DecimalField("eixo z", default=0.000, decimal_places=3,max_digits=12)
    temp = models.DecimalField("Temperatura", default=0.000, decimal_places=1,max_digits=12)

    class Meta:
        verbose_name="Registro"
        verbose_name_plural="Registros"

    def __str__(self):
        return f'Registro de {self.date}'

class Evento(models.Model):
    date = models.DateTimeField('Data',auto_now_add=True)
    node = models.ForeignKey(Node,on_delete=models.CASCADE)
    descricao = models.CharField('Evento',max_length=50,default="generico")
    tipo = models.CharField('tipo de Evento',max_length=50,default="Evento")

    class Meta:
        verbose_name="Evento"
        verbose_name_plural="Eventos"

    def __str__(self):
        return f'Evento de {self.descricao}'

