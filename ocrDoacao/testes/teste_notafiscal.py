from django.test import TestCase
from ocrDoacao.models import NotaFiscal
import datetime

class NotaFiscalTest(TestCase):
    
    def test_validacao_cnpj(self):
        validacao = NotaFiscal.validaCNPJ('11.111.111/1111-11')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaCNPJ('12.aaa11a/1111-a11')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaCNPJ('36.564.851/0001-04')
        self.assertEqual(validacao, True)
        
    def test_validacao_coo(self):
        validacao = NotaFiscal.validaCOO('1')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaCOO('12')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaCOO('123')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaCOO('1234')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaCOO('12345')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaCOO('123456')
        self.assertEqual(validacao, True)
        validacao = NotaFiscal.validaCOO('abcs23')
        self.assertEqual(validacao, False)
    
    def test_validacao_valor(self):
        validacao = NotaFiscal.validaValor('0')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaValor('a.01')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaValor('-10')
        self.assertEqual(validacao, False)
        validacao = NotaFiscal.validaValor('0.1')
        self.assertEqual(validacao, True)
        validacao = NotaFiscal.validaValor('10')
        self.assertEqual(validacao, True)
        
    def test_validacao_data(self):
        hoje = datetime.datetime.now()
        amanha = datetime.datetime(hoje.year, hoje.month, hoje.day + 1)
        mes_passado = datetime.datetime(hoje.year, hoje.month - 1, 1)
        dois_meses_atras = datetime.datetime(hoje.year, hoje.month - 2, 1)
        formato_data = '%d/%m/%Y'
        validacao = NotaFiscal.validaData(hoje.strftime('%d-%m-%Y'))
        self.assertEqual(validacao, 0)
        
        validacao = NotaFiscal.validaData('')
        self.assertEqual(validacao, 0)
        
        validacao = NotaFiscal.validaData('string')
        self.assertEqual(validacao, 0)
        
        validacao = NotaFiscal.validaData(dois_meses_atras.strftime(formato_data))
        self.assertEqual(validacao, 1)
        
        validacao = NotaFiscal.validaData('01/01/2015')
        self.assertEqual(validacao, 1)
        
        if (hoje.day <= 20):
            validacao = NotaFiscal.validaData(mes_passado.strftime(formato_data))
            self.assertEqual(validacao, 2)
        else:
            validacao = NotaFiscal.validaData(mes_passado.strftime(formato_data))
            self.assertEqual(validacao, 1)
        
        validacao = NotaFiscal.validaData(hoje.strftime(formato_data))
        self.assertEqual(validacao, 2)