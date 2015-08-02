# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'CVtek dev'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "CVTek dev"
__status__ = "Development"
__model_name__ = 'gap_servico.GAPServico'
import auth, base_models
from orm import *
from form import *
class GAPServico(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_servico'
        self.__title__ ='Serviço'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['letra'] # define tambem o campo a ser mostrado  no m2m, independentemente da descricao no field do m2m
        self.__order_by__ = 'gap_servico.nome'
        self.__tabs__ = [
            ('Fluxo de Atendimento', ['gap_atendimento']),
            ('FAQ´s', ['gap_faq']),
            ('CheckList', ['gap_checklist']),
            ('Senha', ['gap_senha']),
            ]
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = string_field(view_order=1 , name='Nome', size=40)
        self.ascendente = choice_field(view_order=2 , name='Ascendente', size=40, model='gap_servico', column='nome', options="model.get_self()")
        self.letra = string_field(view_order=3 , name='Letra', size=15)
        self.gap_turno = many2many(view_order=4, name='Horário', size=40 , fields=['hora_inicio'], model_name='gap_turno.GAPTurno', condition="gap_servico='{id}'", onlist=False)
        self.gap_documento = many2many(view_order=5, name='Documento', fields=['nome'], size=60, model_name='gap_documento.GAPDocumento', condition="gap_servico='{id}'", onlist=False)
        self.gap_senha_config = many2many(view_order = 6, name = 'Configurador de Senha', size = 50, fields=['loja'], model_name = 'gap_senha_config.GAPSenhaConfig', condition = "gap_servico='{id}'", onlist=False)
        self.descricao = text_field(view_order=7, name='Descricao', size=60, args="rows=20", onlist=True, search=False)
        self.gap_atendimento = list_field(view_order=8, name ='Fluxo de Atendimento', condition="servico='{id}'",fields=['nome','ordem'], model_name='gap_atendimento.GAPAtendimento', list_edit_mode = 'popup', onlist = False)
        self.gap_faq = list_field(view_order=9, name ='FAQ´s', condition="servico='{id}'",fields=['pergunta','resposta'], model_name='gap_faq.GAPFaq', list_edit_mode='popup', onlist = False)
        self.gap_checklist = list_field(view_order=10, name ='CheckList', condition="servico='{id}'",fields=['nome','checklist'], model_name='gap_checklist.GAPChecklist', list_edit_mode='popup', onlist = False)
        self.gap_senha = list_field(view_order=11, name ='Senha', condition="servico='{id}'",fields=['nr_senha','hora_ped'], model_name='gap_senha.GAPSenha', list_edit_mode='popup', onlist = False)


    #Apanha todos os Serviços
    def get_self(self):
        return self.get_options()

    #Apanha Serviço por nome
    def get_servico_nome(self, nome=''):
        #Essa funçao apanha serviço por nome
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['nome'] == nome:
                        options.append((str(option['id']), option['nome'] + ' - ' + option['descricao']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_servico_nome', createfunc=get_results)


    #Apanha os Serviços
    def get_servico(self):
        #Essa funçao apanha todos os serviços
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                     options.append((str(option['id']))+";"+str(option['letra']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_servico', createfunc=get_results)


    #Apanha a letra do serviço associado a essa id :)
    def get_letra_servico(self,keyservico):
        #Essa funçao apanha a letra do servico xpto
        try:
            self.where = "id = '{keyservico}'".format(keyservico=str(keyservico))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return self.kargs['letra']
        except:
            return None


    #Apanha a letra do serviço associado a essa id :)
    def get_id_servico(self,letraservico):
        #Essa funçao apanha a letra do servico xpto
        try:
            self.where = "letra = '{letraservico}'".format(letraservico=str(letraservico))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return self.kargs['id']
        except:
            return None

