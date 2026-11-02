#!/usr/bin/env python3
"""Todo agente Claude da skill declara `classe:`.

Com `.expx/orquestracao.json` ativo, o ExpxDev resolve o modelo de cada agente pela
classe. `model: inherit` não tem classe, e sem `classe:` o `expx init` falha com
`sem_classe` (achado do Conselhos na 0.13.0). Os agentes do OpenCode não são
instalados pelo `expx init` e ficam fora.
"""
import re
import unittest
from pathlib import Path

AGENTES = sorted((Path(__file__).parents[1] / ".claude" / "agents").glob("*.md"))
CLASSES = {"mecanico_triagem", "raciocinio_normal", "profundo_excepcional"}


def frontmatter(texto):
    m = re.match(r"---\n(.*?)\n---\n", texto, re.S)
    return m.group(1) if m else ""


class ClasseDosAgentesTest(unittest.TestCase):
    def test_frontmatter_aberto_nao_conta_e_comentario_sai_do_valor(self):
        self.assertEqual(frontmatter("---\nname: x\n\nclasse: raciocinio_normal\n"), "")
        m = re.search(r"^classe:[ \t]*(\S+)(?:[ \t]+#.*)?[ \t]*$", frontmatter("---\nclasse: raciocinio_normal # nota\n---\n"), re.M)
        self.assertEqual(m.group(1), "raciocinio_normal")

    def test_ha_agentes(self):
        self.assertTrue(AGENTES)

    def test_todo_agente_declara_classe_do_vocabulario(self):
        for agente in AGENTES:
            with self.subTest(agente=agente.name):
                # comentário no fim da linha é YAML válido e sai do valor
                m = re.search(r"^classe:[ \t]*(\S+)(?:[ \t]+#.*)?[ \t]*$", frontmatter(agente.read_text(encoding="utf-8")), re.M)
                self.assertIsNotNone(m, f"{agente.name} sem classe:")
                self.assertIn(m.group(1), CLASSES)


if __name__ == "__main__":
    unittest.main()
