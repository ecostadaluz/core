# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = ['António Anacleto', 'Jair Medina']
__credits__ = []
__version__ = "1.0"
__maintainer__ =  ['António Anacleto', 'Jair Medina']
__status__ = "Development"
__model_name__= 'sai_pesquisacliente.SaiPesquisacliente'
#import base_models#auth,
from orm import *
from form import *


class SaiPesquisacliente (Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)

        self.__name__ = 'sai_pesquisacliente'
        self.__title__= 'Clientes de um Fornecedor'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__db_mode__ = 'None'
        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Imprimir']}
            )
        self.__workflow_auth__ = {
            'Confirmar':['Gestor'],
            'Rascunho':['Gestor'],

            'Imprimir':['All'],
           }

        self.__no_edit__ = [
            ('estado', ['Confirmado','Impresso'])
            ]



        self.nu_nif = integer_field(view_order=1, name='NIF', size=80)
        self.estado = info_field(view_order=4, name ='Estado', default='Confirmado', hidden=True, nolabel=True,onlist=False)



    def prepare_data(self):
        nu_nif = bottle.request.forms.get('nu_nif')

        descricao = 'Todos as declarações de clientes de um fornecedor'

        record = {}
        #print(nu_nif, cliente)

        data = run_sql("""select nu_nif, nm_contribuinte, dt_periodo, nu_nif_anexo, nm_contribuinte_anexo,nu_factura,dt_factura,vl_factura,vl_liquidado,validar_iva, nif_valido,declarado,info_valido from anexo_cli_out_13 where nu_nif_anexo=  '{nif}'  ORDER BY dt_periodo DESC""".format(nif=nu_nif))
        for i in data:
                record['contribuinte']= i['nm_contribuinte_anexo']
                break
        record['nu_nif'] =  nu_nif
        record['lines'] = data
        record['descricao'] = descricao
        return record


    def Imprimir(self, key, window_id):
        record = self.prepare_data()
        template = 'sai_pesquisacliente'
        return Report(record=record, report_template=template).show()



#252996704