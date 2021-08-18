from django.shortcuts import render,HttpResponse
from django.views.generic import View
import json
from .drive import *
from .models import Gateway, Node, NodeSetup, Hist, Evento
from django.db.models import Q
from datetime import datetime, timedelta


class IndexView(View):
    def get(self,request):
        return render(request,"index.html")

def online(request):
    gate = Gateway.objects.all()[0]
    ret = f'{{"dxm_online":"{gate.online}"}}'
    return  HttpResponse(ret)

def nodes(request):
    n = Node.objects.all()[0]
    ret = f'{{"id":{n.id},"name":"{n.name}","estado":"{n.estado}","online":"{n.online}","vibraX":{n.vibraX/1000},"vibraZ":{n.vibraZ/1000},"temp":{n.temp/20}}}'
    return  HttpResponse(ret)

class Filtra(View):
    def post(self,request):
        inis = str(request.POST['ini'])
        fims = str(request.POST['fim'])
        print(f'{inis}')
        print(f'{fims}')
        iniDA=inis.split('T')[0].split('-')
        iniTA=inis.split('T')[1].split(':')
        fimDA=fims.split('T')[0].split('-')
        fimTA=fims.split('T')[1].split(':')
        ini = datetime(int(iniDA[0]),int(iniDA[1]),int(iniDA[2]),int(iniTA[0]),int(iniTA[1]),0)
        fim = datetime(int(fimDA[0]),int(fimDA[1]),int(fimDA[2]),int(fimTA[0]),int(fimTA[1]),0)
        ini += timedelta(hours=3)
        fim += timedelta(hours=3)
        print(f'{ini}')
        print(f'{fim}')
        dadof = Hist.objects.filter(Q(date__gt=ini) & Q(date__lt=fim)).order_by('date')
        strinfy = ""
        
        for hf in dadof:
            hora = int(hf.date.hour)-3
            if hora<0:
                hora+=23  
            hf.date = f'{hora}:{hf.date.minute} {hf.date.day}/{hf.date.month}/{hf.date.year}'
            strinfy = f'{strinfy}{{"hora":"{hf.date}","Eixo x":{hf.vibraX/1000},"Eixo Z":{hf.vibraZ/1000},"Temperatura":{hf.temp/20},"Alerta X":{hf.alertVibraX},"Alerta Z":{hf.alertVibraZ},"Alerta Temper.":{hf.alertTemp}}},'
        strinfy = "[" + strinfy[:len(strinfy)-1] + "]"
        return HttpResponse(strinfy)

class Eventos(View):
    def post(self,request):
        inis = str(request.POST['ini'])
        fims = str(request.POST['fim'])
        print(f'{inis}')
        print(f'{fims}')
        iniDA=inis.split('T')[0].split('-')
        iniTA=inis.split('T')[1].split(':')
        fimDA=fims.split('T')[0].split('-')
        fimTA=fims.split('T')[1].split(':')
        ini = datetime(int(iniDA[0]),int(iniDA[1]),int(iniDA[2]),int(iniTA[0]),int(iniTA[1]),0)
        fim = datetime(int(fimDA[0]),int(fimDA[1]),int(fimDA[2]),int(fimTA[0]),int(fimTA[1]),0)
        ini += timedelta(hours=3)
        fim += timedelta(hours=3)
        print(f'{ini}')
        print(f'{fim}')
        dadof = Evento.objects.filter(Q(date__gt=ini) & Q(date__lt=fim)).order_by('date')
        strinfy = ""
        
        for hf in dadof:
            hora = int(hf.date.hour)-3
            if hora<0:
                hora+=23  
            hf.date = f'{hora}:{hf.date.minute} {hf.date.day}/{hf.date.month}/{hf.date.year}'
            strinfy = f'{strinfy}{{"hora":"{hf.date}","Node":"{hf.node}","Tipo":"{hf.tipo}","Evento":"{hf.descricao}"}},'
        strinfy = "[" + strinfy[:len(strinfy)-1] + "]"
        return HttpResponse(strinfy)





def para_dict(obj):
    # Se for um objeto, transforma num dict
    if hasattr(obj, '__dict__'):
        obj = obj.__dict__

    # Se for um dict, lê chaves e valores; converte valores
    if isinstance(obj, dict):
        return { k:para_dict(v) for k,v in obj.items() }
    # Se for uma lista ou tupla, lê elementos; também converte
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [para_dict(e) for e in obj]
    # Se for qualquer outra coisa, usa sem conversão
    else: 
        return obj

class dict_to_obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

class objectDict(dict):
    def __getattr__(self,name):
        return self.__getitem__(name)
