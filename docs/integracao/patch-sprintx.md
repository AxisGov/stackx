# Patch de integração — sprintx

Cole este prompt inteiro no repositório da skill **sprintx**.

---

Você vai integrar o stackx ao sprintx. Trabalhe de forma autônoma até o fim: não
faça perguntas, não peça autorização para criar ou editar arquivos, não pare no
meio para confirmar nada. Diante de ambiguidade, escolha a opção mais
conservadora, siga em frente e registre a escolha ao final.

═══════════════════════════════════════════════════════════════════════
PARTE 1 — O CONTRATO
═══════════════════════════════════════════════════════════════════════

O stackx é uma skill do ecossistema que lê o repositório real e produz
`docs/stack/CONVENCOES.md`: o registro das convenções técnicas daquele projeto,
com evidência (arquivo e linha) para cada regra. Ele responde onde os testes
moram e como se chamam, como o banco é isolado entre testes, quais comandos de
teste/lint/build funcionam de verdade, quais camadas existem e quem pode chamar
quem, como erro é sinalizado e como configuração é lida.

Companheiro: `docs/stack/LACUNAS.md`, com os pontos sem evidência.

**REGRA DE ATIVAÇÃO — a mais importante deste patch.** Se
`docs/stack/CONVENCOES.md` não existir, o sprintx precisa se comportar
**exatamente como hoje**. Nenhuma fase pode exigir o arquivo, bloquear por causa
dele, ou pedir que o usuário rode o stackx antes. No máximo, registra a ausência
como lacuna de contexto. Um patch que quebra o sprintx em repositório sem o
arquivo está errado.

**TRÊS CONCEITOS QUE O SPRINTX PRECISA HONRAR**

1. **Evidência.** Toda convenção do arquivo aponta um arquivo real com caminho e
   linha. Convenção sem evidência é PROPOSTA, marcada com o bloco literal
   `> **PROPOSTA**`.

2. **PROPOSTA não governa.** É decisão a levantar na descoberta, nunca regra a
   obedecer. Na auditoria, divergir de uma PROPOSTA gera no máximo aviso — nunca
   reprova.

3. **Precedência do legadox.** Se `docs/legado/PERFIL.md` existir, na área tocada
   manda o padrão local do PERFIL.md; o stackx governa apenas código novo em
   arquivo novo. Nunca alinhe arquivo existente à convenção.

Existe ainda o marcador `> **CONFLITO EM ABERTO**`, para pontos em que o
repositório faz de duas formas e a decisão não foi tomada. Trate como PROPOSTA:
não governa, e vira decisão a levantar.

═══════════════════════════════════════════════════════════════════════
PARTE 2 — O QUE ALTERAR
═══════════════════════════════════════════════════════════════════════

Detecte no início de cada fase:

```bash
test -f docs/stack/CONVENCOES.md && echo "CONVENCOES ativo"
test -f docs/stack/LACUNAS.md    && echo "LACUNAS disponível"
test -f docs/legado/PERFIL.md    && echo "LEGADO — precedência ativa"
```

## F1 — Base / ingestão

Passa a ler `docs/stack/CONVENCOES.md` junto com a base da feature, e
`docs/stack/LACUNAS.md` em seguida.

Registra na base: identidade técnica e comandos reais; **o teste exemplar
apontado em §3**; a estratégia de isolamento de banco (§4); camadas e direção de
dependência (§5); padrão de erro, validação e config (§6); **a lista de pontos
PROPOSTA, separada e nomeada como tal**; e **a lista de CONFLITOS EM ABERTO**.

Não copie o arquivo inteiro para a base. Registre o caminho e os pontos que a
feature toca.

## F2 — Descoberta

Passa a transformar cada PROPOSTA e cada CONFLITO EM ABERTO **que a feature toca**
em pergunta de descoberta.

- PROPOSTA relevante → pergunta explícita, marcada como decisão técnica de
  projeto, não de produto.
- CONFLITO EM ABERTO relevante → apresente os dialetos com contagem e datas, e
  peça a decisão.
- PROPOSTA ou conflito que a feature **não** toca → não pergunte. É ruído.

A decisão vai para o registro de decisões da feature, e deve ser levada de volta
ao CONVENCOES.md via `/stackx-atualizar` depois da entrega.

## F3 — Plano de sprints, fases e tasks

Onde a integração dá o maior retorno. Cada task de código passa a declarar:

| Campo da task | Vem de |
| ------------- | ------ |
| Arquivo de código a criar | §5 — pasta da camada + convenção de nome |
| **Caminho exato** do arquivo de teste | §3 |
| Forma do nome dos casos de teste | §3 |
| Como montar dado de teste | §3 — factory, fixture ou literal |
| Isolamento de banco a usar | §4 |
| Padrão de erro a usar | §6 |
| Camadas que a task pode importar | §5 |
| Comando de teste da task | §2 |

Os dois testes por task passam a ser escritos no formato do exemplar de §3.

Nenhuma task pode declarar caminho de teste, padrão de erro ou camada que
contradiga o CONVENCOES.md sem justificativa escrita na própria task.

Ponto PROPOSTA: a task o declara como decisão pendente, não como regra.

## F4 — Orquestrador

Registra no cabeçalho do `ORQUESTRADOR.md` o caminho e o commit de referência do
CONVENCOES.md usado, e a lista de PROPOSTAS que governaram decisões da feature.

**Paralelismo:** duas tasks que tocam a mesma tabela em teste só podem ser
declaradas paralelas se a estratégia de §4 suportar paralelismo. Isolamento por
truncate sem banco por worker **impede** paralelismo de tasks com banco.

## F5 — Auditoria

Passa a rodar a verificação de aderência do stackx (Etapa 4 / `/stackx-check`)
sobre o diff da feature e incluir a tabela no relatório.

Veredito: qualquer `CRÍTICO` ou `ALTO` → não aprova. `MÉDIO` → aprova com
registro. `AVISO` (PROPOSTA divergida) → **não reprova**.

Confere também se cada task usou o comando de teste declarado em §2.

## F6 — Execução

Passa a usar os comandos reais de §2 — teste, lint, formatador, type check — em
vez de inferir do framework.

Antes de criar arquivo, confere a pasta em §5 e o nome em §6. Antes de criar
teste, confere §3. Antes de escrever acesso a banco em teste, confere §4.

Comando ausente em §2 (marcado LACUNA) → **não invente**. Registre que o passo não
pôde ser verificado e siga.

Consulta aos cartuchos durante a execução:

| Situação na task | Cartucho |
| ---------------- | -------- |
| Cria ou altera migração | `migracao-segura.md`, seção da engine de §4 |
| Adiciona consulta que carrega relação em lista | `orm-carga-de-dados.md`, seção do ORM de §4 |
| Cria teste com banco, paralelismo, tempo ou rede | `teste-instavel.md`, seção do runner de §3 |

═══════════════════════════════════════════════════════════════════════
PARTE 3 — VERIFICAÇÃO
═══════════════════════════════════════════════════════════════════════

1. Sem `docs/stack/CONVENCOES.md`, o sprintx roda F1 a F6 exatamente como antes.
   Simule e confirme: nenhuma fase bloqueia, nenhuma exige o arquivo.
2. Com o arquivo, a F1 registra na base os pontos PROPOSTA **em lista separada**.
3. Simule uma feature que toca um ponto PROPOSTA: a F2 pergunta e a F3 declara
   como decisão pendente. Confirme que nenhuma fase o trata como regra.
4. Simule um ponto com evidência que a task contraria: a F5 gera `ALTO` e não
   aprova.
5. Simule um ponto PROPOSTA que a task contraria: a F5 gera `AVISO` e **aprova**.
6. Simule projeto legado com PERFIL.md contradizendo o CONVENCOES.md na área
   tocada: confirme que o PERFIL.md vence e que nenhuma fase sugere modernizar
   arquivo existente.
7. Simule alvo de comando marcado LACUNA em §2: confirme que a F6 não inventa o
   comando padrão do framework.
8. Confirme que a F4 não declara paralelas duas tasks com banco quando o
   isolamento de §4 não suporta.
9. Grep por caminho absoluto nos arquivos alterados.

═══════════════════════════════════════════════════════════════════════
ENTREGA
═══════════════════════════════════════════════════════════════════════

Mostre: os arquivos alterados com o diff resumido; o trecho de cada fase que
passou a ler o CONVENCOES.md; o resultado das nove verificações da PARTE 3; e as
decisões que você tomou diante de ambiguidade.
