import contextlib
import io
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from modulos.dados import carregar_dados, dados
from modulos import analises


class TestSCIC(unittest.TestCase):
    def test_validacao_csv(self):
        for coluna, valor in [('corrente', float('inf')), ('id', 0), ('prioridade', 4), ('modulo', '')]:
            invalido = dados.copy()
            invalido.loc[0, coluna] = valor
            with tempfile.TemporaryDirectory() as pasta:
                arquivo = Path(pasta) / 'dados.csv'
                invalido.to_csv(arquivo, index=False)
                with self.assertRaises(ValueError):
                    carregar_dados(arquivo)

    def test_zero_e_limites_de_erro(self):
        original = analises.dados
        analises.dados = original.copy()
        analises.dados.loc[0, 'latencia_prevista'] = 0
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                analises.calcular_indicadores()
            self.assertEqual(analises.dados.loc[0, 'situacao_erro'], 'Indefinido')
            self.assertEqual(analises.classificar_erro(10), 'Atencao')
            self.assertEqual(analises.classificar_erro(25), 'Critico')
        finally:
            analises.dados = original

    def test_baseline_perfeito(self):
        original = analises.dados
        analises.dados = original.copy()
        analises.dados['latencia_observada'] = analises.dados['latencia_prevista']
        try:
            saida = io.StringIO()
            with contextlib.redirect_stdout(saida):
                analises.avaliar_desempenho()
            self.assertIn('erro original igual a zero', saida.getvalue())
        finally:
            analises.dados = original


if __name__ == '__main__':
    unittest.main()
