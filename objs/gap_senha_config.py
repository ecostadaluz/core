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
__model_name__ = 'gap_senha_config.GAPSenhaConfig'
import auth, base_models
from orm import *
from form import *


class GAPSenhaConfig(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_senha_config'
        self.__title__ = 'Configurador de Senha'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_senha_config.loja'

        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }

        self.__get_options__ = ['loja']
        self.descricao = string_field(view_order = 1, name = 'Descrição', size = 40, search=True)
        self.mensagem_cabecalho = text_field(view_order = 2, name = 'Mensagem de Cabeçalho', size = 50, search=True)
        self.logotipo = image_field(view_order=3, name='Upload Logo', size=30, onlist=False)
        self.loja = string_field(view_order = 4, name = 'Nome da Loja', size = 40, search=True)
        self.mensagem_rodape = text_field(view_order = 5, name = 'Mensagem de Rodapé', size = 50, search=True)
        self.terminal = many2many(view_order = 6, name = 'Loja', size = 50, fields=['name'], model_name = 'terminal.Terminal', condition = "gap_senha_config='{id}'", onlist=False)
        self.gap_servico = many2many(view_order = 7, name = 'Servico', size = 50, fields=['nome'], model_name = 'gap_servico.GAPServico', condition = "gap_senha_config='{id}'", onlist=False)
        self.data = date_field(view_order = 8, name = 'Data', size=50, default = datetime.date.today(),onlist=False, nolabel=True)



    #Apanha toda a configuraçao disponivel :)
    def get_self(self):
        return self.get_options()

    #Apanhar configurasao para uma loja xpto
    def get_config_loja(self, loja=''):
         #Essa funçao apanha configurasao para uma determinada loja
        def get_results():
            options = []
            opts = self.get()
            for option in opts:
                if option['loja'] == loja:
                    options.append((str(option['id']), option['mensagem_cabecalho'] + ' - ' + option['mensagem_rodape']+ ' - ' + option['descricao']+ ' - ' + option['logotipo']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_config_loja', createfunc=get_results)