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
__model_name__ = 'gap_senha.GAPSenha'
import auth, base_models
from orm import *
from form import *
try:
    from my_gap_servico import GAPServico
except:
    from gap_servico import GAPServico
try:
    from my_terminal  import Terminal
except:
    from terminal  import Terminal

class GAPSenha(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_senha'
        self.__title__ ='Senha' #Gestão de atendimento Presencial senha
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_senha.nr_senha'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.__get_options__ = ['nr_senha']
        self.servico = combo_field(view_order = 1, name  = 'Serviço', size = 50, args = 'required', model = 'gap_servico', search = False, column = 'letra', options = "model.get_opts('GAPServico().get_options()')")
        self.nr_senha = integer_field(view_order=2 , name='Nº Senha', size=30, onlist = True)
        self.data = date_field(view_order = 3, name = 'Data Inicial', size=40, args='readonly', default = datetime.date.today())
        self.hora_ped = time_field(view_order=4, name ='Hora Pedido', size=40, onlist=True, args='readonly', default=time.strftime('%H:%M:%S'))
        self.est_atend = string_field(view_order=5 , name='Estimativa Atendimento', size=40)
        self.pess_fila = string_field(view_order=6, name='Nº Pessoas na Fila', size=40, args='readonly')
        self.estado = combo_field(view_order = 7, name = 'Estado', size = 50, default = 'Espera', options = [('espera','Espera'), ('espera_atendedor','Espera Atendedor'), ('atendido','Atendido'), ('desistiu','Desistiu'), ('transferido','Transferido'), ('para_atendimento','Para Atendimento')], onlist = True)
        self.terminal = many2many(view_order = 8, name = 'Loja', size = 50, fields=['nome'], model_name = 'terminal.Terminal', condition = "gap_senha='{id}'", onlist=False)
        self.opiniao = list_field(view_order=9, name ='Opinião', condition="senha='{id}'", model_name='gap_opiniao.GAPOpiniao', list_edit_mode = 'popup', onlist = False)


    #Apanha Senha Geral :)
    def get_self(self):
        return self.get_options()

    def get_opts(self, get_str):
        """
        Este get_opts em todos os modelos serve para alimentar os choice e combo deste modelo e não chama as funções
        get_options deste modelo quando chamadas a partir de um outro!
        """
        return eval(get_str)


    #Apanha Senhas Atendidas
    def get_atendido(self):
        #Essa funçao apanha todas as senhas atendidas
        def get_results():
            options = []
            opts = self.get(order_by='nr_senha')
            for option in opts:
                if option['estado'] == 'atendido':
                    options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_atendido', createfunc=get_results)

    #Apanha Senhas em Espera
    def get_espera(self):
        #Essa funçao apanha todas as senhas em espera
        def get_results():
            options = []
            opts = self.get(order_by='nr_senha')
            for option in opts:
                if option['estado'] == 'espera':
                    options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_espera', createfunc=get_results)

    #Apanha Senhas que desistiram
    def get_desistiu(self):
        #Essa funçao apanha todas as senhas que desistiram
        def get_results():
            options = []
            opts = self.get(order_by='nr_senha')
            for option in opts:
                if option['estado'] == 'desistiu':
                    options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_desistiu', createfunc=get_results)

    #Apanha Senhas Transferidas
    def get_transferidas(self):
        #Essa funçao apanha todas as senhas transferidas
        def get_results():
            options = []
            opts = self.get(order_by='nr_senha')
            for option in opts:
                if option['estado'] == 'transferido':
                    options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_transferido', createfunc=get_results)

    #Apanha Senhas para atendimento
    def get_para_atendimento(self):
        #Essa funçao apanha todas as senhas para atendimento
        def get_results():
            options = []
            opts = self.get(order_by='nr_senha')
            for option in opts:
                if option['estado'] == 'para_atendimento':
                     options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_para_atendimento', createfunc=get_results)


    #Apanha Senha por Data
    def get_senha_data(self, data=''):
        #Essa funçao apanha todas as senhas em uma determinada data
        def get_results():
            options = []
            opts = self.get(order_by='nr_senha')
            for option in opts:
                if option['data'] == data:
                        options.append((str(option['id']), option['estado'] + ' - ' + option['nr_senha']))
            return options
        return erp_cache.get(key=self.__model_name__ + '_senha_data', createfunc=get_results)


     #Imprimir Senha
    def Imprimir_Senha(self, key, window_id):
            #E necessario ainda criar template senha para a impressao
            #Essa funçao serve para imprimir uma senha ainda imcompleta
            template = 'senha'
            record = get_records_to_print(key=key, model=self)
            return Report(record=record, report_template=template).show()


    #Mudar Estado Senha para Espera
    def  Espera(self, id):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'espera'
                self.put()
            return True
         except:
            return False

     #Mudar Estado Senha para Atendido
    def  Atendido(self, id):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'atendido'
                self.put()
            return True
         except:
            return False

    #Mudar Estado Senha para Desistido
    def  Desistiu(self, id):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'desistiu'
                self.put()
            return True
         except:
            return False

    #Mudar Estado Senha para Transferido
    def  Transferido(self, id,keyservico):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get()
            if self.kargs:
                from gap_servico import GAPServico
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'transferido'
                self.kargs['servico'] = GAPServico().get_letra_servico(keyservico=keyservico)
                self.put()
            return True
         except:
            return False

    #Mudar Estado Senha para atendimento
    def  Para_Atendimento(self, id):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'para_atendimento'
                self.put()
            return True
         except:
            return False

    #Mudar Estado Senha para espera por atendedor
    def  Espera_Atendedor(self, id):
         try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['user'] = bottle.request.session['user']
                self.kargs['estado'] = 'espera_atendedor'
                self.put()
            return True
         except:
            return False


    #get Estimativa atendimento
    def get_estimativa(self):
        #apanha a estimativa de atendimento para uma determinada senha
        return 1

    #get Numero de senha
    def get_numero_senha(self, loja=''):
        #apanha o numero de senha
        try:
            from my_gap_sequencia import GAPSequencia
        except:
            from gap_sequencia import GAPSequencia
        return GAPSequencia().get_sequence(loja=loja)


    #get Numero de pessoas na fila
    def get_pessoas_fila(self):
        #Essa funçao retorna o numero de pessoas em fila
        options = []
        opts = self.get(order_by='nr_senha')
        count = 0
        for option in opts:
                if (option['estado'] == 'espera'):
                        count += 1
        return count

    #Apanhar a proxima senha em espera ou transferido ordenando pela ordem
    def get_proximo(self):
        try:
            options = []
            opts = self.get(order_by='nr_senha')
            data_hoje = datetime.date.today()
            for f in get_model_fields(self):
                if f[0] == 'servico':
                    field=f
            for option in opts:
                    data_senha = str(option['data']).split("-")
                    if (option['estado'] == 'espera') or (option['estado'] == 'transferido'):
                            if (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2]))==data_hoje):
                                    letraservico = get_field_value(record=option, field=field, model=self)['field_value'][1]
                                    res = str(option['id'])+";"+str(letraservico)+option['nr_senha']
                                    return  res
            return None
        except:
            return None



    #Atraves de uma letra e um numero de senha retorna a respectivo senha com o ID
    def get_senha(self,senha):
        try:
            opts = self.get(order_by='nr_senha')
            letrasenha = senha[:1]
            numerosenha = senha[1:]
            data_hoje = datetime.date.today()
            for f in get_model_fields(self):
                if f[0] == 'servico':
                    field=f
            for option in opts:
                    data_senha = str(option['data']).split("-")
                    if(int(option['nr_senha'])==int(numerosenha)) and (datetime.date(int(data_senha[0]),int(data_senha[1]), int(data_senha[2])) == data_hoje):
                            if (option['estado'] == 'espera') or (option['estado'] == 'transferido')  or (option['estado'] == 'espera_atendedor'):
                                    letraservico = get_field_value(record=option, field=field, model=self)['field_value'][1]
                                    if(letrasenha==letraservico):
                                            res = str(option['id'])+";"+str(letraservico)+option['nr_senha']
                                            return  res
            return None
        except:
            #Em caso o inviduo insirir uma senha a brincar logo invalida :)
            return None


    #get senha com mais informaçoes
    def get_senhaInfo(self,id):
        try:
            self.where = "id = '{id}'".format(id=str(id))
            self.kargs = self.get()
            if self.kargs:
                self.kargs = self.kargs[0]
                return str(self.kargs['id'])+";"+str(self.kargs['nr_senha'])+";"+str(self.kargs['hora_ped'])+";"+str(self.kargs['data'])+";"+str(self.kargs['estado'])
            return None
        except:
            return None

    #Retornar ecran de atendimento
    def get_ecran_atendimento(self, window_id):
        return form_gap_atendedor(window_id=window_id).show()

    #essa funçao e chamada quando o cliente retira uma senha
    def get_SenhaCliente(self):
        return None
