<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/banner-light.svg">
  <img alt="stackx — o dialeto tecnico do seu projeto" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/banner-light.svg" width="100%">
</picture>

<p>
  <img alt="harness: Claude Code" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/badge-claude.svg">
  <img alt="harness: OpenCode" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/badge-opencode.svg">
  <img alt="regra: evidencia obrigatoria" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/badge-evidencia.svg">
  <img alt="schema expx v1" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/badge-schema.svg">
  <img alt="docs pt-BR" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/badge-lang.svg">
  <img alt="licenca MIT" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/badge-license.svg">
</p>

<p>
  <a href="https://bittencourtthulio.github.io/expxdev/#stackx"><strong>📘 Documentação do método</strong></a>
  &nbsp;·&nbsp;
  <a href="https://bittencourtthulio.github.io/expxdev/#stackx">Etapas e cartuchos</a>
  &nbsp;·&nbsp;
  <a href="https://bittencourtthulio.github.io/expxdev/#ecossistema">O ecossistema</a>
  &nbsp;·&nbsp;
  <a href="https://bittencourtthulio.github.io/expxdev/#schema">Contratos</a>
</p>

<strong>A camada de convenções do método Expx</strong> — descobre e formaliza o dialeto<br>
técnico do seu repositório para <a href="https://claude.com/claude-code">Claude Code</a> e <a href="https://opencode.ai">OpenCode</a>.

</div>

---

Todo repositório tem um dialeto: onde o teste mora, como o banco é isolado entre
testes, qual comando roda a suíte de verdade, quais camadas podem chamar quais.
Esse dialeto quase nunca está escrito em lugar nenhum — está espalhado nos
arquivos. O stackx lê o repositório, descobre esse dialeto e o formaliza em
`docs/stack/CONVENCOES.md`, com evidência para cada regra: arquivo e linha que a
exemplificam. A partir daí, as skills do ecossistema escrevem código **no dialeto
daquele projeto**, não num dialeto genérico.

---

## O ecossistema Expx

O método Expx é um conjunto de skills que se compõem, instaladas e mantidas pelo CLI [`expxdev`](https://github.com/bittencourtthulio/expxdev).

| Peça | Papel | Relação com a `stackx` |
|---|---|---|
| **[expxdev](https://github.com/bittencourtthulio/expxdev)** | o CLI: instala, atualiza e diagnostica o ecossistema, e sobe o painel de operação | é quem instala esta skill (`npx expxdev init`) |
| **[sprintx](https://github.com/bittencourtthulio/sprintx)** | **Build** — feature nova, F1…F6 | lê o `CONVENCOES.md` na ingestão, no plano, na auditoria e na execução |
| **[runx](https://github.com/bittencourtthulio/runx)** | **Run** — ocorrência em produção, E1…E5 | lê as convenções na investigação e no fix; consulta os cartuchos pelo sintoma |
| **[legadox](https://github.com/bittencourtthulio/legadox)** | **camada** de segurança para código legado | o cartucho de migração alimenta o cálculo de raio; em área legada, quem manda é o `PERFIL.md` |
| **stackx** *(este repositório)* | **camada** de convenções do repositório | — |
| **[mergex](https://github.com/bittencourtthulio/mergex)** | entrega: branch, commit por task, PR e pacote de QA | tira do `CONVENCOES.md` as convenções de branch, commit e teste |
| **[memox](https://github.com/bittencourtthulio/MemoX)** | **camada** de memória do projeto | fonte independente: as convenções não entram no índice dele |
| **[prodx](https://github.com/bittencourtthulio/prodx)** | **camada** de produto: decide **se** há trabalho | fonte independente: convenção técnica não entra em veredito de produto |
| **[buildx](https://github.com/bittencourtthulio/buildx)** | orquestra um projeto inteiro, da descrição ao sistema pronto | no B2 o stackx trabalha invertido: em projeto vazio não há convenção a detectar, então a `buildx` decide e o stackx registra, cada regra marcada `decidido_pelo_buildx` em vez de arquivo:linha; entregue a primeira feature, o `/stackx-detectar` normal roda e converte cada regra para a evidência real |

**Camadas** (`stackx`, `legadox`, `memox`, `prodx`) sozinhas não fazem nada — elas modificam o comportamento da `sprintx` e da `runx`. Sem `docs/stack/CONVENCOES.md`, nada muda: as irmãs se comportam como se comportariam sem esta skill. A `buildx` inverte isso: é a única peça que **depende** de outras para rodar — o `stackx` segue opcional para ela, e sem ele o projeto novo apenas nasce sem convenção registrada.

Detalhes do ecossistema inteiro no [README do expxdev](https://github.com/bittencourtthulio/expxdev).

---

## O problema

Peça a um assistente de IA para escrever um teste no seu projeto. Ele vai
escrever um teste correto — e provavelmente no lugar errado.

Ele coloca `usuario.test.ts` em `tests/`, porque é o que se vê na internet. Só
que neste repositório os 34 testes existentes ficam ao lado do código que testam,
e o `testMatch` do runner nem sequer olha para `tests/` — o teste novo nunca vai
rodar. Ninguém percebe, porque a suíte continua verde.

No mesmo teste, ele grava no banco e limpa com `TRUNCATE` no final. Só que neste
projeto cada teste roda dentro de uma transação com rollback, em quatro processos
paralelos. O `TRUNCATE` apaga os dados dos outros três. A suíte passa quando
alguém roda aquele arquivo sozinho, e falha de forma intermitente no CI — e o
teste que quebra não é o que causou o problema.

Nenhum dos dois erros é falta de conhecimento técnico: o modelo sabe escrever
teste e sabe isolar banco. O erro é não saber **como este repositório faz**.

## Por que não é um catálogo por linguagem

A saída óbvia seria empacotar conhecimento por stack: um pacote para cada
framework, cada runner, cada ORM. Essa abordagem foi considerada e descartada por
três motivos:

**Explosão combinatória.** Linguagem × framework × runner de teste × ORM × banco
gera centenas de combinações impossíveis de manter atualizadas. E pacote
desatualizado é pior que pacote inexistente: dá confiança errada.

**O modelo já sabe.** Uma skill explicando a sintaxe de um runner popular não
acrescenta nada e queima contexto — o recurso mais caro quando a IA já está
carregada de método e do código do projeto.

**O erro real não está na stack, está no dialeto.** A IA não erra "como se
escreve teste". Erra se o teste fica ao lado do arquivo ou em pasta própria, se
usa factory ou fixture, se o banco reseta por transação ou por truncate, se a
camada HTTP é mockada ou sobe container. Nada disso cabe num pacote genérico:
está no repositório do cliente.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/fluxo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/fluxo-light.svg">
  <img alt="O stackx le manifestos, testes, migracoes e codigo do repositorio e gera o CONVENCOES.md, que sprintx, runx e legadox consultam antes de escrever codigo; diante de dois dialetos em conflito, pergunta ao humano em vez de escolher sozinho" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/fluxo-light.svg" width="100%">
</picture>

Por isso o stackx é um **detector e gerador**, não um catálogo. Uma skill só,
qualquer stack, e o resultado é o dialeto verdadeiro do projeto — não um ideal de
artigo de blog.

## As cinco etapas

Estritamente sequenciais, e só a terceira fala com você — porque é a única em
que o repositório não tem a resposta.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/pipeline-light.svg">
  <img alt="As cinco etapas do stackx: deteccao, convencoes, conflito e lacuna, aderencia e atualizacao, com o artefato de cada uma e os caminhos de retorno" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/pipeline-light.svg" width="100%">
</picture>

## O que o CONVENCOES.md responde

- **Identidade técnica** — linguagem, runtime, gerenciador de pacotes e framework,
  com a versão exata do lock.
- **Comandos que funcionam de verdade** — suíte inteira, um teste só, cobertura,
  lint, formatador, type check, build, ambiente local. Cada um com a origem onde
  foi encontrado.
- **Testes** — onde o arquivo mora, como se nomeia o arquivo e o caso, runner e
  biblioteca de asserção, um teste exemplar para copiar a forma, factory ou
  fixture, o que se mocka e o que fica real, como se marca teste lento.
- **Banco em teste** — engine e versão, ORM, como o banco é isolado entre testes,
  como se semeia dado, onde vivem as migrações e como se roda e reverte uma.
- **Estrutura e camadas** — as camadas que existem de fato, quem pode chamar
  quem, e onde entra código novo de cada tipo.
- **Padrões com consequência** — como se sinaliza erro, como e onde se valida
  entrada, como se registra log e o que nunca vai para o log, como se lê
  configuração e segredo, como se nomeia cada coisa.

Cada seção termina com a evidência que a sustenta.

## Conflito e proposta: a skill pergunta em vez de chutar

Duas situações recebem tratamento explícito, e são as que separam o stackx de uma
varredura ingênua.

**Conflito.** O repositório faz a mesma coisa de mais de uma forma. O stackx **não
escolhe sozinho**: lista cada dialeto com quantos arquivos o seguem, onde vivem,
quando nasceram e quando receberam o último arquivo novo — e pergunta qual adotar.

Escolher o majoritário por conta própria seria erro. Às vezes o majoritário é o
legado e o minoritário é o padrão novo, adotado há três meses. Trinta e quatro
arquivos antigos contra nove recentes: a maioria mente, e só o histórico mostra
isso.

**Lacuna.** O repositório não tem evidência sobre um ponto. Isso vai para
`docs/stack/LACUNAS.md` com o impacto de não saber aquilo. O stackx pode registrar
uma **PROPOSTA** no CONVENCOES.md — sempre marcada como tal, nunca apresentada
como convenção existente.

Proposta não governa. As demais skills tratam ponto marcado como PROPOSTA como
decisão a levantar, não como regra a obedecer — e a verificação de aderência,
no máximo, avisa.

## Os três cartuchos

O stackx quase não carrega conteúdo curado, pelos motivos acima. A exceção é uma
faixa estreita, com critério claro: só entra o que é **não óbvio**, **específico
de versão ou engine** e **caro de errar**. Os três, juntos. Nada mais entra.

| Cartucho | Cobre |
| -------- | ----- |
| **Migração segura por engine** | O que trava a tabela e por quanto tempo, quando o índice precisa ser criado sem bloqueio, como adicionar coluna obrigatória em tabela grande, a ordem segura de renomear coluna sem indisponibilidade, como reverter cada alteração — e o que fazer quando reverter não é possível |
| **N+1 e carga de dados no ORM** | Consultas que explodem em produção e passam nos testes com massa pequena; como identificar no ORM detectado e como corrigir sem trocar N+1 por produto cartesiano |
| **Teste instável por runner** | Estado global entre casos, paralelismo sem isolamento de banco, dependência de relógio, de ordem, de fuso e de rede; o que o runner detectado precisa ter desligado ou configurado |

Cada afirmação vem com o motivo técnico, não só a recomendação — sem o motivo, o
agente não consegue generalizar para o caso que não foi previsto. E cada cartucho
manda confirmar a versão exata no CONVENCOES.md antes de aplicar qualquer coisa.

## Instalação

As skills ficam em `.claude/skills/` **nos dois harnesses** — o OpenCode lê essa
pasta nativamente. Duplicar a árvore em `.opencode/skills/` causaria colisão de
nome. Só os comandos existem nas duas pastas, porque cada harness lê a sua.

### Claude Code

```bash
mkdir -p .claude
cp -r caminho/para/stackx/.claude/skills/stackx .claude/skills/
cp -r caminho/para/stackx/.claude/commands/. .claude/commands/
cp caminho/para/stackx/AGENTS.md .
```

Confirme com `/stackx`.

### OpenCode

```bash
mkdir -p .claude/skills .opencode/commands
cp -r caminho/para/stackx/.claude/skills/stackx .claude/skills/
cp -r caminho/para/stackx/.opencode/commands/. .opencode/commands/
cp caminho/para/stackx/AGENTS.md .
```

A skill vem de `.claude/skills/stackx/`; os comandos, de `.opencode/commands/`.
O `AGENTS.md` na raiz instrui o agente a ler o `CONVENCOES.md` antes de escrever
código.

### Para os dois no mesmo repositório

Copie a skill uma vez e os comandos nas duas pastas. Os cinco arquivos de comando
são idênticos entre `.claude/commands/` e `.opencode/commands/`.

## Primeiros passos

1. **Rode `/stackx-detectar`.** A skill varre o repositório e monta o inventário.
2. **Responda os conflitos.** Se houver dois dialetos, ela apresenta os dois com
   contagem e datas e pergunta qual adotar. Este é o único momento em que ela
   pergunta — e é obrigada a perguntar.
3. **Revise o `docs/stack/CONVENCOES.md`.** Confira as evidências por amostragem;
   é o arquivo que vai governar o código novo. Corrija o que estiver errado: a
   edição manual é decisão humana e é preservada nas atualizações.
4. **Leia o `docs/stack/LACUNAS.md`.** Lacuna de impacto ALTO é o que mais rende
   resolver cedo.
5. **Trabalhe normalmente.** As skills irmãs passam a ler o arquivo sozinhas.
6. **Rode `/stackx-check`** antes de fechar uma entrega, e `/stackx-atualizar`
   quando o projeto mudar de runner, de ORM ou de estrutura.

| Comando | Faz |
| ------- | --- |
| `/stackx` | Resumo das convenções, lacunas e propostas |
| `/stackx-detectar` | Varre o repositório e gera o `CONVENCOES.md` |
| `/stackx-check` | Verifica se um diff respeitou as convenções |
| `/stackx-atualizar` | Redetecta e mostra o que mudou |
| `/stackx-migracao` | Consulta o risco de uma alteração de esquema |

## Integração com sprintx, runx e legadox

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/ecossistema-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/ecossistema-light.svg">
  <img alt="O stackx e a camada de convencoes sob sprintx, runx e legadox: as tres consultam o CONVENCOES.md antes de escrever codigo" src="https://raw.githubusercontent.com/bittencourtthulio/stackx/main/.github/assets/ecossistema-light.svg" width="100%">
</picture>

Sem `docs/stack/CONVENCOES.md`, nada muda: as três skills se comportam como hoje.

**sprintx** — a ingestão lê as convenções; a descoberta transforma cada PROPOSTA
e cada conflito em aberto em pergunta; o plano define caminho do teste, camada e
padrão de erro de cada task a partir do arquivo, em vez de deixar para o
executor; a auditoria roda a verificação de aderência; a execução usa os comandos
reais.

**runx** — a investigação lê as convenções e consulta o cartucho conforme o
sintoma; o plano embute as convenções nas tasks; o fix obedece o padrão de teste
e o isolamento de banco; o QA roda a verificação de aderência.

**legadox** — o cartucho de migração alimenta o cálculo de raio de impacto:
alteração que reescreve tabela ou pega lock exclusivo em tabela com tráfego é
raio ALTO.

> ### Regra de precedência
>
> O stackx descreve **o que deve ser seguido daqui pra frente**. O legadox
> descreve **o que existe hoje**, incluindo os dialetos conflitantes.
>
> Em projeto novo, só o stackx governa. **Em projeto legado, na área tocada manda
> o padrão local descrito no `PERFIL.md` do legadox — o stackx governa apenas
> código novo, em arquivo novo.**
>
> Sem essa regra, a IA "moderniza" arquivo antigo achando que está obedecendo
> convenção. É exatamente o colateral que o legadox proíbe, e o mais perigoso,
> porque vem com a justificativa de estar seguindo uma regra.

Os prompts prontos para integrar cada skill estão em
[`docs/integracao/`](docs/integracao/).

## O que o stackx não faz

- **Não ensina linguagem nem framework.** O modelo já sabe; repetir isso queima
  contexto.
- **Não moderniza código.** Não refatora, não renomeia, não realinha arquivo
  existente — nem "para depois".
- **Não corrige violação.** A verificação de aderência aponta e explica; a
  correção é decisão de quem escreveu.
- **Não escolhe padrão por você.** Diante de dois dialetos, apresenta os dois com
  os dados e pergunta.
- **Não substitui revisão humana.** O `CONVENCOES.md` é gerado a partir de
  evidência e precisa ser revisado antes de governar.

## Hooks e agente

O `CONVENCOES.md` é um documento — e documento depende de o modelo lembrar de o ler. Dois hooks fecham essa lacuna, e **nenhum dos dois bloqueia nada**: esta é a skill mais discreta do ecossistema.

| Hook | Quando | O que faz |
|---|---|---|
| `stackx/sem-convencoes.py` | ao abrir a sessão | se não existe `CONVENCOES.md` e o projeto tem código, sugere uma vez `/stackx-detectar` |
| `stackx/aderencia.py` | depois de escrever | confere o arquivo recém-escrito contra as convenções e avisa o que destoou |

Duas contenções deliberadas no hook de aderência: ponto marcado como **PROPOSTA nunca vira violação** — proposta não governa —, e o hook **se cala em arquivo antigo quando existe `docs/legado/PERFIL.md`**, para não empurrar a IA a "modernizar" código legado achando que obedece convenção. É a regra de precedência acima, aplicada em código.

O agente **`stackx-cartografo`** roda em contexto próprio na detecção: varre o repositório e devolve o inventário FATO / EVIDÊNCIA / FORÇA que a Etapa 2 consome. Ele **não escreve o `CONVENCOES.md` e não decide conflito** — quem apresenta os dialetos e pergunta é a skill.

Os dois hooks gravam no rastro append-only `docs/eventos/<trabalho_id>.jsonl`, seguindo o contrato `expx-eventos` v1 — é o que o painel de operação (`npx expxdev panel`) lê.

## Exemplos

Em [`exemplos/`](exemplos/), com um projeto fictício:

- [`CONVENCOES.exemplo.md`](exemplos/CONVENCOES.exemplo.md) — um arquivo gerado
  completo, com evidências, propostas e conflito em aberto
- [`conflito.exemplo.md`](exemplos/conflito.exemplo.md) — o caso em que o dialeto
  majoritário é o antigo
- [`aderencia.exemplo.md`](exemplos/aderencia.exemplo.md) — uma verificação com
  as cinco severidades

## Licença

MIT. Ver [LICENSE](LICENSE).

## Como contribuir

Contribuição mais útil, em ordem:

1. **Fontes de detecção que faltam** — um manifesto, arquivo de configuração ou
   convenção de ecossistema que o `references/01-deteccao.md` não cobre.
2. **Armadilhas para os cartuchos** — uma engine, ORM ou runner com comportamento
   não óbvio, específico de versão e caro de errar. Sempre com o **motivo
   técnico**, não só a recomendação.
3. **Casos em que a skill decidiu sozinha** — se ela adotou um dialeto em vez de
   perguntar, é defeito. Descreva o repositório que produziu isso.

Antes de propor um cartucho novo, confira o critério: não óbvio, específico de
versão ou engine, e caro de errar. Se o conteúdo virou tutorial de sintaxe, ele
não passa — o modelo já sabe aquilo.

---

<div align="center">
<sub>Parte do método <strong>Expx</strong> ·
<a href="https://github.com/bittencourtthulio/expxdev">expxdev</a> ·
<a href="https://github.com/bittencourtthulio/buildx">buildx</a> ·
<a href="https://github.com/bittencourtthulio/sprintx">sprintx</a> ·
<a href="https://github.com/bittencourtthulio/runx">runx</a> ·
<a href="https://github.com/bittencourtthulio/legadox">legadox</a> ·
stackx ·
<a href="https://github.com/bittencourtthulio/mergex">mergex</a></sub>
</div>
