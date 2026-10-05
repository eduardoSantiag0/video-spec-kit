# From screenplay to video: `video-screenplay`

`video-screenplay` turns a **screenplay excerpt** into the kit's standard scene
specs and model prompts. It is for short films, commercials, animation, music
videos and narrative scenes — any text written as a script.

```
$video-screenplay [--model wan|ltx|all] [--duration <s>] [--style <look>] [--ref <image>] [--no-questions]
<paste the excerpt>
```

**Just paste and generate:** add `--no-questions` (or `--not-questions`) and
nothing is asked — every decision is made automatically and listed at the end:

```
$video-screenplay --not-questions
INT. COZINHA - NOITE
Maria entra lentamente na cozinha.
...
```

Automatic choices (from `video-clarify` → *No-questions mode*): shot plan →
split · missing look → `cinematic` · non-visual line → subtle performance, or
omitted when no one is on screen (never a flashback or an added event) ·
ambiguous character → exact-id match or a new suffixed character · blocking
conflicts → the screenplay wins. All are tagged `inferred`, so you can still
see what you didn't decide. The only stop is an empty excerpt or one with
nothing visible.

Aliases: `$video_from_screenwright`, `$video-from-screenplay`
(Claude Code / Gemini CLI: `/video-screenplay`, `/video_from_screenwright`, `/video-from-screenplay`).

## About the name

The skill was requested as `video_from_screenwright`. Two problems with that
as the canonical name:

1. *Screenwright* is not standard English. A script is a **screenplay**; its
   author is a **screenwriter** (*playwright* is the stage equivalent).
2. Agent Skills names may only contain lowercase letters, digits and hyphens,
   and must match their folder — underscores are rejected by strict loaders.

So the skill is **`video-screenplay`**, and `video_from_screenwright` keeps
working as an alias: a slash command in Claude Code and Gemini CLI, and an
alias rule in `AGENTS.md` for Codex, OpenCode and other agents.

## Pipeline

```
source-screenplay.md          the excerpt, verbatim, never edited
   ↓ parse                    sluglines, INT/EXT, characters, action, dialogue,
   ↓                          parentheticals, transitions, camera directions
   ↓ visual extraction        visible actions vs setting vs sound vs non-visual;
   ↓                          beats in order; objects; dialogue; sound cues
screenplay-analysis.yaml      intermediate representation + shot breakdown
   ↓ clarify                  only shot plan / non-visual / character / look
scene-spec.yaml (one per shot)   ← the same format every other skill uses
   ↓ storyboard → shot → prompt
prompts/wan.txt, prompts/ltx.txt
```

Prompts are never written from the raw screenplay.

## What it reads from a screenplay

| Screenplay element | Becomes |
|--------------------|---------|
| `INT. COZINHA - NOITE` | `environment.interior_exterior: interior`, `location: kitchen`, `time_of_day: night` (provenance `screenplay`) |
| Character cue `MARIA` + lines | `audio.dialogue: [{character: MARIA, text: "João?"}]` — verbatim, original language |
| Visible action | A beat in `timeline.beats`, order preserved |
| Sound ("Um barulho vem do corredor.") | `audio.sfx`; drives the reaction's timing and gaze, never drawn |
| `CLOSE ON`, `POV`, `INSERT` | Camera values with provenance `screenplay`, and shot boundaries |
| `CUT TO:` | A shot boundary |
| Thoughts, memories, backstory | `non_visual` — handled explicitly (below) |
| Signs or notes visible in frame | `on_screen_text`, kept in the original language |

## Non-visual information

A line like *"Carlos remembers everything his father told him."* is never
rendered literally. Each one gets a handling:

| Handling | Used when |
|----------|-----------|
| `already-evident` | Other beats already show it |
| `visible-behavior` | Subtle performance can carry it (expression, posture, a pause) — listed as an assumption |
| `ask` | It needs a narrative device (flashback, memory object, voice-over) or is central — the user picks |
| `omit` | It has no bearing on the image, or the user chose no representation |

The `ask` question offers: close-up and change of expression · flashback ·
an object associated with the memory · no explicit representation.

## Duration and shots

`--duration` is the length of **one generation**. Visual-beat budget per clip:
≤ 3 s → 1 beat · 3–6 s → 2 · 6–10 s → 3. Sound beats, and dialogue spoken
inside another beat, don't count.

When the excerpt doesn't fit, the skill warns and offers:

- **split** into shots (recommended) — contiguous beats, fewest shots, max 6 per run;
- **reduce** to the key beats that fit — and says which beats are lost;
- **lengthen** the clip — and says which adapters handle it.

Each shot becomes a normal scene (`scenes/scene-NNN/`) with a `source` block
(`excerpt`, `shot`, `beats`) and `continuity` links to its neighbours.

## Fidelity rules

- No added events, characters, narratively relevant objects, location changes,
  actions, endings, or emotions that contradict the text.
- Neutral cinematic detail (framing, lens, light quality matching the heading,
  non-narrative set dressing) is allowed and tagged `inferred`.
- `must_not_include` blocks common model inventions the screenplay doesn't
  support (other people, a figure in a doorway, blood next to broken glass).
- Existing characters are matched by name/id and reused, never redesigned.
- Provenance distinguishes `screenplay` (written in the text), `user`
  (answers and options), `inferred` and `default`.

## Language

Any language in, questions in the user's language, specs in English, prompts in
English. Proper names, dialogue and on-screen text stay exactly as written.

## Examples

- [`examples/screenplay-rooftop/`](../examples/screenplay-rooftop/walkthrough.md) — English, one shot, a non-visual line as subtle performance.
- [`examples/screenplay-kitchen/`](../examples/screenplay-kitchen/walkthrough.md) — Portuguese, `--duration 5`, six beats → three shots, dialogue and sound cue.

Normative steps: [`.agents/skills/video-screenplay/SKILL.md`](../.agents/skills/video-screenplay/SKILL.md).
