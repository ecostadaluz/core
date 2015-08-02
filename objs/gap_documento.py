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
__model_name__ = 'gap_documento.GAPDocumento'
import auth, base_models
from orm import *
from form import *

class GAPDocumento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_documento'
        self.__title__ ='Documentos'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'gap_atendedor'
        self.__get_options__ = ['nome']
        self.__order_by__ = 'gap_documento.nome'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.nome = string_field(view_order=1 , name='Nome', size=40)
        self.data = date_field(view_order = 2, name = 'Data', size=40, args='readonly', default = datetime.date.today())
        self.documento = image_field(view_order=3, name='Upload Documento', size=50, onlist=False)
        self.gap_servico = many2many(view_order=4, name='Serviço', fields=['letra'], size=50, model_name='gap_servico.GAPServico', condition="gap_documento='{id}'", onlist=False)
        self.tipo = combo_field(view_order = 5, name = 'Tipo', size = 50, onlist = False, args = 'required', search = False, options = [('legislacao','Legislação'),('manual','Manual')])


    #Apanha todos os documentos
    def get_self(self):
        return self.get_options()

    #Apanha todos os documentos do tipo legislaçao
    def get_legislacao(self):
        #somente para testes
        """
        self.kargs['join'] = ",gap_documento_gap_servico"

        self.where =" gap_documento.id=gap_documento_gap_servico.gap_documento and  gap_documento_gap_servico.gap_servico='14504a9c-c1ab-4803-9ecd-4c322c024701' "
        """
        #Essa funçao retorna todos documentos do tipo legilaçao
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['tipo'] == 'legislacao':
                    options.append(option['nome'])
            return options
        return erp_cache.get(key=self.__model_name__ + '_legislacao', createfunc=get_results)


    #Apanha todos os documentos do tipo manuais
    def get_manuais(self):
        #somente para testes
        """
        self.kargs['join'] = ",gap_documento_gap_servico"

        self.where =" gap_documento.id='5041c140-5f49-451c-afa2-0c3dee67013b' and gap_documento_gap_servico.gap_documento='5041c140-5f49-451c-afa2-0c3dee67013b' and  gap_documento_gap_servico.gap_servico='14504a9c-c1ab-4803-9ecd-4c322c024701' "
        """
        #Essa funçao retorna todos documentos do tipo manuais
        def get_results():
            options = []
            opts = self.get(order_by='nome')
            for option in opts:
                if option['tipo'] == 'manual':
                    options.append(option['nome']+";"+option['documento'])
            return options
        return erp_cache.get(key=self.__model_name__ + '_manuais', createfunc=get_results)
