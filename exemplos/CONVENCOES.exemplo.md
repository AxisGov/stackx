---
expx-schema: v1
skill: stackx
documento: convencoes
gerado-em: 2026-03-11
commit-referencia: 7f3a91c
projeto-legado: nao
---

# Convenções técnicas — pedidos-api

> Exemplo de referência. Projeto fictício: uma API de pedidos com Node,
> Fastify, Prisma e PostgreSQL. Mostra os três estados possíveis de um ponto:
> convenção com evidência, PROPOSTA e CONFLITO EM ABERTO.

## 1. Identidade técnica

| Item | Valor | Origem |
| ---- | ----- | ------ |
| Linguagem e versão | TypeScript 5.6.3 | `package.json:41`, `pnpm-lock.yaml` |
| Runtime e versão | Node 20.11.1 | `.nvmrc:1`, `.github/workflows/ci.yml:18` |
| Gerenciador de pacotes | pnpm 9.12.0 | `package.json:6` (`packageManager`) |
| Framework principal | Fastify 4.28.1 (faixa `^4.26`) | `package.json:22`, `pnpm-lock.yaml` |

O `.nvmrc` vence o campo `engines` do manifesto (`>=18`): é o que o CI usa.

**Evidência:** `package.json:6,22,41`, `.nvmrc:1`, `.github/workflows/ci.yml:18`

---

## 2. Comandos que funcionam de verdade

| Alvo | Comando | Origem |
| ---- | ------- | ------ |
| Suíte inteira | `pnpm test` | `package.json:11`, `.github/workflows/ci.yml:34` |
| Um teste só | `pnpm vitest run src/pedidos/criar-pedido.test.ts` | derivado de `package.json:11` |
| Com cobertura | `pnpm test:cov` | `package.json:12`, `.github/workflows/ci.yml:38` |
| Lint | `pnpm lint` | `package.json:13`, `.github/workflows/ci.yml:30` |
| Formatador (verificar) | `pnpm format:check` | `package.json:14`, `.github/workflows/ci.yml:28` |
| Formatador (aplicar) | `pnpm format` | `package.json:15` |
| Type check | `pnpm typecheck` | `package.json:16`, `.github/workflows/ci.yml:32` |
| Build | `pnpm build` | `package.json:10` |
| Subir ambiente local | `docker compose up -d && pnpm dev` | `README.md:22`, `docker-compose.yml:1` |

Nenhum alvo ficou sem origem. A cobertura roda só em `main`, não em PR
(`.github/workflows/ci.yml:36`) — é portão mais fraco que os demais.

**Evidência:** `package.json:10-16`, `.github/workflows/ci.yml:26-38`

---

## 3. Testes

| Item | Convenção |
| ---- | --------- |
| Onde o arquivo mora | Ao lado do código que testa |
| Nome do arquivo | `<modulo>.test.ts` |
| Nome do caso de teste | Frase em português iniciando por verbo no presente: `describe('criarPedido')` + `it('rejeita pedido sem itens')` |
| Runner e versão | Vitest 2.1.4 |
| Biblioteca de asserção | `expect` do próprio Vitest |
| Montagem de dado | Factory em `src/testes/fabricas/` |
| Marcação de teste lento ou de integração | Sufixo `.integration.test.ts`, projeto separado em `vitest.config.ts:19` |
| Paralelismo do runner | `pool: 'forks'`, 4 workers (`vitest.config.ts:11`) |

> **CONFLITO EM ABERTO** — o repositório faz isto de mais de uma forma. Ver
> `docs/stack/LACUNAS.md`. Enquanto não houver decisão, siga o padrão do
> arquivo vizinho e registre a escolha na task.
>
> Aplica-se ao **local do arquivo de teste**: 34 arquivos co-localizados
> (`src/**/*.test.ts`) contra 9 em pasta espelhada (`tests/**/*.test.ts`), estes
> últimos todos dos últimos 6 meses. Detalhe em `exemplos/conflito.exemplo.md`.

**Teste exemplar:** `src/pedidos/criar-pedido.test.ts` — é a forma que o código
novo deve copiar.

**Estrutura típica.** Um `describe` por unidade pública, sem aninhamento além
disso. Arranjo-Ação-Asserção separados por linha em branco. Um comportamento por
`it`, com um ou dois `expect`. Setup dentro do caso, via factory — não há
`beforeEach` com estado em 31 dos 34 arquivos.

**O que se mocka e o que fica real**

| Eixo | Tratamento | Evidência |
| ---- | ---------- | --------- |
| HTTP de saída | `msw` com handlers por teste | `src/testes/msw/servidor.ts:8` |
| HTTP de entrada | Real, via `app.inject()` do Fastify | `src/http/rotas/pedidos.test.ts:19` |
| Relógio | `vi.useFakeTimers()` quando há prazo | `src/pedidos/expirar-pedido.test.ts:12` |
| Sistema de arquivos | Não se toca em disco nos testes | — |
| Fila / mensageria | Driver em memória | `src/fila/fila-memoria.ts:1`, `vitest.setup.ts:14` |
| Serviço externo | `msw`; nenhum container além do banco | `src/testes/msw/servidor.ts:8` |

**Evidência:** `vitest.config.ts:1-24`, `src/pedidos/criar-pedido.test.ts:1-58`,
`src/testes/fabricas/pedido.ts:1`

---

## 4. Banco de dados em teste

| Item | Valor |
| ---- | ----- |
| Engine e versão exata | PostgreSQL 16.4 |
| ORM / camada de acesso | Prisma 5.22.0 |
| **Isolamento entre testes** | Transação com rollback por caso |
| Combinação isolamento × paralelismo | Transação + `pool: 'forks'` com 4 workers — **seguro**: cada processo tem sua conexão e sua transação |
| Semeadura de dado de teste | Factory por caso; não há seed global em teste |
| Onde vivem as migrações | `prisma/migrations/`, nome `AAAAMMDDHHMMSS_descricao` |
| Comando de rodar migração | `pnpm prisma migrate deploy` |
| Comando de reverter migração | — (LACUNA) |
| Migrações têm reversão declarada? | Não. Nenhuma das 23 migrações tem script de reversão. |

A ausência de reversão está registrada como lacuna L-02, impacto ALTO.

**Evidência:** `docker-compose.yml:7` (`image: postgres:16.4`),
`.github/workflows/ci.yml:12` (`services.postgres`), `package.json:29`,
`vitest.setup.ts:22-31`, `prisma/migrations/`

---

## 5. Estrutura e camadas

| Camada (nome no repositório) | Pasta | Pode importar de | Não importa de |
| ---------------------------- | ----- | ---------------- | -------------- |
| `http` | `src/http/` | `casos`, `dominio` | `infra` |
| `casos` | `src/casos/` | `dominio`, `portas` | `http`, `infra` |
| `dominio` | `src/dominio/` | nada | todas as demais |
| `portas` | `src/portas/` | `dominio` | `http`, `infra`, `casos` |
| `infra` | `src/infra/` | `portas`, `dominio` | `http`, `casos` |

**Força da evidência de dependência:** forte — há regra de lint declarada
(`eslint.config.js:34`, `import/no-restricted-paths` com quatro zonas). A
contagem de imports confirma: nenhum dos 47 arquivos de `src/dominio/` importa de
outra camada.

**Onde entra código novo**

| Tipo | Pasta | Arquivo exemplar |
| ---- | ----- | ---------------- |
| Caso de uso | `src/casos/` | `src/casos/criar-pedido.ts` |
| Adaptador | `src/infra/` | `src/infra/prisma/repositorio-pedido.ts` |
| Controlador / handler | `src/http/rotas/` | `src/http/rotas/pedidos.ts` |
| Componente de interface | — | não se aplica: projeto sem interface |
| Job / tarefa agendada | `src/jobs/` | `src/jobs/expirar-pedidos.ts` |

**Violações existentes.** Dois arquivos de `src/http/` importam de `src/infra/`
(`src/http/rotas/relatorios.ts:4`, `src/http/rotas/admin.ts:7`), contra 38 que
não importam. É violação existente da regra de lint (ambos com
`eslint-disable-next-line`), não convenção. Não replicar.

**Evidência:** `eslint.config.js:34-52`, `src/casos/criar-pedido.ts:1-12`

---

## 6. Padrões de código com consequência

### Sinalização de erro
Retorno tipado `Result<T, E>` de `src/dominio/resultado.ts` nos casos de uso e no
domínio. Exceção apenas na borda HTTP, convertida por um handler central
(`src/http/erro-handler.ts:14`). Erros de domínio herdam de `ErroDominio`
(`src/dominio/erros.ts:1`). 41 casos de uso usam `Result`; nenhum usa `throw`.
**Evidência:** `src/dominio/resultado.ts:1`, `src/casos/criar-pedido.ts:28`,
`src/http/erro-handler.ts:14`

### Validação de entrada
`zod` **na borda HTTP**, nunca no domínio. Esquemas em
`src/http/esquemas/*.ts`, um por rota. O caso de uso recebe o tipo já validado e
não revalida.
**Evidência:** `src/http/esquemas/criar-pedido.ts:1`, `src/http/rotas/pedidos.ts:22`

### Log
`pino` estruturado, com `requestId` em todo log de requisição, injetado pelo
Fastify.
**Nunca vai para o log:** `senha`, `token`, `authorization`, `cpf`, `cartao` —
redigidos em `src/infra/log/logger.ts:11` (`redact.paths`).
**Evidência:** `src/infra/log/logger.ts:9-18`

### Configuração e segredo
Config centralizada em `src/config.ts`, validada por `zod` na inicialização —
a aplicação não sobe com variável faltando. **Nenhum outro arquivo lê
`process.env`**: 1 ocorrência em todo o `src/`.
Segredo vem do ambiente; em produção, injetado pelo orquestrador.
**Evidência:** `src/config.ts:1-34`

### Nomeação

| Elemento | Forma | Observação |
| -------- | ----- | ---------- |
| Arquivo | `kebab-case.ts` | Consistente nas cinco camadas |
| Classe / tipo | `PascalCase` | |
| Função / método | `camelCase` | |
| Variável de ambiente | `SCREAMING_SNAKE_CASE`, agrupada por prefixo de serviço (`DATABASE_`, `REDIS_`, `SMTP_`) | `.env.example:1-14` — só as chaves foram lidas |

**Evidência:** `src/casos/criar-pedido.ts:1`, `.env.example:1-14`

---

## Conflitos em aberto

**§3 — Local do arquivo de teste.** Apresentado em 2026-03-11, sem decisão.
Detalhe em `exemplos/conflito.exemplo.md`.

## Decisões registradas

| Data | Quem decidiu | Ponto | Decisão | Dialeto abandonado |
| ---- | ------------ | ----- | ------- | ------------------ |
| 2026-03-11 | ana | §3 montagem de dado | Factory em `src/testes/fabricas/` | Objeto literal na mão (7 arquivos, todos de 2024) |

## Histórico de atualização

| Data | Commit | O que mudou |
| ---- | ------ | ----------- |
| 2026-03-11 | 7f3a91c | Geração inicial |
