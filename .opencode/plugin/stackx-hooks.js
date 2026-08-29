/**
 * stackx — hooks para OpenCode.
 *
 * Mesma lógica dos hooks do Claude Code: este plugin apenas invoca os MESMOS
 * scripts em .claude/hooks/stackx/. A lógica não é duplicada — só o registro,
 * porque os dois harnesses têm mecanismos diferentes.
 *
 *   sem-convencoes  → na primeira mensagem da sessão
 *   aderencia       → depois de cada escrita de arquivo
 *
 * Ambos nascem em modo aviso (.expx/hooks.json). Nenhum bloqueia.
 */
import { spawn } from "node:child_process"
import { existsSync } from "node:fs"
import path from "node:path"

const TEMPO_LIMITE = 5000

function rodar(diretorio, script, entrada) {
  return new Promise((resolve) => {
    const alvo = path.join(diretorio, ".claude", "hooks", "stackx", script)
    if (!existsSync(alvo)) return resolve({ codigo: 0, erro: "" })

    let saida = ""
    let erro = ""
    let processo
    try {
      processo = spawn("python3", [alvo], { cwd: diretorio })
    } catch {
      return resolve({ codigo: 0, erro: "" })
    }

    const relogio = setTimeout(() => processo.kill("SIGKILL"), TEMPO_LIMITE)
    processo.stdout.on("data", (d) => (saida += d))
    processo.stderr.on("data", (d) => (erro += d))
    processo.on("error", () => {
      clearTimeout(relogio)
      resolve({ codigo: 0, erro: "" }) // falha aberta: hook de método não trava trabalho
    })
    processo.on("close", (codigo) => {
      clearTimeout(relogio)
      resolve({ codigo: codigo ?? 0, saida, erro })
    })

    processo.stdin.end(JSON.stringify(entrada ?? {}))
  })
}

const FERRAMENTAS_DE_ESCRITA = new Set(["write", "edit", "patch", "multiedit"])

export const StackxHooks = async ({ directory, worktree }) => {
  const raiz = worktree ?? directory
  let avisouNaSessao = false

  return {
    // sem-convencoes: uma linha no contexto, no início da sessão
    "chat.message": async (_entrada, _saida) => {
      if (avisouNaSessao) return
      avisouNaSessao = true
      const r = await rodar(raiz, "sem-convencoes.py", { hook_event_name: "SessionStart" })
      if (r.saida?.trim()) console.log(r.saida.trim())
    },

    // aderencia: verifica o arquivo recém-escrito
    "tool.execute.after": async (entrada, saida) => {
      const ferramenta = (entrada?.tool ?? "").toLowerCase()
      if (!FERRAMENTAS_DE_ESCRITA.has(ferramenta)) return

      const args = saida?.args ?? entrada?.args ?? {}
      const caminho = args.filePath ?? args.file_path ?? args.path
      if (!caminho) return

      const r = await rodar(raiz, "aderencia.py", {
        tool_name: entrada.tool,
        tool_input: { file_path: caminho },
      })
      if (r.erro?.trim()) console.warn(r.erro.trim())
    },
  }
}
