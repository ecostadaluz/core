//chamar pela proxima senha em espera
function chamar_senha() {
    var strURL = '/chamar';
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
             startchamada(r);
        }).fail(function(r) {
             showMSG('warning', "Actualmente nao temos nenhuma senha em espera","#message","#message_container");
        });
  }

//chamar por uma senha especifica
function chamar_por_senha() {
    if($('#numero_senha').val()){
         var strURL = '/chamar_por_senha/'+$('#numero_senha').val();
         $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
          }).done(function(r) {
               closeModel();
               startchamada(r);
          }).fail(function(r) {
              showMSG('alert', "Senha Invalida","#ModalCSmessage","#ModalCSmessage_container");
        });
     }else{
              showMSG('alert', "Por favor introduza o numero de senha","#ModalCSmessage_container");
     }
 }

//Chamar por uma senha especifica em espera pelo atendedor xpto
function chamar_senhaEspera(numero_senha,tagID) {
    var strURL = '/chamar_senhaEspera/'+numero_senha;
    $.ajax({type: 'POST', url: strURL,data: $('#erpForm').serialize()
        }).done(function(r) {
              startchamada(r);
              refreshListaEspera();
              setTime(getTime(tagID),"timer");
        }).fail(function(r) {
             showMSG('alert', "Senha Invalida","#message","#message_container");
        });
}

//coloca uma senha em espera
function espera_senha(){
    var strURL = '/esperar/'+getTime("timer")+'/'+$('#comentario').val();
    $.ajax({type: 'POST', url: strURL,data: $('#erpForm').serialize()
        }).done(function(r) {
             refreshListaEspera();
             startEsperaTime();
             endchamada('warning','As Senha '+getSenha()+" foi adicionada a sua lista de espera");
        }).fail(function(r) {
             showMSG('warning', "Nao foi possivel colocar essa senha em espera","#message","#message_container");
        });
}


//guarda/actualiza o tempo em espera na base de dados
function saveTime(tagID){
    var strURL = '/saveTime/'+ document.getElementById("SenhaEspera"+tagID).innerText+'/'+getTime("timer"+tagID);
    $.ajax({type: "POST", url: strURL,});
  }

//incia uma chamada
function startchamada(r){
     refreshContent();
     set_userEstado();
     setSenha(r);
     startTime();
     showFields();
}

//termina uma chamada
function endchamada(type,message){
      refreshContent();
      hideFields();
      stopTime();
      setTime("00:00:00","timer");
      showMSG(type,message,"#message","#message_container");
}

function getSenha(){
    senha = $('#senha').val().split(";");
    return senha[1];
}


function getIDSenha(){
    senha = $('#senha').val().split(";");
    return senha[0];
}


function setSenha(senha){
        $('#senha').val(senha);
        senha = senha.split(";");
        document.getElementById("Divsenha").innerText = "Senha Actual: "+senha[1];
}


function set_userEstado(){
    if($('#user_estado').val()=="terminado" || $('#user_estado').val()=="intervalo"){
          setEstado('em_servico');
          showMSG("warning","O teu estado foi Alterado para em Serviço","#message","#message_container");
    }
}

//faz o set do estado do utilizador
function setEstado(estado){
    $('#user_estado').val(estado);
}

//funçao responsavel por mostrar as mensagens
function showMSG(type,content,message,message_container){
    var mymessage_container = $(message_container);
    showMessage(type, content, $(message), mymessage_container);
    mymessage_container.delay(2000).slideUp();
}

//tranferir uma senha para um servico xpto
function transferir_senha(keyservico,letraservico) {
    var strURL = '/transferir/'+keyservico;
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
              endchamada("warning","A Senha  "+getSenha()+" foi transferida para o Serviço "+letraservico);
        }).fail(function(r) {
             showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

//termina uma senha
function terminar_senha() {
    var strURL = '/terminar/'+getTime("timer");
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
             endchamada("warning","A Senha  "+getSenha()+"  terminado com sucesso");
        }).fail(function(r) {
             showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

  // desistir de uma senha
  function desistir_senha() {
    var strURL = '/desistir/'+getTime("timer");
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
              endchamada("warning","A Senha  "+getSenha()+" desistiu");
        }).fail(function(r) {
              showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

  // atendedor modo intervalo
  function fazer_intervalo() {
    var strURL = '/fazer_intervalo';
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
                setEstado('intervalo');
                showMSG("warning","O seu estado foi Alterado para o modo intervalo","#message","#message_container");
        }).fail(function(r) {
                showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

  // atendedor modo terminado atendimento
  function terminar_atendimento() {
    var strURL = '/terminar_atendimento';
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
               setEstado('terminado');
               showMSG("warning","O seu estado foi Alterado para Atendimento Terminado","#message","#message_container");
        }).fail(function(r) {
                showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

  //faz o refresh das principais divs
  function refreshContent(){
        $('#gap_fluxo').load(document.URL +  ' #gap_fluxo');
        $('#panel0').load(document.URL +  ' #panel0');
        $('#panel1').load(document.URL +  ' #panel1');
        $('#panelEspera').load(document.URL +  ' #panelEspera');
  }

  // faz o refresh apenas da lista de espera
  function refreshListaEspera(){
       $('#panelEspera').load(document.URL +  ' #panelEspera');
  }

  //fecha o model
  function closeModel(){
      $('#ModalCS').foundation('reveal', 'close');
  }



 //show time
//Variaveis globais necessarias para o controlo do time
var start;
var startEspera;

//actualiza o tempo de atendimento que aparece na bara do atendedor
function updateTime(){
     setTimeContent("timer");
}


//actualiza o tempo na lista de espera
function updateTimeEspera(){
    count = $('#countEspera').val();
    var i;
    for(i=0; i<count; i++){
            //set Time na lista de espera
            setTimeContent("timer"+i);
            //actualiza o respectivo tempo na base de dados
            saveTime(i);
    }
}


function setTimeContent(tagID){
  var value = String(document.getElementById(tagID).innerText);
  updatedTime = TimeManager(value);
  document.getElementById(tagID).innerText = updatedTime;
}

//Ainda nao e perfeito mas para o que precisamos da conta :)
function TimeManager(value){
  var content = value.split(":");
  var hora = parseInt(content[0]);
  var minuto = parseInt(content[1]);
  var segundos = parseInt(content[2]);

 if(segundos<59)
        segundos=segundos+1;
else if(segundos==59){
      segundos=00;
      if(minuto<59)
          minuto=minuto+1;
      else if(minuto==59){
            minuto=00;
            hora=hora+1;
      }
  }

  if(segundos<10)
          segundos = "0"+segundos;
  if(minuto<10)
          minuto =  "0"+minuto;
  if(hora<10)
          hora = "0"+hora;

  return hora+":"+minuto+":"+segundos;
}

  //start time incia o tempo
  function startTime(){
    if(start)
        clearInterval(start);

     start = setInterval(updateTime, 1000); //essa funçao faz o delay em cada 1000 milisegundos actualiza o time
  }


  //stop time para o tempo
  function  stopTime(){
         clearInterval(start);
  }

  //para o tempo das senhas na lista de espera pelo atendedor
  function stopEsperaTime(){
      clearInterval(startEspera);
  }

  // inicia o tempo na lista de espera pelo atendedor
  function startEsperaTime(){
      if(startEspera)
            clearInterval(startEspera);

     startEspera= setInterval(updateTimeEspera, 1000); //essa funçao faz o delay em cada 1000 milisegundos actualiza o time
  }

  //controla o tempo das senhas em espera pelo atendedor
  function EsperaManager(){
      count = parseInt($('#countEspera').val());
      if(count>0){
          startEsperaTime();
      }else{
          stopEsperaTime();
      }
  }

  //get o time actual
  function getTime(tagID){
      return document.getElementById(tagID).innerText
  }

  //setTime faz o set do tempo
  function setTime(value,tagID){
      document.getElementById(tagID).innerText = value;
}



// faz o get do rss das noticias
function getNews(feedUrl){
        $.ajax({
                url: document.location.protocol + '//ajax.googleapis.com/ajax/services/feed/load?v=1.0&output=xml&num=10&callback=?&q=' + encodeURIComponent(feedUrl),
                  dataType : 'json',
                  success  : function (data) {
                    if (data.responseStatus == 200) {
                          var xmlDoc = $.parseXML(data.responseData.xmlString);
                          var $xml = $(xmlDoc);
                          $xml.find('item').each(function(i,p) {
                                $("#footermessage").append($(p).find('title').text()+" - "+$(p).find('description').text()+"  ");
                          });
                      }
                 }
        });
  }

//procura os rss
function searchNews(){
      try {
              var asemana = ['http://www.asemana.publ.cv/spip.php?page=backend&id_mot=1&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=4&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=13&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=5&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=15&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=19&ak=1'];

            for (var i = 0; i < asemana.length; i++) {
                         getNews(asemana[i]);
            }

      }
      catch(err){}
 }


//actualiza cliente em espera no ecran da televisao
function updateListaEsperaTV(){
      $.ajax({
               url: '/tv',
               type: 'PUT',
               success: function(response){
               }});
 }

//Controla a lista de reproduçao video
function videoManager(){
    var video = document.getElementById("Videotv");
    video.onended = function() {
          playerControler();
    };
}

var startimageTimer; //controla a duraçao da imagem

//Controla as Imagens que aparecem no ecran de espera
function imageManager(){
      if($('#currentTime').val()==$('#targetTime').val()){
              stopImageTime();
              $('#currentTime').val("00:00:00");
              playerControler();
      }else{
            updatedTime = TimeManager($('#currentTime').val());
            $('#currentTime').val(updatedTime);
      }
}

//Inicia a contagem do tempo da imagem
function startImageTime(){
     if(startimageTimer)
           clearInterval(startimageTimer);

     startimageTimer = setInterval(imageManager, 1000); //essa funçao faz o delay em cada 1000 milisegundos actualiza o time
}

//Para a contagem do tempo da imagem
function stopImageTime(){
      clearInterval(startimageTimer);
}

//player controler e necessario para fazer o controlo das imagens e videos a reproduzir
function playerControler(){
      var video = document.getElementById("Videotv");
      var image = document.getElementById("Imagetv");
      var i=0;
      var count =0; // conta os elementos
      var toplay; //guarda o url do item a reproduzir :)
      var value = 4;
      var playlistsize = $("#playlistsize").val();
      playlist = String($("#playlist").val()).split(";");
      for(i;i<playlistsize;i++){
             if($("#nextmultimedia").val()==playlistsize || $("#nextmultimedia").val()==0){
                    $("#nextmultimedia").val(1);
                    toplay = playlist[1];
                    break;
              }else{
                      if(count==$("#nextmultimedia").val() && $("#nextmultimedia").val()<playlistsize){
                            toplay = playlist[value-3];
                            $("#nextmultimedia").val(count+1);
                            break;
                        }
              }
              value=value+4;
              count++;
      }

      if(playlist[value-2]=='video'){
          $('#Imagetv').hide();
          $("#Videotv").show();
          video.src = toplay;
          video.play();
          videoManager();
      }else if(playlist[value-2]=='image'){
          $("#Videotv").hide();
          $('#Imagetv').show();
          $('#targetTime').val(playlist[value-1]);
          image.src = toplay;
          startImageTime();
      }
}

  //mostra os campos
  function showFields(){
      $("#BtChamar").hide();
      $("#BtIntervalo").hide();
      $("#BtTerminar").hide();
      $("#BtChamarPS2").hide();
      $("#BtChamar").hide();
      $("#BtRechamar").show();
      $("#BtTransferir").show();
      $("#BtEspera").show();
      $("#BtDesistir").show();
      $("#Divsenha").show();
      $("#BtTerminarsenha").show();
      $("#DivInformativo").show(1000);
  }

  //esconde os campos
  function hideFields(){
     $("#BtRechamar").hide();
     $("#BtDesistir").hide();
     $("#BtTransferir").hide();
     $("#BtEspera").hide();
     $("#BtTerminarsenha").hide();
     $("#DivInformativo").hide(1000);
     $("#BtChamar").show();
     $("#Divsenha").hide();
     $("#BtChamarPS2").show();
     $("#BtIntervalo").show();
     $("#BtTerminar").show();
     $("#DivTransfSenha").hide(1000);
  }

window.onload = $(document).ready(function () {
                      var height = window.innerHeight;
                      var heightForm = height -70;
                      height = height -190;
                      var conteudo_atendedor = document.getElementById('DivAllContent');
                      var conteudo_erpForm = document.getElementById('erpForm');
                      conteudo_atendedor.style.height= height+'px';
                      conteudo_atendedor.style.overflowX = 'hidden';
                      conteudo_erpForm.style.height= heightForm+'px';
                      $("#erpFooter").hide();
                      $("#BtRechamar").hide();
                      $("#BtDesistir").hide();
                      $("#BtTransferir").hide();
                      $("#BtEspera").hide();
                      $("#BtTerminarsenha").hide();
                      $("#DivInformativo").hide();
                      $("#Divsenha").hide();
                      $("#DivTransfSenha").hide();
                  });

   $("#BtTransferir").click(function () {
            $("#DivInformativo").hide(1000);
            $("#DivTransfSenha").show(1000);
      });

  $("#BtComentario").click(function () {
        $('#ModalEspera').foundation('reveal', 'close');
        stopTime();
        hideFields();
  });

//change page a troca da paginaçao nos documentos, legislaçoes e outros
  function changepage(page){
    var strURL = "";
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
        }).fail(function(r){
        });
 }


//responsavel pelo controlo da lista de espera
EsperaManager();