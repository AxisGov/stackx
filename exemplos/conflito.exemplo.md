# Exemplo — apresentação de conflito

> Projeto fictício `pedidos-api`, o mesmo de `CONVENCOES.exemplo.md`.
>
> **Este é o caso que prova por que a skill não escolhe sozinha: o dialeto
> majoritário é o antigo, e o minoritário é o novo padrão.**

---

## Foram encontrados 2 conflitos. Preciso da sua decisão em ambos.

---

### CONFLITO 1 — Local do arquivo de teste

| Dialeto | Arquivos | Onde | Nascido | Último novo | Último toque |
| ------- | -------- | ---- | ------- | ----------- | ------------ |
| A — co-localizado | **34** | `src/**/*.test.ts` | 2023-04 | 2025-08 | 2026-02 |
| B — pasta espelhada | **9** | `tests/**/*.test.ts` | 2025-09 | 2026-03 | 2026-03 |

Exemplo A: `src/pedidos/criar-pedido.test.ts:1`
Exemplo B: `tests/faturamento/emitir-nota.test.ts:1`

**Sinal do histórico:** o dialeto A tem quase quatro vezes mais arquivos, mas não
recebe arquivo novo desde agosto de 2025. Os 9 arquivos criados nos últimos 6
meses seguem B, sem exceção — inclusive os 4 do módulo de faturamento, o mais
recente do projeto. Os toques em A desde setembro de 2025 são todos edições de
testes existentes, nenhum arquivo novo.

**Observação sobre a configuração do runner:** o `include` do Vitest
(`vitest.config.ts:8`) casa os dois padrões, então os dois grupos rodam. Não há
teste morto aqui.

**Qual adotar para código novo?**

```
(1) A — co-localizado, ao lado do código
(2) B — pasta espelhada em tests/
(3) manter os dois, decidir por área
(4) adiar — fica como CONFLITO EM ABERTO
```

> **Por que este conflito não pode ser resolvido pela contagem.** Adotar A por
> ser majoritário significaria escolher o padrão que o time abandonou há sete
> meses, e mandar todo código novo contrariar a direção real do projeto. A
> contagem descreve o passado; a data do último arquivo novo descreve a decisão
> em vigor. Só quem trabalha no projeto sabe se B é um padrão adotado
> deliberadamente ou uma inconsistência que passou na revisão — e é por isso que
> a pergunta existe.

---

### CONFLITO 2 — Montagem de dado de teste

| Dialeto | Arquivos | Onde | Nascido | Último novo | Último toque |
| ------- | -------- | ---- | ------- | ----------- | ------------ |
| A — factory | **36** | `src/testes/fabricas/` | 2023-04 | 2026-03 | 2026-03 |
| B — objeto literal na mão | 7 | `src/pagamentos/**` | 2023-06 | 2024-11 | 2024-11 |

Exemplo A: `src/pedidos/criar-pedido.test.ts:14`
Exemplo B: `src/pagamentos/estornar.test.ts:9`

**Sinal do histórico:** aqui o padrão é o inverso do CONFLITO 1 — o majoritário
também é o mais recente. B está concentrado num único módulo e parado desde
novembro de 2024.

**Qual adotar para código novo?**

```
(1) A — factory em src/testes/fabricas/
(2) B — objeto literal no próprio teste
(3) manter os dois, decidir por área
(4) adiar — fica como CONFLITO EM ABERTO
```

---

## Depois da resposta

**CONFLITO 1 — adiado (opção 4).** Gravado em `docs/stack/CONVENCOES.md` §3:

```markdown
> **CONFLITO EM ABERTO** — o repositório faz isto de duas formas. Ver
> `docs/stack/LACUNAS.md`. Enquanto não houver decisão, siga o padrão do
> arquivo vizinho e registre a escolha na task.
```

E em `docs/stack/LACUNAS.md`, seção "Conflitos em aberto":

| ID | Ponto | Dialetos | Apresentado em |
| -- | ----- | -------- | -------------- |
| C-01 | §3 local do arquivo de teste | co-localizado (34) × pasta espelhada (9, todos recentes) | 2026-03-11 |

Consequência prática enquanto estiver em aberto: `/stackx-check` emite `AVISO`
para qualquer um dos dois padrões, nunca violação. O sprintx levanta a questão na
descoberta de qualquer feature que crie teste.

**CONFLITO 2 — decidido, opção 1.** Gravado em §3:

```markdown
Dado de teste é montado por factory em `src/testes/fabricas/`.

Decidido por ana em 2026-03-11. Dialeto anterior: objeto literal na mão em
`src/pagamentos/**`, não replicar.
**Evidência:** `src/testes/fabricas/pedido.ts:1`, `src/pedidos/criar-pedido.test.ts:14`
```

E na tabela "Decisões registradas" do CONVENCOES.md.

Consequência prática: a partir daqui, teste novo com objeto literal gera violação
`ALTO` em `/stackx-check`. Os 7 arquivos existentes em `src/pagamentos/` **não**
são realinhados — a decisão vale para código novo.
