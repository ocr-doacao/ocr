from django.test import TestCase
from ocrDoacao.models import Ong

class OngTest(TestCase):
    def test_get_path(self):
        nome_modulo = __name__.split(".")[0]
        ong = Ong()
        ong.nome = 'teste_ong'
        self.assertEqual(ong.get_path(), nome_modulo + '/static/ongs/teste_ong')