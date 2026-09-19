# Etapa 6 — Consulta dirigida: a dependência de stack de um módulo

Etapa **de consulta**, não de detecção. Ela não varre o repositório: recebe a
seção 6 de um `MODULO.md` do `modulex` — a dependência de stack, separada em
duas colunas — e devolve a tradução para este projeto e os conflitos.

Roda sob demanda, tipicamente chamada pela F1 ou pela F3 do sprintx, depois de
um módulo ter sido injetado. Nunca roda sozinha, e nunca altera o
`CONVENCOES.md`.

## A premissa que governa a etapa inteira

**O módulo é informação, nunca autoridade.**

Um módulo carrega stack e arquitetura acopladas ao sistema de onde foi
extraído. Injetá-las inteiras num projeto que já tem as suas é colocar a casa
de origem dentro da casa de destino — e é o maior risco do `modulex`.

Por isso a seção 6 de todo `MODULO.md` vem em duas colunas, e as duas têm
destinos opostos:

| Coluna | Definição | Viaja? |
| ------ | --------- | ------ |
| **essencial ao problema** | o que quebra se for mudado, porque o terceiro exige | **sim** — vale em qualquer projeto |
| **herdada do sistema de origem** | escolha da casa onde o módulo nasceu | **não** — tem que ser traduzida |

## Roteiro

### a) Cada item da coluna ESSENCIAL, confrontado com o `CONVENCOES.md`

Compatível: registre e siga.

Incompatível: é **conflito** (item c). Não traduza, não adapte, não escolha.

### b) Cada item da coluna HERDADA, traduzido

Para cada um, ache o equivalente deste projeto, com evidência de arquivo e
linha — a mesma regra de evidência que governa a skill inteira:

```
<item do modulo> → <equivalente neste projeto>   CONVENCOES.md:<linha>
```

Sem equivalente detectado no `CONVENCOES.md`, escreva `PENDENTE`.

**Nunca preencha por analogia.** Inventar o equivalente reintroduz a convenção
alheia com outro nome, que é exatamente o que esta etapa existe para impedir —
e é pior que não traduzir, porque parece traduzido.

### c) Conflito: item essencial sem tradução possível

```
CONFLITO — modulo <id>
  Modulo (essencial): <convencao>
  Projeto (CONVENCOES.md:<linha>): <convencao>
  Nao ha traducao. Isto e decisao humana, na F2 do sprintx.
```

Exemplo real: um módulo de mensageria exige endpoint público, sem autenticação
de sessão, porque o provedor chama de fora. Um projeto cujo `CONVENCOES.md` diz
"toda rota exige token autenticado" tem um conflito **verdadeiro**.

Ele não é do stackx nem do modulex resolver. **Mostre os dois e cale.**

### d) Coluna HERDADA vazia é suspeita, e se sinaliza

Praticamente todo módulo extraído carrega convenção da casa de origem. Uma
coluna herdada vazia quase nunca significa "não há herança": significa que
quem extraiu não a enxergou — e não enxergá-la é o caminho mais curto para
injetá-la.

Sinalize em uma linha, e siga. Não é erro que bloqueia; é aviso que muda a
leitura do resto.

## Formato da saída

```
Modulo <id> — dependencia de stack neste projeto

ESSENCIAL (viaja)
  <item>  OK          compativel com CONVENCOES.md:<linha>
  <item>  CONFLITO    ver abaixo

HERDADA (traduzida)
  <item do modulo> → <equivalente daqui>   CONVENCOES.md:<linha>
  <item do modulo> → PENDENTE              sem evidencia neste projeto

CONFLITOS
  <o bloco do item c, um por conflito>

<aviso da coluna herdada vazia, quando for o caso>
```

## O que esta etapa NÃO faz

- **Não altera o `CONVENCOES.md`.** O módulo não é evidência do que este
  repositório faz; é informação sobre o que outro repositório fez.
- **Não resolve conflito.** Conflito vai ao humano, na F2 do sprintx.
- **Não decide se o módulo será usado.** Isso é do sprintx, com o veredito do
  prodx na mesa.
- **Não vira PROPOSTA.** Uma PROPOSTA nasce de lacuna deste projeto, não de
  convenção de outro.

## Critério de saída

- [ ] Todo item da coluna essencial está marcado `OK` ou `CONFLITO`.
- [ ] Todo item da coluna herdada tem equivalente com arquivo e linha, ou
      `PENDENTE`. Nenhum foi preenchido por analogia.
- [ ] Cada conflito traz as duas convenções, as duas evidências, e nenhuma
      escolha entre elas.
- [ ] Coluna herdada vazia foi sinalizada.
- [ ] O `CONVENCOES.md` não foi alterado.
