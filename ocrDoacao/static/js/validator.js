var data_invalida = 0;
var data_fora_prazo = 1;
var data_valida = 2;
    
function validaCNPJ(cnpj) {
    var tamanho, numeros, digitos, soma, pos, resultado, i;
    cnpj = cnpj.replace(/[^\d]+/g,'');
 
    if(cnpj == '') return false;
     
    if (cnpj.length != 14)
        return false;
 
    // Elimina CNPJs invalidos conhecidos
    if (cnpj == "00000000000000" || 
        cnpj == "11111111111111" || 
        cnpj == "22222222222222" || 
        cnpj == "33333333333333" || 
        cnpj == "44444444444444" || 
        cnpj == "55555555555555" || 
        cnpj == "66666666666666" || 
        cnpj == "77777777777777" || 
        cnpj == "88888888888888" || 
        cnpj == "99999999999999")
        return false;
         
    // Valida DVs
    tamanho = cnpj.length - 2
    numeros = cnpj.substring(0,tamanho);
    digitos = cnpj.substring(tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(0))
        return false;
         
    tamanho = tamanho + 1;
    numeros = cnpj.substring(0,tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(1))
          return false;
           
    return true;
    
}

function validaValor(valor) {
    valor = parseFloat(valor);
    
    if(!valor) { 
        return false;
    }
    
    return true;
}

function validaData(data) {
    var data_split = data.split('/');
    var dia = parseInt(data_split[0], 10);
    var mes = parseInt(data_split[1], 10);
    var ano = parseInt(data_split[2], 10);
    var novaData = new Date(ano,mes-1,dia);
    var hoje = new Date();
    var primeiro_dia_valido;

    if (ano.toString().length != 4)
        return data_invalida;
    if (novaData.getFullYear() != ano || novaData.getMonth() + 1 != mes || novaData.getDate() != dia) 
        return data_invalida;
    if (novaData > hoje)
        return data_invalida;
    if (hoje.getDate() < 20) {
        if (hoje.getMonth() > 0 ) {
            primeiro_dia_valido = new Date(hoje.getFullYear(), hoje.getMonth() - 1, 1);
        } else {
            primeiro_dia_valido = new Date(hoje.getFullYear() - 1, 11, 1);
        }
    } else {
        primeiro_dia_valido = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    }
    if (primeiro_dia_valido > novaData) {
        return data_fora_prazo;
    }
    return data_valida;
}

function validaCOO(coo) {
    
    if(coo.length < 6)
        return false;
        
    return true;
}

$(document).ready(function() {
    var erro = false;
    $("#data").mask("00/00/0000");
    $("#valor").mask("###0.00", { reverse: true });
    $("#coo").mask("000000");
    $("#cnpj").mask("00.000.000/0000-00");
    $("form").submit(function(e) {
        var data = $("#data").val();
        var valor = $("#valor").val();
        var coo = $("#coo").val();
        var cnpj = $("#cnpj").val();
        if (data == null || data == "" ||
            valor == null || valor == "" ||
            coo == null ||  coo == "" ||
            cnpj == null || cnpj == "")
        {
            if (!erro){
                erro = true;
                $("#erro").prepend("<p class='validation_error'>* Todos os campos são obrigatórios</p>");
            }
            e.preventDefault();
        }
    });
    var msg_erros = {};
    msg_erros['#cnpj'] = '* CNPJ inválido.';
    msg_erros['#coo'] = '* COO inválido.';
    msg_erros['#valor'] = '* Valor inválido.';
    msg_erros['#data'] = [];
    msg_erros['#data'][0] = '* Data inválida.';
    msg_erros['#data'][1] = '* Data fora do prazo de doação';
    
    var funcoes_validacao = {};
    funcoes_validacao['#cnpj'] = validaCNPJ;
    funcoes_validacao['#coo'] = validaCOO;
    funcoes_validacao['#data'] = validaData;
    funcoes_validacao['#valor'] = validaValor;
    
    $.fn.extend({
        pegaId: function () {
            return '#' + $(this).attr('id');
        },
        mostraErro: function (msg) {
            var id = $(this).pegaId();
            if (typeof msg === 'undefined') {
                msg = msg_erros[id];   
            }
            $(id).adicionaClasse('has-error');
            $(id + ' + p').text(msg);
       },
       mostraSucesso: function () {
            var id = $(this).pegaId(); 
            $(id).adicionaClasse('has-success');
            $(id + ' + p').text('');
       },
       adicionaClasse: function (classe) {
           $(this).closest('.form-group').addClass(classe);
       },
       removeClasse: function (classe) {
           $(this).closest('.form-group').removeClass(classe);
       }
    });
    
    $('form').submit(function (e) {
        var cnpj, valor, coo, data;
        var notaValida = true;
        cnpj = $('#cnpj').val();
        coo = $('#coo').val();
        valor = $('#valor').val();
        data = $('#data').val();
        
        $('.form-group p').text('');
        $('.form-group').removeClass('has-error').removeClass('has-success');
        if (!validaCNPJ(cnpj)) {
            $('#cnpj').mostraErro();
            notaValida = false;
        } else {
            $('#cnpj').mostraSucesso();
        }
        if (!validaCOO(coo)) {
            $('#coo').mostraErro();
            notaValida = false;
        } else {
            $('#coo').mostraSucesso();
        }var data_validada = validaData(data);
        
        if (data_validada != data_valida) {
            $('#data').mostraErro(msg_erros[data_validada]);
            notaValida = false;
        } else {
            $('#data').mostraSucesso();
        }
        if (!validaValor(valor)) {
            $('#valor').mostraErro();
            notaValida = false;
        } else {
            $('#valor').mostraSucesso(); 
        }
        if (!notaValida) {
            e.preventDefault();
        }            
    });
    
    $('input[type=text]').focusout(function () {
        var valor_elemento = $(this).val();
        var id = $(this).pegaId();
        var funcao_validacao = funcoes_validacao[id];
        var elemento_valido;
        $(this).removeClasse('has-success');
        $(this).removeClasse('has-error');
        elemento_valido = funcao_validacao(valor_elemento);
        if (typeof elemento_valido === 'number' && elemento_valido != data_valida) { // para datas
            $(this).mostraErro(msg_erros['#data'][elemento_valido]);
        } else if (!elemento_valido) {
            $(this).mostraErro();
        } else {
            $(this).mostraSucesso();
        }
    });

});