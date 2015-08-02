# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVtek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVtek dev"
__status__ = "Development"
__model_name__ = 'gap_balcao.GAPBalcao'
import auth, base_models
from orm import *
from form import *
from terminal import Terminal as TerminalOriginal

class GAPBalcao(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_balcao'
        self.__title__ ='Balcão' #Gestão de atendimento Presencial serviço
        self.__model_name__ = __model_name__
        self.__get_options__ = ['numero']
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_balcao.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = string_field(view_order=1 , name='Nome', size=80)
        self.terminal = choice_field(view_order=2 , name='Loja', size=40, model='terminal', column='nome', options="model.get_self()")
        self.numero = integer_field(view_order=3 , name='Número', size=30)
        self.gap_turno = many2many(view_order=4, name='Horário', size=40 , fields=['hora_inicio'], model_name='gap_turno.GAPTurno', condition="gap_balcao='{id}'", onlist=False)
        self.users = many2many(view_order = 5, name = 'Atendedor', size = 50, fields=['nome'], model_name = 'users.Users', condition = "gap_balcao='{id}'", onlist=False)
        

    #Apanha todos os balcoes
    def get_self(self):
        return self.get_options()

    #Apanha balcoes por nome
    def get_balcao_nome(self, nome=''):
        #Essa funçao apanha balcao por nome
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                    if option['nome'] == nome:
                        options.append((str(option['id']), option['nome']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_balcao_nome', createfunc=get_results)