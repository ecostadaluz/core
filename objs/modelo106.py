# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
ERP+
"""
__author__ = 'António Anacleto'
__credits__ = []
__version__ = "1.0"
__maintainer__ = "António Anacleto"
__status__ = "Development"
__model_name__ = 'modelo106.Modelo106'
import auth, base_models
from orm import *
from form import *
from area_fiscal import AreaFiscal
import erp_config
from anexo_clientes import AnexoClientes
from linha_anexo_cliente import LinhaAnexoCliente
from anexo_fornecedor import AnexoFornecedor
from linha_anexo_fornecedor import LinhaAnexoFornecedor
from factura_cli import FacturaCliente
from factura_forn import FacturaFornecedor
from terceiro import Terceiro
from codigo_pais import CodigoPais
from linha_factura_cli import LinhaFacturaCliente
from linha_factura_forn import LinhaFacturaFornecedor

class Modelo106(Model, View):

    def __init__(self, **kargs):
        #depois por aqui entre datas e só de um diario ou periodo, etc, etc.
        Model.__init__(self, **kargs)
        self.__name__ = 'modelo106'
        self.__title__ = 'Modelo 106'
        self.__model_name__ = __model_name__
        self.__list_edit_mode__ = 'edit'
        self.__get_options__ = ['nome']

        self.__workflow__ = (
            'estado', {'Rascunho':['Confirmar'], 'Confirmado':['Gerar Mod106', 'Gerar Anexo Cliente', 'Gerar Anexo Fornecedor', 'Gerar Anexo Reg Cliente', 'Gerar Anexo Reg Fornecedor']}
            )

        self.__workflow_auth__ = {
            'Gerar Mod106':['All'],
            'Gerar Anexo Cliente':['All'],
            'Gerar Anexo Fornecedor':['All'],
            'Gerar Anexo Reg Cliente':['All'], 
            'Gerar Anexo Reg Fornecedor':['All'],
            'Confirmar':['All'],
            'full_access':['Gestor']
            }       

        self.__auth__ = {
            'read':['All'],
            'write':['All'],
            'create':['All'],
            'delete':['Gestor'],
            'full_access':['Gestor']
            }

        self.__tabs__ = [        
        ('Anexo Cliente', ['anexo_clientes']), 
        ('Anexo Fornecedor', ['anexo_fornecedor']),
        ('Anexo Reg. Cliente', ['anexo_reg_cliente']),
        ('Anexo Reg. Fornecedor', ['anexo_reg_fornecedor']),        
        ('Campos do Modelo',['cp01','cp02','cp03','cp04','cp05','cp06','cp07','cp08','cp09','cp10','cp11','cp12','cp13','cp14','cp15','cp16','cp17','cp18','cp19','cp20','cp21','cp22','cp23','cp24','cp25','cp26','cp27','cp28','cp29','cp30','cp31','cp32','cp33','cp34','cp35','cp36','cp37','cp38','cp39','cp40','cp41','cp42','cp43','cp44','cp45','cp46','cp47','cp48','cp49','cp50']),
        ]


        self.nome = string_field(view_order = 1, name = 'Nome', size = 80, default='modelo106_{data}'.format(data=datetime.date.today()))

       	self.tipo_declaracao = combo_field(view_order = 2, name = 'Tipo Declaração', size = 65, default = '1', options = [('1','Entrega no Prazo'), ('2','Entrega fora de Prazo'),('4', 'Substituição do modelo')], onlist = False)        
        
        self.nif=string_field(view_order=3, name='Nif', size=50, default=erp_config.nif)

        self.ano = combo_field(view_order = 4, name ='Ano', args = 'required', default = datetime.date.today().year, options='model.getAno()')

        self.mes = combo_field(view_order = 5, name ='Mês',args = 'required', default=datetime.date.today().strftime("%m"), options =[('01','Janeiro'),('02','Fevereiro'),('03','Março'),('04','Abril'),('05','Maio'),('06','Junho'),('07','Julho'),('08','Agosto'),('09','Setembro'),('10','Outubro'),('11','Novembro'),('12','Dezembro')])

        self.anexo_cli = combo_field(view_order = 6, name = 'Anexos Clientes',onlist=False, size=45,args='required',default='0',options=[('0','Sem Anexos'),('1','Com Anexos')])

        self.anexo_forn = combo_field(view_order = 7, name = 'Anexos Fornecedores',onlist=False, size=45,args='required',default='0',options=[('0','Sem Anexos'),('1','Com Anexos')])

        self.anexo_reg_cli = combo_field(view_order = 8, name = 'Anexos Regularização Cli',onlist=False,size=45,args='required',default='0',options=[('0','Sem Anexos Reg.'),('1','Com Anexos Reg.')])

        self.anexo_reg_forn = combo_field(view_order = 9, name = 'Anexos Regularização de Forn',onlist=False,size=70,args='required',default='0',options=[('0','Sem Anexos Reg.'),('1','Com Anexos Reg.')])

        self.area_fiscal = combo_field(view_order = 10, name = 'Área Fiscal', size = 50, model = 'area_fiscal',args = 'required', onlist = False, search = True, column = 'codigo', options = "model.get_opts('AreaFiscal().get_options_buyable()')")
        
        self.operacoes = combo_field(view_order = 11, name = 'Tipo de Operacoes', args='required', size = 73, default = '1', options = [('0','Activas e/ou Passivas'), ('1','Inexistência de operações'),('2', 'Unica Operação 1ª vez')], onlist = False)
        
        self.data_apresentacao = date_field(view_order=12, size=40, name ='Data de Apresentação', args='required ', default=datetime.date.today())

        self.local_apresentacao = combo_field(view_order = 13, name = 'Local de Apresentação', size = 70, model = 'area_fiscal', args = 'required', onlist = False, search = False, column = 'local', options = "model.get_opts('AreaFiscal().get_options()')")

        self.nif_tecnico = string_field(view_order = 14, name = 'Nif do Técnico O.C.', onlist=False,size = 50)
        
        self.num_reg_tec_ordem = string_field(view_order = 15, name = 'Nº Registo do Técnico',onlist=False, size = 50)

        self.data_recepcao = date_field(view_order=16, size=40, name ='Data de Recepção', default=datetime.date.today())

        self.observacoes = text_field(view_order=17, name='Observações', size = 80,onlist=False)
        
        self.cp01 = string_field(view_order= 18, name ='Campo 01', args='required',default='0', size=45,onlist=False,onchange="soma_campo32")
        self.cp02 = string_field(view_order= 19, name ='Campo 02', args='required', default='0',size=45,onlist=False,onchange="soma_campo34")
        self.cp03 = string_field(view_order= 20, name ='Campo 03', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp04 = string_field(view_order= 21, name ='Campo 04', args='required', default='0',size=45,onlist=False,onchange="soma_campo34")
        self.cp05 = string_field(view_order= 22, name ='Campo 05', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp06 = string_field(view_order= 23, name ='Campo 06', args='required', default='0',size=45,onlist=False,onchange="soma_campo34")
        self.cp07 = string_field(view_order= 24, name ='Campo 07', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp08 = string_field(view_order= 25, name ='Campo 08', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp09 = string_field(view_order= 26, name ='Campo 09', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp10 = string_field(view_order=27, name ='Campo 10', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp11 = string_field(view_order=28, name ='Campo 11', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp12 = string_field(view_order=29, name ='Campo 12', args='required', default='0',size=45,onlist=False,onchange="soma_campo33")
        self.cp13 = string_field(view_order=30, name ='Campo 13', args='required', default='0',size=45,onlist=False,onchange="soma_campo34")
        self.cp14 = string_field(view_order=31, name ='Campo 14', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp15 = string_field(view_order=32, name ='Campo 15', args='required', default='0',size=45,onlist=False,onchange="soma_campo33")
        self.cp16 = string_field(view_order=33, name ='Campo 16', args='required', default='0',size=45,onlist=False,onchange="soma_campo34")
        self.cp17 = string_field(view_order=34, name ='Campo 17', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp18 = string_field(view_order=35, name ='Campo 18', args='required', default='0',size=45,onlist=False,onchange="soma_campo33")
        self.cp19 = string_field(view_order=36, name ='Campo 19', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp20 = string_field(view_order=37, name ='Campo 20', args='required', default='0',size=45,onlist=False,onchange="soma_campo33")
        self.cp21 = string_field(view_order=38, name ='Campo 21', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp22 = string_field(view_order=39, name ='Campo 22', args='required', default='0',size=45,onlist=False,onchange="soma_campo33")
        self.cp23 = string_field(view_order=40, name ='Campo 23', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp24 = string_field(view_order=41, name ='Campo 24', args='required', default='0',size=45,onlist=False,onchange="soma_campo33")
        self.cp25 = string_field(view_order=42, name ='Campo 25', args='required', default='0',size=45,onlist=False,onchange="soma_campo32")
        self.cp26 = string_field(view_order=43, name ='Campo 26', args='required', default='0',size=45,onlist=False,onchange="soma_campo33")
        self.cp27 = string_field(view_order=44, name ='Campo 27', args='required', default='0',size=45,onlist=False,onchange="soma_campo33")
        self.cp28 = string_field(view_order=45, name ='Campo 28', args='required', default='0',size=45,onlist=False,onchange="soma_campo34")
        self.cp29 = string_field(view_order=46, name ='Campo 29', args='required', default='0',size=45,onlist=False,onchange="soma_campo33")
        self.cp30 = string_field(view_order=47, name ='Campo 30', args='required', default='0',size=45,onlist=False,onchange="soma_campo34")
        self.cp31 = string_field(view_order=48, name ='Campo 31', args='required', default='0',size=45,onlist=False)
        self.cp32 = string_field(view_order=49, name ='Campo 32', args='required', default='0',size=45,onlist=False)
        self.cp33 = string_field(view_order=50, name ='Campo 33', args='required', default='0',size=45,onlist=False)
        self.cp34 = string_field(view_order=51, name ='Campo 34', args='required', default='0',size=45,onlist=False)
        self.cp35 = string_field(view_order=52, name ='Campo 35', args='required', default='0',size=45,onlist=False)
        self.cp36 = string_field(view_order=53, name ='Campo 36', args='required', default='0',size=45,onlist=False)
        self.cp37 = string_field(view_order=54, name ='Campo 37', args='required', default='0',size=45,onlist=False)
        self.cp38 = string_field(view_order=55, name ='Campo 38', args='required', default='0',size=45,onlist=False)
        self.cp39 = string_field(view_order=56, name ='Campo 39', args='required', default='0',size=45,onlist=False)
        self.cp40 = string_field(view_order=57, name ='Campo 40', args='required', default='0',size=45,onlist=False)
        self.cp41 = string_field(view_order=58, name ='Campo 41', args='required', default='0',size=45,onlist=False)
        self.cp42 = string_field(view_order=59, name ='Campo 42', args='required', default='0',size=45,onlist=False)
        self.cp43 = string_field(view_order=60, name ='Campo 43', args='required', default='0',size=45,onlist=False)
        self.cp44 = string_field(view_order=61, name ='Campo 44', args='required', default='0',size=45,onlist=False)
        self.cp45 = string_field(view_order=62, name ='Campo 45', args='required', default='0',size=45,onlist=False)
        self.cp46 = string_field(view_order=63, name ='Campo 46', args='required', default='0',size=45,onlist=False)
        self.cp47 = string_field(view_order=64, name ='Campo 47', args='required', default='0',size=45,onlist=False)
        self.cp48 = string_field(view_order=65, name ='Campo 48', args='required', default='0',size=45,onlist=False)
        self.cp49 = string_field(view_order=66, name ='Campo 49', args='required', default='0',size=45,onlist=False)
        self.cp50 = string_field(view_order=67, name ='Campo 50', args='required', default='0',size=45,onlist=False)
        
        self.estado = info_field(view_order = 68, name ='Estado', hidden = True, default='Rascunho')

        self.anexo_clientes = list_field(view_order = 69, name= '', nolabel =True, args ='readonly', condition = "modelo106='{id}'", model_name = 'anexo_clientes.AnexoClientes', list_edit_mode = 'edit', onlist = False)        

        self.anexo_fornecedor = list_field(view_order = 70, name= '', nolabel =True, args ='readonly', condition = "modelo106='{id}'", model_name = 'anexo_fornecedor.AnexoFornecedor', list_edit_mode = 'edit', onlist = False)

        self.xml = text_field(view_order=71,name="XML", onlist=False)


    def get_opts(self, get_str):       
        return eval(get_str)


    def getAno(self):
        options = []
        opts = range(2014,2051)
        for option in opts:
            options.append((str(option), str(option)))
        return options


    """ Metodo para a confirmacao do anexo"""
    def Confirmar(self, key, window_id, internal = False):
        self.kargs = get_model_record(model = self, key = key, force_db = self.__force_db__)
        if self.kargs['estado'] == 'Rascunho' or self.kargs['estado'] == 'Confirmado':
            self.kargs['estado'] = 'Confirmado'
            self.put()
            ctx_dict = get_context(window_id)
            ctx_dict['main_key'] = self.kargs['id']
            set_context(window_id, ctx_dict)            
            result = form_edit(window_id = window_id).show()
        if not internal:
            return result

    def soma_campo32(self, record):
        result = record.copy()
        soma = (int(record['cp01'])+int(record['cp03'])+int(record['cp05'])+int(record['cp07'])+int(record['cp08'])+int(record['cp09'])+int(record['cp10'])+int(record['cp11'])
        +int(record['cp14'])+int(record['cp17'])+int(record['cp19'])+int(record['cp21'])+int(record['cp23'])+int(record['cp25']))
        result['cp32']=str(soma)
        return result

    def soma_campo33(self, record):
        result = record.copy()
        soma = (int(record['cp12'])+int(record['cp15'])+int(record['cp18'])+int(record['cp20'])
            +int(record['cp22'])+int(record['cp24'])+int(record['cp26'])+int(record['cp27'])+int(record['cp29']))
        result['cp33']=str(soma)
        return result

    def soma_campo34(self, record):
        result = record.copy()
        soma = (int(record['cp02'])+int(record['cp04'])+int(record['cp06'])+int(record['cp13'])
            +int(record['cp16'])+int(record['cp28'])+int(record['cp30']))
        result['cp34']=str(soma)
        return result

    #define a tipologia do anexo de regularizacao segundo o tipo de produto da linha de factura
    def getTipologia(self, tipo_produto):
        """
        retorna a tipologia da linha de anexo regularizacao baseado no tipo de produto
        """
        if tipo_produto in ('servico','','None',None):
            #servico
            return 'SRV'
        elif tipo_produto == 'consumivel':
            #outros bens de consumo
            return 'OBC'
        elif tipo_produto == 'imobilizado':
            #investimento
            return 'IMO'
        elif tipo_produto in ('armazenavel','produzido'):
            #inventario
            return 'INV'


    """ Metodo para gerar o arquivo xml do modelo 106 """
    def Gerar_Mod106(self, key, window_id):
        
        self.kargs = get_model_record(model=self, key=key)

        areaFiscal = AreaFiscal(where="id='{id}'".format(id=self.kargs['local_apresentacao'])).get()
        nome_local_apresentacao = areaFiscal[0]['local']
        ###################################
        import xml.dom.minidom
        doc = xml.dom.minidom.Document()
        tag_modelo106 = doc.createElement('modelo106')
        tag_tp_dec_anx = doc.createElement('tp_dec_anx')
        tag_nif = doc.createElement('nif')
        tag_periodo = doc.createElement('periodo')
        tag_cd_af = doc.createElement('cd_af')
        tag_exist_oper = doc.createElement('exist_oper')
        tag_dt_apresentacao = doc.createElement('dt_apresentacao')
        tag_loc_apresentacao = doc.createElement('loc_apresentacao')
        tag_nif_toc = doc.createElement('nif_toc')
        tag_num_ordem_toc = doc.createElement('num_ordem_toc')
        tag_dt_recepcao = doc.createElement('dt_recepcao')
        tag_obs = doc.createElement('obs')
        ####################################
        tag_tp_dec_anx.setAttribute('dec', self.kargs['tipo_declaracao'])
        tag_tp_dec_anx.setAttribute('cli', self.kargs['anexo_cli'])
        tag_tp_dec_anx.setAttribute('for', self.kargs['anexo_forn'])
        tag_tp_dec_anx.setAttribute('cli_reg', self.kargs['anexo_reg_cli'])
        tag_tp_dec_anx.setAttribute('for_reg', self.kargs['anexo_reg_forn'])
        tag_periodo.setAttribute('ano', self.kargs['ano'])
        tag_periodo.setAttribute('mes', self.kargs['mes'])
        ######################################
        # Cria a estrutura
        doc.appendChild(tag_modelo106)
        tag_modelo106.appendChild(tag_tp_dec_anx)
        tag_modelo106.appendChild(tag_nif)
        tag_modelo106.appendChild(tag_periodo)
        tag_modelo106.appendChild(tag_cd_af)
        tag_modelo106.appendChild(tag_exist_oper)
        ######################################        
        for x in range(1,51):
            if x<10:
                campo='cp0{num}'.format(num=x)
            else:
                campo='cp{num}'.format(num=x)
            tags = doc.createElement(campo)
            tag_modelo106.appendChild(tags)
            if self.kargs[campo] in ('','None',None,'0'):
                tags.appendChild(doc.createTextNode('0'))
            else:
                tags.appendChild(doc.createTextNode(self.kargs[campo]))
        #######################################        
        tag_modelo106.appendChild(tag_dt_apresentacao)
        tag_modelo106.appendChild(tag_loc_apresentacao)
        tag_modelo106.appendChild(tag_nif_toc)
        tag_modelo106.appendChild(tag_num_ordem_toc)
        tag_modelo106.appendChild(tag_dt_recepcao)
        tag_modelo106.appendChild(tag_obs)
        #######################################
        tag_nif.appendChild(doc.createTextNode(self.kargs['nif']))
        tag_cd_af.appendChild(doc.createTextNode(self.kargs['area_fiscal']))
        tag_exist_oper.appendChild(doc.createTextNode(self.kargs['operacoes']))
        tag_dt_apresentacao.appendChild(doc.createTextNode(self.kargs['data_apresentacao']))
        tag_loc_apresentacao.appendChild(doc.createTextNode(nome_local_apresentacao))
        tag_dt_recepcao.appendChild(doc.createTextNode(self.kargs['data_recepcao']))
        tag_nif_toc.appendChild(doc.createTextNode(self.kargs['nif_tecnico']))
        tag_num_ordem_toc.appendChild(doc.createTextNode(self.kargs['num_reg_tec_ordem']))
        tag_obs.appendChild(doc.createTextNode(self.kargs['observacoes']))
        ########################################
        conteudoXmlCriado= doc.toprettyxml()
        conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="utf-8"?>')
        self.kargs['xml']=conteudoFinalXml
        Modelo106(**self.kargs).put()
        return form_edit(window_id=window_id).show()





    """ Metodo para gerar o anexo cliente """
    def Gerar_Anexo_Cliente(self, key, window_id):
        informacoes = self.get_info_anexo_cli(key)
        if len(informacoes) > 0:
            self.guardar_anexo_cli(info_anexo=informacoes[0]['info_anexo'], info_linhas=informacoes[0]['info_linhas'])
        return form_edit(window_id=window_id).show()


    def guardar_anexo_cli(self, info_anexo, info_linhas):
        #GUARDANDO OS DADOS
        if len(info_linhas)!=0:
            conteudoFinalXml = self.gerar_XML_anexo_cli(info_anexo=info_anexo, info_linhas=info_linhas)            
            content ={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'ano': str(info_anexo['anx_cli_ano']),
                'mes': str(info_anexo['anx_cli_mes']),
                'area_fiscal': str(info_anexo['anx_cli_area_fiscal']),
                'nif_contribuinte': str(info_anexo['anx_cli_nif_contr']),
                'data_entrega': str(info_anexo['anx_cli_dt_entrega']),
                'modelo106':str(info_anexo['anx_cli_modelo106']),
                'nome':str(info_anexo['anx_cli_nome']),
                'estado':'Gerado',
                'total_factura':str(info_anexo['anx_cli_total_fact']),
                'total_base_incidencia':str(info_anexo['anx_cli_total_bs_incid']),
                'total_liquidado':str(info_anexo['anx_cli_total_liq']), 
                'xml_gerado':str(conteudoFinalXml)                                  
            }
            id_anxCli = AnexoClientes(**content).put()            
            #guardandos as linhas do anexo
            for line in info_linhas:
                content={
                    'user': '{user}'.format(user=bottle.request.session['user']),
                    'factura_cliente':str(line['ln_anx_factura_cliente']),
                    'designacao':str(line['ln_anx_cli_designacao']),
                    'nif_cliente':str(line['ln_anx_cli_nif']),
                    'origem':str(line['ln_anx_cli_origem']),
                    'serie':str(line['ln_anx_cli_serie']),
                    'tipo_doc':str(line['ln_anx_cli_tipoDoc']),
                    'numero_doc':str(line['ln_anx_cli_num_doc']),
                    'data':str(line['ln_anx_cli_data']),
                    'valor_factura':str(int(line['ln_anx_cli_vl_fatura'])),
                    'valor_base_incidencia':str(int(line['ln_anx_cli_Incidencia'])),
                    'taxa_iva':str(line['ln_anx_cli_taxa_iva']),
                    'iva_liquidado':str(int(line['ln_anx_cli_total_Iva'])),
                    'nao_liq_imposto':str(line['ln_anx_cli_nao_liq_imp']),
                    'linha_mod106':str(line['ln_anx_cli_linha_MOD106']),
                    'anexo_clientes':str(id_anxCli)                
                }
                LinhaAnexoCliente(**content).put()



    def gerar_XML_anexo_cli(self, info_anexo, info_linhas):      
        conteudoFinalXml=''
        if len(info_linhas)!=0:
            #CRIACAO DO MODELO XML        
            import xml.dom.minidom
            doc = xml.dom.minidom.Document()

            # Cria os elementos
            tag_anexo_cli = doc.createElement('anexo_cli')
            tag_header = doc.createElement('header')
            tag_linhas = doc.createElement('linhas')
            tag_dt_entrega = doc.createElement('dt_entrega')
            tag_total_fatura = doc.createElement('total_fatura')
            tag_total_base_incid = doc.createElement('total_base_incid')
            tag_total_liquidado = doc.createElement('total_liquidado')

            # Cria os atributos de header, os mesmos do modelo106
            # é necessario guardar as informacaoes            
            tag_header.setAttribute('ano', str(info_anexo['anx_cli_ano']))
            tag_header.setAttribute('mes', str(info_anexo['anx_cli_mes']))
            tag_header.setAttribute('cd_af', str(info_anexo['anx_cli_area_fiscal']))
            tag_header.setAttribute('nif', str(info_anexo['anx_cli_nif_contr']))

            # Cria a estrutura
            doc.appendChild(tag_anexo_cli)
            tag_anexo_cli.appendChild(tag_header)
            tag_anexo_cli.appendChild(tag_linhas)
            tag_anexo_cli.appendChild(tag_dt_entrega)
            tag_anexo_cli.appendChild(tag_total_fatura)
            tag_anexo_cli.appendChild(tag_total_base_incid)
            tag_anexo_cli.appendChild(tag_total_liquidado)

            #colocar os valores
            for line in info_linhas:
                #criar a tag linha
                tag_linha = doc.createElement('linha')
                #colocar os valor da linnha
                tag_linha.setAttribute('designacao',str(line['ln_anx_cli_designacao']))
                tag_linha.setAttribute('nif_cliente',str(line['ln_anx_cli_nif']))
                tag_linha.setAttribute('origem',str(line['ln_anx_cli_origem']))
                tag_linha.setAttribute('serie',str(line['ln_anx_cli_serie']))
                tag_linha.setAttribute('tipo_doc',str(line['ln_anx_cli_tipoDoc']))
                tag_linha.setAttribute('numero_doc',str(line['ln_anx_cli_num_doc']))
                tag_linha.setAttribute('data',str(line['ln_anx_cli_data']))
                tag_linha.setAttribute('valor_factura',str(int(line['ln_anx_cli_vl_fatura'])))
                tag_linha.setAttribute('valor_base_incidencia',str(int(line['ln_anx_cli_Incidencia'])))
                tag_linha.setAttribute('taxa_iva',str(line['ln_anx_cli_taxa_iva']))
                tag_linha.setAttribute('iva_liquidado',str(int(line['ln_anx_cli_total_Iva'])))
                tag_linha.setAttribute('nao_liq_imposto',str(line['ln_anx_cli_nao_liq_imp']))
                tag_linha.setAttribute('linha_mod106',str(line['ln_anx_cli_linha_MOD106']))

                #adicionar a tag linha na tag linhas
                tag_linhas.appendChild(tag_linha)

            tag_dt_entrega.appendChild(doc.createTextNode(str(info_anexo['anx_cli_dt_entrega'])))
            tag_total_fatura.appendChild(doc.createTextNode(str(info_anexo['anx_cli_total_fact'])))
            tag_total_base_incid.appendChild(doc.createTextNode(str(info_anexo['anx_cli_total_bs_incid'])))
            tag_total_liquidado.appendChild(doc.createTextNode(str(info_anexo['anx_cli_total_liq'])))
            # GERANDO O XML
            conteudoXmlCriado= doc.toprettyxml()        
            #colocar o encoding
            conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="utf-8"?>')           
        
        return conteudoFinalXml


   
    def get_info_anexo_cli(self, key):              
        self.kargs = get_model_record(model=self, key=key)        
        informacoes=[]
        #inicializar os totais
        
        anx_cli_total_fact =0
        anx_cli_total_bs_incid = 0
        anx_cli_total_liq = 0
        #array de linhas
        info_linhas =[]

        #buscar as facturas de cliente do periodo
        facturas_clientes = FacturaCliente(where = "estado='Confirmado' and to_char(data,'yyyy')='{ano}' and to_char(data,'mm')='{mes}'".format(ano=str(self.kargs['ano']), mes =str(self.kargs['mes']))).get()
        if len(facturas_clientes) > 0:                                
            for facturaCli in facturas_clientes:                
                terceiro = Terceiro(where="id = '{id}'".format(id=facturaCli['cliente'])).get()
                #criar os atributos das linhas
                ln_anx_cli_origem=terceiro[0]['origem']
                ln_anx_cli_designacao=terceiro[0]['nome']
                ln_anx_cli_nif = ""
                if terceiro[0]['nif'] not in ('', None,'None'):                        
                    ln_anx_cli_nif= terceiro[0]['nif']
                else:
                    ln_anx_cli_nif= '000000000'

                ln_anx_cli_serie = facturaCli['serie']
                ln_anx_cli_tipoDoc = 'FT'
                
                ######atributos por descutir sua situacao######
                ln_anx_cli_nao_liq_imp = ''
                ln_anx_cli_linha_MOD106 = '01'
                ###############################################                
                ln_anx_cli_num_doc = facturaCli['numero']
                ln_anx_cli_data = facturaCli['data']
                ln_anx_cli_vl_fatura = facturaCli['total']
                ln_anx_factura_cliente = facturaCli['id']

                #para cada factura buscar as taxas de iva existente nela
                sql="""select distinct produto.iva from produto where produto.id in (select linha_factura_cli.produto from linha_factura_cli
                where linha_factura_cli.factura_cli = '{idFactura}'                               
                and (linha_factura_cli.active=True OR linha_factura_cli.active is NULL))""".format(idFactura = facturaCli['id'])

                taxas = run_sql(sql)            
                for taxa in taxas:                                    
                    linhas_fact_cli = LinhaFacturaCliente(where="factura_cli='{factId}' AND iva ='{taxaIva}'".format(factId=facturaCli['id'], taxaIva=taxa['iva'])).get()                   
                    #calcular a nova base incidencia e novo total de iva
                    ln_anx_cli_Incidencia = FacturaCliente().get_total_incidencia_por_taxa(record_lines=linhas_fact_cli)                    
                    ln_anx_cli_total_Iva = FacturaCliente().get_total_iva_por_taxa(record_lines=linhas_fact_cli)

                    ###para cada linha do anexo, é necessario somar os totais ao totais no anexo
                    anx_cli_total_fact += int(facturaCli['total'])
                    anx_cli_total_liq += int(ln_anx_cli_total_Iva)
                    anx_cli_total_bs_incid += int(ln_anx_cli_Incidencia)             
                    ###############
                    ln_anx_cli_taxa_iva =""
                    if str(taxa['iva']) in ('None', None,'',0):
                        ln_anx_cli_taxa_iva=0
                    elif '.5' in str(taxa['iva']):
                        ln_anx_cli_taxa_iva= round(to_decimal(taxa['iva']),1)
                    else:
                        ln_anx_cli_taxa_iva = int(taxa['iva'])
                    #adicionar as informacoes das linhas
                    linha = {
                        'ln_anx_cli_Incidencia':ln_anx_cli_Incidencia,
                        'ln_anx_cli_nif':ln_anx_cli_nif,
                        'ln_anx_cli_data':ln_anx_cli_data,
                        'ln_anx_cli_serie':ln_anx_cli_serie,
                        'ln_anx_cli_tipoDoc':ln_anx_cli_tipoDoc,
                        'ln_anx_cli_designacao':ln_anx_cli_designacao,
                        'ln_anx_cli_origem':ln_anx_cli_origem,
                        'ln_anx_cli_taxa_iva':ln_anx_cli_taxa_iva,
                        'ln_anx_cli_total_Iva':ln_anx_cli_total_Iva,
                        'ln_anx_cli_vl_fatura':ln_anx_cli_vl_fatura,
                        'ln_anx_cli_num_doc':ln_anx_cli_num_doc,
                        'ln_anx_cli_linha_MOD106':ln_anx_cli_linha_MOD106,
                        'ln_anx_cli_nao_liq_imp':ln_anx_cli_nao_liq_imp,
                        'ln_anx_factura_cliente':ln_anx_factura_cliente
                    }
                    info_linhas.append(linha)
            #adiconar as info do anexo cliente
            info_anexo={
                'anx_cli_ano':self.kargs['ano'],
                'anx_cli_mes':self.kargs['mes'],
                'anx_cli_area_fiscal': self.kargs['area_fiscal'],
                'anx_cli_nif_contr': self.kargs['nif'],
                'anx_cli_dt_entrega':self.kargs['data_apresentacao'],
                'anx_cli_modelo106': key,
                'anx_cli_nome': 'Anexo clientes_{ano}-{mes}'.format(ano=self.kargs['ano'], mes=self.kargs['mes']),
                'anx_cli_estado': 'Gerado',
                'anx_cli_total_fact':anx_cli_total_fact,
                'anx_cli_total_bs_incid':anx_cli_total_bs_incid,
                'anx_cli_total_liq':anx_cli_total_liq
            }
            informacoes.append({'info_anexo':info_anexo, 'info_linhas':info_linhas})
        return informacoes           


        

    """Metodo para gerar o anexo fornecedor"""  
    def Gerar_Anexo_Fornecedor(self, key, window_id):
        informacoes = self.get_info_anexo_forn(key)
        if len(informacoes) > 0:
            self.guardar_anexo_forn(info_anexo=informacoes[0]['info_anexo'], info_linhas=informacoes[0]['info_linhas'])
        return form_edit(window_id=window_id).show()

    
    def get_info_anexo_forn(self, key):
        #array contendo toda a informacao do anexo fornecedor
        informacoes=[]         
        self.kargs = get_model_record(model=self, key=key)
        #criar os dicionarios de dados      
        anx_forn_total_fact = 0
        anx_forn_total_bs_incid = 0
        anx_forn_total_ded = 0
        anx_forn_total_sup = 0

        #array de linhas de anexo
        info_linhas = []
        #buscar as facturas de fornecedor do periodo
        facturas_fornecedores = FacturaFornecedor(where = "estado='Confirmado' and to_char(data,'yyyy')='{ano}' and to_char(data,'mm')='{mes}'".format(ano=str(self.kargs['ano']), mes =str(self.kargs['mes']))).get()
        if len(facturas_fornecedores) > 0:                                 
            for facturaForn in facturas_fornecedores:                
                terceiro = Terceiro(where="id = '{id}'".format(id=facturaForn['fornecedor'])).get()
                #criar os atributos das linhas
                ln_anx_forn_origem=terceiro[0]['origem']
                ln_anx_forn_designacao=terceiro[0]['nome']
                ln_anx_forn_nif= terceiro[0]['nif']                
                ln_anx_forn_tipoDoc = 'FT'                
                ###### atributos por descutir sua situacao ######                
                ln_anx_forn_linha_MOD106 = '23'                
                ###############################################                
                ln_anx_forn_num_doc = facturaForn['numero']
                ln_anx_forn_data = facturaForn['data']
                ln_anx_forn_vl_fatura = facturaForn['total']
                ln_anx_forn_factura = facturaForn['id']
                
                #para cada factura buscar as taxas de iva existente nela
                sql="""select distinct produto.iva, produto.deducao, produto.tipo from produto where produto.id in (select linha_factura_forn.produto from linha_factura_forn
                where linha_factura_forn.factura_forn = '{idFactura}'                              
                and (linha_factura_forn.active=True OR linha_factura_forn.active is NULL))""".format(idFactura = facturaForn['id'])
                
                taxas = run_sql(sql)        
                for taxa in taxas:
                    #colocar a tipologia
                    ln_anx_forn_tipologia = self.getTipologia(taxa['tipo'])
                    #buscar as linhas de factura_forn que contem a taxa de iva e de deducao                                                       
                    linhas_fact_forn = LinhaFacturaFornecedor(where="factura_forn='{factId}' AND iva ='{taxaIva}' AND direito_deducao = '{esteDeducao}'".format(factId=facturaForn['id'], taxaIva=taxa['iva'],esteDeducao=taxa['deducao'])).get()                   
                    
                    #calcular a nova base incidencia, novo total de iva suportado e novo total deducao
                    ln_anx_forn_Incidencia =FacturaFornecedor().get_total_incidencia_por_taxa(record_lines=linhas_fact_forn)
                    ln_anx_forn_total_sup = round(to_decimal(to_decimal(ln_anx_forn_Incidencia)*to_decimal(taxa['iva'])/100),0)               
                    ln_anx_forn_total_ded = FacturaFornecedor().get_total_dedutivel_por_taxa(record_lines=linhas_fact_forn)                  
                    
                    ###para cada linha do anexo, é necessario somar os totais ao totais no anexo
                    anx_forn_total_fact += int(facturaForn['total'])
                    anx_forn_total_sup += int(ln_anx_forn_total_sup)
                    anx_forn_total_bs_incid += int(ln_anx_forn_Incidencia)
                    anx_forn_total_ded += int(ln_anx_forn_total_ded)         
                    ###############

                    ln_anx_forn_taxa_iva =""
                    if str(taxa['iva']) in ('None', None,'',0):
                        ln_anx_forn_taxa_iva=0
                    elif '.5' in str(taxa['iva']):
                        ln_anx_forn_taxa_iva= round(to_decimal(taxa['iva']),1)
                    else:
                        ln_anx_forn_taxa_iva = int(taxa['iva'])
                    ln_anx_forn_direito_ded = str(taxa['deducao'])                    
                    
                    #adicionar as informacoes das linhas
                    linha = {
                        'ln_anx_forn_Incidencia':ln_anx_forn_Incidencia,
                        'ln_anx_forn_nif':ln_anx_forn_nif,
                        'ln_anx_forn_data':ln_anx_forn_data,                        
                        'ln_anx_forn_tipoDoc':ln_anx_forn_tipoDoc,
                        'ln_anx_forn_designacao':ln_anx_forn_designacao,
                        'ln_anx_forn_origem':ln_anx_forn_origem,
                        'ln_anx_forn_taxa_iva':ln_anx_forn_taxa_iva,
                        'ln_anx_forn_total_sup':ln_anx_forn_total_sup,
                        'ln_anx_forn_direito_ded':ln_anx_forn_direito_ded,
                        'ln_anx_forn_total_ded':ln_anx_forn_total_ded,
                        'ln_anx_forn_vl_fatura':ln_anx_forn_vl_fatura,
                        'ln_anx_forn_num_doc':ln_anx_forn_num_doc,
                        'ln_anx_forn_linha_MOD106':ln_anx_forn_linha_MOD106,
                        'ln_anx_forn_tipologia':ln_anx_forn_tipologia,
                        'ln_anx_forn_factura':ln_anx_forn_factura
                    }
                    info_linhas.append(linha)
            #adicionar as info do anexo
            info_anexo ={
                'anx_forn_ano': self.kargs['ano'],
                'anx_forn_mes': self.kargs['mes'],
                'anx_forn_area_fiscal': self.kargs['area_fiscal'],
                'anx_forn_nif_entidade': self.kargs['nif'],
                'anx_forn_dt_entrega': self.kargs['data_apresentacao'],
                'anx_forn_modelo106': key,
                'anx_forn_nome' :'Anexo fornecedor_{ano}-{mes}'.format(ano=self.kargs['ano'], mes=self.kargs['mes']),
                'anx_forn_estado':'Gerado',
                'anx_forn_total_fact' : anx_forn_total_fact,
                'anx_forn_total_bs_incid': anx_forn_total_bs_incid,
                'anx_forn_total_ded': anx_forn_total_ded,
                'anx_forn_total_sup': anx_forn_total_sup           
            }       
            informacoes.append({'info_anexo':info_anexo,'info_linhas':info_linhas}) 
           
        return informacoes



    def gerar_XML_anexo_forn(self, info_anexo, info_linhas):
        conteudoFinalXml=''         
        if len(info_linhas)!=0:         
            #CRIACAO DO MODELO XML        
            import xml.dom.minidom
            doc = xml.dom.minidom.Document()
            # Cria os elementos
            tag_anexo_for = doc.createElement('anexo_for')
            tag_header = doc.createElement('header')
            tag_linhas = doc.createElement('linhas')
            tag_dt_entrega = doc.createElement('dt_entrega')
            tag_total_fatura = doc.createElement('total_fatura')
            tag_total_base_incid = doc.createElement('total_base_incid')
            tag_total_suportado = doc.createElement('total_suportado')
            tag_total_dedutivel = doc.createElement('total_dedutivel')

            # Cria os atributos de header
            tag_header.setAttribute('ano', str(info_anexo['anx_forn_ano']))
            tag_header.setAttribute('mes', str(info_anexo['anx_forn_mes']))
            tag_header.setAttribute('cd_af', str(info_anexo['anx_forn_area_fiscal']))
            tag_header.setAttribute('nif', str(info_anexo['anx_forn_nif_entidade']))
            

            # Cria a estrutura
            doc.appendChild(tag_anexo_for)
            tag_anexo_for.appendChild(tag_header)
            tag_anexo_for.appendChild(tag_linhas)
            tag_anexo_for.appendChild(tag_dt_entrega)
            tag_anexo_for.appendChild(tag_total_fatura)
            tag_anexo_for.appendChild(tag_total_base_incid)
            tag_anexo_for.appendChild(tag_total_suportado)
            tag_anexo_for.appendChild(tag_total_dedutivel)

            #colocar os valores
            for line in info_linhas:
                #criar a tag linha
                tag_linha = doc.createElement('linha')
                #colocar os valor da linnha                               
                tag_linha.setAttribute('designacao',str(line['ln_anx_forn_designacao']))
                tag_linha.setAttribute('nif',str(line['ln_anx_forn_nif']))
                tag_linha.setAttribute('origem',str(line['ln_anx_forn_origem']))                
                tag_linha.setAttribute('tp_doc',str(line['ln_anx_forn_tipoDoc']))
                tag_linha.setAttribute('num_doc',str(line['ln_anx_forn_num_doc']))
                tag_linha.setAttribute('data',str(line['ln_anx_forn_data']))
                tag_linha.setAttribute('vl_fatura',str(int(line['ln_anx_forn_vl_fatura'])))
                tag_linha.setAttribute('vl_base_incid',str(int(line['ln_anx_forn_Incidencia'])))
                tag_linha.setAttribute('tx_iva',str(line['ln_anx_forn_taxa_iva']))
                tag_linha.setAttribute('iva_sup',str(int(line['ln_anx_forn_total_sup'])))
                tag_linha.setAttribute('direito_ded',str(line['ln_anx_forn_direito_ded']))         
                tag_linha.setAttribute('iva_ded',str(line['ln_anx_forn_total_ded']))
                tag_linha.setAttribute('tipologia',str(line['ln_anx_forn_tipologia']))
                tag_linha.setAttribute('linha_dest_mod',str(line['ln_anx_forn_linha_MOD106']))
                #adicionar a tag linha na tag linhas
                tag_linhas.appendChild(tag_linha)

            #adicionar os totais
            tag_dt_entrega.appendChild(doc.createTextNode(str(info_anexo['anx_forn_dt_entrega'])))
            tag_total_fatura.appendChild(doc.createTextNode(str(info_anexo['anx_forn_total_fact'])))
            tag_total_base_incid.appendChild(doc.createTextNode(str(info_anexo['anx_forn_total_bs_incid'])))
            tag_total_suportado.appendChild(doc.createTextNode(str(info_anexo['anx_forn_total_sup'])))
            tag_total_dedutivel.appendChild(doc.createTextNode(str(info_anexo['anx_forn_total_ded'])))
            
            # GERANDO O XML
            conteudoXmlCriado = doc.toprettyxml()        
            #colocar o encoding
            conteudoFinalXml=conteudoXmlCriado.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="utf-8"?>')       
           
        return conteudoFinalXml




    def guardar_anexo_forn(self, info_anexo, info_linhas):
        #gerar o xml
        conteudoFinalXml = self.gerar_XML_anexo_forn(info_anexo, info_linhas)
        #GUARDANDO OS DADOS
        content ={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'ano': str(info_anexo['anx_forn_ano']),
                'mes': str(info_anexo['anx_forn_mes']),
                'area_fiscal': str(info_anexo['anx_forn_area_fiscal']),
                'nif_entidade': str(info_anexo['anx_forn_nif_entidade']),
                'data_entrega': str(info_anexo['anx_forn_dt_entrega']),
                'modelo106':str(info_anexo['anx_forn_modelo106']),
                'nome':str(info_anexo['anx_forn_nome']),
                'estado':'Gerado',
                'total_factura':str(info_anexo['anx_forn_total_fact']),
                'total_base_incidencia':str(info_anexo['anx_forn_total_bs_incid']),
                'total_suportado':str(info_anexo['anx_forn_total_sup']),
                'total_dedutivel':str(info_anexo['anx_forn_total_ded']),
                'xml_gerado':str(conteudoFinalXml)                                      
        }           
        id_anxForn = AnexoFornecedor(**content).put()        
        #guardandos as linhas do anexo
        for line in info_linhas:
            content={
                'user': '{user}'.format(user=bottle.request.session['user']),
                'factura_fornecedor':str(line['ln_anx_forn_factura']),
                'anexo_fornecedor':str(id_anxForn),
                'designacao':str(line['ln_anx_forn_designacao']),
                'nif_fornecedor':str(line['ln_anx_forn_nif']),
                'origem':str(line['ln_anx_forn_origem']),
                'tipologia':str(line['ln_anx_forn_tipologia']),
                'tipo_doc':str(line['ln_anx_forn_tipoDoc']),
                'numero_doc':str(line['ln_anx_forn_num_doc']),
                'data':str(line['ln_anx_forn_data']),
                'valor_factura':str(int(line['ln_anx_forn_vl_fatura'])),
                'valor_base_incid':str(int(line['ln_anx_forn_Incidencia'])),
                'taxa_iva':str(line['ln_anx_forn_taxa_iva']),
                'iva_suportado':str(int(line['ln_anx_forn_total_sup'])),
                'direito_ded':str(int(line['ln_anx_forn_direito_ded'])),
                'iva_dedutivel':str(line['ln_anx_forn_total_ded']),
                'linha_mod106':str(line['ln_anx_forn_linha_MOD106'])                                   
            }
            LinhaAnexoFornecedor(**content).put()



    def get_alteracoes_forn(self, key, ano, mes):
        """
        metodo que verifica a existencia de alteracoes nas facturas de fornecdor, e retorna um array de dados
        informando a accao a tomar e os dados (informacao das linhas de anexo actuais e anteriores) a utilizar na acao.
        """
        
        #informacao das facturas anteriores
        anterior =[]
        info_anexo = AnexoFornecedor(where="ano='{ano}' AND mes='{mes}'".format(ano=ano,mes =mes)).get()
        if len(info_anexo)!=0:
            info_linhas = LinhaAnexoFornecedor(where="anexo_fornecedor='{id}'".format(id=info_anexo[0]['id'])).get()
            if len(info_linhas)!=0:
                anterior.append({'info_anexo':info_anexo[0],'info_linhas':info_linhas})               

        #informacao das factuaras actuais        
        actual = self.get_info_anexo_forn(key)
        print('\n\n\n\n----------------inicio verificacao alteracoes--------------------\n\n\n')
        if len(actual)!=0:
            print('\n\nInformacoes Actuais:\n',actual[0],'\n\n')
        if len(anterior)!=0:
            print('\n\nInformacoes Anteriores:\n\n',anterior[0],'\n\n')

        #TOMAR DECISAO SOBRE AS INFORMACOES EXISTENTES (actual e anterior)
        
        if (len(actual)==0) & (len(anterior)==0):
            #nao existe facturas (actuais ou anteriro) logo nao existe alteracoes
            print('\n\n\n\n------------------ 1º condicao ------------------\n\n\n')
            return []

        elif (len(actual)> 0) & (len(anterior)==0):
            #todos as facturas actuais foram adicionadas (criar anexo reg. fornecedor de adicão de facturas)
            print('\n\n\n\n------------------ 2º condicao ------------------\n\n\n')
            alteracoes = []
            alteracoes.append({'accao':'adicionar','info_anexo_act':actual[0]['info_anexo'],'info_linhas_act':actual[0]['info_linhas']})
            return alteracoes

        elif (len(actual)==0) & (len(anterior)>0):
            #todas as facturas do periodo foram eliminadas, logo deve-se criar anexo regularizacao com ação de "eliminar" todas
            print('\n\n\n\n---------------- 3º condicao --------------------\n\n\n')
            alteracoes = []
            alteracoes.append({'accao':'eliminar','info_anexo_ant':anterior[0]['info_anexo'],'info_linhas_ant':anterior[0]['info_linhas']})
            return alteracoes

        elif (len(actual)>0) & (len(anterior)>0):
            #existe facturas anterior e actuais, porem podera existir adicao, eliminacao e alteracoes de factura, logo é preciso a analise factura a factura
            print('\n\n\n\n------------------ 4º condicao ------------------\n\n\n')
            #comparar linha a linha, e remover as que existir em ambas, e sem alteraçoes
            
            act = actual[0]
            ant = anterior[0]

            
            linhasAlterarAnt = []
            linhasAlterarAct = []
            linhasAdicionar=[]
            linhasEliminar=[]

            print('\n\nLinhas Act antes da verificacao de identicos:\n\n',act['info_linhas'],'\n\n')
            print('\n\nLinhas ant antes da verificacao de identicos:\n\n',ant['info_linhas'],'\n\n')
            for line_act in act['info_linhas']:
                existe = False
                for line_ant in ant['info_linhas']:
                    #detectar os iguais 
                    if ((str(line_act['ln_anx_forn_factura']) == line_ant['factura_fornecedor'])
                        & (str(line_act['ln_anx_forn_taxa_iva']) == line_ant['taxa_iva'])
                        & (str(line_act['ln_anx_forn_direito_ded']) == line_ant['direito_ded'])
                        & (str(int(line_act['ln_anx_forn_total_sup'])) == line_ant['iva_suportado'])
                        & (str(int(line_act['ln_anx_forn_total_ded'])) == line_ant['iva_dedutivel'])
                        & (str(int(line_act['ln_anx_forn_vl_fatura'])) == line_ant['valor_factura'])
                        & (str(line_act['ln_anx_forn_num_doc']) == line_ant['numero_doc'])):
                        print('\n\n\n---aqui no iguais--------\n\n')
                        ant['info_linhas'].remove(line_ant)
                        existe = True
                        break
                    # detectar os modificados que sao para alterar
                    elif ((str(line_act['ln_anx_forn_factura']) == line_ant['factura_fornecedor'])
                        & (str(line_act['ln_anx_forn_num_doc']) == line_ant['numero_doc'])):
                        print('\n\n\n---aqui no modificado--------\n\n')
                        linhasAlterarAct.append(line_act)
                        linhasAlterarAnt.append(line_ant)
                        #remover esta linha do ant['info_linhas']
                        ant['info_linhas'].remove(line_ant)
                        existe = True
                        break

                       
                #caso nao existe em ambas deve adiciona-la
                if not existe:
                    linhasAdicionar.append(line_act)
                # o que restou das linhas anteriores sao para eliminar
                linhasEliminar = ant['info_linhas']            
                        

            print('\n\nLinhas a eliminar:\n',linhasEliminar,'\n\n')
            print('\n\nLinhas a adicionar:\n',linhasAdicionar,'\n\n')
            print('\n\nLinhas Anterior a alterar:\n',linhasAlterarAnt,'\n\n')
            print('\n\nLinhas Actuis a alterar:\n',linhasAlterarAct,'\n\n')

            alteracoes = []
            # caso exista alguma linha no linhaAlterarAnt esta é para a acção de alterar
            if len(linhasAlterarAnt)>0:                    
                alteracoes.append({'accao':'alterar','info_anexo_ant':ant['info_anexo'],'info_linhas_ant':linhasAlterarAnt,'info_anexo_act':act['info_anexo'],'info_linhas_act':linhasAlterarAct})
                
            # caso continua existindo linhas no act['info_linhas'], essas devem ser da acção adicionar
            if len(linhasAdicionar)>0:                    
                alteracoes.append({'accao':'adicionar','info_anexo_act':act['info_anexo'],'info_linhas_act':linhasAdicionar})
                
            # caso continua existindo linhas no ant['info_linhas'], essas devem ser da acção eliminar
            if len(linhasEliminar)>0:                    
                alteracoes.append({'accao':'eliminar','info_anexo_ant':ant['info_anexo'],'info_linhas_ant':linhasEliminar})
            
            return alteracoes

        



    def Gerar_Anexo_Reg_Fornecedor(self, key, window_id):
        #buscar as informacoes enviadas anteriormente
        #verificar a existencia de alteracoes
        #verificar o tipo alteracao (alteracao da factura, remocao da factura ou adicao de mais facturas)
        #tomar a decisao de acordo com o tipo alteracao
        #decidir a linha do modelo 106, que entra cada valor de cada linha (por padrao a iniciativa sera do contribuinte)
        self.kargs=get_model_record(model=self, key=key)
        
        print('Retorno: ',self.get_alteracoes_forn(key=key, ano=self.kargs['ano'],mes=self.kargs['mes']))
        print('\n\n\n\n----------------fim verificacao alteracoes-------------------\n\n\n')
        return form_edit(window_id=window_id).show()


    def Gerar_Anexo_Reg_Cliente(self, key, window_id):
        return form_edit(window_id=window_id).show()