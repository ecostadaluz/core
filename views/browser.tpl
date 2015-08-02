% #print('Im in browser------------------------------------')
% #print('wysiwyg', wysiwyg)
% #print('message', message)

<!DOCTYPE html>
<html  class="no-js" lang="pt-PT">
  <head>
    <meta charset="utf-8">
    <title>Navegador de Ficheiros</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Navegador de Ficheiros">
    <meta name="author" content="António Anacleto">
    <link href="/static/css/normalize.css" rel="stylesheet">
    <link href="/static/css/foundation.min.css" rel="stylesheet">
    <link href="/static/css/foundation-icons.css" rel="stylesheet">
    <link href="/static/css/erp.css" rel="stylesheet">

    <link rel="shortcut icon" href="/static/logos/favicon.png">
    <script src="/static/js/modernizr.js"></script>
  </head>

  <body>

  <div id='loadingDiv' style='position:absolute; top:0px; left:0px; z-index: 100; height: 100%; width: 100%; display:flex; vertical-align:middle; text-align:center; background: #fff; filter:alpha(opacity=55); opacity:.55;
   color: #000; visibility:hidden;'>
   <div style="display:block; margin:auto;">
    Aguarde ...  <br><br>
    <img src='/static/images/RunningWoman.gif'/>
    </div>
 </div>


    <div data-alert  id="message_container" style="display:none" class="alert-box info radius">
        <div id="message" style="color:black;"></div>
        <a href="#" class="close">&times;</a>
    </div>

% if message:
    <div data-alert  id="xp_message_container" class="alert-box {{message[0]}} radius">
        <div id="xp_message" style="color:black;">{{message[1]}}</div>
        <a href="#" class="close">&times;</a>
    </div>
% end


<div class="">

  <div class="main-section">

    <form id="mainForm" action="/browser_upload/{{wysiwyg}}" method="post" enctype="multipart/form-data">
        <fieldset id="content">

  <div class="row">
    <div class="small-2 medium-2  large-2 columns">
      <h1><img src="/static/logos/logo100x100.png"/></h1>
    </div>
    <div class="small-9 medium-9 large-9 columns">
      <ul class="inline-list right">
        <li><input type="file" name="upload" />
        <input type="submit" value="Carregar Para o Servidor" /></li>
        <li>
      <div class="row collapse">
        <div class="small-9 medium-9 large-9 columns">
          <input name="new_dir" id="new_dir" placeholder="Nova Pasta" type="text">
        </div>
        <div class="small-3 medium-3 large-3 columns">
          <span class="postfix">
            <a href="#" class="button tiny radius success" onclick="mkdir();"><i class="fi-plus"></i></a>
          </span>
        </div>
      </div>
        </li>
      </ul>
    </div>
  </div>
            <input name="obj" id="obj" type="hidden" value="{{!obj}}"></input>
            <input name="obj_key" id="obj_key" type="hidden" value="{{!obj_key}}"></input>
            <input name="main_window_id" id="main_window_id" type="hidden" value="{{!window_id}}"></input>
            <input name="button_name" id="button_name" type="hidden" value="{{!button_name}}"></input>
            <input name="funcNum" id="funcNum" type="hidden" value="{{funcNum}}"></input>
            <input name="wysiwyg" id="wysiwyg" type="hidden" value="{{wysiwyg}}"></input>
            <input name="anexo_file" id="anexo_file" type="hidden"></input>
            <input name="path" id="path" type="hidden" value="{{path}}"></input>
        </fieldset>
    </form>


<div class="row">

<div class="small-10 medium-10 large-10 push-2 columns">
<div id="dir_content">

%f_count = 0
%for f in files[0]:
    %if f_count == 0:
        <div class="row">
    %end
    %file_extension = f.split('.')[-1]
    % if wysiwyg == 'True':
      %#print('im wysiwyg', wysiwyg)
      %if file_extension in ['jpg', 'png', 'jpeg', 'tiff', 'gif', 'bmp', 'svg', 'JPG']:
          <div class="small-3 medium-3 large-3  columns"><img src="/static/files/{{path}}/{{f}}" onclick="return_url('{{funcNum}}', '{{user}}', '{{f}}');"></img>{{f.replace('_', '-')}}</div>
      %elif file_extension in ['xls', 'csv', 'xlsx']:
          <div class="small-3 medium-3 large-3  columns"><a href="/static/files/{{path}}/{{f}}"><img src="/static/images/ExcelLogo.png"></img>{{f.replace('_', '-')}}</a></div>
      %elif file_extension in ['doc', 'docx']:
          <div class="small-3 medium-3 large-3  columns"><a href="/static/files/{{path}}/{{f}}"><img src="/static/images/WordLogo.png"></img>{{f.replace('_', '-')}}</a></div>
      %elif file_extension in ['ppt', 'pptx']:
          <div class="small-3 medium-3 large-3  columns"><a href="/static/files/{{path}}/{{f}}"><img src="/static/images/PowerpointLogo.png"></img>{{f.replace('_', '-')}}</a></div>
      %elif file_extension in ['pdf']:
          <div class="small-3 medium-3 large-3  columns"><a href="/static/files/{{path}}/{{f}}"><img src="/static/images/PdfLogo.jpg"></img>{{f.replace('_', '-')}}</a></div>
      %elif file_extension in ['txt']:
          <div class="small-3 medium-3 large-3  columns"><a href="/static/files/{{path}}/{{f}}"><img src="/static/images/TxtLogo.png"></img>{{f.replace('_', '-')}}</a></div>
      %elif file_extension in ['mp4', 'avi', 'rmvb', 'mkv']:
          <div class="small-3 medium-3 large-3  columns"><a href="/static/files/{{path}}/{{f}}"><img src="/static/images/Video.png"></img>{{f.replace('_', '-')}}</a></div>
      %else:
          <div class="small-3 medium-3 large-3  columns"><a href="/static/files/{{path}}/{{f}}"><img src="/static/images/OtherLogo.png"></img>{{f.replace('_', '-')}}</a></div>
      %end
    %else:
      %#print('im not wysiwyg', wysiwyg, f)
      %if file_extension in ['jpg', 'png', 'jpeg', 'tiff', 'gif', 'bmp', 'svg', 'JPG']:
          <div class="small-2 medium-2 large-2 columns"><img src="/static/files/{{path}}/{{f}}" onclick="link_anexo('{{f}}');"></img>{{f.replace('_', '-')}}</div>
      %elif file_extension in ['xls', 'csv', 'xlsx']:
          <div class="small-2 medium-2 large-2 columns"><img src="/static/images/ExcelLogo.png" onclick="link_anexo('{{f}}');"></img>{{f.replace('_', '-')}}</div>
      %elif file_extension in ['doc', 'docx']:
          <div class="small-2 medium-2 large-2 columns"><img src="/static/images/WordLogo.png" onclick="link_anexo('{{f}}');"></img>{{f.replace('_', '-')}}</div>
      %elif file_extension in ['ppt', 'pptx']:
          <div class="small-2 medium-2 large-2 columns"><img src="/static/images/PowerpointLogo.png" onclick="link_anexo('{{f}}');"></img>{{f.replace('_', '-')}}</div>
      %elif file_extension in ['pdf']:
          <div class="small-2 medium-2 large-2 columns"><img src="/static/images/PdfLogo.jpg" onclick="link_anexo('{{f}}');"></img>{{f.replace('_', '-')}}</div>
      %elif file_extension in ['txt']:
          <div class="small-2 medium-2 large-2 columns"><img src="/static/images/TxtLogo.png" onclick="link_anexo('{{f}}');"></img>{{f.replace('_', '-')}}</div>
      %elif file_extension in ['mp4', 'avi', 'rmvb', 'mkv']:
          <div class="small-2 medium-2 large-2  columns"><img src="/static/images/Video.png" onclick="link_anexo('{{f}}');"></img>{{f.replace('_', '-')}}</a></div>
      %else:
          <div class="small-2 medium-2 large-2 columns"><img src="/static/images/OtherLogo.png" onclick= "link_anexo('{{f}}');"></img>{{f.replace('_', '-')}}</div>
      %end
    %end
    %f_count += 1
    %if f_count == 5:
        %f_count = 0
        </div>
    %end
%end

%if f_count != 0:
    <div class="small-1 medium-1 large-1 columns"></div>
    </div>
%end

    </div>
    </div>


    <div class="small-2 medium-2 large-2 pull-10 columns" style="background:#F1FAFA;">
      <ul class="side-nav" id="pastas_locais">
            <li><a href="#" onclick="chdir('Users+{{user}}');" style="color:#FF6600;">Pasta Pessoal</a></li>
            <li><a href="#" onclick="chdir('Public');" style="color:#FF6600;">Pastas Publicas</a></li>
      </ul>
      <ul class="side-nav" id="public_folders">
        %for d in dirs[0]:
            %#print(d)
            %safe_path = path.replace('/', '+')
            <li><a href="#" onclick="chdir('{{safe_path}}+{{d}}');">{{d}}</a></li>
        %end
      </ul>
    </div>
  </div>

      </div><!--/.fluid-container-->
      <footer>
        <p>&copy; <small>ERP+ @ 2014</small></p>
      </footer>
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/fastclick.js"></script>
    <script src="/static/js/foundation.min.js"></script>
    <script src="/static/js/erp.js"></script>
    <script>
      $(document).foundation();

      $( document ).ajaxStart(function() {
          $( "#loadingDiv" ).show();
      });

      $( document ).ajaxStop(function() {
          $( "#loadingDiv" ).hide();
      });
    </script>
  </body>
</html>