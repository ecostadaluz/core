# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVTek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVTek dev"
__status__ = "Development"
__model_name__ = 'gap_multimedia.GAPMultimedia'
import auth, base_models
from orm import *
from form import *

class GAPMultimedia(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_multimedia'
        self.__title__ = 'Multimedia'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_multimedia.nome'
        self.__workflow__ = (
            'tipo', {'image':['TesteButton']}
            )
        self.__workflow_auth__ = {
            'TesteButton':['All'],
            }
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.__get_options__ = ['nome']
        self.nome = string_field(view_order = 1, name = 'Nome', size = 70)
        self.ficheiro = image_field(view_order=2, name='UploadFicheiro', size=30, onlist=False)
        self.data_ini = date_field(view_order=3, name ='Data Inicio',size = 40, args='required',  default=datetime.date.today())
        self.data_fim = date_field(view_order=4, name ='Data Fim',size = 40, args='required',  default=datetime.date.today())
        self.duracao_imagem = time_field(view_order=5, name ='Duraçao Imagem', size=40, onlist=False, default=time.strftime('%H:%M:%S'))
        self.tipo = combo_field(view_order = 6, name = 'Tipo', size = 50, args='required', default = 'image', options = [('image','Imagem'), ('video','Video')], onlist = True)
        self.ordem = integer_field(view_order = 7, name = 'Ordem', size = 40)
        self.terminal = many2many(view_order = 8, name = 'Loja', size = 50, fields=['name'], model_name = 'terminal.Terminal', condition = "gap_multimedia='{id}'", onlist=False)



    #Apanha toda a multimedia disponivel :)
    def get_self(self):
        return self.get_options()


    def get_opts(self, get_str):
        return eval(get_str)

    #Apanha a lista multimedia disponivel para reproduzir
    def get_playlist(self):
        #retorna a lista do playlist
        def get_results():
            options = []
            opts = self.get(order_by='ordem')
            for option in opts:
                    options.append(option['nome']+';'+option['ficheiro']+';'+option['tipo']+";"+str(option['duracao_imagem'])+";")
            return options
        return erp_cache.get(key=self.__model_name__ + '_playlist', createfunc=get_results)


    #Apanha a lista multimedia disponivel para reproduzir para uma determinada loja ainda precisa de toque
    def get_playlist_loja(self,loja=''):
        #Descartar a musica ou imagem cujo a data final >= data actual
        self.descartar_multimedia(loja=loja)
        def get_results():
            options = []
            opts = self.get(order_by='ordem')
            for option in opts:
                   options.append(option['nome']+' - '+ option['ficheiro']+' - '+ option['tipo']+' - '+str(option['duracao_imagem']))
            return options
        #Retorna a playlist para uma loja xpto :)
        return erp_cache.get(key=self.__model_name__ + '_playlist_loja', createfunc=get_results)


    #Descartar ficheiros multimedia com data limite expirada para uma loja(nome) especifica
    def descartar_multimedia(self):
        #Descartar a musica ou imagem cujo a data final <= data hoje
        args = self.get(order_by='ordem')
        data_hoje = datetime.date.today()
        for self.kargs in args:
            data_fim = str(self.kargs['data_fim']).split("-")
            if  (datetime.date(int(data_fim[0]),int(data_fim[1]), int(data_fim[2])) <= data_hoje) and (self.kargs['active'] == True):
                    #Muda o estado do ficheiro multimedia para false fazendo com que o mesmo nao apareça mais na playlist
                    self.kargs['user'] = bottle.request.session['user']
                    self.kargs['where'] = "id='{id}'".format(id=self.kargs['id'])
                    self.delete()
        return True


    #Apanha a lista multimedia disponivel para reproduzir e apenas imagens
    def get_playlist_type_Image(self):
        #retorna a lista do playlist com apenas imagens
        def get_results():
            options = []
            opts = self.get()
            for option in opts:
                if option['tipo'] == 'imagem':
                     options.append(option['nome'] + ' - ' + option['ficheiro']+ ' - ' + option['duracao_imagem'])
            return options
        return erp_cache.get(key=self.__model_name__ + '_playlist_type_Image', createfunc=get_results)

    #Apanha a lista multimedia disponivel para reproduzir e apenas videos
    def get_playlist_type_video(self):
        #retorna a lista do playlist com apenas videos
        def get_results():
            options = []
            opts = self.get()
            for option in opts:
                if option['tipo'] == 'video':
                     options.append(option['nome'] + ' - ' + option['ficheiro'])
            return options
        return erp_cache.get(key=self.__model_name__ + '_playlist_type_video', createfunc=get_results)

    def TesteButton(self, key, window_id):
        print("here tst button")
        print("my key="+str(key))
        self.kargs = get_model_record(model=self, key=str('8de3b321-1ca7-4008-a5c7-ab4e45cd9a0e'))
        print("aqui para atendimento 2")
        self.kargs['tipo'] = 'video'
        print("aqui para atendimento 3")
        self.put()
        return "done"
