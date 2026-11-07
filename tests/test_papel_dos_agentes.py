#!/usr/bin/env python3
"""Todo agente Claude da skill declara `papel:`, e o papel é o decidido para ele.

A F4 do ExpxDev vai decidir pelo papel, e não pelo nome, quais agentes passam
pela integridade final e rodam em primeiro plano: `revisar` e `testar`
(CONTRATO-expx-orquestracao §2.2, §12.2 e §13.1). Sem `papel:`, o agente
deixará de ser verificado sem nenhum erro. Os agentes do OpenCode não são instalados pelo
`expx init` e ficam fora.
"""
import re
import unittest
from pathlib import Path

AGENTES = sorted((Path(__file__).parents[1] / ".claude" / "agents").glob("*.md"))
PAPEIS = {"planejar", "implementar", "investigar", "testar", "revisar"}
# O papel de cada agente, pelo nome do arquivo. Agente novo entra aqui.
ESPERADO = {"stackx-cartografo": "investigar"}


def frontmatter(texto):
    m = re.match(r"---\n(.*?)\n---\n", texto, re.S)
    return m.group(1) if m else ""


def papel(texto):
    # Como o YAML lê a linha: `papel:x` sem espaço não é a chave, as aspas delimitam
    # o valor, e o comentário no fim sai dele.
    m = re.search(r"^papel:[ \t]+(\S+)(?:[ \t]+#.*)?[ \t]*$", frontmatter(texto), re.M)
    if not m:
        return None
    v = m.group(1)
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'" else v


class PapelDosAgentesTest(unittest.TestCase):
    def test_frontmatter_aberto_nao_conta_e_comentario_sai_do_valor(self):
        self.assertIsNone(papel("---\nname: x\n\npapel: investigar\n"))
        self.assertEqual(papel("---\npapel: investigar # nota\n---\n"), "investigar")

    def test_valor_entre_aspas_e_o_mesmo_e_sem_espaco_nao_e_chave(self):
        # YAML: as aspas delimitam o valor; `papel:x` sem espaço é um texto, não a chave
        self.assertEqual(papel('---\npapel: "investigar"\n---\n'), "investigar")
        self.assertEqual(papel("---\npapel: 'investigar' # nota\n---\n"), "investigar")
        self.assertIsNone(papel("---\npapel:investigar\n---\n"))

    def test_ha_agentes(self):
        self.assertTrue(AGENTES)

    def test_todo_agente_declara_o_papel_decidido(self):
        for agente in AGENTES:
            with self.subTest(agente=agente.name):
                p = papel(agente.read_text(encoding="utf-8"))
                self.assertIsNotNone(p, f"{agente.name} sem papel:")
                self.assertIn(p, PAPEIS)
                self.assertEqual(p, ESPERADO.get(agente.stem), f"{agente.name}: papel sem decisão neste teste ou diferente do decidido")


if __name__ == "__main__":
    unittest.main()
