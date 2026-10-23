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


if __name__ == "__main__":
    unittest.main()
