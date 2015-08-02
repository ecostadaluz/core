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
__model_name__ = 'gap_timeAtendimento.GAPTimeAtendimento'
import auth, base_models
from orm import *
from form import *
try:
    from my_gap_servico import GAPServico
except:
    from gap_servico import GAPServico

class GAPTimeAtendimento(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_timeAtendimento'
        self.__title__ ='Gap Time Atendimento'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_timeAtendimento.nr_senha'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
        }
        self.nome_atendedor = string_field(view_order = 1, name = 'Nome Atendedor', size = 80)
        self.nr_senha = integer_field(view_order= 2 , name='Nº Senha', size=30, onlist = True)
        self.servico = string_field(view_order = 3, name = 'servico', size = 50)
        self.hora_entrada= time_field(view_order=4, name ='Hora Pedido', size=40, onlist=True)
        self.data = date_field(view_order = 5, name = 'Data', size=40, args='readonly')
        self.tempo_atendimento= time_field(view_order=6, name ='Tempo Atendimento', size=40, onlist=True)
        self.estado = combo_field(view_order = 7, name = 'Estado', size = 50, default = 'Espera', options = [('espera','Espera'), ('espera_atendedor','Espera Atendedor'), ('atendido','Atendido'), ('desistiu','Desistiu'), ('transferido','Transferido'), ('para_atendimento','Para Atendimento')], onlist = True)
        self.observacao = text_field(view_order=8, name='Observação', size=100, args="rows=30", onlist=True, search=False)
        self.loja = string_field(view_order = 9, name = 'Loja', size = 50)

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)


    def getTimeAtendimento(self,nr_senha=None,servico=None):
        try:
            self.where = "nome_atendedor = '{name}' and nr_senha='{nr_senha}' and servico='{servico}' and data='{data}'".format(name=bottle.request.session['user_name'],nr_senha=nr_senha,servico=servico,data=str(datetime.date.today()))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return self.kargs['tempo_atendimento']
            return None
        except:
            return None

    def setTimeAtendimento(self,nr_senha=None,servico=None,tempo_atendimento=None):
        try:
            self.where = "nome_atendedor = '{name}' and nr_senha='{nr_senha}' and servico='{servico}' and data='{data}'".format(name=bottle.request.session['user_name'],nr_senha=nr_senha,servico=servico,data=str(datetime.date.today()))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['tempo_atendimento'] = tempo_atendimento
                self.put()
            return True
        except:
            return False

    def setEstadoAtendimento(self,nr_senha=None,servico=None,estado=None):
        try:
            self.where = "nome_atendedor = '{name}' and nr_senha='{nr_senha}' and servico='{servico}'  and data='{data}' ".format(name=bottle.request.session['user_name'],nr_senha=nr_senha,servico=servico,data=str(datetime.date.today()))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = estado
                self.put()
            return True
        except:
            return False


    def setObservacao(self,nr_senha=None,servico=None,comentario=None):
        try:
            self.where = "nome_atendedor = '{name}' and nr_senha='{nr_senha}' and servico='{servico}' and data='{data}'".format(name=bottle.request.session['user_name'],nr_senha=nr_senha,servico=servico,data=str(datetime.date.today()))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['observacao'] = comentario
                self.put()
            return True
        except:
            return False


    #Faz o get das senhas em espera pelo atendedor xtpo na loja y (a filtragem e feita no proprio formulario devido a alguns factos...)
    def getClienteEspera(self):
        options = []
        self.where = "nome_atendedor = '{name}' and estado='espera_atendedor' ".format(name=bottle.request.session['user_name'])
        opts = self.get()
        for option in opts:
                options.append(option['servico']+str(option['nr_senha'])+';'+option['observacao']+';'+str(option['tempo_atendimento']))
        return options



    def getServicoAtendimento(self):
         try:
            self.where = "nome_atendedor = '{name}' and  estado='para_atendimento' and data='{data}'".format(name=bottle.request.session['user_name'],data=str(datetime.date.today()))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return self.kargs['servico']
            return None
         except:
            return None