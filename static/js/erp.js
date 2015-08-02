function return_url(funcNum, user, file_url){
  window.opener.CKEDITOR.tools.callFunction( funcNum, '/static/userfiles/' + user + '/' + file_url );
  close();
};


function link_anexo(anexo_file){
  $('#anexo_file').val(anexo_file);
  var button_name = $('#button_name').val()
  var path = $('#path').val()
  //alert(path);
  var anexo_file = $('#anexo_file').val()
  var strURL = '/link_anexo';
  $.ajax({type: 'POST', url: strURL, data: $('#mainForm').serialize()
      }).done(function(r) {
          //alert(button_name)
          window.opener.set_anexo(button_name, path, anexo_file);
          close();
      });
};


function set_anexo(button_name, path, anexo_file){
    //alert('im in set anexo');
    //alert(anexo_file);
    $('#' + button_name).val('/static/files/' + path + '/' + anexo_file);
    $('#img_' + button_name).attr('src','/static/files/' + path + '/' + anexo_file);
  };


//function openBrowser(button_name, obj, obj_key) {
//    window_id = $('#window_id').val();
//    var strURL = '/browse/'  + window_id + '/' + obj + '/' + obj_key + '/' + button_name + '/False?';
//    $.ajax({type: 'GET', url: strURL
//        }).done(function(r) {
//            OpenWindow=window.open("", "_blank");
//            OpenWindow.document.write(r);
//            OpenWindow.document.close();
//        });
//    };


//function openBrowser(button_name, obj, obj_key) {
//    window_id = $('#window_id').val();
//    var strURL = '/browse/'  + window_id + '/' + obj + '/' + obj_key + '/' + button_name + '/False?';
//    $.ajax({type: 'GET', url: strURL
//        }).done(function(r) {
//            OpenWindow=window.open("", "_blank");
//            OpenWindow.document.write(r);
//            OpenWindow.document.close();
//        });
//};


function openBrowser(button_name, obj, obj_key) {
    $('#message').html('');
    var strURL = '/browse/' + obj + '/' + obj_key + '/' + button_name + '/False?';
    $.ajax({type: 'POST', url: strURL
        }).done(function(r) {
            $('#popupContent').html(r);
            $('#popup').foundation('reveal', 'open');
        }).fail(function(r) {
            showMessage('alert', r.responseText, $('#message'), $('#message_container'));
        });
    };


  function mkdir() {
    var new_dir = $('#new_dir').val()
    var strURL = '/mkdir';
    $.ajax({type: 'POST', url: strURL, data: $('#mainForm').serialize()
        }).done(function(r) {
            $('#pastas_locais').append('<li><a href="#" onclick="chdir(\'userfiles\', \'' + new_dir + '\');">' + new_dir + '</a></li>');
            $('#dir_path').val('userfiles');
            $('#dir_name').val(new_dir);
            $('#dir_content').html('');
        }).fail(function(r) {
            showMessage('alert', r.responseText, $('#message'), $('#message_container'));
        });
  };


    function chdir(new_path) {
    var strURL = '/chdir/' + new_path;
    //$('#path').val(new_path);
    $.ajax({type: 'POST', url: strURL, data: $('#mainForm').serialize()
        }).done(function(r) {
            document.write(r);
            document.close();
        }).fail(function(r) {
            showMessage('alert', r.responseText, $('#message'), $('#message_container'));
        });
  };


    function showHelp(obj) {
      var strURL = '/show_help/' + obj;
      $.ajax({type: 'GET', url: strURL
        }).done(function(r) {
            OpenWindow=window.open("", "_blank");
            OpenWindow.document.write(r);
            OpenWindow.document.close();
        });
      };

            /*função que permite controlar o comportamento da tecla enter*/
            function handleEnter(e, type, name, option) {
                var charCode;
                if(e && e.which){
                    charCode = e.which;
                }else if(window.event){
                    e = window.event;
                    charCode = e.keyCode;
                    };
                if(charCode == 13) {
                    //alert("Enter was pressed");
                    switch(type){
                        case 'search':
                            var content_id = 'content';
                            if (option == 'True') {
                                content_id = 'popupContent';
                            };
                            filter(name, content_id, option);
                            break;
                        case 'calc':
                            run_calc();
                            break;
                        case 'choice':
                            choice(option, name);
                            break;
                        default:
                            alert('not one option!')
                    };
                    e.preventDefault();
                    };
                if(charCode == 9) {
                    alert("tab was pressed");
                    switch(type){
                        case 'choice':
                            $('#' + name + '_RealValue').val='';
                            choice(option,name);
                            break;
                        default:
                            alert('not one option!')
                    };
                    e.preventDefault();
                    };
                };

            function showMessage(type, message, id, container) {
                if (message == ''){
                    message = 'erro indeterminado!'
                }
                switch(type){
                    case 'alert':
                        container.removeClass('success').removeClass('info').removeClass('warning').addClass('alert');
                        container.show();
                        id.html(message);
                        break;
                    case 'warning':
                        container.removeClass('success').removeClass('info').removeClass('alert').addClass('warning');
                        container.show();
                        id.html(message);
                        break;
                    case 'success':
                        container.removeClass('alert').removeClass('info').removeClass('warning').addClass('success');
                        container.show();
                        id.html(message);
                        break;
                    default:
                            /*means its info*/
                        container.removeClass('success').removeClass('alert').removeClass('warning').addClass('info');
                        container.show();
                        id.html(message);
                        break;
                };
            };

            /*permite mudar o limite ou seja o numero de linhas por p´agina*/
            function change_limit(name, content_id, popup){
                $('#message').html('');
                var strURL = '/' + name + '/change_limit/' + popup;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#' + content_id).html(r);
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };

            /*activa ou desactiva as checkbox nas listas*/
            function toggle_lines(){
                $("[id*=lines]").each(function(){
                    if ($('#lines_controler').is(':checked')){
                        $(this).prop("checked", true);
                        }
                    else {
                        $(this).prop("checked", false);
                        }
                    });
                };

            /*controla o workflow*/
            function workflow(key, name, action) {
                $('#message').html('');
                var strURL = '/' + name + '/' + action + '/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#content').html(r);
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };

            /*imprime o documento base do objecto, um factura por exemplo*/
            function print_doc(key, name, action) {
                $('#message').html('');
                var strURL = '/' + name + '/' + action + '/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        OpenWindow=window.open("", "_blank");
                        OpenWindow.document.write(r);
                        OpenWindow.document.close();
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };

            /*Permite exportar os dados disponibilizados pelo objecto*/
            function export_doc(key, id, name, action) {
                $('#message').html('');
                var strURL = '/' + name + '/' + action + '/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#' + id).html(r);
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };

            //$('#erpForm')
             // .on('invalid', function () {
             //   var invalid_fields = $(this).find('[data-invalid]');
             //   console.log(invalid_fields);
             // })
             // .on('valid', function () {
             //   console.log('valid!');
             // });

            /*função que permitar usar filtros nos formulários de lista*/
            function filter(name, content_id, popup) {
                $('#message').html('');
                var form = $('#erpForm');
                if (popup == 'True') {
                    form = $('#popupForm');
                };
                var strURL = '/' + name + '/filter/' + popup;
                $.ajax({type: 'POST', url: strURL, data: form.serialize()
                    }).done(function(r) {
                        $('#' + content_id).html(r);
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };

            /*serve para a paginação nas listas*/
            function pages(page, name, content_id) {
                $('#message').html('');
                var strURL = '/' + name + '/get_page/' + page + '&' + content_id;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#' + content_id).html(r);
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };

            /*Serve para editar as listas, ambos os form e os field também permite refrescar
            no caso dos onchange dos campos
            aqui o argumento inputs da função pode ser 'form_list_action', 'list_field_action',
            'form_list_onchange', 'list_field_onchange' consoante o sitio de onde for invocado*/
            function listEdit(key, name, inputs, focus_id) {
                $('#message').html('');
                var strURL = '/' + name + '/' + inputs + '/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#' + key).html(r);/*key aqui na verdade é o id de destino*/
                        $('#' + focus_id).focus();
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                 };

            /*Abre ou refresca os formulários de edição*/
            function formEdit(key, name, action, content_id) {
                $('#message').html('');
                var strURL = '/' + name + '/' + action + '/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#' + content_id).html(r);
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                if (content_id=='popupContent') {
                    $('#popup').foundation('reveal', 'open');
                    };
                };

            function runEditOnchange(key, name, onchange_function, dynamic_atrs_function){
                $('#message').html('');
                //alert(onchange_function);
                //alert(dynamic_atrs_function);
                if (onchange_function != '' && onchange_function != 'False' && onchange_function != false) {
                    //alert('sou onchange');
                    //alert('/' + name + '/' + onchange_function + '/' + key);
                    var strURL = '/' + name + '/' + onchange_function + '/' + key;
                    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                        }).done(function(r) {
                            $.each(r,function(index, item) {
                                $('#' + index).val(item);
                                })
                        }).fail(function(r) {
                            showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                        });
                    }
                if (dynamic_atrs_function != '' && dynamic_atrs_function != 'False'  && dynamic_atrs_function != false) {
                    //alert('sou_dynamic_atrs')
                    var strURL = '/' + name + '/' + dynamic_atrs_function + '/' + key;
                    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                        }).done(function(r) {
                            $.each(r,function(index, item) {
                                $('#' + index).attr(item, true);
                                })
                        }).fail(function(r) {
                            showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                        });
                    }
                };


            /*permite editar um registo numa nova janela, o caso dos modelos que são do tipo edit*/
            function editNewWin(key, name, content_id) {
                $('#message').html('');
                var OpenWindow = window.open('./');
                $(OpenWindow).load( function(){
                    var strURL = '/' + name + '/editNewWin/' + key;
                    $.ajax({type: 'POST', url: strURL, data: $(OpenWindow.document.body).find('#erpForm').serialize()
                        }).done(function(r) {
                            $(OpenWindow.document.body).find('#' + content_id).html(r);
                        }).fail(function(r) {
                            parent.jQuery.$('#message_container').removeClass('success').removeClass('info').addClass('alert');
                            parent.jQuery.$('#message_container').show();
                            parent.jQuery.$('#message').html(r.responseText);
                        });
                    });
                $(OpenWindow).document.close();
                $(OpenWindow).setFocus();
                };

            /*Grava os registos, tanto das lista como dos formulários de edição aqui o id
            é o id do elemento html que será refrescado pelo ajax e a mensagem a que deverá aparecer no
            div message que está no formulário*/
            function save(key, name, id, message, popup) {
                var strURL = '/' + name + '/save/' + key;
                var myform = $('#erpForm');
                var mymessage_container = $('#message_container');
                var mymessage = $('#message');
                if (popup=='True') {
                    myform = $('#popupForm');
                    mymessage_container = $('#popup_message_container');
                    mymessage = $('#popup_message')
                    };
                mymessage.html('');
                $.ajax({type: 'POST', url: strURL, data: myform.serialize()
                    }).done(function(r) {
                        $('#' + id).html(r);
                        showMessage('success', message, mymessage, mymessage_container);
                        mymessage_container.delay(3000).slideUp();
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, mymessage, mymessage_container);
                    });
                $('#add_new').focus();
                };

            /*, function oncomplete() {$('add_new').focus();}    $('add_new').focus();*/

            /*remove registos, tanto de listas como de formulários de edição*/
            function del(key, name) {
                $('#message').html('');
                var strURL = '/' + name + '/remove/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#' + key).remove();
                        showMessage('success', 'Removido com Sucesso!', $('#message'), $('#message_container'));
                        $('#message_container').delay(3000).slideUp();
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };


            /*remove registos, tanto de listas como de formulários de edição*/
            function del_form(key, name) {
                $('#message').html('');
                var strURL = '/' + name + '/remove/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        window.close();
                        showMessage('success', 'Removido com Sucesso!', $('#message'), $('#message_container'));
                        $('#message_container').delay(3000).slideUp();
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };


            /*Adiciona elementos num list_field simples */
            function AddList(parent_key, model_real_name, name){
                $('#message').html('');
                var bodyName = 'ContentBody' + name
                var strURL = '/' + model_real_name + '/add_list/' + parent_key;
                $('#'+ bodyName).insert({'top':'<tr id="New"></tr>'});
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#content').html(r);
                        showMessage('success', 'Adicionado com Sucesso!', $('#message'), $('#message_container'));
                        $('#message_container').delay(3000).slideUp();
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };


            /*Remove elementos de uma lista many2many*/
            function DelList(key, model_real_name){
                $('#message').html('');
                var strURL = '/' + model_real_name + '/del_list/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#content').html(r);
                        showMessage('success', 'Removido com Sucesso', $('#message'), $('#message_container'));
                        $('#message_container').delay(3000).slideUp();
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };


            /*Adiciona elementos numa lista de many2many*/
            function AddM2M(name){
                $('#message').html('');
                var bodyName = 'ContentBody' + name
                var strURL = '/' + name + '/add_m2m/None';
                $('#' + bodyName).prepend('<tr id="New"></tr>');
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#content').html(r);
                        //showMessage('success', 'Adicionado com Sucesso!', $('#message'), $('#message_container'));
                        $('#message_container').delay(3000).slideUp();
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                     });
                };


            /*Remove elementos de uma lista many2many*/
            function DelM2M(key, name){
                $('#message').html('');
                var strURL = '/' + name + '/del_m2m/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#' + key).remove();
                        showMessage('success', 'Removido com Sucesso!', $('#message'), $('#message_container'));
                        $('#message_container').delay(3000).slideUp();
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };


            /*função que alimenta a calculadora*/
            function run_calc() {
                $('#message').html('');
                $.ajax({type: 'POST', url: '/calc', data: $('#sidebar').serialize()
                    }).done(function(r) {
                        $('#calc').html(r);
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };


            /*Permite exportar para CSV*/
            function exportCSV(name) {
                $('#message').html('');
                var strURL = '/' + name + '/export/key';
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#export').html(r);
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };


            /*Permite importar de CSV*/
            function importCSV(name) {
                $('#erpForm').enctype='multipart/form-data';
                $('#erpForm').action=name + '/import_csv/key';
                $('#erpForm').method='post';
                $('#erpForm').submit();
            };


            /*requisita e apresenta o relatório simple das listas*/
            function simpleReport(name) {
                var sData;
                var $inputs = $('#erpForm :input');
                sData = "<form name='simple_report' id='simple_report' action='/" + name + "/print_report/key' method='post'>";
                $inputs.each(function() {
                    sData += "<input value='" + $(this).val() + "' name='" + this.name + "' type='hidden'></input>";
                });
                sData += "</form>";
                sData += "<script type='text/javascript'>document.simple_report.submit();</sc" + "ript>";
                OpenWindow=window.open("", "_blank");
                OpenWindow.document.write(sData);
                OpenWindow.document.close()
            };


            /*realisa os calculos no ecrã de pagamento*/
            function calculos() {
                var valor = 0;
                $("input[id=metodos]").each(function() {
                    valor += Number($(this).val());
                });
                $('#total_entregue').val(valor);
                $('#troco').val(valor - Number($('#total_a_pagar').val()));
                };


            /*efectua o pagamento propriamente dito*/
            function pagamento(key, name) {
                $('#message').html('');
                var strURL = '/' + name + '/efectuar_pagamento/' + key;
                $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        $('#content').html(r);
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                };


            function hideSideBar() {
                $('#content').style.width="98%";
                $('#SideBarContent').style.visibility="hidden";
                $('#SideBar').style.width="10px";
            };

            function showSideBar() {
                $('#content').style.width="80%";
                $('#SideBarContent').style.visibility="visible";
                $('#SideBar').style.width="18%";
            };


            /*Função para os choice_field depois criar um onchange que quando o campo volta a não ter valores torna a por o icon original, a lupinha, mariquice mas fica fixe e é mais claro para o utilizador
            recebe model que é o modelo, name que é o nome do campo e name_value que é o valor passado*/
            function choice(model, name) {
                $('#message').html('');
                var value = $('#' + name + '_value').val();
                if (value) {
                    var strURL = '/' + model + '/get_option/' + name + '&' + value;
                    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                    }).done(function(r) {
                        if (r instanceof Array) {
                            if (r[1] != null){
                                $('#' + name + '_value').val(r[0]);
                                $('#' + name + '_RealValue').val(r[1]);
                                $('#' + name + '_img').removeClass('glyphicon glyphicon-search').addClass('glyphicon glyphicon-ok');
                                $('#' + name + '_RealValue').onchange();
                                }
                            else {
                                alert('no json');
                                };
                            }
                        else {
                            $('#popupContent').html(r);
                            $('#popup').foundation('reveal', 'open');
                        };
                    }).fail(function(r) {
                        showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                    });
                }
                else {
                    var strURL = '/' + model + '/get_option/' + name + '&None';
                    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
                        }).done(function(r) {
                            $('#popupContent').html(r);
                        }).fail(function(r) {
                            showMessage('alert', r.responseText, $('#message'), $('#message_container'));
                        });
                    $('#popup').foundation('reveal', 'open');
                }
            };

            /*Função que é chamada pelo botão apply do popup que permite escolher um determinado registo*/
            function select_key(key, value, name) {
                $('#' + name + '_value').val(value);
                $('#' + name + '_RealValue').val(key);
                $('#' + name + '_img').removeClass('glyphicon glyphicon-search').addClass('glyphicon glyphicon-ok');
                $('#popup').foundation('reveal', 'close');
                $('#' + name + '_RealValue').change();
            };
