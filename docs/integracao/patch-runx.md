# Patch de integração — runx

Cole este prompt inteiro no repositório da skill **runx**.

---

Você vai integrar o stackx ao runx. Trabalhe de forma autônoma até o fim: não
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
`docs/stack/CONVENCOES.md` não existir, o runx precisa se comportar **exatamente
como hoje**. Nenhuma etapa pode exigir o arquivo ou bloquear por causa dele. Um
patch que quebra o runx em repositório sem o arquivo está errado.

**TRÊS CONCEITOS QUE O RUNX PRECISA HONRAR**

1. **Evidência.** Toda convenção aponta um arquivo real com caminho e linha.
   Convenção sem evidência é PROPOSTA, marcada com `> **PROPOSTA**`.

2. **PROPOSTA não governa.** É decisão a levantar na investigação, nunca regra a
   obedecer. No QA, divergir de PROPOSTA gera no máximo aviso.

3. **Precedência do legadox.** Se `docs/legado/PERFIL.md` existir, na área tocada
   manda o padrão local; o stackx governa apenas código novo em arquivo novo.

**PARTICULARIDADE DO RUNX — o ponto que mais distingue este patch do patch do
sprintx.** Ocorrência quase sempre toca **código existente**. Logo:

| Tipo de arquivo | Quem manda |
| --------------- | ---------- |
| Arquivo **novo** (teste de regressão, novo módulo) | CONVENCOES.md |
| Arquivo **existente** sendo corrigido | O padrão local do arquivo — **sempre** |

Corrigir um defeito **e** alinhar o arquivo à convenção na mesma task é melhoria
colateral, e é proibido. O fix é a task; o alinhamento, se valer a pena, é
ocorrência própria. Em projeto legado, o alinhamento é proibido pelo legadox.

Também vale: se o arquivo de teste já existe, o caso de regressão novo vai nele,
**no formato daquele arquivo**, mesmo que divirja do CONVENCOES.md. Consistência
local vence; a divergência vira nota.

═══════════════════════════════════════════════════════════════════════
PARTE 2 — O QUE ALTERAR
═══════════════════════════════════════════════════════════════════════

Detecte no início de cada etapa:

```bash
test -f docs/stack/CONVENCOES.md && echo "CONVENCOES ativo"
test -f docs/legado/PERFIL.md    && echo "LEGADO — precedência ativa"
```

## E1 — Causa / investigação

Passa a ler `docs/stack/CONVENCOES.md` antes de formular hipótese, com foco em:

- **§2 comandos** — para reproduzir o defeito com o comando certo. Reproduzir com
  o comando errado (só o arquivo, quando a convenção é a suíte) é a causa mais
  comum de "não consigo reproduzir".
- **§4 banco em teste** — para saber por que o defeito aparece ou some conforme o
  isolamento.
- **§6 padrão de erro e log** — para saber **onde** o erro deveria ter aparecido.
  Se a convenção é retorno tipado e o código faz `throw`, o erro pode estar sendo
  engolido por um handler que não o esperava: a convenção violada **é** a causa.

Consulta aos cartuchos conforme o sintoma — aqui eles rendem mais que em qualquer
outra etapa, porque o defeito já existe e o cartucho descreve a forma dele:

| Sintoma da ocorrência | Cartucho |
| --------------------- | -------- |
| Lentidão que aparece com volume, some em homologação | `orm-carga-de-dados.md`, seção do ORM de §4 |
| Timeout ou indisponibilidade durante deploy/migração | `migracao-segura.md`, seção da engine de §4 |
| Teste que passa e falha alternadamente; "só falha no CI" | `teste-instavel.md`, seção do runner de §3, e o roteiro de investigação em 6 passos |

Se a investigação concluir que a causa raiz é uma **violação de convenção** já
existente, isso vai escrito na causa: é sinal de que o mesmo defeito pode existir
em outros pontos do repositório.

Se a área da ocorrência não tem convenção documentada, registre como lacuna, não
como violação. Não invente a convenção para justificar a causa.

## E2 — Plano

Passa a montar as tasks com as convenções embutidas:

| Campo da task | Vem de |
| ------------- | ------ |
| Caminho exato do teste de regressão | §3 |
| Forma do nome do caso de teste | §3 |
| Montagem de dado | §3 |
| Isolamento de banco | §4 |
| Padrão de erro do fix | §6 |
| Camada onde o fix entra | §5 |
| Comando de verificação | §2 |

Aplicando a distinção arquivo novo × arquivo existente da PARTE 1. O plano separa
fix de alinhamento: nunca na mesma task.

## E3 — Fix

Passa a obedecer §3 (padrão de teste) e §4 (isolamento de banco) ao escrever o
teste de regressão, e a usar os comandos de §2 para verificar.

TDD estrito continua valendo: a convenção define a **forma** do teste, nunca
dispensa o vermelho. O teste de regressão precisa falhar antes do fix e passar
depois.

Padrão de erro de §6 no código novo. Fix que toca migração: consultar
`migracao-segura.md` antes de escrever, e informar o raio ao legadox quando
aplicável. Comando ausente em §2 → não invente; registre.

## E4 — QA

Passa a rodar a verificação de aderência do stackx (Etapa 4 / `/stackx-check`)
sobre o diff da ocorrência e anexar a tabela ao relatório.

Veredito:
- `CRÍTICO` ou `ALTO` em **arquivo novo** → não aprova.
- Divergência em **arquivo existente** → `INFO`, nunca reprova. O QA do runx não
  cobra modernização.
- `AVISO` de PROPOSTA → não reprova.

Continua conferindo o de sempre: o teste de regressão existe, falha sem o fix, e
o comando executado é o de §2.

## E5 — Relatar

Passa a incluir no relatório técnico: o commit de referência do CONVENCOES.md
usado; a tabela de aderência do E4; **as lacunas novas descobertas na
investigação** — ocorrência é a melhor fonte de lacuna que existe, porque o
defeito prova que a convenção faltava; e, se a causa raiz foi violação de
convenção, dizer isso explicitamente.

As lacunas novas viram entrada para `/stackx-atualizar`.

═══════════════════════════════════════════════════════════════════════
PARTE 3 — VERIFICAÇÃO
═══════════════════════════════════════════════════════════════════════

1. Sem `docs/stack/CONVENCOES.md`, o runx roda E1 a E5 exatamente como antes.
   Simule e confirme que nenhuma etapa bloqueia.
2. Com o arquivo, o E1 lê §2, §4 e §6 antes de formular hipótese.
3. Simule ocorrência de lentidão com volume: confirme que o E1 consulta o
   cartucho de ORM, na seção do ORM registrado em §4.
4. Simule fix em **arquivo existente** cujo padrão diverge do CONVENCOES.md:
   confirme que o E2 manda seguir o padrão local e que o E4 emite `INFO`, não
   violação.
5. Simule teste de regressão em **arquivo novo**: confirme que segue §3 e §4.
6. Simule teste de regressão que vai num arquivo de teste **existente** com
   formato próprio: confirme que segue o formato do arquivo, não o do §3.
7. Simule uma task que corrige o defeito **e** alinha o arquivo à convenção:
   confirme que o plano rejeita isso e separa em duas ocorrências.
8. Simule divergência de PROPOSTA no diff: confirme `AVISO` e que o QA aprova.
9. Simule projeto legado com PERFIL.md: confirme a precedência e que nenhuma
   etapa sugere modernizar.
10. Grep por caminho absoluto nos arquivos alterados.

═══════════════════════════════════════════════════════════════════════
ENTREGA
═══════════════════════════════════════════════════════════════════════

Mostre: os arquivos alterados com o diff resumido; o trecho de cada etapa que
passou a ler o CONVENCOES.md; a tabela arquivo novo × arquivo existente tal como
ficou escrita; o resultado das dez verificações da PARTE 3; e as decisões que
você tomou diante de ambiguidade.
