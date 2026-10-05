# Video Spec Kit

🇧🇷 [Leia em português](README.pt-BR.md)

**Specify before you prompt.** Turn a vague idea for an AI-generated video into
a clear, structured, versioned specification — and compile it into prompts
tuned for each video model.

```
$video A woman rides a bicycle through Tokyo at night during heavy rain.
```

→ two smart questions → a scene spec, a storyboard, a shot spec, a Wan prompt,
an LTX prompt, and reproducible generation settings. You generate the clip in
your own tool, describe what you see, and the kit helps you fix it **one
variable at a time**.

> Video Spec Kit does **not** generate video. It is a set of Markdown skills,
> schemas, templates and model adapters that run inside the coding agent you
> already use. No backend, no API, nothing paid required.

Already have a script? Paste a screenplay excerpt instead of an idea —
`$video-screenplay` turns it into shots and prompts without inventing story.

---

## Table of contents

- [The problem](#the-problem)
- [The proposal](#the-proposal)
- [Philosophy](#philosophy)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Example](#example)
- [From a screenplay](#from-a-screenplay)
- [Workflow](#workflow)
- [File structure](#file-structure)
- [Agent support](#agent-support)
- [Model support](#model-support)
- [Create an adapter](#create-an-adapter)
- [Create a preset](#create-a-preset)
- [Languages](#languages)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [How this project was made](#how-this-project-was-made)
- [License](#license)

---

## The problem

Prompting a video model usually looks like this: write a paragraph, generate
(minutes of GPU), something is off, rewrite the whole paragraph, generate
again. After ten attempts:

- you don't know which change fixed what — or broke what;
- the model filled every gap you didn't specify (camera, light, wardrobe…) at random;
- the prompt that worked for Wan doesn't work for LTX;
- the character looks different in every clip;
- you can't reproduce last week's best result because you didn't record the seed.

## The proposal

Treat the video like software built from a spec:

1. **Clarify** only the decisions that change the video completely.
2. **Specify** the scene in structured YAML — the source of truth.
3. **Plan** time (storyboard) and the shot (camera, lens, framing, start/end).
4. **Compile** the spec into a prompt per model with a *prompt adapter*.
5. **Generate** in your tool (ComfyUI, a CLI, anything).
6. **Review** what you saw; get a diagnosis tied to spec fields.
7. **Iterate** with a controlled experiment: one change, same seed, recorded diff.

```
IDEA → CLARIFY → SCENE SPEC → STORYBOARD → SHOT SPEC → MODEL PROMPT
     → (you generate) → REVIEW → ITERATE
```

Inspired by the philosophy of GitHub's Spec Kit (specification-driven
development), applied to video — with no dependency on it.

## Philosophy

1. Specify before prompting.
2. Separate intent from model syntax.
3. Clarify only what matters.
4. Prefer structured specifications.
5. Prompts are compiled artifacts.
6. Preserve continuity.
7. Change one variable at a time.
8. Record experiments.
9. Make generation reproducible.
10. Remain model-agnostic.

Each principle and how the kit implements it: [docs/philosophy.md](docs/philosophy.md).

## Installation

You need:

- **git**, and
- **a coding agent** that can read and write files in a folder — Codex,
  Claude Code, Gemini CLI, OpenCode, or any other (free tiers and local models
  work; see [Agent support](#agent-support)).

```bash
git clone https://github.com/<your-org>/video-spec-kit.git
cd video-spec-kit
```

That's it. No packages, no build step. Optional extras:

- `pip install pyyaml jsonschema` → `python tools/validate.py` checks your specs.
- VS Code + the YAML extension → live schema validation while editing
  (configured in `.vscode/settings.json`).

## Quick start

1. Open your agent **in the repository folder**:

   ```bash
   codex        # or: claude · gemini · opencode
   ```

2. Describe your video:

   | Agent | Type |
   |-------|------|
   | Codex | `$video A samurai walks through Tokyo during heavy rain at night.` |
   | Claude Code, Gemini CLI | `/video A samurai walks through Tokyo during heavy rain at night.` |
   | OpenCode | `Use the video skill: a samurai walks through Tokyo during heavy rain at night.` |
   | Any other agent | `Read .agents/skills/video/SKILL.md and follow it: a samurai walks…` |

   Write in any language — the agent asks its questions in your language and
   keeps the specs and prompts in English.

3. Answer the (few) questions — or add `--not-questions` to the command to skip
   them and let the kit decide (every decision is listed afterwards). The agent writes your files to
   `projects/<name>/scenes/scene-001/v001/` and shows the prompts.

4. Paste `prompts/wan.txt` (or `ltx.txt`) into your video tool, use the
   settings in `generation-config.yaml`, note the seed.

5. Tell the agent what you saw:

   ```
   $video the camera is great but her face changes halfway through
   ```

   It writes a review, proposes one change, and on "yes" creates `v002` with
   only that change.

## Example

[`examples/tokyo-rain/`](examples/tokyo-rain/) is a complete, versioned run:
idea → clarify → spec → storyboard → shot → Wan + LTX prompts → generation
config → review → v002 experiment → review.
Start with the [walkthrough](examples/tokyo-rain/walkthrough.md).

The same shot compiled for two models:

**Wan** (`v001/prompts/wan.txt`, 134 words, shot first, negative prompt used)

> Medium tracking shot at eye level. A Japanese woman in her late 20s with a
> short black bob, wearing a translucent yellow raincoat over a charcoal hoodie,
> dark jeans and white sneakers, carrying a small red backpack, rides a bicycle
> steadily through heavy rain, tired but determined, … The camera tracks
> alongside her from the left at her speed, keeping her centered. …

**LTX** (`v001/prompts/ltx.txt`, 174 words, action first, chronological)

> A woman rides a bicycle steadily through heavy rain along a narrow Tokyo side
> street at night. She is a Japanese woman in her late 20s with a short black
> bob, … Her legs pedal at a steady rhythm and her upper body leans slightly
> forward against the rain. …

And the experiment that fixed the face (`v002/iteration.md`):

```diff
  timeline.beats[1].description:
-   She glances toward the camera for a moment, then looks back at the road ahead …
+   She keeps her eyes on the road ahead and leans slightly into the pedals …
```

Seed, model and settings unchanged → the result is attributable to that one line.

## From a screenplay

```
$video-screenplay --duration 5

INT. COZINHA - NOITE

Maria entra lentamente na cozinha.
A luz da geladeira aberta ilumina seu rosto.
Ela percebe um copo quebrado no chão.

MARIA
João?

Um barulho vem do corredor.
Maria congela.
```

The skill parses sluglines, characters, action, dialogue and sound; separates
what is **visible** from thoughts, memories and sounds; keeps the beats in
order; warns that 5 visual beats don't fit one 5-second clip; and — after you
pick "split" — writes three ordinary scenes (enter into the fridge light ·
insert of the broken glass · call, noise, freeze) with Wan and LTX prompts.
`"João?"` is kept verbatim but not voiced, the noise is only a sound cue, and
nobody appears in the hallway.

Don't want questions? Add `--not-questions` (or `--no-questions`), paste the
excerpt, and everything is generated; the report lists each decision the kit
made for you (e.g. "shot plan → split", "look → cinematic").

Also available as `$video_from_screenwright` and `$video-from-screenplay`.
Guide: [docs/screenplay.md](docs/screenplay.md) · examples:
[single shot](examples/screenplay-rooftop/walkthrough.md),
[three shots, PT-BR](examples/screenplay-kitchen/walkthrough.md).

## Workflow

Most people only use **`video`**. It runs the whole pipeline and routes your
feedback. The other skills give fine control:

| Skill | Purpose |
|-------|---------|
| `video` | Orchestrator: idea → files; feedback → review → iteration. |
| `video-clarify` | Find the ambiguities that matter; ask only those (CRITICAL vs OPTIONAL). |
| `video-character` | Reusable characters with a consistency lock and a verbatim prompt anchor. |
| `video-scene` | Write `scene-spec.yaml`, the source of truth, with provenance on every value. |
| `video-storyboard` | First frame, 1–3 timed beats, last frame. |
| `video-shot` | Camera, lens, movement, framing; merge presets/characters; detect conflicts. |
| `video-prompt` | Compile for a model: `$video-prompt wan`, `$video-prompt ltx`. |
| `video-review` | Diagnose a generation from your description. |
| `video-iterate` | New version, one change, same seed, recorded diff. |
| `video-screenplay` | Screenplay excerpt → visual analysis → shot breakdown → scene specs → prompts. Aliases: `video_from_screenwright`, `video-from-screenplay`. |

Details: [docs/workflow.md](docs/workflow.md) ·
how prompts are compiled: [docs/prompt-compiler.md](docs/prompt-compiler.md).

### You always know what you said vs. what the agent chose

Every value in a spec has provenance:

```yaml
provenance:
  user:     [camera.movement, environment.weather, environment.time_of_day]
  inferred: [camera.movement_detail, presets.lighting]
  default:  [format.duration_s, format.aspect_ratio, format.fps]
```

`user` = you said it · `screenplay` = written in your screenplay excerpt ·
`inferred` = derived from what you said · `default` = a kit default you never mentioned.

## File structure

```
video-spec-kit/
├── AGENTS.md  CLAUDE.md  GEMINI.md     # agent entry points (all point to AGENTS.md)
├── .agents/skills/<skill>/SKILL.md     # the 10 skills — canonical source
├── .claude/{skills,commands}/  .gemini/commands/  # generated wrappers + aliases
├── kit/
│   ├── conventions.md                  # layout, versioning, provenance, language policy
│   ├── defaults.yaml                   # defaults + inference rules
│   └── vocabulary.md                   # controlled camera/style terms
├── schemas/*.schema.json               # JSON Schema (draft 2020-12)
├── templates/                          # skeletons for every generated file
├── adapters/
│   ├── wan/  adapter.md  prompt-template.md
│   ├── ltx/  adapter.md  prompt-template.md
│   └── _template/
├── presets/{styles,cameras,lighting}/*.yaml
├── projects/                           # YOUR work goes here
├── examples/
│   ├── tokyo-rain/                     # idea → v001 → review → v002
│   ├── screenplay-rooftop/             # screenplay → one shot
│   └── screenplay-kitchen/             # screenplay (PT-BR) → three shots
├── docs/                               # philosophy, workflow, compiler, screenplay, agents, extending, comfyui
└── tools/                              # optional: validate.py, sync_agent_wrappers.py
```

What one scene looks like in your project:

```
projects/<project>/
  project.yaml
  characters/<id>.yaml
  screenplay/excerpt-001/      # only when you start from a screenplay
    source-screenplay.md       # verbatim
    screenplay-analysis.yaml   # beats, dialogue, sound, non-visual, shot breakdown
  scenes/scene-001/
    history.md                 # one row per version: change → result → verdict
    v001/
      scene-spec.yaml          # source of truth
      storyboard.md            # beats over time
      shot-spec.yaml           # resolved + conflict-checked (compiler IR)
      prompts/wan.txt  wan.negative.txt  ltx.txt  ltx.negative.txt
      generation-config.yaml   # model, seed, size, frames, steps, CFG, sampler…
      comfyui-notes.md         # optional
      review.md                # after you generate
    v002/ … + iteration.md     # what changed and why
```

Each version folder is self-contained and frozen once reviewed, so every result
stays reproducible. Rules: [kit/conventions.md](kit/conventions.md).

## Agent support

| Agent | How it finds the skills | Invoke |
|-------|-------------------------|--------|
| Codex | `.agents/skills/` (native) | `$video …` |
| Claude Code | `.claude/skills/` (generated wrappers) | `/video …` |
| Gemini CLI | `.agents/skills/` + `.gemini/commands/` | `/video …` |
| OpenCode | `.agents/skills/` (native) | "use the video skill: …" |
| Anything else | `AGENTS.md` | "Read `.agents/skills/video/SKILL.md` and follow it: …" |

Skills follow the open Agent Skills format (`SKILL.md` + `name`/`description`
frontmatter). Wrappers are generated, so each skill exists in one place.
More, including local-model tips: [docs/agent-support.md](docs/agent-support.md).

## Model support

| Adapter | Models | Prompt style | Negative prompt | Notes |
|---------|--------|--------------|-----------------|-------|
| [`wan`](adapters/wan/adapter.md) | Wan 2.1, Wan 2.2 (T2V, I2V, TI2V-5B, FLF2V) | Shot → subject → action → scene → camera → light → style; 80–150 words | Yes (official list, adapted) | 16 fps / 81 frames (4n+1) on 14B models |
| [`ltx`](adapters/ltx/adapter.md) | LTX-Video 0.9.x, 13B; LTX-2 | Action first, chronological, literal; 100–180 words | Yes, with CFG > 1 | 24 fps, 8n+1 frames, sizes ÷ 32 |

Both are open-weight models you can run locally (e.g. in ComfyUI). The
spec is model-agnostic; adding a model means adding an adapter folder.
ComfyUI usage: [docs/comfyui.md](docs/comfyui.md).

> Adapter settings (steps, CFG, shift…) are documented starting points written
> against public model docs. Your workflow may differ — the kit records what you
> actually ran.

## Create an adapter

```bash
cp -r adapters/_template adapters/<model-id>
```

Fill the frontmatter profile (word budget, slot order, negative prompt,
frame rule, sizes per aspect ratio, sampler defaults) and the guidance
sections (camera, motion, reference images, temporal consistency, dialogue
and sound, duration, limitations). Then `$video-prompt <model-id>`.
Full guide: [docs/extending.md](docs/extending.md#create-a-prompt-adapter).

## Create a preset

```yaml
# presets/lighting/blue-hour.yaml
spec_version: 1
id: blue-hour
kind: lighting
description: Deep blue twilight after sunset; city lights just turning on.
values:
  lighting:
    type: residual skylight plus early street lights
    contrast: medium
    color_temperature: mixed
```

Use it in a scene with `presets: { lighting: blue-hour }`; any field the scene
sets explicitly overrides the preset.
Full guide: [docs/extending.md](docs/extending.md#create-a-preset).

## Languages

- Write ideas and screenplays in **any language**.
- The agent asks questions and reports **in your language**.
- Specs are normalized to **English** internally, so they stay comparable
  across projects and contributors.
- Prompts are in **English** unless a model's adapter sets another language
  because the model benefits from it.
- Never translated: your original idea, the screenplay excerpt, proper names,
  dialogue, and text that must appear inside the image.

Full rule: `kit/conventions.md` §7.

## Contributing

Adapters for more models, presets, translations of the docs, and reports of
"what actually worked" are the most valuable contributions.
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Roadmap

Planned — **not** in V1, on purpose:

- [ ] Automatic ComfyUI integration (send a version to a running ComfyUI)
- [ ] Import/export of ComfyUI workflows from/to `generation-config.yaml`
- [ ] Automatic multimodal evaluation of generated clips
- [ ] Frame comparison between versions
- [ ] Direct integration with local video models
- [ ] A dedicated CLI (`vsk new`, `vsk compile`, `vsk diff`)
- [ ] Package installer (add the kit to an existing repo)
- [ ] Adapter marketplace / registry
- [ ] Community presets
- [ ] Timeline / story editor across scenes
- [ ] Multi-shot generation in one clip

## How this project was made

This project was built **mainly with AI**. The architecture, skills, schemas,
adapters, examples and documentation were generated by an AI coding agent
(Claude, in Claude Code) from detailed specifications written by the
maintainer, who directed the design, set the requirements and reviewed the
result. The kit's own files were checked with the included validator, but the
Wan/LTX settings were not tested against real generations — treat them as
documented starting points — and the reviews in the examples are fictional.
Corrections from people who run these models are especially welcome.

## License

[Apache License 2.0](LICENSE). Chosen over MIT because it is equally
permissive (commercial use, modification, redistribution) and adds an explicit
patent grant and clear contribution terms — useful for a project that hopes to
collect adapters and presets from many contributors.
