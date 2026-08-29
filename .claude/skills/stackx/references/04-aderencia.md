# Etapa 4 — Verificação de aderência

Confere se um conjunto de mudanças respeitou o `CONVENCOES.md`. Serve de portão
antes de fechar uma task (sprintx F5, runx E4).

**A regra que governa esta etapa: aponta, não corrige.** Você não edita arquivo
nenhum aqui. Nem para "só arrumar o nome". A correção é decisão de quem escreveu.

## Pré-requisitos verificáveis

```bash
test -f docs/stack/CONVENCOES.md || echo "SEM CONVENCOES.md — rode /stackx-detectar antes"
test -f docs/legado/PERFIL.md && echo "LEGADO — precedência do PERFIL.md ativa"
```

- [ ] `docs/stack/CONVENCOES.md` existe.
- [ ] Há um alvo: diff, branch, lista de arquivos ou pasta.
- [ ] Você leu o CONVENCOES.md **inteiro** antes de olhar o diff. Verificar
      contra memória do que "costuma ser convenção" é o erro clássico aqui.

## Coleta do alvo

```bash
# diff contra a base
git diff --name-status <base>...HEAD
git diff <base>...HEAD

# só o que foi adicionado (arquivo novo é o que mais importa em projeto legado)
git diff --diff-filter=A --name-only <base>...HEAD

# trabalho não commitado
git diff --name-status HEAD

# pasta
find <pasta> -type f | grep -v node_modules
```

Classifique cada arquivo do alvo em **NOVO** ou **MODIFICADO**. Essa distinção
decide a precedência em projeto legado.

## Precedência em projeto legado

Se `docs/legado/PERFIL.md` existe:

| Arquivo | Quem manda |
| ------- | ---------- |
| **NOVO**, fora de área tocada | CONVENCOES.md do stackx |
| **NOVO**, dentro de área tocada descrita no PERFIL.md | Padrão local do PERFIL.md |
| **MODIFICADO** | **PERFIL.md sempre** |

Consequências, e são absolutas:

- Em arquivo MODIFICADO, divergência do CONVENCOES.md **não é violação**. No
  máximo `INFO`, e só quando for útil registrar.
- **Nunca** sugira alinhar arquivo existente à convenção. Isso é melhoria
  colateral, e o legadox proíbe.
- Se o CONVENCOES.md e o PERFIL.md se contradizem na área tocada, a saída
  registra a contradição como `INFO` e diz que o PERFIL.md venceu. Não pergunte,
  não modernize.

## O que verificar, ponto a ponto

Para cada item: só gera violação se a convenção correspondente tiver
**evidência** no CONVENCOES.md. Item marcado PROPOSTA nunca gera violação.

### 1. Local e nome de arquivo de teste
O teste ficou onde a convenção manda? O nome casa com o padrão **e** com o
`testMatch` do runner? Um teste no lugar certo com nome que o runner não casa é
`CRÍTICO`: nunca vai rodar.

### 2. Presença dos testes exigidos
Todo arquivo de código NOVO tem teste correspondente? A task exigia dois testes
por task (contrato do ecossistema) — os dois existem?

### 3. Uso do padrão de erro
O código novo sinaliza erro do jeito da convenção (exceção × retorno tipado ×
objeto de resultado)? Introduziu classe de erro fora da hierarquia base? Fez
`catch` que engole erro sem relançar nem logar?

### 4. Respeito às camadas e dependências proibidas
Cada arquivo novo está na pasta da sua camada? Os imports respeitam a direção
permitida? Uma dependência proibida introduzida é `CRÍTICO`.

### 5. Factory ou fixture conforme a convenção
Se a convenção é factory e o teste monta objeto literal na mão, é violação
`MÉDIO`. Se a convenção é fixture e apareceu factory nova, idem.

### 6. Isolamento de banco conforme a convenção
O teste novo usa o mecanismo de isolamento do projeto, ou escreve no banco sem
ele? Teste que suja o banco é `CRÍTICO`: quebra a suíte inteira de forma
intermitente, e o sintoma aparece longe da causa.

### 7. Comando de teste efetivamente executado
Qual comando rodou? Foi o declarado no CONVENCOES.md? Rodar só o arquivo alterado
quando a convenção é rodar a suíte é `AVISO`. **Nenhum** comando executado é
`CRÍTICO` — a task não pode fechar.

### 8. Nomeação, log e configuração
Nome de arquivo/classe/função na forma do projeto. Nada de segredo em log. Nada
de leitura direta de ambiente quando existe módulo de config centralizado.
Segredo hardcoded é `CRÍTICO`, sempre, mesmo sem convenção que fale disso.

## Severidade

| Severidade | Quando | Fecha a task? |
| ---------- | ------ | ------------- |
| `CRÍTICO` | Quebra a suíte, vaza segredo, viola dependência proibida, teste que nunca roda | **Não** |
| `ALTO` | Viola convenção com evidência forte (UNÂNIME) | **Não** |
| `MÉDIO` | Viola convenção com evidência mais fraca (MAJORITÁRIO, ÚNICO CASO) | Sim, com registro |
| `AVISO` | Diverge de **PROPOSTA**, ou de CONFLITO EM ABERTO, ou comando parcial | Sim |
| `INFO` | Contexto legado: divergência em arquivo MODIFICADO | Sim |

**Regra 3 aplicada:** PROPOSTA nunca passa de `AVISO`. Se você se pegar
escrevendo `ALTO` para um ponto marcado PROPOSTA, o erro é seu.

## Formato exato da saída

Use `assets/TEMPLATE-aderencia.md`:

```markdown
## Verificação de aderência — <alvo>

CONVENCOES.md: `docs/stack/CONVENCOES.md` (gerado em 2025-08-12, commit a1b2c3d)
Contexto: projeto legado — PERFIL.md ativo na área `src/billing/`
Arquivos no alvo: 7 (4 novos, 3 modificados)

| Severidade | Arquivo | Convenção violada | Correção sugerida |
| ---------- | ------- | ----------------- | ----------------- |
| CRÍTICO | `tests/billing/invoice.spec.ts:1` | Nome de arquivo — a convenção é `*.test.ts` e o `testMatch` do runner não casa `*.spec.ts` | Renomear para `invoice.test.ts` |
| ALTO | `src/billing/refund.ts:22` | Padrão de erro — a convenção é `Result<T, E>`; aqui há `throw` | Retornar `err(new RefundDeclined(...))` |
| AVISO | `src/billing/refund.ts:5` | Ordem de imports — ponto marcado **PROPOSTA** | Nenhuma ação exigida |
| INFO | `src/billing/legacy-charge.ts:88` | Arquivo MODIFICADO em área do PERFIL.md; o padrão local diverge do CONVENCOES.md | Manter o padrão local. Não alinhar. |

**Veredito:** 1 CRÍTICO, 1 ALTO — a task **não** pode fechar.
**Comando de teste executado:** `pnpm test` ✓ (conforme CONVENCOES.md §2)
```

Sem achados: escreva a tabela vazia com "Nenhuma violação" e o veredito, não
apenas "ok" — o registro serve de evidência da passagem pelo portão.

## Critério de saída

- [ ] Todo arquivo do alvo foi classificado NOVO ou MODIFICADO.
- [ ] Cada linha da tabela cita a convenção **por seção do CONVENCOES.md**.
- [ ] Nenhum ponto PROPOSTA gerou severidade acima de `AVISO`.
- [ ] Nenhum arquivo foi editado por você.
- [ ] Em projeto legado, nenhuma sugestão de alinhar arquivo existente.
- [ ] O veredito diz explicitamente se a task pode fechar.
- [ ] O comando de teste executado foi confirmado, não presumido.

## Quando o critério não é atendido

| Situação | O que fazer |
| -------- | ----------- |
| Não existe CONVENCOES.md | Não improvise convenção. Diga que o portão não pode rodar e aponte `/stackx-detectar`. |
| O diff toca área sem convenção documentada | Não vire violação. Registre `INFO` e uma lacuna nova para a Etapa 5. |
| Evidência do CONVENCOES.md aponta arquivo que sumiu | O CONVENCOES.md está velho. Marque `INFO`, não viole, e recomende `/stackx-atualizar`. |
| O usuário pede para você corrigir | Corrigir é outra tarefa: a verificação entrega a tabela primeiro. Depois, se pedido explicitamente, aplique as correções fora deste modo. |
| Muitos CRÍTICOS por convenção nova recém-adotada | Provável CONVENCOES.md desalinhado do repositório. Sinalize e recomende `/stackx-atualizar` antes de tratar como violação em massa. |
