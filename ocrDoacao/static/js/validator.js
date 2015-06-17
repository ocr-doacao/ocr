function validaCNPJ(cnpj) {
 
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
    var data = data.split('/');
    var dia = parseInt(data[0], 10);
    var mes = parseInt(data[1], 10);
    var ano = parseInt(data[2], 10);
    var novaData = new Date(ano,mes-1,dia);
    var hoje = new Date();

    if (ano.toString().length != 4)
        return false;
    if (novaData.getFullYear() != ano || novaData.getMonth() + 1 != mes || novaData.getDate() != dia) 
        return false;
    if (novaData > hoje)
        return false;
    
    return true;
    
}

function validaCOO(coo) {
    
    if(coo.length < 6)
        return false;
        
    return true;
}