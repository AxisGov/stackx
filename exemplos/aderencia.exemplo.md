# Exemplo — verificação de aderência

> Projeto fictício `pedidos-api`, o mesmo de `CONVENCOES.exemplo.md`.
> Diff de uma feature que adiciona estorno parcial de pagamento.
>
> Mostra as cinco severidades e, em especial, a diferença entre violar uma
> convenção **com evidência** e divergir de um ponto marcado **PROPOSTA**.

---

## Verificação de aderência — `git diff main...feat/estorno-parcial`

CONVENCOES.md: `docs/stack/CONVENCOES.md` (gerado em 2026-03-11, commit 7f3a91c)
Contexto: projeto legado — PERFIL.md ativo na área `src/pagamentos/`
Alvo: diff `main...feat/estorno-parcial`
Arquivos no alvo: 8 (5 novos, 3 modificados)

| Severidade | Arquivo | Convenção violada | Correção sugerida |
| ---------- | ------- | ----------------- | ----------------- |
| CRÍTICO | `src/casos/estornar-parcial.ts:47` | §6 log — `cartao` não pode ir para o log; o campo é redigido em `src/infra/log/logger.ts:11` mas aqui é interpolado na mensagem, escapando da redaction | Passar como campo estruturado, ou remover. Redaction não alcança string interpolada. |
| CRÍTICO | `tests/pagamentos/estornar-parcial.test.ts:22` | §4 isolamento — o teste faz `TRUNCATE` no `afterEach`; a convenção é transação com rollback, e o runner roda 4 workers em `pool: 'forks'` | Remover o `TRUNCATE` e usar o helper `comTransacao()` de `vitest.setup.ts:22`. O truncate apaga o dado dos outros 3 workers. |
| ALTO | `src/casos/estornar-parcial.ts:31` | §6 padrão de erro — a convenção é `Result<T, E>` nos casos de uso (41 de 41); aqui há `throw new Error(...)` | Retornar `err(new EstornoRecusado(...))`, com `EstornoRecusado` herdando de `ErroDominio` |
| ALTO | `src/casos/estornar-parcial.ts:8` | §5 camadas — `casos` não importa de `infra`; a regra de lint em `eslint.config.js:34` foi suprimida com `eslint-disable-next-line` | Injetar via porta `RepositorioPagamento` (`src/portas/`), como em `src/casos/criar-pedido.ts:6` |
| MÉDIO | `tests/pagamentos/estornar-parcial.test.ts:14` | §3 montagem de dado — a convenção é factory (decidida em 2026-03-11); aqui há objeto literal na mão | Usar `fabricaPagamento()` de `src/testes/fabricas/pagamento.ts` |
| AVISO | `tests/pagamentos/estornar-parcial.test.ts:1` | §3 local do arquivo de teste — **CONFLITO EM ABERTO** (co-localizado × pasta espelhada) | Nenhuma ação exigida. O arquivo segue o dialeto B; registre a escolha na task. |
| AVISO | `src/casos/estornar-parcial.ts:1` | §6 ordem de imports — ponto marcado **PROPOSTA**, sem evidência no repositório | Nenhuma ação exigida. |
| INFO | `src/pagamentos/processador.ts:88` | Arquivo MODIFICADO em área do PERFIL.md; o padrão local usa exceção, o CONVENCOES.md §6 registra `Result` | Manter o padrão local. Não alinhar — modernização é colateral proibido. |

**Veredito:** 2 CRÍTICO, 2 ALTO, 1 MÉDIO, 2 AVISO, 1 INFO — a task **não pode
fechar**.

**Comando de teste executado:** `pnpm vitest run tests/pagamentos/` ✗ divergente
de §2, que declara `pnpm test` para a suíte inteira. Como o diff toca `src/casos/`
e `src/pagamentos/`, rodar só uma pasta não exercita os consumidores. `AVISO`.

---

## Como ler este resultado

**O par que importa.** As duas últimas linhas de teste divergem de pontos do
CONVENCOES.md, e o tratamento é oposto:

| Linha | Ponto | Estado no CONVENCOES.md | Severidade |
| ----- | ----- | ----------------------- | ---------- |
| `tests/…:14` montagem de dado | factory | **convenção com evidência** (`src/testes/fabricas/pedido.ts:1`, decidida por ana) | `MÉDIO` — violação |
| `tests/…:1` local do teste | co-localizado × espelhado | **CONFLITO EM ABERTO** | `AVISO` — não é violação |
| `src/…:1` ordem de imports | — | **PROPOSTA**, sem evidência | `AVISO` — não é violação |

É a regra 3 em ação: PROPOSTA não governa, e por isso nunca passa de `AVISO`.
Convenção com evidência governa, e por isso vira violação. O que separa as duas
não é a importância do ponto — é a existência de evidência no código.

**Os dois CRÍTICOS não são "estilo".** O `TRUNCATE` quebra a suíte de forma
intermitente para os outros três workers, e o sintoma vai aparecer num teste que
não tem nada a ver com estorno. O `cartao` interpolado escapa da redaction do
logger — a proteção existe e foi contornada sem intenção.

**O INFO é o legadox.** `src/pagamentos/processador.ts` é arquivo existente em
área tocada descrita no PERFIL.md: ali manda o padrão local, mesmo contrariando
o §6. A tabela registra a divergência para quem lê, e não sugere correção. **Não
existe linha nenhuma pedindo para alinhar o arquivo** — nem "para depois".

**A verificação não corrigiu nada.** Nenhum dos 8 arquivos foi editado. A coluna
"correção sugerida" é texto, e a decisão é de quem escreveu o código.
