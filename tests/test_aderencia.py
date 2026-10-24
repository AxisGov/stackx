#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path


HOOK = Path(__file__).parents[1] / ".claude" / "hooks" / "stackx" / "aderencia.py"
SPEC = importlib.util.spec_from_file_location("stackx_aderencia", HOOK)
MODULO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULO)


class CaminhoDaEntradaTest(unittest.TestCase):
    def test_notebook_edit_snake_case(self):
        self.assertEqual(
            MODULO.caminho_da_entrada({"notebook_path": "notebooks/a.ipynb"}),
            "notebooks/a.ipynb",
        )

    def test_notebook_edit_camel_case(self):
        self.assertEqual(
            MODULO.caminho_da_entrada({"notebookPath": "notebooks/b.ipynb"}),
            "notebooks/b.ipynb",
        )

    def test_write_continua_compativel(self):
        self.assertEqual(
            MODULO.caminho_da_entrada({"file_path": "src/app.py"}),
            "src/app.py",
        )


class SegredoAparenteTest(unittest.TestCase):
    # CodeAnt em katosmv/conselhos-municipais#208: o detector parava na linha 400.
    def test_credencial_depois_da_linha_400_e_detectada(self):
        conteudo = "x = 1\n" * 450 + 'API_KEY = "abcdefgh12345678"\n'
        self.assertEqual(MODULO.linha_de_segredo(conteudo), 451)

    def test_credencial_no_comeco_continua_detectada(self):
        self.assertEqual(MODULO.linha_de_segredo('TOKEN: "abcdefgh12345678"\n'), 1)

    def test_leitura_de_ambiente_nao_e_segredo(self):
        self.assertIsNone(MODULO.linha_de_segredo('API_KEY = os.environ.get("API_KEY", "abcdefgh12")\n'))

    def test_interpolacao_de_ambiente_casa_a_regex_e_nao_e_segredo(self):
        # Casa com SEGREDO (valor entre aspas com 8+ caracteres): quem decide e a exclusao.
        linha = 'TOKEN: "${process.env.TOKEN}"\n'
        self.assertIsNotNone(MODULO.SEGREDO.search(linha))
        self.assertIsNone(MODULO.linha_de_segredo(linha))


if __name__ == "__main__":
    unittest.main()
