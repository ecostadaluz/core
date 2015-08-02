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

import os, sys
sys.path.append('/var/www/core')

from auth import require_auth
from utils import set_base_context, get_context, set_context, get_window_id
from objs import *
from bottle import *
import uuid
import uwsgi

#from erp_config import *

#para implementação do CUBES
#from . import cubes
#MODEL_PATH = "/var/www/core/static/cubes/model.json"
#DB_URL = "sqlite:////var/www/core/static/cubes/data.sqlite"
#CUBE_NAME = "irbd_balance"
#workspace = None
#model = None

TEMPLATE_PATH.insert(0, '/var/www/core/views/')
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.data_dir': '/tmp/',  # home_path +
    'session.timeout': 6000,
    'session.auto': True
}

#ser_url='''<a href=""></a>'''

#import subprocess
#child = subprocess.Popen("/usr/bin/python3 /var/www/core/check_pop3.py")
#child = subprocess.Popen("/usr/bin/python3 /var/www/core/check_pop3.py", shell=True)


class StripPathMiddleware(object):
    '''
    Get that slash out of the request
    '''

    def __init__(self, a):
        self.a = a

    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

application = SessionMiddleware(app(), session_opts)
app = StripPathMiddleware(application)


@hook('before_request')
def setup_request():
    """Implements the request session"""
    request.session = request.environ['beaker.session']


@post('/get_new_window_id/<window>')
def get_new_window_id(window):
    """A funçao que atribui novos window_id a chamar de base.tpl"""
    #print(window)
    window = window.split('_')
    window_name = window[0]
    window_id = window[1]
    #print('im in the get_new_window_id called by base.tpl',
     #     window_name,
      #    window_id)
    return get_window_id(window_name=window_name, window_id=window_id)


@post('/popup_close/<window_id>')
def popup_close(window_id):
    """A funçao que permite retornar o window_status a edit quando o popup fecha"""
    #print ('oi estou no popup_close')
    from utils import get_context as gtx
    ctx_dict = gtx(window_id)
    ctx_dict['window_status'] = 'edit'
    set_context(window_id, ctx_dict)
    #print ('sai do popup_close')


@route('/')
@view('base')
#@require_auth
def main():
    """Funçao index"""
    print('Init do main_route')
    window_id = str(get_window_id())
    print(window_id)
    set_base_context(window_id)
    print('oi')
    ctx_dict = get_context(window_id)
    print(ctx_dict)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'index'
    ctx_dict['title'] = 'ERP +'
    ctx_dict['form'] = ''
    print(ctx_dict)
    set_context(window_id, ctx_dict)
    return ctx_dict


# @route('/ws')
# def websocket():
#     print('im in ws')
#     env = request.environ
#     uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
#     while True:
#         msg = uwsgi.websocket_recv()
#         uwsgi.websocket_send(msg)


@route('/ws')
def websocket():
    print('im in ws')
    env = request.environ
    uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    channel = r.pubsub()
    channel.subscribe('teste_ws')
    websocket_fd = uwsgi.connection_fd()
    redis_fd = channel.connection._sock.fileno()
    while True:
        print("here in the loop")
        # wait max 4 seconds to allow ping to be sent
        ready = gevent.select.select([websocket_fd, redis_fd], [], [], 4.0)
        # send ping on timeout
        if not ready[0]:
            uwsgi.websocket_recv_nb()
        for fd in ready[0]:
            if fd == websocket_fd:
                msg = uwsgi.websocket_recv_nb()
                if msg:
                    r.publish('teste_ws', msg)
            elif fd == redis_fd:
                msg = channel.parse_response()
                # only interested in user messages
                if msg[0] == b'message':
                    uwsgi.websocket_send(msg[2])



@route('/webservice/<variavel>')
@view('simple')
#@require_auth
def webservice(variavel):
    """Funçao teste de webservice"""
    #print('Init do teste_webservice')
    return variavel


# def initialize_model():
#   ##print('got in initialize_model')
#   global workspace
#   global model
#   #print('before {var1} {var2}'.format(var1=str(workspace), var2=str(model)))
#   model = cubes.load_model(MODEL_PATH)
#   #print('model')
#   workspace = cubes.create_workspace("sql", model, url=DB_URL, fact_prefix="ft_")
#   #print('after {var1} {var2}'.format(var1=str(workspace), var2=str(model)))

# def get_browser():
#   ##print('oi in get_browser')
#   return workspace.browser(model.cube(CUBE_NAME))

# @route('/bi')
# @view('bi')
# def bi():
#   ##print('Inicio')
#   dim_name = 'item' # no original vem do url
#   initialize_model()
#   ##print('modelo iniciado')
#   global model
#   browser = get_browser()
#   ##print('browser iniciado')
#   # First we need to get the hierarchy to know the order of levels. Cubes
#   # supports multiple hierarchies internally.
#   dimension = model.dimension(dim_name)
#   hierarchy = dimension.hierarchy()
#   # Parse the`cut` request parameter and convert it to a list of
#   # actual cube cuts. Think of this as of multi-dimensional path, even that
#   # for this simple example, we are goint to use only one dimension for
#   # browsing.
#   cutstr = request.forms.get('cut')
#   #print('my cutstr e: {var1}'.format(var1=str(cutstr)))
#   cell = cubes.Cell(browser.cube, cubes.cuts_from_string(cutstr))
#   # Get the cut of actually browsed dimension, so we know "where we are" -
#   # the current dimension path
#   cut = cell.cut_for_dimension(dimension)
#   if cut:
#       path = cut.path
#   else:
#       path = []
#   # Do the work, do the aggregation.
#   result = browser.aggregate(cell, drilldown=[dim_name])
#   # If we have no path, then there is no cut for the dimension, # therefore
#   # there is no corresponding detail.
#   if path:
#       details = browser.cell_details(cell, dimension)[0]
#   else:
#       details = []
#   # Find what level we are on and what is going to be the drill-down level
#   # in the hierarchy
#   levels = hierarchy.levels_for_path(path)
#   if levels:
#       next_level = hierarchy.next_level(levels[-1])
#   else:
#       next_level = hierarchy.next_level(None)
#   # Are we at the very detailed level?
#   is_last = hierarchy.is_last(next_level)
#   # Finally, we render it
#   context = get_base_context()
#   context['name'] = 'bi'
#   context['title'] = 'ERP + Business Inteligence'
#   context['dimensions'] = model.dimensions
#   context['dimension'] = dimension
#   context['levels'] = levels
#   context['next_level'] = next_level
#   context['result'] = result
#   context['cell'] = cell
#   context['is_last'] = is_last
#   context['details'] = details

#   code = """
#       oi
#   """
#   context['form'] = code
#   return context


@route('/upload', method='POST')
def do_upload():
    """
    Este é o upload utilizado no WYSIWYG
    """
    user = request.session['user']
    user_name = request.session['user_name']
    data = request.files.upload
    message = ''
    url = ''
    #print(request.query.keys())
    #POST /upload?CKEditor=descricao&CKEditorFuncNum=1&langCode=pt
    #dict_keys(['langCode', 'CKEditorFuncNum', 'CKEditor'])
    funcNum = request.query.get('CKEditorFuncNum')
    #Optional: instance name (might be used to load a specific configuration file or anything else).
    CKEditor = request.query.get('CKEditor')
    #Optional: might be used to provide localized messages.
    langCode = request.query.get('langCode')

    dir_path= request.forms.get('dir_path')
    dir_name= request.forms.get('dir_name')
    #print(dir_path, dir_name)
    #name, ext = os.path.splitext(data.filename)
    if dir_path == 'userfiles':
        if dir_name == 'Pasta Pessoal':
            save_path = "/var/www/core/static/userfiles/{user}".format(user=user)
        else:
            save_path = "/var/www/core/static/userfiles/{user}/{dir_name}".format(dir_name=dir_name, user=user)
    else:
        save_path = "/var/www/core/static/publicfiles/{dir_name}".format(dir_name=dir_name)

    if not path.exists(save_path):
        makedirs(save_path)

    if data and data.file:
        #raw = data.file.read() # This is dangerous for big files
        filename = save_path + '/' + data.filename
        with open(filename, 'wb') as open_file:
            open_file.write(data.file.read())
        url = save_path[13:] + '/' + data.filename
        #print(url)
        new_anexo = add_anexo(anexo_file=data.filename, user_name=user_name)
    else:
        message = 'Erro a carregar o ficheiro!'

    return "<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction({funcNum}, '{url}', '{message}');</script>".format(message=message, url=url, funcNum=funcNum)


@post('/mkdir')
def mkdir():
    """Cria novas directorias nas páginas de utilizador e projeto da área de anexos"""
    #print('estou em mkdir')
    new_dir = request.forms.get('new_dir')
    user = str(request.session['user'])
    path_newdir = "/var/www/core/static/files/Users/{user}/{new_dir}".format(user=user, new_dir=new_dir)
    #print(new_dir)
    if not os.path.exists(path_newdir):
        os.makedirs(path_newdir)


@post('/chdir/<new_path>')
def chdir(new_path=None):
    """Muda de  directoria nas páginas de utilizador e projeto da área de anexos"""
    print('Im in chdir')
    funcNum = request.forms.get('funcNum')
    obj = request.forms.get('obj')
    obj_key = request.forms.get('obj_key')
    button_name = request.forms.get('button_name')
    window_id = request.forms.get('main_window_id')
    #print('obj', obj)
    #print('obj_key', obj_key)
    #print('window_id', window_id)
    wysiwyg = request.forms.get('wysiwyg')
    user = str(request.session['user'])
    print('end of it')
    return browse(wysiwyg=wysiwyg, window_id=window_id, obj=obj, obj_key=obj_key, button_name=button_name, message='', path=new_path)


#@get('/browse/<window_id>/<obj>/<obj_key>/<button_name>/<wysiwyg>')
#@view('browser')
#def browse(wysiwyg=False, window_id=None, obj=None, obj_key=None, button_name=None, message='', path=''):

@post('/browse/<obj>/<obj_key>/<button_name>/<wysiwyg>')
#@view('browser')
def browse(wysiwyg=False, obj=None, obj_key=None, button_name=None, message='', path=''):
    print('in browse')
    print(obj, obj_key)
    print('button_name', button_name)
    forms = '/var/www/core/forms/'
    user = request.session['user']
    user_name = request.session['user_name']
    result_dict= {}
    funcNum = 1#request.query.get('CKEditorFuncNum')
    #print(window_id)
    #ctx_dict = get_context(window_id)
    if path == '':
        print('sem path', path)
        save_path = '/var/www/core/static/files/Users/' + str(user)
        path = 'Users/' + str(user)
    else:
        print('com path', path, type(path))
        path = path.replace('+', '/')
        save_path = '/var/www/core/static/files/' + path
    print ('save_path', save_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print('created')
    print(save_path)
    dirs = []
    files = []
    for (dirpath, dirnames, filenames) in os.walk(save_path):
        dirs.append(dirnames)
        files.append(filenames)
    #print ({'dirs': dirs, 'files': files, 'user': user, 'funcNum': funcNum, 'wysiwyg':wysiwyg, 'message':message, 'path':path, 'obj':obj, 'obj_key':obj_key, 'window_id':window_id, 'button_name':button_name})
    #return {'dirs': dirs, 'files': files, 'user': user, 'funcNum': funcNum, 'wysiwyg':wysiwyg, 'message':message, 'path':path, 'obj':obj, 'obj_key':obj_key, 'window_id':window_id, 'button_name':button_name}
    result_dict={'dirs':dirs, 'files':files, 'wysiwyg': False, 'message':message, 'path':path, 'obj':obj, 'obj_key':obj_key, 'button_name':button_name, 'user': user, 'funcNum': funcNum}
    print('result_dict', result_dict)
    return SimpleTemplate(name = forms + 'browser').render(result_dict)
    #return {'dirs': dirs, 'files': files, 'user': user, 'funcNum': funcNum, 'wysiwyg':wysiwyg, 'message':message, 'path':path, 'obj':obj, 'obj_key':obj_key, 'button_name':button_name}# 'window_id':window_id,


@route('/browser_upload/<wysiwyg>', method='POST')
def do_browser_upload(wysiwyg=False):
    """
    Este é o upload utilizado no browser
    """
    print('Im in upload anexo')
    user = str(request.session['user'])
    user_name = request.session['user_name']
    obj = request.forms.get('obj')
    obj_key = request.forms.get('obj_key')
    window_id = request.forms.get('main_window_id')
    button_name = request.forms.get('button_name')
    print('obj', obj)
    print('obj_key', obj_key)
    print('window_id', window_id)

    #print(1)
    data = request.files.get('upload')
    #print(2)
    path = request.forms.get('path')
    print(path)
    #name, ext = os.path.splitext(data.filename)
    save_path = "/var/www/core/static/files/{path}".format(path=path)
    print(3, save_path)
    #if not os.path.exists(save_path):
     #   os.makedirs(save_path)
    #print(4, type(data), dir(data))
    if data:
        filename = save_path + '/' + data.filename
        print(5, filename)
        with open(filename, 'wb') as open_file:
            open_file.write(data.file.read())
        new_anexo = add_anexo(anexo_file=data.filename, user=user)
        print(6)
        return browse(wysiwyg=wysiwyg, window_id=window_id, obj=obj, obj_key=obj_key, button_name=button_name, message=['success', 'ficheiro carregado com sucesso!'], path=path)#'<a href="/static/userfiles/' + user_name + '/' + data.filename + '">' + data.filename + '</a>\n'
    else:
        print('no data')
        return browse(wysiwyg=wysiwyg, window_id=window_id, obj=obj, obj_key=obj_key, button_name=button_name, message=['alert', 'Erro ao carregar o ficheiro!'], path=path)


def add_anexo(anexo_file, user):
    """Este add_anexo refere-se a adicionar um anexo novo a função link_anexo é a que permite adicionar um anexo a uma tarefa ou projeto ou seja que objecto for"""
    #print('im in add_anexo')
    anexo = {}
    anexo_path = "/static/files/Users/{user}".format(user=str(user))
    anexo['id'] = str(uuid.uuid4())
    anexo['path'] = anexo_path
    anexo['nome'] = anexo_file
    #anexo_node, = db.create(anexo)
    #anexo_node.add_labels('Anexo')
    return anexo['id']


@post('/link_anexo')
def link_anexo():
    """Este link_anexo permite adicionar um anexo a uma tarefa ou projeto ou seja que objeto for! """
    #print('im in link_anexo')
    anexo_file = request.forms.get('anexo_file')
    obj = request.forms.get('obj')
    obj_key = request.forms.get('obj_key')
    #print('anexo_file', anexo_file)
    #print('obj', obj)
    #print('obj_key', obj_key)
    user = request.session['user']
    user_name = request.session['user_name']
    #print(user_name)
    anexo_path = "/static/userfiles/{user}".format(user=user)
    obj = obj.split('.')
    model_obj = obj[0]
    model_name = obj[1]
    import importlib
    mod = importlib.import_module(model_obj)
    record = eval("""mod.{model_name}(where="id='{obj_key}'").get()[0]""".format(model_name=model_name, obj_key=obj_key))
    #print('record', record)
    #print(anexo_path, anexo_file)
    kargs = dict(record)
    kargs['foto'] = anexo_path + '/' + anexo_file
    kargs['user'] = user
    #print('kargs', kargs)
    result = eval('mod.{model_name}(**kargs).put()'.format(model_name=model_name))
    #print(result)
    #print('fim')
    return False


@get('/show_help/<obj>')
def show_help(obj):
    """Abre os ficheiro de ajuda da pasta help"""
    code = 'Sem Ficheiro de ajuda!'
    filename = '/var/www/core/help/' + obj + '.html'
    try:
        with open(filename, 'r') as open_file:
            code = open_file.read()
    except:
        pass
    return code


@route('/about')
@view('base')
def about():
    """Devolve a pagina about"""
    window_id = str(get_window_id())
    set_base_context(window_id)
    ctx_dict = get_context(window_id)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'about'
    ctx_dict['title'] = 'Sobre'
    code = """
        <div class="small-12 large-12 columns">
        <textarea rows="30" readonly>
    """
    code += """
    Sobre o ERP+

    Versão 1.0 de 2015

    O ERP + é uma plataforma de Gestão sobre a qual qualquer pessoa pode desenvolver
    objectos que suportem o seu negócio ou actividade.

    Bom trabalho

    Contactos:

    Dario Costa
    +238 983 04 90

    """
    code += """
        </textarea>
        </div>
    """
    ctx_dict['form'] = code
    set_context(window_id, ctx_dict)
    return ctx_dict


@route('/help')
@view('base')
def help():
    """Devolve a pagina de Ajuda"""
    window_id = str(get_window_id())
    set_base_context(window_id)
    ctx_dict = get_context(window_id)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'help'
    ctx_dict['title'] = 'Ajuda'


    code = """
        <textarea rows="30" class="small-12 large-12 columns">
    """
    code += """
    Ajuda

    Por Implementar...

    """
    code += """
        </textarea>
    """
    ctx_dict['form'] = code
    set_context(window_id, ctx_dict)
    return ctx_dict


@route('/update')
@view('base')
def update():
    """Devolve a pagina de Actualizaçao da Implementacao Local"""
    window_id = str(get_window_id())
    set_base_context(window_id)
    ctx_dict = get_context(window_id)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'update'
    ctx_dict['title'] = 'Actualização'

    code = """
        <textarea rows="30" class="small-12 large-12 columns">
    """
    code += """
    Actualização

    Por Implementar...

    """
    code += """
        </textarea>
    """
    ctx_dict['form'] = code
    set_context(window_id, ctx_dict)
    return ctx_dict


@route('/licence')
@view('base')
def licence():
    """Devolve a pagina da Licença"""
    window_id = str(get_window_id())
    set_base_context(window_id)
    ctx_dict = get_context(window_id)
    ctx_dict['window_id'] = window_id
    ctx_dict['name'] = 'licence'
    ctx_dict['title'] = 'Licença'

    licence_file = open('/var/www/core/help/licence.txt', 'r', encoding='utf8')
    code = """
        <textarea rows="30" class="small-12 large-12 columns">
    """
    code += licence_file.read()
    code += """
        </textarea>
    """
    ctx_dict['form'] = code
    set_context(window_id, ctx_dict)
    return ctx_dict


@get('/static/<filepath:path>')
def server_static(filepath):
    """Defina a Root para os ficheiros estaticos"""
    return static_file(filepath, root='/var/www/core/static')


@get('/login')
@view('login')
def login_form():
    """Implementa o Ecra de Login"""
    window_id = str(get_window_id())
    import erp_config as ec
    return dict(name='login', title='Autenticação do ERP+', url='url', favicon=ec.favicon, system_logo=ec.system_logo, logotipo=ec.logotipo, enterprise=ec.enterprise, form='', window_id=window_id)


@post('/login')
@view('login')
def login_submit():
    """Valida o Login"""
    print('Im on login submit')
    window_id = request.forms.get('window_id')

    #este código elimina os dicionarios json que vão sendo criados para guardara informação contextual
    now = time.time()
    path = '/var/www/tmp/'
    for f in os.listdir(path):
        if os.stat(os.path.join(path,f)).st_mtime < now - 86400:
            os.remove(os.path.join(path, f))

    import base64
    from users import Users
    user = request.forms.get('login')
    password = request.forms.get('password')
    print('before db request')
    db_user = Users(where="login = '{user}'".format(user=user)).get()
    autenticated = False
    print('1', user, db_user)
    if db_user:
        db_user = db_user[0]
        if base64.decodestring(db_user['password'].encode('utf-8')).decode('utf-8')[6:] == password:
            print('o utilizador {user} autenticou-se com sucesso!'.format(user=db_user['nome']))
            request.session['user'] = db_user['id']
            request.session['user_name'] = db_user['nome']
            request.session.save()
            autenticated = True
    print('2')
    if not autenticated:
        return HTTPResponse(status=500, output='Autenticação Inválida!!!')
    else:
        #print('estou autenticado')
        if window_id:
            #print('tenho window_id')
            ctx_dict = get_context(window_id)
            if 'redirect_url' in ctx_dict:
                #print('tenho redirect'+str(ctx_dict['redirect_url']))
                return ctx_dict['redirect_url']
            else:
                return '/'
        else:
            #print('nao tenho window_id')
            return '/'
    print('end')


@post('/change_pass')
@view('login')
def change_pass_submit():
    """Valida a mudança de Password"""
    print('im in change_pass')
    import base64
    from users import Users
    user = request.forms.get('login')
    password = request.forms.get('password')
    new_password = request.forms.get('new_password')
    confirm_password = request.forms.get('confirm_password')
    print('before db request')
    db_user = Users(where = "login='{user}'".format(user=user)).get()
    autenticated = False
    if db_user:
        db_user = db_user[0]
        if base64.decodestring(db_user['password'].encode('utf-8')).decode('utf-8')[6:] == password:
            if request.forms.get('new_password') != request.forms.get('confirm_password'):
                return HTTPResponse(status=500, output='A nova password e a password de confirmação tem que ser iguais!!!')
            if len(request.forms.get('new_password')) > 3:
                import base64
                pass_string = 'noops!' + request.forms.get('new_password')
                db_user['password'] = base64.encodestring(pass_string.encode('utf-8')).decode('utf-8')
                db_user['user'] = db_user['id']
                Users(**db_user).put()
            else:
                return HTTPResponse(status=500, output='A nova password deve ter mais de 3 caracteres!!!')
            print('o utilizador {user} mudou a password com sucesso!'.format(user=db_user['nome']))
            request.session['user'] = db_user['id']
            request.session['user_name'] = db_user['nome']
            request.session.save()
            autenticated = True
    print('end')
    if not autenticated:
        return HTTPResponse(status=500, output='Autenticação Inválida!!!')
    else:
        return 'Password modificada com sucesso!'


@route('/logout')
def logout():
    """Implementa o Logout"""
    for key in request.session:
        del request.session[key]
    redirect('/login')


@post('/calc')
def calc():
    """Implementa a funçao da calculadora"""
    #print('{var1}'.format(var1=str(request.forms.get('calc'))))
    try:
        value = eval(request.forms.get('calc'))
    except:
        value = 'Error'
    return str(value)


@post('/chamar')
@view('base')
def gap_chamar():
    user_estado = request.forms.get('user_estado')
    from gap_sequencia import GAPSequencia
    res = GAPSequencia().chamar_senha(user_estado=user_estado)
    #Se for igual a none retorna uma mensagem de erro
    if res == None:
        #E necessario ver ainda o porque do javascript nao estar a captar o output de erro
        return HTTPResponse(status=500, output='Actualmente nao temos nenhuma senha em espera')
    #Se nao for none retorna o numero da senha solicitada
    else:
        return str(res)

@post('/chamar_por_senha/<numero_senha>')
@view('base')
def gap_chamar_por_senha(numero_senha):
    user_estado = request.forms.get('user_estado')
    from gap_sequencia import GAPSequencia
    res = GAPSequencia().chamar_por_senha(senha=numero_senha,user_estado=user_estado)
    #Se for igual a none retorna uma mensagem de erro
    if res == None:
        #E necessario ver ainda o porque do javascript nao estar a captar a mensagem de erro
        return HTTPResponse(status=500, output='Senha Invalida')
    #Se nao for none retorna o numero da senha solicitada
    else:

        return str(res)

@post('/chamar_senhaEspera/<numero_senha>')
@view('base')
def gap_chamar_senhaEspera(numero_senha):
    user_estado = request.forms.get('user_estado')
    from gap_sequencia import GAPSequencia
    res = GAPSequencia().chamar_senhaEspera(senha=numero_senha,user_estado=user_estado)
    #Se for igual a none retorna uma mensagem de erro
    if res == None:
        #E necessario ver ainda o porque do javascript nao estar a captar a mensagem de erro
        return HTTPResponse(status=500, output='Senha Invalida')
    #Se nao for none retorna o numero da senha solicitada
    else:
        return str(res)


@post('/transferir/<keyservico>')
@view('base')
def gap_transferir(keyservico):
    senha = request.forms.get('senha')
    from gap_sequencia import GAPSequencia
    return str(GAPSequencia().transferir_senha(senha=senha, keyservico=keyservico))

@post('/terminar/<tempo_atendimento>')
@view('base')
def gap_terminar(tempo_atendimento):
    senha = request.forms.get('senha')
    from gap_sequencia import GAPSequencia
    return str(GAPSequencia().terminar_senha(senha=senha,tempo_atendimento=tempo_atendimento))

@post('/esperar/<tempo_atendimento>/<comentario>')
@view('base')
def gap_esperar(tempo_atendimento,comentario):
    senha = request.forms.get('senha')
    from gap_sequencia import GAPSequencia
    return str(GAPSequencia().espera_atendedor(senha=senha,tempo_atendimento=tempo_atendimento,comentario=comentario))

@post('/desistir/<tempo_atendimento>')
@view('base')
def gap_desistir(tempo_atendimento):
    senha = request.forms.get('senha')
    from gap_sequencia import GAPSequencia
    return str(GAPSequencia().desistir_senha(senha=senha,tempo_atendimento=tempo_atendimento))

@post('/fazer_intervalo')
@view('base')
def gap_intervalo():
    from my_users import Users
    return str(Users().Intervalo())

@post('/terminar_atendimento')
@view('base')
def gap_terminar_atendimento():
    from my_users import Users
    return str(Users().Terminado())

@post('/saveTime/<senha>/<tempo_atendimento>')
@view('base')
def  guardarTempo(senha,tempo_atendimento):
    from gap_sequencia import GAPSequencia
    return str(GAPSequencia().saveTime(senha=senha,tempo_atendimento=tempo_atendimento))


#ecran de Espera TV
@route('/tv')
@view('ecranEspera')
def get_ecranEspera():
    window_id = str(get_window_id())
    from gap_multimedia import GAPMultimedia
    playlist = GAPMultimedia().get_playlist()
    playlistsize = len(playlist) #para ajudar no controlo do playlist
    playlist = ''.join(playlist)
    return dict(title='Ecran Espera', window_id=window_id,playlist=playlist,playlistsize=playlistsize)