# Kit Conventions

This file is the single source of rules shared by every `video-*` skill:
workspace layout, naming, versioning, provenance, and value resolution.
Skills reference it instead of restating it.

---

## 1. Workspace layout

User work lives under `projects/`. One project = one video (one or more scenes).

```
projects/<project-id>/
  project.yaml                 # project metadata, defaults, target adapters
  characters/<character-id>.yaml
  refs/                        # user reference images (optional)
  screenplay/<excerpt-id>/     # only for scenes made by video-screenplay
    source-screenplay.md       # the excerpt, verbatim — never edited
    screenplay-analysis.yaml   # parse, visual extraction, beats, shot breakdown
  scenes/<scene-id>/
    history.md                 # experiment log for this scene (one row per version)
    v001/
      scene-spec.yaml          # SOURCE OF TRUTH for this version
      storyboard.md            # derived: human-readable beats
      shot-spec.yaml           # derived: resolved, conflict-checked shot (compiler IR)
      prompts/
        wan.txt                # derived: positive prompt for the Wan adapter
        wan.negative.txt       # derived: negative prompt (only if the adapter uses one)
        ltx.txt
        ltx.negative.txt
      generation-config.yaml   # reproducibility record: model, seed, size, steps...
      comfyui-notes.md         # optional: how to apply this version in ComfyUI
      review.md                # written by video-review after the user generates
      outputs/                 # optional: generated videos the user drops here
    v002/
      ...same files...
      iteration.md             # what changed vs. the parent version, and why
```

A scene is one continuous generated clip (one shot). Multi-shot sequences are
built from several scenes linked through `continuity`. A screenplay excerpt that
needs several shots becomes several scenes; each one points back to its excerpt,
shot number and beats with a `source` block.

## 2. Naming

| Thing        | Format                      | Example          |
|--------------|-----------------------------|------------------|
| project id   | kebab-case                  | `tokyo-rain`     |
| character id | kebab-case                  | `mika`           |
| scene id     | `scene-` + 3 digits         | `scene-001`      |
| version      | `v` + 3 digits              | `v002`           |
| excerpt id   | `excerpt-` + 3 digits       | `excerpt-001`    |
| adapter id   | lowercase directory name    | `wan`, `ltx`     |
| preset ref   | `<kind>/<id>`               | `lighting/neon-night` |

Field paths use dots and zero-based indices: `camera.movement`,
`subjects[0].action`, `timeline.beats[1].description`.

## 3. Versioning rules

1. The current version of a scene is the highest `vNNN` folder.
2. Each version folder is self-contained: it holds a full copy of every file
   needed to reproduce it. Never reference files of another version.
3. A version is **frozen** once it has a `review.md` or a non-null `seed` in
   any `generation-config.yaml` run with `status: generated`.
   Frozen versions are never edited. Changes go into a new version created by
   `video-iterate`.
4. A version that is not frozen (still a draft) may be edited in place.
5. Every version from `v002` on has an `iteration.md` describing the change.
6. `history.md` gets one row per version. It is the index, not the detail.

## 4. Source of truth and derivation

```
kit/defaults.yaml ─┐
project.yaml ──────┤
presets/*.yaml ────┼──> scene-spec.yaml ──> shot-spec.yaml ──> prompts/<adapter>.txt
characters/*.yaml ─┘     (truth)            (resolved IR)        (compiled artifact)
                                 └──> storyboard.md
```

- `scene-spec.yaml` holds the intent. Everything downstream is derived.
- For screenplay work the chain starts one step earlier and is mandatory:
  `source-screenplay.md → screenplay-analysis.yaml → scene-spec.yaml → shot-spec.yaml → prompts`.
  Prompts are never written from the raw screenplay.
- To change the video, change the spec (or a character/preset) and recompile.
- If a user hand-edits a prompt, the agent back-ports the intent into
  `scene-spec.yaml` and recompiles. A manual prompt that cannot be expressed in
  the spec is recorded as `prompt_override: true` in `generation-config.yaml`
  with a one-line reason.

## 5. Value resolution order

When building `shot-spec.yaml`, each field takes the value from the highest
layer that defines it:

```
1. kit/defaults.yaml          (lowest)
2. project.yaml → defaults
3. presets, in this order: style, camera, lighting
4. characters/<id>.yaml       (only subject appearance fields)
5. scene-spec.yaml            (highest — explicit scene values always win)
```

Rule for `video-scene`: **never write a kit default into `scene-spec.yaml` for a
field that a referenced preset already defines.** Otherwise the default would
override the preset. Defaults only fill fields no layer covers.

## 6. Provenance

Every value written to `scene-spec.yaml` is tagged by where it came from, in a
`provenance` block grouped by source. Every explicit leaf field must appear in
exactly one group. Header fields are not listed: `spec_version`, `id`,
`project`, `version`, `idea`, `idea_language`, `source`, `notes`.

| Source     | Meaning                                                              |
|------------|----------------------------------------------------------------------|
| `user`     | The user stated it (in the idea or an answer).                       |
| `screenplay` | Stated in the screenplay excerpt (heading, action, dialogue, camera direction). |
| `inferred` | The agent derived it from what the user said (e.g. night → artificial light). |
| `default`  | Taken from `kit/defaults.yaml` / `project.yaml` with no evidence.    |

```yaml
provenance:
  user:
    - subjects[0].action        # paths with [i] must be in block lists (see §9)
    - environment.weather
  inferred: [environment.location, camera.lens]
  default: [format.fps, format.aspect_ratio]
```

A path may name a whole section (`lighting`) when every field in it shares the
source. `shot-spec.yaml` uses the same block plus two extra groups for resolved
values: `preset` (map of preset ref → paths) and `character` (map of id → paths).

When the user later confirms or changes an inferred/default value, move its path
to `user`.

## 7. Language policy

This policy is mandatory for every skill.

1. **Accept input in any language.** Never ask the user to switch to English.
2. **Preserve the user's intent.** Translate meaning, not words. Keep culturally
   specific terms when no faithful English equivalent exists, with a short
   gloss (`"engawa (wooden veranda)"`). If a term is ambiguous in translation,
   treat it as an ambiguity for `video-clarify`, not as a guess.
3. **Converse in the user's language.** Clarification questions, options,
   assumption lists, reviews shown in chat and reports use the language of the
   user's latest message.
4. **Normalize specs to English.** All structured files (`scene-spec.yaml`,
   `characters/*.yaml`, `shot-spec.yaml`, `storyboard.md`, `review.md`,
   `iteration.md`, `history.md`) are written in English so they are
   comparable across projects and contributors. Two exceptions keep the
   original words:
   - `idea` — the user's idea verbatim, in the original language, with
     `idea_language` set (e.g. `pt-BR`);
   - user quotes in `review.md` ("User observation (verbatim)");
   - `source-screenplay.md` and every `original` field of
     `screenplay-analysis.yaml`;
   - dialogue text (`audio.dialogue[].text`) and proper names as written;
   - text that must appear inside the image (signs, notes, screens) — never
     translate it unless the user asks.
5. **Prompts in English** unless the adapter's profile sets another
   `prompt.language` because the target model explicitly benefits from it.
   The adapter, not the user's language, decides the prompt language.

## 8. Files the agent must not modify during user work

`kit/`, `schemas/`, `templates/`, `adapters/`, `presets/`, `.agents/`,
`.claude/`, `.gemini/`, `docs/`, `examples/`. User work goes in `projects/`.
New presets or characters requested by the user go in the project
(`projects/<id>/characters/`) unless the user asks to contribute them to the kit.

Project-local presets are allowed at `projects/<id>/presets/<kind>/<id>.yaml`
and take precedence over kit presets with the same ref.

## 9. YAML pitfalls

- A path containing `[` (e.g. `subjects[0].action`) breaks an inline list
  `[a, b]`. Use a block list (`- subjects[0].action`) or quote it.
- Quote dates (`created: "2026-10-01"`), aspect ratios (`"16:9"`) and any
  string containing `: ` or starting with `*`, `&`, `!`, `{`, `[`, `>` or `|`.
- No tabs; two-space indentation.

Optional check: `python tools/validate.py` (needs `pyyaml` and `jsonschema`).
