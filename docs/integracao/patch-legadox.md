# Patch de integração — legadox

Cole este prompt inteiro no repositório da skill **legadox**.

---

Você vai integrar o stackx ao legadox. Trabalhe de forma autônoma até o fim: não
faça perguntas, não peça autorização para criar ou editar arquivos, não pare no
meio para confirmar nada. Diante de ambiguidade, escolha a opção mais
conservadora, siga em frente e registre a escolha ao final.

═══════════════════════════════════════════════════════════════════════
PARTE 1 — O CONTRATO
═══════════════════════════════════════════════════════════════════════

O stackx é uma skill do ecossistema que lê o repositório real e produz
`docs/stack/CONVENCOES.md`: o registro das convenções técnicas daquele projeto,
com evidência (arquivo e linha) para cada regra — onde os testes moram, como o
banco é isolado, quais comandos funcionam, quais camadas existem, como erro é
sinalizado.

Este é o encontro mais delicado do ecossistema, porque as duas skills descrevem a
mesma coisa com propósitos opostos:

| Skill | Descreve | Propósito |
| ----- | -------- | --------- |
| stackx | o que **deve** ser seguido daqui pra frente | uniformizar o novo |
| legadox | o que **existe** hoje, incluindo dialetos conflitantes | conter o colateral |

**REGRA DE ATIVAÇÃO.** Se `docs/stack/CONVENCOES.md` não existir, o legadox
precisa se comportar **exatamente como hoje**. Nenhuma fase pode exigir o
arquivo ou bloquear por causa dele.

**A REGRA DE PRECEDÊNCIA — o coração deste patch, e é inegociável**

```
Projeto novo   (sem PERFIL.md) → só o stackx governa.
Projeto legado (com PERFIL.md) → na ÁREA TOCADA manda o padrão local do
                                 PERFIL.md. O stackx governa APENAS código
                                 novo, em arquivo novo.
```

Por que a regra existe: sem ela, a IA "moderniza" arquivo antigo achando que está
obedecendo convenção. É exatamente o colateral que o legadox proíbe — e o mais
perigoso, porque vem com a justificativa de estar seguindo uma regra.

Tabela de decisão, arquivo a arquivo:

| Arquivo | Área | Quem manda |
| ------- | ---- | ---------- |
| Novo | fora de área tocada descrita no PERFIL.md | CONVENCOES.md |
| Novo | dentro de área tocada | **PERFIL.md** — nasce no dialeto do vizinho |
| Existente, modificado | qualquer | **PERFIL.md**, sempre |
| Existente, não modificado | qualquer | ninguém — não se toca |

A segunda linha costuma surpreender e está certa: arquivo novo no meio de um
módulo com dialeto próprio segue **o módulo**, não o repositório. Um teste novo
em formato diferente dos 40 vizinhos é ruído, não melhoria.

Empate ou dúvida sobre a fronteira da área tocada: decide o PERFIL.md.

═══════════════════════════════════════════════════════════════════════
PARTE 2 — O QUE ALTERAR
═══════════════════════════════════════════════════════════════════════

Detecte:

```bash
test -f docs/legado/PERFIL.md    && echo "LEGADO ativo"
test -f docs/stack/CONVENCOES.md && echo "CONVENCOES ativo"
```

## 1. Ordem de leitura — altere isto primeiro

Com os dois arquivos presentes, a ordem é obrigatória:

1. `docs/legado/PERFIL.md` — **primeiro, sempre**. Ele define a área tocada e o
   dialeto local; sem isso não há como aplicar a precedência.
2. `docs/stack/CONVENCOES.md` — depois, para código novo fora da área tocada.
3. O cartucho relevante, se a mudança envolve migração, carga de dados ou teste
   com banco/tempo/rede.

Ler na ordem inversa é o erro que produz modernização acidental: o agente chega
ao código já convencido da convenção global.

## 2. Cálculo de raio de impacto

O cartucho `migracao-segura.md` do stackx passa a ser insumo direto do raio:

| Achado | Raio |
| ------ | ---- |
| Migração que reescreve tabela, ou lock exclusivo em tabela com tráfego | **ALTO** |
| Migração irreversível (`DROP COLUMN`, `DROP TABLE`, backfill destrutivo) | **ALTO** |
| Índice sem bloqueio, coluna nullable, constraint `NOT VALID` | MÉDIO |
| Alteração só de metadados em tabela pequena | BAIXO |

O CONVENCOES.md §5 (camadas e direção de dependência) alimenta a **superfície**
do raio: quem importa a camada tocada é quem pode quebrar.

## 3. Testes de caracterização

O CONVENCOES.md §3 e §4 passam a dizer **como** escrever o teste de
caracterização neste projeto — runner, local, forma, isolamento.

**Mas:** se a área tocada tem dialeto de teste próprio descrito no PERFIL.md, a
caracterização segue **esse** dialeto. Caracterização existe para registrar o
comportamento atual; escrevê-la em formato estranho ao módulo dificulta a leitura
de quem conhece o módulo.

## 4. Orçamento de mudança

O CONVENCOES.md ajuda a **cortar escopo**, nunca a expandi-lo:

- Alinhar arquivo existente à convenção **não entra** no orçamento. Nunca.
- O comando de verificação de §2 entra como custo de execução.
- Se seguir a convenção num arquivo novo custar muito mais que seguir o padrão
  local, siga o padrão local e registre.

## 5. Plano de reversão

O cartucho de migração fornece a coluna "reverte?" por tipo de alteração, e o
tratamento para quando não reverte: backup verificado imediatamente antes, janela
combinada, e caminho de "seguir para a frente" escrito **antes** de rodar.

## 6. Proibições explícitas — escreva esta lista na skill

Cada item já foi feito com boa intenção. A lista precisa estar visível:

1. **Não** refatore arquivo existente para alinhar à convenção.
2. **Não** renomeie arquivo, teste ou símbolo existente por causa de §6.
3. **Não** troque o padrão de erro de um módulo inteiro porque §6 diz outra coisa.
4. **Não** mova teste de lugar porque §3 diz outro local.
5. **Não** migre o módulo para o runner novo porque §3 registra outro runner.
6. **Não** trate divergência de arquivo existente como violação — é `INFO`.
7. **Não** sugira nenhuma das coisas acima "para depois", dentro da entrega. Se
   valer a pena, é ocorrência própria, com seu próprio raio e orçamento.

## 7. Quando o CONVENCOES.md contradiz o PERFIL.md

Isso não é erro: é a situação normal de um repositório legado, e o motivo de a
regra existir.

1. Siga o PERFIL.md na área tocada.
2. Registre a contradição como `INFO` na tabela de aderência.
3. **Não pergunte ao usuário.** A precedência já respondeu.
4. Se a contradição for ampla e recorrente, registre uma linha em
   `docs/stack/LACUNAS.md` — "o CONVENCOES.md descreve o padrão de X, e a área Y
   segue outro; a convergência é decisão de projeto, fora do escopo desta
   entrega". Registrar não é propor migração.

O caso inverso — o PERFIL.md descreve um padrão que o CONVENCOES.md desconhece
porque a área é isolada — não é contradição: é informação que falta ao stackx, e
vira lacuna na próxima `/stackx-atualizar`.

═══════════════════════════════════════════════════════════════════════
PARTE 3 — VERIFICAÇÃO
═══════════════════════════════════════════════════════════════════════

1. Sem `docs/stack/CONVENCOES.md`, o legadox se comporta exatamente como antes.
2. Com os dois arquivos, confirme que o PERFIL.md é lido **primeiro**.
3. Simule uma convenção do stackx que contradiz o padrão local da área tocada:
   confirme que o PERFIL.md vence e que a skill **não** sugere modernizar o
   arquivo — nem "para depois".
4. Simule um **arquivo novo dentro da área tocada**: confirme que ele nasce no
   dialeto do vizinho, não no do CONVENCOES.md.
5. Simule um **arquivo novo fora da área tocada**: confirme que segue o
   CONVENCOES.md.
6. Simule uma migração que reescreve tabela grande: confirme raio **ALTO** e que
   o plano de reversão exige backup verificado por ser irreversível.
7. Simule um índice criado sem bloqueio: confirme raio MÉDIO.
8. Confirme que nenhum item de alinhamento à convenção entrou no orçamento de
   mudança.
9. Simule caracterização em área com dialeto de teste próprio: confirme que segue
   o dialeto local, não o §3.
10. Confirme que a lista de sete proibições está escrita na skill, visível.
11. Grep por caminho absoluto nos arquivos alterados.

═══════════════════════════════════════════════════════════════════════
ENTREGA
═══════════════════════════════════════════════════════════════════════

Mostre: os arquivos alterados com o diff resumido; a regra de precedência e a
tabela arquivo a arquivo tal como ficaram escritas; a lista de sete proibições
tal como ficou; a tabela de raio alimentada pelo cartucho de migração; o
resultado das onze verificações da PARTE 3; e as decisões que você tomou diante
de ambiguidade.
