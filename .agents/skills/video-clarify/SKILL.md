---
name: video-clarify
description: Finds the ambiguities in a video idea that would really change the generated clip, asks only those (CRITICAL) questions with concrete options, and states sensible assumptions for everything else (OPTIONAL). Never re-asks what the user already said. Use when starting a scene from an idea, or when the user types $video-clarify. Called by the video skill.
---

# video-clarify

## Purpose

Remove the ambiguity that matters — and only that. Output a clarification
record that `video-scene` turns into a spec, where every value is tagged
`user`, `inferred` or `default`.

## When to use

- Step 2 of `video` (new scene).
- The user types `$video-clarify <idea>` to see what is ambiguous without
  writing files.
- An answer to a previous round introduced a new critical gap (round 2).
- Called by `video-screenplay` with a pre-filled record: dimensions the
  screenplay states are STATED with source `screenplay` and are never asked.

## Inputs

- The idea (verbatim).
- Project context, if any: `project.yaml`, existing `characters/*.yaml`,
  previous scenes' `scene-spec.yaml` (for continuity).
- `kit/defaults.yaml` (defaults and inference rules).

## Workflow

### 0. Mode

If the request carries `--no-questions` or `--not-questions` (or says "no
questions", "sem perguntas", "don't ask", "just generate"), run in
**no-questions mode**: do steps 1–2, then skip steps 3–6 and resolve every
CRITICAL dimension with the table in *No-questions mode* below. Never send a
question in this mode.

### 1. Extract

Go through the dimension table below. For each dimension, mark it:

- **STATED** — the user said it (keep a short quote as evidence).
- **INFERABLE** — follows from what was said, via an inference rule in
  `kit/defaults.yaml` or an obvious implication ("neon signs" → night).
- **MISSING** — neither.

### 2. Classify every MISSING dimension

| Dimension | Spec paths | CRITICAL when missing if... | Otherwise OPTIONAL — assume |
|-----------|------------|-----------------------------|-----------------------------|
| Subject | `subjects[].description` / `character_id` | always (no subject = no video) | — |
| Action | `subjects[].action` | always | — |
| Setting | `environment.location` | no location at all and the action does not imply one | the most plausible location for the action |
| Look / realism | `style.realism`, `style.visual_style`, `presets.style` | no style cue at all (photo, film, anime, 3D, documentary, cinematic, realistic...) | — |
| Camera viewpoint & movement | `camera.movement`, `camera.shot_size`, `camera.angle` | the subject travels through space (walks, runs, rides, drives, flies, swims) — follow / alongside / lead / static produce different videos | static medium shot, eye level |
| Subject appearance | character fields | the project already has scenes, or the user implied a specific person ("my character", "the same woman") | a reusable character coherent with the setting |
| Continuity | `continuity.*`, `timeline.first_frame` | the project has other scenes and the relation is unclear | standalone scene |
| Input mode | `format.input_mode`, `references.images` | the user mentions having an image/photo/reference | text-to-video |
| Duration | `format.duration_s` | never | 5 s |
| Aspect ratio | `format.aspect_ratio` | never (inference rule covers platforms) | 16:9 |
| Time of day, weather, era | `environment.*` | never | day, clear, present day |
| Lighting | `lighting.*` | never | inferred from time + weather |
| Pace, speed | `motion.pace`, `camera.movement_speed` | never | inferred from action |
| First / last frame | `timeline.*` | never (video-storyboard designs them) | — |
| Exclusions | `constraints.must_not_include` | never | none beyond adapter quality negatives |
| Audio | `audio.*` | never; only include if the user mentions sound | omitted |

### 3. Decide

- 0 CRITICAL → ask nothing. Return the record. (`video` shows the assumptions
  in its final report.)
- 1 or more CRITICAL → one message with every CRITICAL question (no upper
  limit — ask as many as the idea actually needs), then the assumptions list.
  If the idea is so vague that the list would be unreadable, group the
  closely related ones into a single question with combined options rather
  than dropping any.

### 4. Ask (single message)

Format:

```
A few choices change this video a lot:

1. <Question about dimension>?
   a) <option> (recommended)   b) <option>   c) <option>   — or describe your own
2. ...

I'll assume the rest — reply "change <item>" for anything you want different:
- <assumption>
- <assumption>   (max 8, most impactful first)
```

Option rules: 2–4 options, concrete and visual, mutually exclusive, the
recommended one first and labeled. The recommendation must fit the idea and
the intent (e.g. "alongside" for a ride through a city: shows the rider and the
city at once).

### 5. Parse the answer

- Map each answer to spec paths. Picked option or own words → `user`.
- Values stated in a screenplay excerpt → `screenplay` (not `user`).
- "You choose" / "whatever" → recommended option, tagged `inferred`.
- Extra details the user volunteers (e.g. "she looks tired") → `user`.
- An answer that changes an assumption → that path becomes `user`.
- Unanswered questions → recommended option, tagged `inferred`, and mention it.

### 6. Further rounds

Only if an answer creates a new CRITICAL gap (e.g. "make it part of my other
project" → continuity unclear). Keep asking additional rounds for as long as
each answer keeps introducing new CRITICAL gaps; stop as soon as a round
introduces none. There is no fixed cap on the number of rounds.

## No-questions mode

Each CRITICAL dimension gets the choice that preserves the source best and
adds the least. Every auto-decision is tagged `inferred` (never `user`) and
listed in the record under `auto_decisions` so the final report can show it.

| CRITICAL dimension | Automatic choice |
|--------------------|------------------|
| Look / realism | `presets.style: cinematic` (photorealistic) — unless the project defines a style preset |
| Camera viewpoint & movement | the option that would have been marked *(recommended)* |
| Subject appearance | a reusable character designed by `video-character` |
| Continuity unclear | standalone scene (no `previous_scene`) |
| Input mode — reference mentioned but no file given | `text-to-video`, plus a warning |
| Shot plan does not fit the clip (screenplay) | **split** into shots |
| Non-visual statement that needs a representation (screenplay) | subtle performance (close-up feel, change of expression) if the character is on screen in that beat; otherwise **omit**. Never a flashback, memory object, voice-over or any added event. |
| Ambiguous character match (screenplay) | the file whose id equals the normalized name; if none, a new character with a suffixed id (`maria-2`) and a warning |
| Screenplay trait contradicts an existing character file | keep the file (continuity), warn with the screenplay's wording |

The only case that still stops is input that cannot produce a video at all
(no subject and no action, or an empty excerpt). That is reported as an
error with an example, not asked as a question.

## Rules

1. Never ask about a STATED dimension, even to "confirm".
2. Never turn an OPTIONAL dimension into a question. It goes in the
   assumptions list.
3. No cap on the number of questions — ask every CRITICAL dimension, however
   many that is. Further rounds only while an answer keeps introducing a new
   CRITICAL gap (see §6).
4. Questions are about the video, not about the files or the kit.
5. No yes/no questions when options are possible.
6. Do not ask about technical generation settings (steps, CFG, seed).
7. Assumptions list ≤ 8 items; never list trivial defaults that the user would
   not notice (e.g. `depth_of_field: moderate`).
8. Language (`kit/conventions.md` §7): accept the idea in any language; write
   questions, options and assumptions in the language of the user's latest
   message; store record values in English that preserve the user's meaning.
   If a word has no faithful English equivalent or two plausible readings that
   change the image, keep the original term with a gloss, or — if the readings
   differ visually — make it a CRITICAL question.

## Output

A clarification record (kept in the conversation and passed to `video-scene`;
printed as YAML when the skill is invoked directly):

```yaml
idea: "<verbatim, original language>"
idea_language: en
values:                # values in English; evidence quotes stay in the original language
  - { path: environment.location, value: "Tokyo side street", source: user, evidence: "through Tokyo" }
  - { path: camera.movement, value: tracking-side, source: user, evidence: "answer 2: alongside" }
  - { path: format.duration_s, value: 5, source: default }
characters_needed: [ { subject: rider, reason: "main human subject" } ]
open_questions: []
auto_decisions:        # only in no-questions mode
  - { path: presets.style, value: cinematic, reason: "no style stated" }
```

## Failure handling

| Situation | Action |
|-----------|--------|
| User answers only some questions | Use recommended options for the rest (`inferred`), say so in one line. |
| Answer contradicts the idea ("no rain" for a rain idea) | The latest statement wins; tag `user`; mention the change. |
| User refuses to answer / "just do it" | Recommended options for all, tagged `inferred`. |
| Idea is not visual (e.g. a podcast) | Explain the kit specifies visual clips; ask what should be on screen. |

## Examples

**One question.** Idea: *"8-second medium shot of a woman running through rainy
Tokyo at night, camera following from behind."*
STATED: duration, shot size, subject, action, location, weather, time, camera
movement. CRITICAL missing: look. → Ask 1 question (look). Assume: 16:9,
reusable character, neon/street light, eye level, 35mm.

**Zero questions.** Idea: *"Photorealistic close-up of a cup of coffee steaming
on a wooden table, static camera, morning light."* Nothing critical missing →
no questions.

**Two questions.** Idea: *"A woman rides a bicycle through Tokyo at night
during heavy rain."* CRITICAL: look; camera viewpoint (she travels). → 2
questions + assumptions. See `examples/tokyo-rain/walkthrough.md`.

**Non-English input.** Idea: *"Um pescador idoso conserta a rede no cais ao
amanhecer, câmera parada."* STATED: subject, action, location, time (dawn),
camera (static). CRITICAL missing: look. → One question, asked in Portuguese:

```
Uma escolha muda bastante este vídeo:
1. Qual visual?
   a) fotorrealista cinematográfico (recomendado)  b) documentário  c) animação 2D
Vou assumir o resto — responda "mude <item>" para ajustar:
- 5 s, 16:9 · plano médio ao nível dos olhos · luz quente e baixa do amanhecer
```

Record values are English (`environment.location: "wooden pier"`,
`environment.time_of_day: dawn`), `idea` stays in Portuguese with
`idea_language: pt-BR`.
