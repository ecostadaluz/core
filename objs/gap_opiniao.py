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
__model_name__ = 'gap_opiniao.GAPOpiniao'
import auth, base_models
from orm import *
from form import *
try:
    from my_gap_senha import GAPSenha
except:
    from gap_senha import GAPSenha

class GAPOpiniao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_opiniao'
        self.__title__ = 'Opiniao'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_opiniao.nome'
        self.__workflow__ = (
            'estado', {'Confirmado':[]}
            )
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.__no_edit__ = [
            ('estado', ['Confirmado'])
            ]
        self.__get_options__ = ['nome']
        self.nome = string_field(view_order = 1, name = 'Nome', size = 80, search=True)
        self.contacto = string_field(view_order = 2, name = 'Contacto', size = 40)
        self.data = date_field(view_order=4, name ='Data', args='readonly', default=datetime.date.today())
        self.hora = time_field(view_order=5, name ='Hora', args='readonly', default=time.strftime('%H:%M:%S'))
        self.observacao = text_field(view_order=6, name='Observação', size=100, args="rows=30", onlist=True, search=False)
        self.senha = choice_field(view_order=7 , name='Senha', size=60, model='gap_senha', column='nr_senha', options="model.get_opts('GAPSenha().get_self()')")
        self.estado = info_field(view_order = 8, name='Estado', default='Confirmado', args='style:visibility="hidden"', nolabel=True, onlist=False)


    #Apanha todas as opinioes disponiveis
    def get_self(self):
        return self.get_options()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)

    #Apanha todas as opinioes por data
    def get_opiniao_data(self, data=''):
        #Essa funçao apanha opiniao por data
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                    if option['data'] == data:
                        options.append((str(option['id']), option['nome'] + ' - ' + option['observacao']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_opiniao_data', createfunc=get_results)


   #Apanha todas as opinioes por nome
    def get_opiniao_nome(self, nome=''):
        #Essa funçao apanha opiniao por nome
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['nome'] == nome:
                    options.append((str(option['id']), option['nome'] + ' - ' + option['observacao']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_opiniao_nome', createfunc=get_results)


    #Mudar o estado para cancelado
    def change_estado(self, key):
        #Essa funçao muda o estado da senha para espera
        self.kargs = get_model_record(model=self, key=key)
        self.kargs['estado'] = 'Cancelado'
        self.put()
        return form_edit(window_id=window_id).show()