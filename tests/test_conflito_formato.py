#!/usr/bin/env python3
"""O formato da apresentação de conflito vale para dois ou mais dialetos.

Achado M2 do CodeAnt em katosmv/conselhos-municipais#208: o formato só previa as linhas
A/B e as opções (1)–(4), e um terceiro dialeto não tinha linha na tabela nem opção de
escolha. Teste de documento: fixa o contrato no reference e no template.
"""
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).parents[1] / ".claude" / "skills" / "stackx"
REFERENCE = (RAIZ / "references" / "03-conflito-e-lacuna.md").read_text(encoding="utf-8")
TEMPLATE = (RAIZ / "assets" / "TEMPLATE-conflito.md").read_text(encoding="utf-8")


def secao(texto, titulo):
    inicio = texto.index(titulo)
    fim = texto.find("\n## ", inicio + len(titulo))
    return texto[inicio:fim if fim != -1 else len(texto)]


class ConflitoComNDialetosTest(unittest.TestCase):
    def test_reference_declara_a_regra_de_n_dialetos(self):
        formato = secao(REFERENCE, "## Formato exato da apresentação")
        self.assertIn("dois ou mais dialetos", formato)
        self.assertRegex(formato, r"cada dialeto[^.]*linha na tabela[^.]*exemplo[^.]*opção")

    def test_exemplo_do_reference_tem_tres_dialetos_e_as_opcoes_fixas_depois(self):
        formato = secao(REFERENCE, "## Formato exato da apresentação")
        for letra in "ABC":
            self.assertRegex(formato, rf"\| {letra} — ")
            self.assertIn(f"Exemplo {letra}:", formato)
        opcoes = re.findall(r"^\s*\((\d+)\) (.+)$", formato, re.M)
        self.assertEqual([n for n, _ in opcoes], ["1", "2", "3", "4", "5"])
        self.assertTrue(opcoes[0][1].startswith("A — "))
        self.assertTrue(opcoes[2][1].startswith("C — "))
        self.assertIn("manter vários, decidir por área", opcoes[3][1])
        self.assertIn("adiar", opcoes[4][1])

    def test_nenhuma_formulacao_binaria_sobra(self):
        for nome, texto in (("reference", REFERENCE), ("template", TEMPLATE)):
            with self.subTest(arquivo=nome):
                self.assertNotIn("de duas formas", texto)
                self.assertNotRegex(texto, r"opções reais encontradas \+ \"manter os dois")

    def test_template_repete_por_dialeto_e_ordena_dialetos_manter_adiar(self):
        self.assertIn("uma linha por dialeto", TEMPLATE)
        self.assertIn("um exemplo por dialeto", TEMPLATE)
        bloco = TEMPLATE[TEMPLATE.index("**Qual adotar para código novo?**"):]
        bloco = bloco[:bloco.index("```", bloco.index("```") + 3)]
        linhas = [l.strip() for l in bloco.splitlines() if l.strip().startswith("(")]
        self.assertTrue(linhas[0].startswith("(1) A — "))
        self.assertTrue(any("um por dialeto" in l or "<n>" in l for l in linhas))
        i_manter = next(i for i, l in enumerate(linhas) if "manter" in l)
        i_adiar = next(i for i, l in enumerate(linhas) if "adiar" in l)
        self.assertLess(i_manter, i_adiar)
        self.assertEqual(i_adiar, len(linhas) - 1)


if __name__ == "__main__":
    unittest.main()
