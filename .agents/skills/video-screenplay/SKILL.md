---
name: video-screenplay
description: Turns a screenplay excerpt (sluglines, action, dialogue, in any language) into a faithful visual analysis, a shot breakdown that respects the clip duration, the standard scene specs, and Wan/LTX prompts — separating what is visible from internal states, dialogue and sound, and never inventing story. Use when the user pastes a screenplay or script excerpt, or types $video-screenplay, $video_from_screenwright or $video-from-screenplay.
metadata:
  aliases: video_from_screenwright, video-from-screenplay
---

# video-screenplay

Aliases: `$video_from_screenwright` (original request name), `$video-from-screenplay`.

## Purpose

Read a screenplay excerpt like a director and assistant director would: find
where and when it happens, who is on screen, what is *visible*, in what order,
and how many shots that needs at the requested duration. Then feed the existing
pipeline so the result is the **same `scene-spec.yaml`** every other skill uses.

The screenplay is never turned into a prompt directly. The chain is mandatory:

```
source-screenplay.md → screenplay-analysis.yaml → scene-spec.yaml (one per shot)
  → storyboard.md → shot-spec.yaml → prompts/<adapter>.txt
```

## When to use

- The user pastes text with screenplay structure: sluglines (`INT.`/`EXT.`),
  CHARACTER cues, dialogue, transitions — in any language.
- `$video-screenplay`, `$video_from_screenwright`, `$video-from-screenplay`,
  with the excerpt in the same message or the next one.
- `video` routes here when the idea is a screenplay excerpt.

Not for a one-sentence idea (use `video`), or for writing/rewriting the
screenplay itself.

## Inputs

| Input | Required | Form |
|-------|----------|------|
| Excerpt | yes | Pasted text (screenplay or prose) |
| `--model <wan\|ltx\|all>` | no | Adapters to compile (default: project adapters) |
| `--duration <seconds>` | no | Length of **one generation** (default: `kit/defaults.yaml → format.duration_s`) |
| `--style <preset-id or words>` | no | Look (e.g. `cinematic`, "black-and-white noir") |
| `--ref <path>` | no | Character or style reference image (repeatable) |

Natural-language equivalents work too ("for LTX, 5 seconds, noir look").

Also read: `kit/conventions.md`, `kit/defaults.yaml`, `kit/vocabulary.md`,
existing `projects/<id>/characters/*.yaml`, `templates/source-screenplay.md`,
`templates/screenplay-analysis.yaml`, `schemas/screenplay-analysis.schema.json`.

## Workflow

### 1. Intake

1. Split options from the excerpt. If there is no excerpt, ask the user to
   paste it. Stop.
2. If the text is a plain idea with no screenplay structure and no sequence of
   events, hand over to `video`.
3. **Project**: as in `video` Step 1 (reuse the conversation's project, or one
   named by a character/title, else create one). Excerpt id = next free
   `excerpt-NNN`.
4. Write `screenplay/<excerpt-id>/source-screenplay.md` from the template:
   the excerpt **verbatim** in a fenced block, with line numbers kept
   implicit (line 1 = first line of the excerpt). Never edit this file later.

### 2. Parse

Classify every non-empty line. First matching rule wins:

| Element | Recognize by | Examples |
|---------|--------------|----------|
| Scene heading | Starts with `INT.`, `EXT.`, `INT./EXT.`, `I/E`, `INTERIOR`, `EXTERIOR` (any case/language variant) | `INT. COZINHA - NOITE`, `EXT. PRAIA – PÔR DO SOL` |
| Transition | Ends with `TO:` or is `FADE IN/OUT`, `CUT TO`, `DISSOLVE`, `CORTA PARA`, `FUSÃO` | `CUT TO:` |
| Character cue | Line in capitals, ≤ 4 words, optionally `(V.O.)`, `(O.S.)`, `(O.C.)`, `(CONT'D)`, followed by dialogue | `MARIA`, `JOÃO (O.S.)` |
| Parenthetical | `( … )` line directly under a cue or inside dialogue | `(whispering)` |
| Dialogue | Lines after a cue until a blank line | `João?` |
| Camera direction | `CLOSE ON`, `ANGLE ON`, `POV`, `WE SEE`, `INSERT`, `WIDE`, `PLANO DETALHE`… | `CLOSE ON the glass.` |
| Action / description | Everything else | `Maria entra lentamente.` |

Heading → `interior_exterior`, `location` (English) + `location_original`,
`time_of_day` (English) + `time_original`. Text without any screenplay
formatting is treated as action lines (`format_detected: prose`).

### 3. Visual extraction

Split action lines into sentences and classify each one:

| Class | Test | Goes to |
|-------|------|---------|
| **Visible action** | A camera would record it | a beat (`action`, `reveal` or `reaction`) |
| **Setting description** | Describes place/objects without change | environment / objects (no beat) |
| **Sound** | Something heard: "a noise", "BANG", "we hear", words in CAPS that are sounds | `sound_cues` + a `sound` beat (no visual) |
| **Non-visual** | Thought, memory, feeling stated as fact, backstory, intention, knowledge | `non_visual` (step 4) |
| **Camera direction** | See parse table | `camera_hints` (provenance `screenplay`) |

Then build:

- **Characters**: every name in cues and action. `presence`: `on-screen`
  (acts or is described in the frame), `offscreen` (V.O./O.S., or heard only),
  `mentioned` (named, never present). Only `on-screen` characters are rendered.
  Pronouns in the screenplay ("she") are evidence for gender presentation.
- **Objects**: every object an action depends on. `key` if the story needs it
  (the broken glass); `implied: true` when an action requires it but the text
  does not name it (a watering can for "waters").
- **Beats**: one beat per visible change or per sound/dialogue event, **in
  screenplay order**. `original` = source sentence verbatim; `visual` =
  English description of only what is visible. Estimate durations:

  | Beat type | Estimate |
  |-----------|----------|
  | action (walk in, sit, pick up) | 2–3 s |
  | reveal (light on a face, an object noticed) | 2 s |
  | reaction (freeze, turn, flinch) | 1.5–2 s |
  | dialogue | 0.5 s + words ÷ 2.5 s |
  | sound | 0.5 s (no visual time of its own) |

- **Dialogue**: exact text in the original language, speaker as written,
  parenthetical, `on_screen`. Its `visual_consequence` is what the speaker
  visibly does ("calls out toward the hallway") — never the words.
- **Sound cues**: English `cue`; `affects` = the reaction, gaze or timing it
  motivates **only if the screenplay shows that reaction** (the next beat).
- **On-screen text**: signs, notes, screens — kept verbatim, never translated.
- **Mood**: one word or short phrase, `inferred` unless written.

### 4. Non-visual information

For every non-visual statement decide, in this order:

| Handling | When | Result |
|----------|------|--------|
| `already-evident` | Other beats already show it ("She is afraid." after "She freezes.") | Nothing added. |
| `visible-behavior` | It can be shown with **subtle performance only** (expression, posture, pause), adding no event, object, person or cut | Expression/posture in the spec, `status: assumed`, listed under "I assumed". |
| `ask` | Showing it needs a narrative device — flashback, insert of an associated object, voice-over, visual metaphor — or the statement is central to the scene | CRITICAL question with options (below). |
| `omit` | Irrelevant to the image (e.g. backstory with no bearing on the shot) or the user chose "no explicit representation" | Recorded, not shown. |

Question format for `ask`:

```
The screenplay describes an internal state: "<original>".
How should it appear on screen?
a) close-up and a change of expression (recommended)
b) a short flashback (adds a separate shot)
c) an object associated with the memory
d) no explicit representation
```

Never invent a narratively important representation without asking.

### 5. Characters and continuity

For each `on-screen` character:

1. Match against `projects/<id>/characters/*.yaml`: id = name lowercased,
   accents removed, spaces → hyphens (`João` → `joao`); also compare `name`.
   - one match → reuse (`match: existing`). Do not re-describe appearance.
     If the screenplay states a trait that contradicts the file, flag it as a
     conflict (asked in step 7).
   - several candidates → `match: ambiguous` → ask which one.
   - none → `match: new` → `video-character`, with traits stated in the
     screenplay tagged `screenplay` and the rest `inferred`.
2. One character file per person for the whole excerpt; every shot reuses it.

### 6. Shot breakdown and duration

`clip_duration_s` = `--duration` if given, else the kit default (5 s, tagged
`default`). Visual-beat budget per generation (from `video-storyboard`):

| Clip duration | Max visual beats |
|---------------|------------------|
| ≤ 3 s | 1 |
| 3–6 s | 2 |
| 6–10 s | 3 |

Sound beats and dialogue beats spoken by an on-screen character in the same
setup do not count as separate visual beats when they happen inside another
beat's time.

1. `est_total_s` = sum of beat estimates. `fits_single_generation` = visual
   beats ≤ budget **and** `est_total_s` ≤ `clip_duration_s` + 1.
2. If it fits → 1 shot covering all beats.
3. If it does not fit → set `warning` ("This excerpt contains N visual beats
   (~T s) and is unlikely to work as a single X-second generation.") and
   prepare three options for step 7:
   - **split** into shots (recommended);
   - **reduce** to the key beats that fit one clip (list which ones stay);
   - **lengthen** the clip (state which adapters handle it; see each
     `adapter.md → Duration`).
4. Splitting rules:
   - Hard cut points: new scene heading, transition, location or time change,
     a camera direction (`INSERT`, `CLOSE ON`, `POV`).
   - Natural cut points: an object reveal (insert/POV), a reaction to sound,
     a change of who is in frame.
   - Each shot covers **contiguous** beats in order and respects the budget.
   - Use the fewest shots that respect the budget. Maximum 6 shots per run;
     if more are needed, propose processing the excerpt in parts.
   - Shot duration = max(3 s, its beats' estimate rounded up), ≤ `clip_duration_s`.
   - `camera_suggestion`: neutral coverage implied by the beats (entrance →
     medium/wide; reveal of an object → close-up/POV insert; reaction →
     medium close-up). Tagged `inferred`.

### 7. Clarify (one message, ≤ 4 questions)

Run the policy of `video-clarify` with a pre-filled record: everything the
screenplay states is STATED (source `screenplay`) and is **never asked**
(location, interior/exterior, time, who is present, actions, dialogue).
Possible CRITICAL questions, in this priority:

1. Shot plan — only when the excerpt does not fit (split / reduce / lengthen).
2. Non-visual statements with `handling: ask`.
3. Ambiguous character match or screenplay-vs-character-file contradiction.
4. Look/style — only if neither the screenplay, `--style`, nor the project
   defines it.

Everything else is an assumption in the list (character design, camera per
shot, lighting, duration if defaulted). Ask in the language of the user's
message; if the user only pasted the excerpt, use the excerpt's language.

### 8. Write the analysis

`screenplay/<excerpt-id>/screenplay-analysis.yaml` from the template, valid
against `schemas/screenplay-analysis.schema.json`, with the user's decisions
(`shot_breakdown.decision`, non-visual `status`, ambiguity `resolution`) and a
`provenance` block (`screenplay` / `user` / `inferred` / `default`).

### 9. Feed the standard pipeline — once per shot

Scene ids: next free `scene-NNN` in shot order. For each shot:

1. `video-scene` with a record built from the analysis:
   - `idea` = the source lines this shot covers, verbatim; `idea_language`.
   - `source` = `{type: screenplay, excerpt, shot, beats}`.
   - `environment.interior_exterior`, `location`, `time_of_day` from the
     heading → `screenplay`.
   - `subjects` = on-screen characters in this shot (`character_id`), or the
     key object when no character is visible (an insert).
   - `timeline.beats` = this shot's **visual** beats, `description` = the
     beat's `visual` text (provenance `screenplay`), timing `inferred`.
   - `audio.dialogue` / `audio.sfx` = lines and cues that occur in this shot,
     verbatim; `audio.generate: false` unless the user asked for sound.
   - `constraints.must_include` = key objects of these beats (`screenplay`);
     `must_not_include` = characters that are offscreen/mentioned/absent as
     "other people", plus story elements the model tends to add that the
     screenplay does not have (e.g. "blood" next to broken glass) → `inferred`.
   - `continuity.previous_scene` / `next_scene` = neighbouring shots;
     `must_remain_consistent` = character traits, light source, time of day.
   - camera from `camera_hints` (`screenplay`) or `camera_suggestion` (`inferred`).
2. `video-storyboard` (beats are given: it only times them and designs first
   and last frames; it must not add, drop or reorder beats).
3. `video-shot`.
4. `video-prompt` for the adapters from `--model` or the project.
5. `history.md` for the scene; append the scene id to `project.yaml → scenes`.

### 10. Report (user's language)

```
Excerpt saved: projects/<p>/screenplay/excerpt-NNN/ (source + analysis)

Read from the screenplay: <INT/EXT>, <location>, <time> · on screen: <names> · <N> beats
Not visual: <NV items and how each is handled>
Dialogue kept verbatim (not sent to the video model): <lines>
Sound cues: <cues> — used only for timing/reactions

Shots (<clip_duration_s> s each max):
1. scene-NNN — beats 1–2 — <summary> — <camera>
2. ...

I assumed: <character design, camera, lighting, duration if default>
Warnings: <from shot-specs>
Prompts: scenes/scene-NNN/v001/prompts/<adapter>.txt for each shot
Next: generate shot by shot; review with "$video-review" on each scene.
```

## Rules

1. **Fidelity first.** Never add events, characters, narratively relevant
   objects, location changes, actions, endings, or emotions that contradict
   the text. Neutral cinematic detail (lens, framing, light quality consistent
   with the heading, non-narrative set dressing) is allowed and tagged `inferred`.
2. **Order is sacred.** Beats keep screenplay order; each shot covers a
   contiguous range. `video-shot` blocks any reordering (check C16).
3. **Visible only.** Prompts describe what a camera records. Thoughts, sounds
   and dialogue words never become literal images.
4. **Dialogue is preserved, not voiced.** Exact text goes to `audio.dialogue`;
   prompts show only the speaking action. Sound is generated only if
   `audio.generate: true` and the adapter supports audio.
5. **Don't translate visible text or names.** Proper names stay as written;
   on-screen text stays in the original language.
6. **Reuse characters.** Never redesign a character that already has a file.
7. **Duration is a hard constraint.** Never put more visual beats in a clip
   than the budget allows; warn and offer split / reduce / lengthen.
8. **Few shots.** Fewest shots that respect the budget; never more than 6 per run.
9. **Honest provenance.** `screenplay` only for what the text states; anything
   derived is `inferred`; kit defaults are `default`.
10. **One spec format.** Output scenes are ordinary scenes — `video-review` and
    `video-iterate` work on them unchanged.

## Output

```
projects/<project-id>/
  screenplay/<excerpt-id>/
    source-screenplay.md
    screenplay-analysis.yaml
  characters/<id>.yaml                  # new characters only
  scenes/<scene-id>/                    # one per shot
    history.md
    v001/scene-spec.yaml  storyboard.md  shot-spec.yaml
         prompts/<adapter>.txt (+ .negative.txt)  generation-config.yaml
```

## Failure handling

| Situation | Action |
|-----------|--------|
| No excerpt pasted | Ask for it; show the expected format in one line. |
| Several scene headings in one excerpt | Each heading starts a new group of shots; if more than 6 shots result, process the first heading and offer to continue. |
| No heading (prose) | Ask for location/time only if no sentence implies them; otherwise infer (`inferred`). |
| A character's appearance contradicts their file | Ask: keep the file, or update the character (affects other scenes). |
| User wants all beats in one short clip | Explain the budget, offer reduce/lengthen; if they insist, compile and record the risk in `warnings`. |
| Excerpt mostly non-visual (inner monologue) | Report it; ask how to represent the core idea before writing any spec. |
| Requested adapter missing | List `adapters/*/`; compile the available ones. |

## Examples

**Single shot** — `examples/screenplay-rooftop/` (English):

```
EXT. ROOFTOP GARDEN - DAWN
ELENA (60s), in a grey wool cardigan, waters a row of tomato plants.
She pauses and looks out over the waking city.
Elena has waited all winter for this morning.
```

2 visual beats, ~5 s → 1 shot. The last line is backstory → `visible-behavior`
(a quiet, content expression), listed as an assumption. One question (look).

**Multi-shot** — `examples/screenplay-kitchen/` (PT-BR, `--duration 5`):

```
INT. COZINHA - NOITE
Maria entra lentamente na cozinha.
A luz da geladeira aberta ilumina seu rosto.
Ela percebe um copo quebrado no chão.
MARIA
João?
Um barulho vem do corredor.
Maria congela.
```

6 beats (~10.5 s) vs a 5 s clip → warning; user chooses split → 3 shots:
enter into the fridge light · insert of the broken glass · call, noise, freeze.
"João?" is kept verbatim in `audio.dialogue`; João is mentioned only and never
rendered; the noise is a sound cue that motivates the freeze.
