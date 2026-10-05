# Agent support

The skills follow the open **Agent Skills** format: a folder with a `SKILL.md`
that has `name` and `description` frontmatter. The canonical copies live in
`.agents/skills/`, a location several agents read natively. For the others, the
repo ships thin generated wrappers that point back to the canonical file, so
each skill's instructions exist in one place only.

| Agent | Discovers skills from | Invoke | Notes |
|-------|-----------------------|--------|-------|
| **Codex** (CLI / IDE) | `.agents/skills/` | `$video …` — or type `$` to pick, `/skills` to list | Native. |
| **Claude Code** | `.claude/skills/` (generated wrappers) | `/video …` | Wrapper tells Claude to read `.agents/skills/video/SKILL.md`. `CLAUDE.md` imports `AGENTS.md`. |
| **Gemini CLI** | `.agents/skills/` (skills) and `.gemini/commands/` (slash commands) | `/video …` or describe your idea | `/skills list` to verify. `GEMINI.md` imports `AGENTS.md`. |
| **OpenCode** | `.agents/skills/` and `.claude/skills/` | Ask: "use the video skill: …" | The agent loads skills with its `skill` tool. It sees both copies of each name; both lead to the same canonical file. |
| **Any other agent** | `AGENTS.md` | "Read `.agents/skills/video/SKILL.md` and follow it: <idea>" | Works with any agent that can read files in the repo, including ones backed by local models. |

## No `$video` in your agent?

Every skill is a plain Markdown file. Paste this as your first message:

```
Read .agents/skills/video/SKILL.md and kit/conventions.md, then follow the
skill for this idea: A samurai walks through Tokyo during heavy rain at night.
```

## Free and local options

Nothing in the kit calls an API. Any agent that can read and write files in the
repository works, including open-source agents (OpenCode, Gemini CLI, Codex
CLI) configured with free tiers or local models (e.g. via Ollama or LM Studio).
Smaller local models follow the skills less reliably; the `video` skill is
long, so prefer a model with a context window of at least 32k tokens.

## Keeping wrappers in sync (maintainers)

Edit skills only in `.agents/skills/`. Then:

```bash
python tools/sync_agent_wrappers.py          # regenerate .claude/skills and .gemini/commands
python tools/sync_agent_wrappers.py --check  # CI: fail if wrappers are stale
```

The script uses only the Python standard library.
