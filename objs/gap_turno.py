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
__model_name__ = 'gap_turno.GAPTurno'
import auth, base_models
from orm import *
from form import *

class GAPTurno(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_turno'
        self.__title__ ='Horário' #Gestão de atendimento Presencial turno
        self.__model_name__ = __model_name__
        self.__get_options__ = ['hora_inicio']
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_turno.numero'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }

        self.data = date_field(view_order=1, name ='Data',size=40, args='required', default=datetime.date.today())
        self.hora_inicio = time_field(view_order=2, name ='Hora Inicio',size=40, args='required', default=time.strftime('%H:%M:%S'))
        self.hora_fim = time_field(view_order=3, name ='Hora Fim',size=40, args='required')
        self.gap_servico = many2many(view_order=4, name='Serviço', fields=['nome'], size=80, model_name='gap_servico.GAPServico', condition="gap_turno='{id}'", onlist=False)
        self.gap_balcao = many2many(view_order=5, name='Balcão', fields=['nome'], size=80, model_name='gap_balcao.GAPBalcao', condition="gap_turno='{id}'", onlist=False)
        self.estado = info_field(view_order = 6, name = 'Estado', default = 'Aberta')
        self.numero = info_field(view_order = 7, name = 'Número')


#Precisamos fazer a funcao para fechar o turno
"""
    def Fechar(self, key, window_id):
        #Fecha a turno
        if key != 'None':
            self.kargs = get_model_record(model = self, key = key)
            if not self.kargs['numero']:
                self.kargs['numero'] = base_models.Sequence().get_sequence('caixa')
            if not self.kargs['hora_final']:
                self.kargs['hora_final'] = time.strftime('%H:%M')
            self.kargs['estado'] = 'Fechada'
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)
            return form_edit(window_id = window_id).show()
"""
