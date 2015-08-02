# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"

#import os, sys
#sys.path.append(os.getcwd())
#import datetime, time
from utils import *#set_base_context, get_inputs, get_model_fields, parent2DB, data_to_csv
import bottle
#from orm import run_sql, get_identity
#from decimal import Decimal
#from erp_config import *

class model_action(object):
    """É chamada pelos objectos e define as acções que são comuns a todos os objectos como gravar, remover, etc"""
    def __init__(self, obj):#, key=None, internal=False
        #Aqui o que estiver em context é relativo ao formulario principal mas o model, name, title e model_name é sempre relativamente ao modelo que foi chamado que pode ser um child
        #print('oi estou no model_action')
        self.widgets = '/var/www/core/widgets/'
        import objs
        #import form
        #self.form = form
        self.objs = objs
        #print (1)
        self.window_id = bottle.request.forms.get('window_id')
        #print ('2 - o window_id e ', self.window_id)
        if self.window_id:
            self.ctx_dict = get_context(self.window_id)
        else:
            self.ctx_dict = {}
        #print (self.ctx_dict[obj.__name__])
        #print (3)
        #print('o window_id do model_action is {var1} and the self.ctx_dict is {var2}'.format(var1 = self.window_id, var2 = self.ctx_dict))
        #print('obj : {var1}'.format(var1=str(obj)))
        #print('teste ao request.get {var1}'.format(var1=bottle.request.forms.get('nome')))
        self.name = obj.__name__
        self.title = obj.__title__
        self.model_name = obj.__model_name__
        self.main_key = self.ctx_dict.get('main_key')
        #print('self.main_key {var1}'.format(var1 = str(self.main_key)))
        #self.parent_key = self.ctx_dict.get('parent_key')# os parent só são utilizados se um modelo abrir outro que é child, no caso dos modelos que ficam no mesmo form, como as list_field o parent_model é na verdade o self.ctx_dict['model_name'] na verdade acho que nesta nova vers~ao j´a nao uso os parent_key e model
        #self.parent_model = self.ctx_dict.get('parent_name')
        self.parent_model = self.ctx_dict.get('model_name')
        #self.page = self.ctx_dict.get('page')
        #self.limit = self.ctx_dict.get('limit')
        self.model = obj
        if hasattr(self.model, '__order_by__'):
            self.order_by = self.model.__order_by__
        else:
            self.order_by = ''
        #print ('fim do init')

    def get_option(self, key):
        """Esta opção devolve a resposta nos choice_field"""
        #print('{var1} Estou no get_option do choice e a minha key e {var2}'.format(var1 = self.name, var2 = str(key)))
        key = key.split('&')
        value = key[1]
        field_name = key[0]
        if value not in [None,'None']:
            #o pedido veio com valor que pode ser por exemplo o filtro
            if bottle.request.forms.getunicode(self.name):
                #já tenho um valor real no campo escondido que por isso vem no request
                #print('tenho no request {var1}'.format(var1 = self.name))
                result = eval("""self.objs.{model_name}(where = "id = '{value}'").get()""".format(model_name = self.model_name, value = bottle.request.forms.getunicode(self.name)))
                value = result[0][self.model.__get_options__]#[1]
            else:
                #Ainda não tenho valor real no campo escondido e por isso vou fazer um select na tabela avaliando o meu filtro
                #print('não tenho no request {var1}'.format(var1=self.name))
                #print('values {var1} and name is {var2}'.format(var1=str(value), var2=self.name))
                model_field = ''
                for opt in self.model.__get_options__:
                    model_field += opt + ','
                model_field = model_field[:-1]
                where = """to_tsvector('portuguese', ({field})) @@ to_tsquery('portuguese', '{value}') """.format(field = model_field, value = value.replace(' ','+'))
                result = eval('self.objs.{model_name}(where="{where}").get()'.format(model_name = self.model_name, where = where))
            #print('result is {var1} where is {var2}'.format(var1 = result, var2 = where))
            if len(result) == 1:
                #Se o resultado é igual a 1 significa que encontrei o que queria e devolvo o valor via json, devo então actualizar o valor real no campo escondido e o valor de exibição no campo visivel
                #print('o meu resultado e um vou devolver json')
                import json
                bottle.response.content_type = 'application/json'
                result = result[0]

                final_result = ''
                for opt in self.model.__get_options__:
                    final_result += result[opt] + ' '
                final_result =  final_result[:-1]
                result = ('string', json.dumps([final_result, result['id']]))#self.model.__get_options__
                #print(code)



            else:
                #O resultado não é 1 por isso terei que abrir o popup para filtrar melhor os resultados até encontrar o que quero, ai terei que atualizar o campo escondido e o visível carregando na imagem do certinho do registo escolhido.
                print('o resultado não e 1 value is {var1}'.format(var1 = str(value)))
                self.ctx_dict['popup_model_name'] = self.model_name
                self.ctx_dict['popup_name'] = self.name
                self.ctx_dict['popup_field_name'] = field_name
                self.ctx_dict['popup_title'] = self.title
                self.ctx_dict['window_status'] = 'popup'
                if self.name not in self.ctx_dict:
                    self.ctx_dict[self.name] = {}
                # povoa o dicionário da lista
                self.ctx_dict[self.name]['page'] = 0
                self.ctx_dict[self.name]['limit'] = 10
                self.ctx_dict[self.name]['cols'] = 12
                self.ctx_dict[self.name]['filter_expression'] = value
                set_context(self.window_id, self.ctx_dict)
                result = ('form', "form_list(window_id='{window_id}').show()".format(window_id = self.window_id))
        else:
            # o pedido veio sem valor o que significa que não pus nada no filtro, deverá então abrir o popup com todas as opções
            print('value is none')
            print(self.name)
            self.ctx_dict['popup_model_name'] = self.model_name
            self.ctx_dict['popup_name'] = self.name
            self.ctx_dict['popup_field_name'] = field_name
            self.ctx_dict['popup_title'] = self.title
            self.ctx_dict['window_status'] = 'popup'
            if self.name not in self.ctx_dict:
                self.ctx_dict[self.name] = {}
            # povoa o dicionário da lista
            #print('filter_expression', self.ctx_dict[self.name]['filter_expression'])
            self.ctx_dict[self.name]['page'] = 0
            self.ctx_dict[self.name]['limit'] = 10
            self.ctx_dict[self.name]['cols'] = 12
            set_context(self.window_id, self.ctx_dict)
            print('im calling the tham list on a popup', self.ctx_dict['window_status'], self.name)
            result = ('form', "form_list(window_id='{window_id}').show()".format(window_id = self.window_id))
        return result


    def Pagar(self, key):
        """Mostra o ecrã de pagamento"""
        try:
            from my_metodo_pagamento import MetodoPagamento
        except:
            from metodo_pagamento import MetodoPagamento
        total = self.model.get_total(key)
        metodos_pagamento = MetodoPagamento().get_options()
        metodos = []
        first = True
        for metodo in metodos_pagamento:
            value = ''
            if first == True:
                value = total
                first = False
            metodos.append((metodo[1], value))
        data = {'key':key, 'total':total, 'name':self.model.__name__, 'metodos':metodos}
        return ('string', bottle.SimpleTemplate(name='/var/www/core/forms/pagamento').render(data))

    def efectuar_pagamento(self, key):
        """Esta acção efectua o pagamento"""
        active = False
        record = get_model_record(model=self.model, key=key)
        record['estado'] = 'Pago'
        #Verifica se tem caixa aberta, se não tiver abre
        #Faz o pagamento em caixa
        from caixa import Caixa
        from linha_caixa import LinhaCaixa
        from terminal import Terminal
        terminal = Terminal(where = """name='MiniMercado'""").get()# substituir por get_terminal
        if len(terminal) > 0:
            terminal=terminal[0]['id']
        caixa = Caixa(where="estado = 'Aberta' AND terminal='{terminal}' AND data_inicial <= '{today}'".format(terminal=terminal, today=record['data'])).get()
        if not caixa:
            caixa = Caixa(data_inicial=record['data'], hora_inicial=time.strftime('%H:%M:%s'), valor_inicial=0, valor_final=0 , estado='Aberta', user=bottle.request.session.get('user', None), vendedor=bottle.request.session.get('user', None), terminal=terminal).put()
        else:
            caixa = caixa[0]['id']
        if record['factura']:
            active = True
        from metodo_pagamento import MetodoPagamento
        metodos_pagamento = MetodoPagamento().get_options()
        first = True
        total_entregue = to_decimal('0')
        for metodo in metodos_pagamento:
            if bottle.request.forms.get(metodo[1]):
                method = to_decimal(str(bottle.request.forms.get(metodo[1])))
            else:
                method = to_decimal('0')
            if method > to_decimal('0'):
                total_entregue += to_decimal(str(bottle.request.forms.get(metodo[1])))
        if total_entregue >= to_decimal(str(bottle.request.forms.get('total_a_pagar'))):
            for metodo in metodos_pagamento:
                if first == True:
                    default_metodo = metodo
                    first = False
                if bottle.request.forms.get(metodo[1]):
                    method = to_decimal(str(bottle.request.forms.get(metodo[1])))
                else:
                    method = to_decimal('0')
                if method > to_decimal('0'):
                    linha_caixa = LinhaCaixa(caixa=caixa, descricao='Nosso Talão', documento='talao', num_doc=record['numero'], valor_documento=to_decimal(str(bottle.request.forms.get('total_a_pagar'))), terceiro=record['cliente'], metodo=metodo[0], entrada=bottle.request.forms.get(metodo[1]), saida=0, active=active, user=bottle.request.session.get('user', None)).put()
            troco = total_entregue - to_decimal(str(bottle.request.forms.get('total_a_pagar')))
            if troco > to_decimal('0'):
                linha_caixa = LinhaCaixa(caixa=caixa, descricao='Nosso Talão', documento='talao', num_doc=record['numero'], valor_documento=to_decimal(str(bottle.request.forms.get('total_a_pagar'))), terceiro=record['cliente'], metodo=default_metodo[0], entrada=0, saida=troco, active=active, user=bottle.request.session.get('user', None)).put()
            else:
                troco = to_decimal('0')
            record['residual'] = to_decimal(str(bottle.request.forms.get('total_a_pagar'))) - total_entregue + troco
            #Faz o lançamento contabilistico se tiver factura como movimento activo, se não como movimento geral
            #Vê o metodo de pagamento e lança na conta adequada
            try:
                from my_diario import Diario
            except:
                from diario import Diario
            diario = Diario().get_diario(diario='stock')
            try:
                from my_periodo import Periodo
            except:
                from periodo import Periodo
            periodo = Periodo().get_periodo(data=self.kargs['data'])
            from movimento import Movimento
            from linha_movimento import LinhaMovimento
            movimento = Movimento(data=record['data'], numero=base_models.Sequence().get_sequence('movimento'), num_doc=record['numero'], descricao='Pagamento de Talão de Venda', diario=diario, documento='talao', periodo=periodo, estado='Rascunho', user=bottle.request.session.get('user', None), active=active).put()
            self.put()
            from terceiro import Terceiro
            conta_cliente = Terceiro().get(key=record['cliente'])[0]['a_receber']
            for metodo in metodos_pagamento:
                if bottle.request.forms.get(metodo[1]):
                    method = to_decimal(str(bottle.request.forms.get(metodo[1])))
                else:
                    method = to_decimal('0')
                if method > to_decimal('0'):
                    conta_pagamento = MetodoPagamento().get(key=metodo[0])[0]['conta']
                    LinhaMovimento(movimento=movimento, descricao='Pagamento de Talão de Venda', conta=conta_pagamento, quant_debito=to_decimal('0'), debito=to_decimal(str(bottle.request.forms.get(metodo[1]))), quant_credito=to_decimal('0'), credito=to_decimal('0'), user=bottle.request.session.get('user', None)).put()
                    LinhaMovimento(movimento=movimento, descricao='Pagamento de Talão de Venda', conta=conta_cliente, quant_debito=to_decimal('0'), debito=to_decimal('0'), quant_credito=to_decimal('0'), credito=to_decimal(str(bottle.request.forms.get(metodo[1]))), user=bottle.request.session.get('user', None)).put()
            self.ctx_dict['window_status'] = 'edit'
            response = ('form', "form_edit(key='None', window_id='{window_id}')".format(window_id=self.window_id))
        else:
            response = ('string', 'Segundo as Regras da Empresa não é possivel receber valores inferiores ao valor a Pagar, Torne a efectuar o pagamento por Favor!')#depois ver a possibilidade de ficar no mesmo sitio

    def form_list_action(self, key = None):
        """Serve para os list_forms"""
        #print ('a minha action e form_list_action')
        #print('oi estou no form_list_action! and my key is {var1}, model {var2}, name {var3}'.format(var1=str(key), var2=str(self.model), var3=self.name))
        return ('string', get_inputs(key = key, model = self.model, name = self.name, content_id = 'content'))

    def list_field_action(self, key = None):
        """Serve para os list_fields"""
        #print ('a minha action e list_field_action')
        return ('string', get_inputs(key = key, model = self.model, name = self.name, content_id = self.name))

    def form_list_onchange(self, option, key = None):#'form_list_onchange' in action
        """Serve para os list_forms na opção onchange"""
        #print('im on form_list_onchange')
        #print('esta e a minha option {var1}'.format(var1=option))
        onchange_field = option
        return ('string', get_inputs(key = key, model = self.model, name = self.name, content_id = 'content', onchange = onchange_field))

    def list_field_onchange(self, option, key=None):#'list_field_onchange' in action
        """Serve para os list_fields na opção onchange"""
        #print('esta e a minha option {var1}'.format(var1=option))
        onchange_field = option
        return ('string', get_inputs(key = key, model = self.model, name = self.name, content_id = self.name, onchange = onchange_field))

    def form_edit_popup(self, key = None):
        #print('a minha key é: {var1}, window_id {var2},window_status {var3}'.format(var1=str(key), var2=str(self.window_id), var3=self.ctx_dict['window_status']))
        self.ctx_dict['window_status'] = 'popup'
        self.ctx_dict['popup_main_key'] = key
        self.ctx_dict['popup_name'] = self.name
        self.ctx_dict['popup_model_name'] = self.model_name
        self.ctx_dict['popup_title'] = self.title
        #print('key is {var1}, name is {var2}, model_name is {var3}'.format(var1=str(key), var2=self.name, var3=self.model_name))

        #o choice estava com blue com o window_status = popup e o list_edit_mode = popup sei que nalguns casos o list_edit_mode nao pode transformar o window_status em popup

        #print('Im out of form_edit_popup')
        set_context(self.window_id, self.ctx_dict)
        return ('form', "form_edit(window_id = '{window_id}').show()".format(window_id = self.window_id))

    def form_edit_action(self, key = None):
        #print('Im in form_edit_action e a minha key é:{var1}, window_id {var2}, window_status {var3}'.format(var1 = str(key), var2 = str(self.window_id), var3 = self.ctx_dict['window_status']))
        #print (self.ctx_dict[self.name])
        #print("aqui no form")
        self.ctx_dict['window_status'] = 'edit'
        self.ctx_dict['main_key'] = key
        self.ctx_dict['name'] = self.name
        self.ctx_dict['model_name'] = self.model_name
        #print('key is {var1}, name {var2}, model_name {var3}'.format(var1=str(key), var2=self.name, var3=self.model_name))
        #print('Im out of form_edit_action')
        set_context(self.window_id, self.ctx_dict)
        return ('form', "form_edit(window_id = '{window_id}').show()".format(window_id = self.window_id))

    def form_edit_dyn_atrs(self, key = None, option = None):
        dyn_atrs_field = option
        self.ctx_dict['main_key'] = key
        self.ctx_dict['name'] = self.name
        self.ctx_dict['model_name'] = self.model_name
        self.ctx_dict['dynamic_atrs'] = dyn_atrs_field
        self.ctx_dict['window_status'] = 'edit'
        set_context(self.window_id, self.ctx_dict)
        return ('form', "form_edit(window_id='{window_id}').show()".format(window_id=self.window_id))

    def editNewWin(self, key=None):
        #print ('I got in the editNewWin!')
        new_ctx_dict = self.ctx_dict.copy()
        window_id = self.window_id#get_window_id()
        new_ctx_dict['window_id'] = window_id
        new_ctx_dict['cols'] = 12
        new_ctx_dict['main_key'] = key
        new_ctx_dict['name'] = self.name
        new_ctx_dict['model_name'] = self.model_name
        new_ctx_dict['title'] = self.title
        new_ctx_dict['window_status'] = 'edit'
        new_ctx_dict[self.name] = {}
        # povoa o dicionario da lista
        new_ctx_dict[self.name]['page'] = 0
        new_ctx_dict[self.name]['limit'] = 10
        new_ctx_dict[self.name]['title'] = self.title
        new_ctx_dict[self.name]['show_search'] = True
        set_context(window_id, new_ctx_dict)
        #print ('oi estou no fim do editNewWin', key, self.name, self.model_name, self.title, window_id)
        return ('form', "form_edit(window_id='{window_id}').show()".format(window_id=window_id))

    def remove(self, key = None):
        where = """id='{key}'""".format(key=key)
        result = eval('self.objs.{model_name}(where="{where}", user="{user}").delete()'.format(model_name=self.model_name, where=where, user=bottle.request.session['user']))
        #esta coisa aqui muda pois agora n~ao elimino s´o mudo de active=True para active=False
        if 'foreign key constraint failed' in str(result):
            return ('string', error_message('Não pode remover este registo, deve ter outros registos que dependem deste!'))
        else:
            return ('string', bottle.HTTPResponse(status=200, output='ok'))

    def save(self, key=None, internal=False):
        print('im in save do actions', key)
        if key == 'None':
            key = None
        if self.ctx_dict.get('internal_saved'):
            key = self.main_key
        #print(self.ctx_dict.get('window_status'), self.ctx_dict.get('internal_saved'), self.main_key)

        #print('vou gravar um: {var1},  e a minha key e {var2}  e o meu internal e {var3} a minha main_key {var4}  e o meu parent_model e {var5}'.format(var1=str(self.model), var2=str(key), var3=str(internal), var4=str(self.main_key), var5=str(self.parent_model)))
        #print(key, self.ctx_dict.get('internal_saved'))
        #print('save window_status {var1}'.format(var1 = self.ctx_dict['window_status']))
        #se gravei usando o internal a minha key vira como None mas a minha mainkey ter´a valor
        kargs = {}
        for field in get_model_fields(self.model):
            # vai correr por todos os campos definidos no modelo
            #print('field {var1} window_status {var2}'.format(var1=field[0], var2=self.ctx_dict['window_status']))
            request_value = bottle.request.forms.get(field[0])
            unicode_request_value = bottle.request.forms.getunicode(field[0])
            #print('request and unicode values are {var1} {var2}'.format(var1=str(request_value), var2=str(unicode_request_value)))
            if field[1].__class__.__name__ == 'date_field':
                try:
                    #tenta gravar no formato aceitavel pela base de dados
                    kargs[field[0]] = datetime.date.fromtimestamp(time.mktime(time.strptime(request_value, '%Y-%m-%d')))
                except:
                    #se n~ao estiver no formato certo desiste, depois ter´a que tentar converter para o formato certo antes de desistir.
                    pass
            elif field[1].__class__.__name__ == 'time_field':
                kargs[field[0]] = request_value
            elif field[1].__class__.__name__ == 'integer_field':
                #temos que garantir que o campo est´a preenchido
                if request_value:
                    kargs[field[0]] = int(request_value)
            elif field[1].__class__.__name__ == 'float_field':
                #temos que garantir que o campo est´a preenchido
                if request_value:
                    kargs[field[0]] = float(request_value)
            elif field[1].__class__.__name__ == 'boolean_field':
                #como s´o podemos ter True ou False se for None ´e considerado False
                if request_value == None:
                    kargs[field[0]] = False
                else:
                    kargs[field[0]] = True
            elif field[1].__class__.__name__ == 'password_field':
                #O Campo password tem que gravar encriptado claro que depois temos que reforçar a segurança desta jonsa
                import base64
                if request_value:
                    try:
                        if base64.decodestring(request_value.encode('utf8'))[0:6] != b'noops!':
                            kargs[field[0]] = base64.encodestring('noops!{name}'.format(name=request_value).encode('utf-8')).decode("utf-8")
                    except:
                        kargs[field[0]] = base64.encodestring('noops!{name}'.format(name=request_value).encode('utf-8')).decode("utf-8")
            elif field[1].__class__.__name__ == 'parent_field':
                #Se estou a gravar um edit_form ele não mexe com os list_field que eventualmente tenha, neste momento só posso gravar uma linha de um list_field com o botão de gravar do list_field, corrigir isso.
                #só tenho que gravar o parent_field que faz parte do modelo dos list_field????? o que queria eu dizer com isto?
                #print('o meu field_name que e parent e {var1}'.format(var1=field[0]))
                if self.ctx_dict.get('parent_name') not in [None, 'None'] and self.ctx_dict.get('parent_name') != self.ctx_dict.get('model_name'):
                    #o context so tem parent_name em casos como o contacto por exemplo
                    #o model_name do contexto é o nome do objecto actual
                    #isto significa que eu estou a gravar um objecto tipo o contacto que vem do terceiro, por isso tenho que gravar primeiro o terceiro e depois o contacto
                    #print('tenho parent na sessao {var1}'.format(var1=self.ctx_dict.get('parent_name')))
                    parent_name = self.ctx_dict.get('parent_name')
                    parent_key = self.ctx_dict.get('parent_key')
                else:
                    #este refere-se a todos os outros casos
                    #print('nao tenho parent na sessao, model_name {var1}, parent {var2}'.format(var1=field[1].model_name, var2=bottle.request.forms.get('parent_name')))
                    parent_name = field[1].model_name
                parent_model = eval('self.objs.{model_name}()'.format(model_name=parent_name))
                #print('parent_model {var1}'.format(var1=str(parent_model)))
                if request_value:
                    #tem lá o parent_field escondido e não é None
                    #Este é o caso em que os parent estao embutidos no meu objecto
                    #print('tem lá o parent_field escondido e não é None {var1}'.format(var1=str(request_value)))
                    value = request_value
                    options = parent_model.get_options()
                    #print('parent_model.get_options()')
                    kargs[field[0]] = parent2DB(value=value, options=options)
                    #print('kargs[field[0]], {var1}'.format(var1=str(kargs[field[0]])))
                else:
                    #Aqui vou procurar por um list_field no meu parent, se tiver um com o meu model name é esse o meu parceiro
                    if self.ctx_dict.get('parent_name') not in [None, 'None'] and self.ctx_dict.get('parent_name') != self.ctx_dict.get('model_name'):
                        #Venho de um modelo como o contacto com o terceiro ou seja um edit que vem de um list_field
                        if field[1].model_name == parent_name:
                            for parent_model_field in get_model_fields(parent_model):
                                if parent_model_field[1].__class__.__name__ == 'list_field' and parent_model_field[1].model_name == self.model_name:
                                    #print ('Temos um list_field correspondente a este parent_field e eu tenho um parent_name na sessao {var1}'.format(var1=parent_model.__name__))
                                    condition = parent_model_field[1].condition
                                    record = eval('self.objs.{model_name}()'.format(model_name=field[1].model_name)).get(key=parent_key)[0]
                                    #O valor do campo na BD será o id do parent, dai a parent_key
                                    kargs[field[0]] = parent_key
                    else:
                        #print('restantes casos')
                        #aqui temos uma possibilidade que é um edit poder vir de um list ou ser chamado directamente, se vem do list está no if e se chamo directamente vem aqui no else, heheheheh fudido né, lol
                        for parent_model_field in get_model_fields(parent_model):
                            if parent_model_field[1].__class__.__name__ == 'list_field' and parent_model_field[1].model_name == self.model_name:
                                #print('Temos um list_field correspondente a este parent_field {var1} , {var2}, {var3}, {var4}'.format(var1=parent_model.__name__, var2=self.ctx_dict.get('main_key'), var3=parent_model.__model_name__, var4=self.ctx_dict.get('model_name')))
                                parent_key = None
                                if self.ctx_dict.get('main_key') and self.ctx_dict.get('main_key') not in ['None', None]:
                                    parent_key = self.ctx_dict.get('main_key')
                                else:
                                    #gravar o registo ascendente, caso o parent_field corresponda ao parent de onde veio, em contrário deixa como está!
                                    #aqui não está bem, deverá ser na função que eu mando gravar o parent sempre que gravo o child a não ser que não tenha alterações no parent
                                    if parent_model.__model_name__ == self.ctx_dict.get('model_name'):
                                        m_action = model_action(obj=parent_model)
                                        parent_key = m_action.save(key=None, internal=True)
                                        #print('my parent_key depois de gravar o parent e', parent_key)
                                        self.ctx_dict['main_key'] = parent_key
                                        self.ctx_dict['internal_saved'] = True
                                        set_context(self.window_id, self.ctx_dict)
#                                   else:
#                                       parent_key = None
                                condition = parent_model_field[1].condition
                                record = eval('self.objs.{model_name}()'.format(model_name=field[1].model_name)).get(key=parent_key)
                                if len(record) > 0:
                                    record = record[0]
                                    #para que necessito do record?????
                                    #O valor do campo na BD será o id do parent, dai a parent_key
                                    kargs[field[0]] = parent_key
                                    #print('kargs[field[0]] {var1} = parent_key {var2}'.format(var1=str(kargs[field[0]]), var2=str(parent_key)))

            elif field[1].__class__.__name__ == 'info_field':
                if hasattr(self.model, '__workflow__') and self.model.__workflow__ != ():
                    if self.model.__workflow__[0] == field[0]:
                        if request_value:
                            kargs[field[0]] = unicode_request_value
                        else:
                            kargs[field[0]] = field[1].default
                    else:
                        kargs[field[0]] = unicode_request_value
            elif field[1].__class__.__name__ == 'list_field':
                #se for list_field deve gravar as linhas que eventualmente não estejam gravadas, ver como!!
                #talvez ver os field do modelo e verificar se tenho esses fields no request!!
                pass
            elif field[1].__class__.__name__ == 'many2many':
                #não tenho que fazer nada nunca pois o many2many grava sempre
                pass
            elif field[1].__class__.__name__ == 'function_field':
                #aqui poderá eventualmente ter que gravar se eu tiver a opção "save_on_db"
                pass
            elif field[1].__class__.__name__ in ['combo_field', 'choice_field']:
                #print('ok estou em combo ou choice no save {var1} {var2}'.format(var1=str(field[0]), var2=str(request_value)))
                if request_value:
                    value = request_value
                    #print('{var1} {var2}'.format(var1=str(self.model), var2=str(value)))
                    if isinstance(field[1].options, list):
                        options = field[1].options
                    else:
                        options = eval('self.' + field[1].options)
                    #print('{var1}'.format(var1=str(parent2DB(value=value, options=options))))
                    kargs[field[0]] = parent2DB(value=value, options=options)
                else:
                    #print('problema, pa!!!')
                    kargs[field[0]] = ''
            elif field[1].__class__.__name__ == 'image_field':
                kargs[field[0]] = request_value.replace('C:\\fakepath\\','')
            else:
                #Nos restantes tipos de field
                #print('estou no else {var1}, {var2}'.format(var1=field[0], var2=str(unicode_request_value)))
                kargs[field[0]] = unicode_request_value
        #print('depois de fields no save')
        if key:
            kargs['id'] = key
        kargs['user'] = bottle.request.session.get('user')
        #print('utils funcao save kargs')
        ##print('{var1}'.format(var1=str(kargs)))
        #print('{var1}'.format(var1=str(self.model)))
        self.model.kargs = kargs
        new_key = self.model.put()

        if internal:
            #print('sou internal')
            return new_key
        else:
            #print('Im not internal')
            if self.ctx_dict.get('window_status') == 'popup':
                #print('im saving the popup content')
                form = ('form', "form_edit(window_id='{window_id}').show()".format(window_id=self.window_id))
            elif self.ctx_dict.get('window_status') == 'edit':
                if self.ctx_dict['model_name'] != self.model_name:
                    #print('fui chamado do save sou um list_field e o meu nome e {var1} e o do ctx_dict {var2}'.format(var1=self.name, var2=self.ctx_dict['model_name']))
                    if 'selected_ids' in self.ctx_dict[self.name]:
                        del self.ctx_dict[self.name]['selected_ids']
                    #print(record)
                    #print(condition)
                    self.ctx_dict[self.name]['filter_expression'] = get_condition(condition=condition, record=record)
                    set_context(self.window_id, self.ctx_dict)
                    #print(self.ctx_dict[self.name])
                    list_data = prepare_list_data(model=self.model, ctx_dict=self.ctx_dict, list_name=self.name)
                    list_data['size'] = self.ctx_dict[self.name]['size']
                    list_data['cols'] = self.ctx_dict[self.name]['cols']
                    list_data['recalled'] = True
                    #print('after list_data')
                    form = ('string', bottle.SimpleTemplate(name=self.widgets + 'list_field').render(list_data))
                else:
                    #print('vou gravar o meu edit form ! estou num edit principal {var1}, {var2}'.format(var1=str(new_key), var2=self.name))
                    self.ctx_dict['main_key'] = new_key
                    self.ctx_dict['name'] = self.name
                    self.ctx_dict['model_name'] = self.model_name
                    self.ctx_dict['window_status'] = 'edit'
                    set_context(self.window_id, self.ctx_dict)
                    #print('my window_id is {var1}'.format(var1 = str(self.window_id)))
                    form = ('form', "form_edit(window_id='{window_id}').show()".format(window_id=self.window_id))
            elif self.ctx_dict.get('window_status') == 'list':
                #print('acabei de gravar a lista inline!!!')
                self.ctx_dict['window_status'] = 'list'
                set_context(self.window_id, self.ctx_dict)
                form = ('form', "form_list(window_id='{window_id}').show()".format(window_id=self.window_id))
            #print('Fim do save')
            return form

    def add_list(self, key=None):
        #ou ter que garantir que o registo parent esteja gravado
        #print('entrei no addlist')
        if key != 'None':
            parent_name = self.ctx_dict.get('model_name')
            parent_model = eval('self.objs.{model_name}()'.format(model_name=parent_name))
            #print('parent_model {var1}'.format(var1=str(parent_model)))
            for field in get_model_fields(parent_model):
                if hasattr(field[1], 'model_name') and field[1].model_name == self.model_name:
                    parent_field = field
                #fields[field[0]] = field[1].model_name.split('.')[0]
            #print('parent_field {var1}'.format(var1=str(parent_field)))
            #print('self.model {var1}'.format(var1=str(self.model)))
            for item in bottle.request.forms.items():
                #print('{var1}'.format(var1=item))
                if item[0] == parent_field[0]:
                    value = item[1]
            #if self.main_key not in [None, 'None']:
                #print('tenho main_key')
            #   main_key = self.main_key
            #else:
                #print('nao tenho main_key')
            m_action = model_action(obj=parent_model)
            main_key = m_action.save(key=self.main_key, internal=True)
            #print('a main_key e: {var1}'.format(var1=str(main_key)))
            self.model.kargs[parent_name.split('.')[0]] = key
            self.model.kargs['id'] = value
            self.model.kargs['user'] = bottle.request.session.get('user', None)
            #print('{var1}'.format(var1=str(self.model.kargs)))
            self.model.put()
            #bottle.SimpleTemplate.defaults['main_key'] = main_key
            self.ctx_dict['window_status'] = 'edit'
            #print('cheguei ao fim do add_list')
            set_context(self.window_id, self.ctx_dict)
            return ('form', "form_edit(window_id='{window_id}').show()".format(window_id=self.window_id)) #aqui estava key=key
        #else:
        #   print('porra nao tenho kei no addlist')

    def del_list(self, key=None):
        if key != 'None':
            #print('estou no del_list')
            parent_name = self.ctx_dict.get('name')
            parent_model = eval('self.objs.{model_name}()'.format(model_name=parent_name))
            m_action = model_action(obj=parent_model)
            main_key = m_action.save(key=self.main_key, internal=True)
            #print('{var1}'.format(var1=parent_name))
            self.model.kargs[parent_name] = 'Null'
            #print('{var1}'.format(var1=str(bottle.request.forms.getall('key'))))
            #print('esta e a minha key {var1}'.format(var1=str(key)))
            parent_key = str(key).split('&')[0]
            key = key.split('&')[1]
            self.model.kargs['id'] = key
            self.model.kargs['user'] = bottle.request.session.get('user', None)
            #print('este e o kargs do del_list {var1}'.format(var1=str(self.model.kargs)))
            self.model.put()
            #bottle.SimpleTemplate.defaults['name'] = parent_name
            #bottle.SimpleTemplate.defaults['model_name'] = parent_name
            self.ctx_dict['window_status'] = 'edit'
            #key=parent_key
            set_context(self.window_id, self.ctx_dict)
            return ('form', "form_edit(window_id='{window_id}').show()".format(window_id=self.window_id))

    def add_m2m(self, key=None):
        """Adiciona registo no Many2Many"""
        #tenho que garantir que o parent está gravado, ver se tem main_key não serve pois posso apenas estar a modifica-lo e dessa forma ele já tem key mas os campos podem ter sido modificados, a unica solução parece-me gravar outra vez ou em alternativa guardar a chave hash no registo e assim comparar se necessita realmente de gravar
        #print('estou no add_m2m')
        parent_model_name = self.ctx_dict.get('model_name')
        parent_name = self.ctx_dict.get('name')
        #print('my main key é :', self.ctx_dict.get('main_key'), self.main_key)
        #print('addm2m main key {var1} , model_name {var2} e parent_name {var3}'.format(var1=str(self.main_key), var2=self.model_name, var3=parent_model_name))
        #print('estou no add_m2m {var1} {var2}'.format(var1=str(self), var2=str(key)))
        #print('template defaults {var1}'.format(var1=str(bottle.SimpleTemplate.defaults)))
        #print('parent_name {var1} e depois self.name {var2}'.format(var1=parent_name, var2=self.name))
        #print('add_m2m parent_name {var1}'.format(var1=parent_name))
        for item in bottle.request.forms.items():
            #print('item do request {var1} e depois self.name {var2}'.format(var1=item, var2=self.name))
            if self.name in item[0]:
                value = item[1]
                key = item[1]
        print('depois de request')
        for f in get_model_fields(self.model):
            print(f)
            #esta abordagem obriga a que o nome do campo seja igual ao da tabela, mudar depois
            if hasattr(f[1], 'model_name'):
                print('o meu model_name é', f[1].model_name)
            else:
                print('não tenho model_name')
            if hasattr(f[1], 'model_name') and f[1].model_name == parent_model_name:
                #print('tenho model_name')
                parent_model = eval('self.objs.' + f[1].model_name + '()')
                condition = f[1].condition
                #print('condition {var1}'.format(var1=condition))
        print('parent_model_name ', parent_model_name)
        print('parent_model ', parent_model)
        if value:
            options = self.model.get_options()
            for option in options:
                if option[0] == value:
                    value = option[1]
            kargs = {}
            kargs[self.name] = key
            #if self.main_key not in [None, 'None']:
            #   print('tenho main_key')
            #   main_key = self.main_key
            #else:
            #   print ('nao tenho main_key')
            #print(type(self.main_key), self.main_key)
            print('parent_model', parent_model)
            m_action = model_action(obj=parent_model)
            main_key = m_action.save(key=self.main_key, internal=True)
            print('a main_key e: {var1}'.format(var1=str(main_key)))
            kargs[parent_name] = main_key

            kargs['parent_name'] = parent_name
            kargs['user'] = bottle.request.session.get('user', None)
            #print(kargs)
            eval("""self.objs.{model_name}(**kargs).put_m2m()""".format(model_name = self.model_name))
            #rows = self.model.get(order_by = self.order_by)#limit=20, offset=0,
            #data = rows[1]
            #bottle.SimpleTemplate.defaults['main_key'] = main_key
            #bottle.SimpleTemplate.defaults['name'] = parent_model.__name__
            #bottle.SimpleTemplate.defaults['model_name'] = parent_model.__model_name__
            print('Fim')
            self.ctx_dict['window_status'] = 'edit'
            self.ctx_dict['main_key'] = main_key
            set_context(self.window_id, self.ctx_dict)
            return ('form', "form_edit(window_id='{window_id}').show()".format(window_id = self.window_id))
        else:
            return ('string', '')

    def del_m2m(self, key=None):
        #print('estou em del_m2m')
        parent_name = self.ctx_dict.get('name')
        parent_model_name = self.ctx_dict.get('model_name')
        #print(parent_name + parent_model_name + self.name + self.model_name + str(key) + str(self.main_key))
        parent_model = eval('self.objs.' + parent_model_name + '()')
        m_action = model_action(obj=parent_model)
        main_key = m_action.save(key=self.main_key, internal=True)
        kargs = {}
        #estes name aqui deviam ser key e nao name!!!! e no addm2m a mesma coisa
        kargs[self.name] = key
        kargs[parent_name] = self.main_key
        kargs['parent_name'] = parent_name
        result = eval("""self.objs.{model_name}(**kargs).remove_m2m()""".format(model_name = self.model_name))
        #print('fim de del_m2m')
        if 'failed' in str(result):
            return ('string', error_message('Erro ao remover!'))
        else:
            return ('string', bottle.HTTPResponse(status = 200, output = 'ok'))

    def get_page(self, key = None):
        #print('estou no get_page {var1}'.format(var1=str(key)))
        page_string = key.split('&')
        #print('{var1}'.format(var1=page_string))
        page = int(page_string[0])#onde key foi a pagina selecionada
        #aqui temos que ver como tratar a quest~ao de ser popup ou n~ao
        #if page_string[1] == 'popup_content':
        #   popup = True
            #my_context = self.popup_context
        #else:
        #   popup = False
            #my_context = self.context
        #print('popup {var1}'.format(var1=str(popup)))
        #limit = self.ctx_dict.get('limit')
        #if not limit:
        #   limit = 20
        #filters = {}
        #for field in get_model_fields(self.model):
        #   if bottle.request.forms.get('search_{field}'.format(field=field[0])):
        #       filters[field[0]] = bottle.request.forms.get('search_{field}'.format(field=field[0]))
        #self.ctx_dict['limit'] = limit
        self.ctx_dict[self.name]['page'] = page
        #print ('im on get_page', self.name, page)
        #self.ctx_dict['window_status'] = 'list'
        set_context(self.window_id, self.ctx_dict)
        #aqui estamos a assumir que s´o vou usar paginacao nos formlist alias todo a plataforma roda a volta disso
        return ('form', "form_list(window_id = '{window_id}').show()".format(window_id = self.window_id))

    def change_limit(self, key = None):
        #print('oi estou no change_limit {var1}'.format(var1=str(key)))
        #popup = bottle.request.session.get('popup', False)
        #aqui temos que ver como tratar a questao de ser popup ou nao
        limit = bottle.request.forms.get('limit_chooser')
        #print('{var1}'.format(var1=str(limit)))
        self.ctx_dict[self.name]['limit'] = limit
        self.ctx_dict[self.name]['page'] = 0
        set_context(self.window_id, self.ctx_dict)
        return ('form', "form_list(window_id='{window_id}').show()".format(window_id = self.window_id))

    def filter(self, key = None):
        """Esta acção filtra dados através do campo search_nome da lista"""
        #print('inicio do filter')
        #print(self.ctx_dict.get('model_name'), self.model_name, str(key))

        if self.ctx_dict.get('model_name') != self.model_name and self.ctx_dict[self.name].get('window_status') != 'popup':
            #print('estou no filter e sou um list_field ou um popup')
            del self.ctx_dict[self.name]['selected_ids']
            list_data = prepare_list_data(model = self.model, ctx_dict = self.ctx_dict, list_name = self.name)
            list_data['size'] = self.ctx_dict[self.name]['size']
            list_data['cols'] = self.ctx_dict[self.name]['cols']
            list_data['recalled'] = True
            #print('after list_data')
            return ('string', bottle.SimpleTemplate(name = self.widgets + 'list_field').render(list_data))
        else:
            filter_expression = bottle.request.forms.getunicode('search_{name}'.format(name = self.name), None)
            if self.name in self.ctx_dict:
                if 'selected_ids' in self.ctx_dict[self.name]:
                    del self.ctx_dict[self.name]['selected_ids']
            #print('estou no filters e os meus filtros são {var1}'.format(var1=filter_expression))
            #como e um form list tenho a certeza que regista em self.name mas o list_fiedl regista no nome do campo para evitar conflitos
            self.ctx_dict[self.name]['filter_expression'] = filter_expression
            #print('out of filter', filter_expression)
            set_context(self.window_id, self.ctx_dict)
            return ('form', "form_list(window_id = '{window_id}').show()".format(window_id = self.window_id))

    def print_report(self, key = None):
        # imprime o relat´orio simples
        #print('im in simple report {var1}'.format(var1=str(bottle.request.forms.getall('key'))))
        ids = to_tuple(bottle.request.forms.getall('key'))
        #print('{var1}'.format(var1=str(ids)))
        where = "id " + ids
        #print('{var1}'.format(var1=where))
        #print('objs.{model_name}(where="{where}").get(order_by = {order_by})'.format(model_name=model_name, where=where, order_by = order_by))
        data = eval("""self.objs.{model_name}(where="{where}").get(order_by = "{order_by}")""".format(model_name = self.model_name, where = where, order_by = self.order_by))
        #print('{var1}'.format(var1=str(data)))
        return ('string', simple_report(data, self.model, self.title))

    def export(self, key = None):
        # por enquanto tive que por a export a totalidade dos registos depois só exportara os da listagem
#       ids = tuple(bottle.request.forms.getall('key'))
#       if len(ids) > 1:
#           where = "id in {ids}".format(ids=ids)
#       else:
#           where = "id = {ids}".format(ids=ids[0])
#       where = "id in {ids}".format(ids=ids)
        #print('before')
        data = eval("""self.objs.{model_name}().get(order_by = "{order_by}")""".format(model_name = self.model_name, order_by = self.order_by))
        #print('after')
        return ('string', data_to_csv(data, self.model))

    def import_csv(self, key = None):
        #Deve poder importar por nome de campo de bd e tambem por nome humano
        import csv
        fileContents = bottle.request.files.fileCSV
        fileContents = fileContents.file.read().decode('utf8')
        fileContents = fileContents.split('\n')
        fileReader = csv.DictReader(fileContents, delimiter = ';')
        #for row in csv_reader:
        #fileReader = strDictReader(fileContents, delimiter=';')
        #def strDictReader(utf8_data, **kwargs):
        #print('{var1}'.format(var1=str(row)))
        #yield dict([(key, value) for key, value in row.iteritems()])
        field_names = {}
        fields = {}
        for field in get_model_fields(self.model):
            field_names[field[0]] = field[1].name
            fields[field[0]] = field[1]
        records = []
        for row in fileReader:
            kargs = {}
            for f in row:
                for key, value in field_names.items():
                    if f.strip() in [key, value]:
                        #aqui só muda se o valor do campo não for nulo
                        if row[f] not in [None, '']:
                            #print('{var1}'.format(var1=str(row[f])))
                            if row[f][0] == '(':
                                row[f] = row[f].replace('(','').split(',')
                                #print('{var1}'.format(var1=str(type(row[f]))))
                                row[f] = row[f][0]
                            if fields[key].__class__.__name__ == 'parent_field':
                                kargs[key] = '9' + str(row[f])[1:]
                            elif fields[key].__class__.__name__ == 'combo_field' and hasattr('model', field[1]):
                                kargs[key] = '9' + str(row[f])[1:]#ver aqui se não tenho que considerar o choice_field
                        else:
                            kargs[key] = correct_value((key,fields[key]), row[f], self.model_name)
            if 'id' in row:
                #Se é um id que está a importar tem varias coisas a ser preservadas,
                #visto que temos que garantir que não entre em conflito com outros registos
                #para tal mudamos o primeiro digito para 9 ou seja mudamos o terminal,
                #esse é um numero reservado para estes efeitos, nenhum terminal começa por 9
                #temos também que mudar todos os que são parent bem como os combo com parent = True
                #isso pode-se ver algumas linhas acima
                kargs['id'] = '9' + str(row['id'])[1:]
            elif 'Id' in row:
                kargs['id'] = '9' + str(row['Id'])[1:]
            else:
                # não tem id por isso vamos gerar um
                kargs['id'] = get_identity(self.name, bottle.request.session.get('user', None))#
            kargs['user'] = bottle.request.session.get('user', None)
            records.append(kargs)
        eval('self.objs.{model_name}(records = {records}).put_many()'.format(model_name = self.model_name, records = records))
        self.ctx_dict['window_status'] = 'list'
        set_context(self.window_id, self.ctx_dict)
        return ('form', "form_list(window_id = '{window_id}').show()".format(window_id = self.window_id))
