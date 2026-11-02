#!/usr/bin/env python3
"""O cartógrafo procura o roteiro onde ele existe.

Revisão do CodeAnt no expxdev#130: a busca alternativa citava `.opencode/skill/stackx/`,
que nenhuma instalação cria (as skills ficam em `.claude/skills/` nos dois harnesses), e
repetia o caminho principal. A alternativa útil é a cópia do plugin do `expx init`.
"""
import unittest
from pathlib import Path

RAIZ = Path(__file__).parents[1]
AGENTES = [RAIZ / ".claude" / "agents" / "stackx-cartografo.md", RAIZ / ".opencode" / "agent" / "stackx-cartografo.md"]


class CaminhoDoRoteiroTest(unittest.TestCase):
    def test_a_busca_alternativa_aponta_para_onde_o_roteiro_existe(self):
        for agente in AGENTES:
            with self.subTest(agente=str(agente.relative_to(RAIZ))):
                texto = agente.read_text(encoding="utf-8")
                self.assertNotIn(".opencode/skill/", texto)
                self.assertIn(".expx/marketplace/plugins/expx/skills/stackx/", texto)

    def test_o_caminho_principal_existe_na_skill(self):
        self.assertTrue((RAIZ / ".claude" / "skills" / "stackx" / "references" / "01-deteccao.md").is_file())


if __name__ == "__main__":
    unittest.main()
