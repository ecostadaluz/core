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
__model_name__ = 'gap_sequencia.GAPSequencia'
import auth, base_models
from orm import *
from form import *
try:
    from my_terminal  import Terminal
except:
    from terminal  import Terminal
try:
    from my_gap_senha import GAPSenha
except:
    from gap_senha import GAPSenha

class GAPSequencia(Model, View):
    def __init__(self, **kargs):
        Model.__init__(self, **kargs)
        self.__name__ = 'gap_sequencia'
        self.__title__ ='Sequência de Senha' #Gestão de sequencia de senha
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__order_by__ = 'gap_sequencia.num_senha'
        self.__auth__ = {
            'read':['All'],
            'write':['Atendedor'],
            'create':['Gestor de Loja'],
            'delete':['Gestor de Atendimento'],
            'full_access':['Gestor de Atendimento']
            }
        self.__get_options__ = ['nome']
        self.num_senha = integer_field(view_order = 1, name = 'Número', args = 'required', size = 20)
        self.data = date_field(view_order = 2, name = 'Data', size=50, args = 'required', default = datetime.date.today())
        self.loja = info_field(view_order=3 , name='Loja', size=40) #inserir a loja consuante o a loja que foi feito login readonly


    def get_sequence(self, loja):
        #Apanha o numero de senha incrimentando +1 do valor da senha anterior
        self.where = "loja = '{loja}' and active=True  ORDER BY num_senha Desc".format(loja=loja)
        self.kargs = self.get()
        if self.kargs:
                self.kargs = self.kargs[0]
                self.kargs['num_senha'] = self.kargs['num_senha'] + 1
                self.put()
                return self.kargs['num_senha']
        else:
            #try a few more times,this it's a temporary turn around for the problem
            for z in range(10):
                self.kargs = self.get()
                if self.kargs:
                    self.kargs = self.kargs[0]
                    self.kargs['num_senha'] = self.kargs['num_senha'] + 1
                    self.kargs['user'] = bottle.request.session['user']
                    self.put()
                    return self.kargs['num_senha']
            self.kargs = {'loja':loja, 'number':1, 'user':bottle.request.session['user']}
            self.put()
            return self.kargs['num_senha']


    #Faz o reset dos numeros das senhas para uma loja xpto
    def reset_numero(self,loja=''):
        try:
            #Faz o reset do numero das senhas para uma loja xpto cujo a data em que foi retirada seja < que a data de hoje
            args = self.get(order_by='num_senha')
            data_hoje = datetime.date.today()
            for self.kargs in args:
                    data_fim = str(self.kargs['data']).split("-")
                    if (datetime.date(int(data_fim[0]),int(data_fim[1]), int(data_fim[2])) < data_hoje) and (self.kargs['loja'] == loja) and (self.kargs['active'] == True):
                            self.kargs['user'] = bottle.request.session['user']
                            self.kargs['where'] = "id='{id}'".format(id=self.kargs['id'])
                            self.delete()
            return True
        except:
            return False



    #Chamar Senha
    def chamar_senha(self,user_estado=None):
        #Apanha a proxima senha em espera na loja xpto
        senha = GAPSenha().get_proximo()
        if senha != None:
            from my_users import Users
            #Se o estado estiver em intervalo ou terminado e alterado e mudado para em serviço
            if (user_estado=='intervalo') or (user_estado=='terminado'):
                 Users().EmServico()

            #Muda o seu estado para_atendimento
            GAPSenha().Para_Atendimento(id=self.get_id_senha(senha=senha))
            #addTimeAtendimento necessario para ajudar na gestao das estatisticas e relatorios
            self.addTimeAtendimento(senha=GAPSenha().get_senhaInfo(id=self.get_id_senha(senha=senha)), tempo_atendimento='00:00:00',comentario='Sem Comentario', servico=self.get_letra_senha(senha=senha))
            #retorna a respectiva senha
            return senha
        else:
            return None


    #Chamar Senha especifica
    def chamar_por_senha(self, senha=None,user_estado=None):
            print("aqui no chamar por senha")
            senha = GAPSenha().get_senha(senha=senha)
            if senha != None:
                from my_users import Users
                #Se o estado estiver em intervalo ou terminado e alterado e mudado para em serviço
                if (user_estado=='intervalo') or (user_estado=='terminado'):
                     Users().EmServico()

                #Muda o seu estado para_atendimento
                GAPSenha().Para_Atendimento(self.get_id_senha(senha=senha))
                #addTimeAtendimento necessario para ajudar na gestao das estatisticas e relatorios
                self.addTimeAtendimento(senha=GAPSenha().get_senhaInfo(id=self.get_id_senha(senha=senha)), tempo_atendimento='00:00:00',comentario='Sem Comentario',servico=self.get_letra_senha(senha=senha))
                #retorna a respectiva senha
                return senha
            else:
                return None


    #coloca a senha em espera pelo atendedor xpto
    def espera_atendedor(self,senha=None,tempo_atendimento=None,comentario=None):
        try:
            #change senha estado para espera pelo atendedor
            GAPSenha().Espera_Atendedor(id=self.get_id_senha(senha=senha))

            #questoes de alteraçoes para dados estatisticos
            from gap_timeAtendimento import  GAPTimeAtendimento
            GAPTimeAtendimento().setEstadoAtendimento(nr_senha=self.get_numero_senha(senha=senha),servico=self.get_letra_senha(senha=senha),estado="espera_atendedor")
            GAPTimeAtendimento().setTimeAtendimento(nr_senha=self.get_numero_senha(senha=senha),servico=self.get_letra_senha(senha=senha),tempo_atendimento=tempo_atendimento)
            GAPTimeAtendimento().setObservacao(nr_senha=self.get_numero_senha(senha=senha),servico=self.get_letra_senha(senha=senha),comentario=comentario)
            return True
        except:
            return False

    #chamar pela senha em espera do utilizador xpto
    def chamar_senhaEspera(self,senha=None,user_estado=None):
            senha = GAPSenha().get_senha(senha=senha)
            if senha != None:
                from my_users import Users
                #Se o estado estiver em intervalo ou terminado e alterado e mudado para em serviço
                if (user_estado=='intervalo') or (user_estado=='terminado'):
                     Users().EmServico()

                #Muda o seu estado para_atendimento
                GAPSenha().Para_Atendimento(self.get_id_senha(senha=senha))
                #mudar o estado da senha em espera pelo atendedor presenta na lista de estatistica
                from gap_timeAtendimento import GAPTimeAtendimento
                GAPTimeAtendimento().setEstadoAtendimento(nr_senha=self.get_numero_senha(senha=senha),servico=self.get_letra_senha(senha=senha),estado="para_atendimento")
                #retorna a respectiva senha
                return senha
            else:
                return None


    #Rechamar Senha
    def rechamar_senha(self, senha=None):
         GAPSenha().Para_Atendimento(id=self.get_id_senha(senha=senha))
         return senha


    #Transferir Senha
    def transferir_senha(self, senha=None, keyservico=None):
        GAPSenha().Transferido(id=self.get_id_senha(senha=senha),keyservico=keyservico)
        from gap_timeAtendimento import GAPTimeAtendimento
        GAPTimeAtendimento().setEstadoAtendimento(nr_senha=self.get_numero_senha(senha=senha),servico=self.get_letra_senha(senha=senha),estado="transferido")
        return senha


    #Terminar Senha
    def terminar_senha(self, senha=None,tempo_atendimento=None):
        #Muda o estado para atendido
        GAPSenha().Atendido(id=self.get_id_senha(senha=senha))
        from gap_timeAtendimento import GAPTimeAtendimento
        #Altera o estado do individuo para atendido na lista necessario para estatistica
        GAPTimeAtendimento().setEstadoAtendimento(nr_senha=self.get_numero_senha(senha=senha),servico=self.get_letra_senha(senha=senha),estado="atendido")
        #Altera o seu tempo de atendimento
        GAPTimeAtendimento().setTimeAtendimento(nr_senha=self.get_numero_senha(senha=senha),servico=self.get_letra_senha(senha=senha),tempo_atendimento=tempo_atendimento)
        return senha

    #Desistir Senha
    def desistir_senha(self, senha=None,tempo_atendimento=None):
        GAPSenha().Desistiu(id=self.get_id_senha(senha=senha))
        from gap_timeAtendimento import GAPTimeAtendimento
        #Altera o estado do individuo para desistiu na lista necessario para estatistica
        GAPTimeAtendimento().setEstadoAtendimento(nr_senha=self.get_numero_senha(senha=senha),servico=self.get_letra_senha(senha=senha),estado="desistiu")
        #Altera o seu tempo de atendimento
        GAPTimeAtendimento().setTimeAtendimento(nr_senha=self.get_numero_senha(senha=senha),servico=self.get_letra_senha(senha=senha),tempo_atendimento=tempo_atendimento)
        return senha


    #get id Senha clean retirando a letra e o numero do respectivo serviço associado
    def get_id_senha(self, senha=None):
        senha= senha.split(";")
        return  senha[0]

    #get a letra da senha clean
    def get_letra_senha(self, senha=None):
        senha= senha.split(";")
        return  senha[1][:1]

    #get a numero da senha clean
    def get_numero_senha(self, senha=None):
        senha= senha.split(";")
        return  senha[1][1:]

    #guarda o tempo de atendimento
    def saveTime(self,senha=None,tempo_atendimento=None):
        try:
            from gap_timeAtendimento import GAPTimeAtendimento
            senha = str(senha).split(' ')
            GAPTimeAtendimento().setTimeAtendimento(nr_senha=senha[1][1:],servico=senha[1][:1],tempo_atendimento=tempo_atendimento)
            return True
        except:
            return False


    #adiciona dados na tabela timeAtendimento para ajudar na qestao dos relatorios :)
    def addTimeAtendimento(self,senha=None,tempo_atendimento=None,comentario=None,servico=None):
        try:
            senha = senha.split(';')
            from gap_timeAtendimento import GAPTimeAtendimento
            content = {
            'user': '{user}'.format(user=bottle.request.session['user']),
            'nome_atendedor': '{name}'.format(name=bottle.request.session['user_name']),
            'nr_senha':senha[1],
            'servico':servico,
            'hora_entrada':senha[2],
            'data':senha[3],
            'tempo_atendimento':tempo_atendimento,
            'estado':senha[4],
            'observacao':comentario,
            'loja':'jungle', #assim que eu poder ter a loja por parte do atendedor colocar aqui
            }
            print("content-----------------------------------------------------------------------------------"+str(content))
            GAPTimeAtendimento(**content).put()
            return True
        except:
            return False