# Video Spec Kit

🇧🇷 [Leia em português](README.pt-BR.md)

Video Spec Kit is a conversational assistant for AI video prompting.
Describe your scene, refine it through conversation, and generate a
polished prompt for video models such as Wan and LTX.

```
$video

> Quero um homem dirigindo numa estrada.

> Como ele é e onde está a câmera?

> 23 anos, machucado. Câmera fixa dentro do carro.

> Quero que seja cinematográfico, 35mm.

> Gera.

<FINAL PROMPT>
```

> Video Spec Kit does **not** generate video. It's a set of Markdown skills
> that run inside the coding agent you already use (Claude Code, Codex,
> Gemini CLI, OpenCode...). No backend, no API, nothing paid required.

Already have a script? Paste a screenplay excerpt instead of an idea —
`$video-screenplay` reads it and joins the same conversation.

---

## Table of contents

- [Why](#why)
- [Philosophy](#philosophy)
- [Installation](#installation)
- [Quick start](#quick-start)
- [From a screenplay](#from-a-screenplay)
- [Skills](#skills)
- [How memory works](#how-memory-works)
- [File structure](#file-structure)
- [Agent support](#agent-support)
- [Model support](#model-support)
- [Create an adapter](#create-an-adapter)
- [Languages](#languages)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

---

## Why

Prompting a video model usually means writing a wall of text up front,
hoping it covers everything, and rewriting the whole thing when it doesn't.
Talking it through instead — a couple of questions, a few corrections, then
"generate" — is closer to how you'd actually brief a cinematographer.

## Philosophy

1. Conversation before prompting.
2. Ask only what matters.
3. Remember what the user already said.
4. Let the user refine naturally.
5. Structured state stays behind the scenes.
6. The final output is the prompt.
7. Never force the user to behave like a programmer.
8. Keep the tool simple.

## Installation

You need:

- **git**, and
- **a coding agent** that can read and write files in a folder — Claude
  Code, Codex, Gemini CLI, OpenCode, or any other that reads Agent Skills.

```bash
git clone https://github.com/<your-org>/video-spec-kit.git
cd video-spec-kit
```

That's it. No packages, no build step, no schema validator to install.

## Quick start

1. Open your agent **in the repository folder**:

   ```bash
   claude        # or: codex · gemini · opencode
   ```

2. Describe your scene:

   | Agent | Type |
   |-------|------|
   | Claude Code, Gemini CLI | `/video A man driving down a rural road at dusk.` |
   | Codex, OpenCode | `$video A man driving down a rural road at dusk.` |
   | Any other agent | `Read .agents/skills/video/SKILL.md and follow it: a man driving…` |

   Write in any language — the agent asks its questions in your language.

3. Answer the one or two questions it actually needs. It remembers
   everything you say.

4. Keep talking: add details, correct something ("troca a camiseta para
   cinza"), or ask it to develop the scene creatively ("deixa mais tenso").

5. Say "gera" / "generate" / "gera para Wan" when you're ready. You get a
   finished prompt, ready to paste into your video tool.

## From a screenplay

```
$video-screenplay

INT. COZINHA - NOITE

Maria entra lentamente na cozinha.
A luz da geladeira aberta ilumina seu rosto.
Ela percebe um copo quebrado no chão.
```

The skill reads the slugline, the characters and the visible action, saves
it to the same memory `video` uses, and asks only what the screenplay
doesn't already answer (usually camera and look). From there it's the same
conversation — correct, add, then "gera".

Also available as `$video_from_screenwright` and `$video-from-screenplay`.
Example: [`examples/screenplay/`](examples/screenplay/).

## Skills

| Skill | Purpose |
|-------|---------|
| `video` | Main entry point: idea → conversation → prompt. |
| `video-screenplay` | Screenplay excerpt → same conversation. Aliases: `video_from_screenwright`, `video-from-screenplay`. |
| `video-reset` | Clear the current scene and start fresh. |

How the loop works under the hood: [docs/how-it-works.md](docs/how-it-works.md).

## How memory works

Everything you say about the scene is kept in `.video/session.yaml` —
subject, action, environment, camera, lighting, style. You never need to
open it; it's not a file you edit, just the agent's memory of the
conversation. A correction always replaces the old value, nothing is asked
twice, and `$video-reset` clears it for a new scene.

```yaml
scene:
  subject: { type: man, age: 23, condition: [bruised], clothing: { top: dark grey t-shirt } }
  action: { primary: driving a car }
  environment: { location: rural highway, weather: hot sunny day }
  camera: { position: inside car, framing: medium shot, movement: static }
  style: { realism: photorealistic, look: cinematic }
```

Full example conversation and the prompt it produced:
[`examples/conversation/`](examples/conversation/).

## File structure

```
video-spec-kit/
├── README.md  README.pt-BR.md
├── AGENTS.md  CLAUDE.md  GEMINI.md     # agent entry points (all point to AGENTS.md)
├── .agents/skills/<skill>/SKILL.md     # the 3 skills — canonical source
├── .claude/{skills,commands}/  .gemini/commands/  # generated wrappers + aliases
├── adapters/
│   ├── wan/adapter.md
│   ├── ltx/adapter.md
│   └── _template/adapter.md
├── templates/
│   └── session.yaml                    # the field vocabulary .video/session.yaml uses
├── examples/
│   ├── conversation/                   # idea → conversation → prompt
│   └── screenplay/                     # screenplay → conversation → prompt
├── docs/
│   └── how-it-works.md
├── projects/                           # optional: your own notes, if you want them
└── tools/
    └── sync_agent_wrappers.py          # regenerates the generated wrappers above
```

At runtime, the only state the kit writes is `.video/session.yaml` (not
checked in — see `.gitignore`) in whatever folder you run your agent from.

## Agent support

| Agent | How it finds the skills | Invoke |
|-------|-------------------------|--------|
| Claude Code | `.claude/skills/` (generated wrappers) | `/video …` |
| Gemini CLI | `.agents/skills/` + `.gemini/commands/` | `/video …` |
| Codex, OpenCode | `.agents/skills/` (native) | `$video …` |
| Anything else | `AGENTS.md` | "Read `.agents/skills/video/SKILL.md` and follow it: …" |

Skills follow the open Agent Skills format (`SKILL.md` + `name`/`description`
frontmatter). Wrappers are generated, so each skill exists in one place.

## Model support

| Adapter | Models | Notes |
|---------|--------|-------|
| [`wan`](adapters/wan/adapter.md) | Wan 2.1 / 2.2 (T2V, I2V) | 80–150 words, negative prompt, 16 fps / 81 frames |
| [`ltx`](adapters/ltx/adapter.md) | LTX-Video 0.9.x / 13B, LTX-2 | 100–180 words, negative prompt (CFG > 1), 24 fps |

Both are open-weight models you can run locally (e.g. ComfyUI). Adding a
model means adding an adapter folder — the kit stays model-agnostic.

## Create an adapter

```bash
cp -r adapters/_template adapters/<model-id>
```

Fill in the plain-language guidance (shape, negative prompt, camera/motion,
dialogue and sound, duration, limitations, language). No frontmatter, no
compiler profile to maintain — the skill reads the file directly.

## Languages

- Describe your scene in **any language**; the agent asks and responds in
  that language.
- Internal memory is normalized to English so the agent reasons about it
  consistently — you never see it.
- The final prompt defaults to **English** (video models are best
  documented in it); ask for another language ("gera em português") and
  you'll get it.
- Never translated: proper names, dialogue, and text that must appear
  inside the image.

## Limitations

- No versioning, seed tracking, or reproducibility record — if you need
  that for your own notes, keep it yourself.
- The adapters' guidance is written against public model documentation,
  not verified against real generations. Corrections from people who
  actually run these models are welcome.
- One scene at a time. A screenplay excerpt that needs several shots is
  handled one at a time, not as a batch.

## Contributing

Adapters for more models and reports of "what actually worked" are the
most valuable contributions. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[Apache License 2.0](LICENSE).
