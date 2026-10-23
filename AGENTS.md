# AGENTS.md

Instruções para qualquer agente que escreva código neste repositório, em
qualquer harness (Claude Code, OpenCode, outros).

## Antes de escrever qualquer código

Verifique:

```bash
test -f docs/stack/CONVENCOES.md && echo "CONVENCOES ativo"
test -f docs/legado/PERFIL.md    && echo "LEGADO ativo"
```

**Se `docs/stack/CONVENCOES.md` existir, leia-o antes de escrever qualquer
código.** Ele registra as convenções técnicas reais deste repositório, com
evidência: onde os testes moram e como se chamam, como o banco é isolado entre
testes, quais comandos de teste/lint/build funcionam de verdade, quais camadas
existem e quem pode chamar quem, como erro é sinalizado, como configuração é
lida.

Leia também `docs/stack/LACUNAS.md`: é onde estão os pontos sem evidência.

**Se `docs/legado/PERFIL.md` também existir, leia-o primeiro.** A precedência
está na regra 6.

Se `docs/stack/CONVENCOES.md` não existir, siga o padrão do código vizinho e
registre a incerteza. Não invente convenção — e, se fizer sentido, sugira rodar
`/stackx-detectar`.

## As regras invioláveis

1. Toda convenção aponta um arquivo real do repositório que a exemplifica, com caminho e linha.
2. Convenção sem evidência no código não é convenção: é PROPOSTA, e é marcada como tal.
3. PROPOSTA não governa. Nas outras skills ela vira decisão a levantar, nunca regra a obedecer.
4. Diante de dialetos conflitantes, o stackx não escolhe sozinho: apresenta os dialetos com contagem e histórico, e pergunta.
5. Comando declarado precisa ter sido encontrado em manifesto, script ou integração contínua. Comando nunca é inferido do nome do framework.
6. Em projeto legado, na área tocada manda o PERFIL.md do legadox. O stackx governa apenas código novo em arquivo novo.
7. Atualização de convenção nunca sobrescreve em silêncio: apresenta diff e espera confirmação.
8. A verificação de aderência aponta, não corrige.
9. Cartucho não repete o que o modelo já sabe. Se virou tutorial de sintaxe, foi escrito errado.
10. Nenhum segredo, credencial ou dado real de cliente entra em CONVENCOES.md, exemplo ou template.

## O que isso significa na prática

- **Teste novo:** caminho, nome do arquivo, forma do nome do caso e montagem de
  dado saem de §3. Copie a forma do teste exemplar apontado ali.
- **Teste que toca banco:** use a estratégia de isolamento de §4. Não invente
  outra.
- **Comando:** use o declarado em §2. Alvo marcado `— (LACUNA)` não tem comando;
  não substitua pelo padrão do framework.
- **Arquivo novo:** pasta da camada em §5, nomeação em §6.
- **Erro:** o padrão de §6 — exceção, retorno tipado ou objeto de resultado.
- **Ponto marcado PROPOSTA:** não é regra. Levante como decisão.
- **CONFLITO EM ABERTO:** siga o arquivo vizinho e registre a escolha.
- **Arquivo existente em projeto legado:** siga o padrão local. Não modernize,
  não renomeie, não realinhe — nem "para depois".

## Hooks e agentes ativos neste repositório

Dois hooks e um agente. Ambos os hooks nascem em modo `aviso` (`.expx/hooks.json`)
e nenhum bloqueia ação.

| Componente | Quando roda | O que faz |
| ---------- | ----------- | --------- |
| agente `stackx-cartografo` | Etapa 1 (`/stackx-detectar`, `/stackx-atualizar`) | varre o repositório em contexto próprio e devolve o inventário de evidência; não escreve arquivo |
| hook `sem-convencoes` | início de sessão | sem `CONVENCOES.md` e com código no projeto, injeta uma linha sugerindo a detecção |
| hook `aderencia` | depois de cada escrita de arquivo | confere nome de arquivo de teste contra o padrão declarado, e segredo literal |

Duas coisas que o `aderencia` **não** faz, por desenho:

- Não gera violação em ponto marcado `PROPOSTA` ou `CONFLITO EM ABERTO` no
  `CONVENCOES.md`. Convenção sem evidência não governa (regra 3).
- Não roda em arquivo já rastreado, nem em área tocada descrita no
  `docs/legado/PERFIL.md`. Ali manda o padrão local (regra 6).

Sem `docs/stack/CONVENCOES.md`, o `aderencia` fica inativo em vez de adivinhar.

O registro fica em `.claude/settings.json` (Claude Code) e
`.opencode/plugin/stackx-hooks.js` (OpenCode) — os dois invocam os mesmos
scripts em `.claude/hooks/stackx/`, para a lógica não divergir.

## Comandos

| Comando | Faz |
| ------- | --- |
| `/stackx` | Roteador: resumo, lacunas e PROPOSTAS |
| `/stackx-detectar` | Gera o `CONVENCOES.md` |
| `/stackx-check` | Verifica aderência de um diff ou pasta |
| `/stackx-atualizar` | Redetecta e apresenta o diff |
| `/stackx-migracao` | Consulta o cartucho de migração segura |

A skill vive em `.claude/skills/stackx/` — os dois harnesses leem daí. Os
comandos existem em `.claude/commands/` e `.opencode/commands/`, com conteúdo
idêntico.
