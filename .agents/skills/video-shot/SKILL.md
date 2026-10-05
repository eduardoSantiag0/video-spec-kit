---
name: video-shot
description: Designs and resolves the shot — camera, lens, movement, framing, focus, start/end of shot — then merges defaults, presets and characters into a fully resolved, conflict-checked shot-spec.yaml with prompt priorities. First half of the Prompt Compiler. Use after the storyboard, when the user types $video-shot, or before compiling prompts for a draft version.
---

# video-shot

## Purpose

Turn the intent in `scene-spec.yaml` into one concrete, unambiguous shot that
every prompt adapter can consume. This is where contradictions are caught —
**before** any prompt is written.

Prompt Compiler stages handled here: (1) read, (2) shot design,
(3) resolve, (4) conflict detection, (5) prioritization. Stages 6–9
(profile, render, lint, write) are in `video-prompt`. Overview: `docs/prompt-compiler.md`.

## When to use

- Step 6 of `video`.
- `$video-shot` on a scene.
- Automatically by `video-prompt` when the target version is a draft.

## Inputs

- `scene-spec.yaml` (with `timeline`).
- Referenced `characters/*.yaml`, `presets/*/*.yaml` (project-local first).
- `project.yaml`, `kit/defaults.yaml`, `kit/vocabulary.md`, `kit/conventions.md` §5.
- `templates/shot-spec.yaml`, `schemas/shot.schema.json`.

## Workflow

### 1. Shot design

Check the camera block against action and intent. Fill missing details →
`inferred` in `scene-spec.yaml` (never change `user` values; skip fields a
referenced preset defines):

- `framing`: subject placement + leading space in the direction of travel.
- `focus_target`: the main subject unless the intent says otherwise.
- `movement_detail`: direction, side, distance, relation to subject speed.
- `lens` / `depth_of_field`: from shot size via `kit/defaults.yaml` rules.
- Start and end of shot: confirm `timeline.first_frame` / `last_frame` are
  achievable with this camera (a static wide shot cannot end on a close-up).

### 2. Resolve

Build every field by the order in `kit/conventions.md` §5:
defaults → project defaults → presets (style, camera, lighting) → character →
scene. Record the winning source per path in the shot-spec `provenance`
(`preset: { lighting/neon-night: [...] }`, `character: { mika: [...] }`).

For each subject: `anchor` = the character's `prompt_anchor` verbatim (plus a
short scene-specific `description` addition if present); `locked` = values of
its `consistency_lock` paths.

### 3. Conflict detection

Run every check. Blocking conflicts stop compilation.

| ID  | Check | Blocking |
|-----|-------|----------|
| C1  | `camera.movement: static` but `movement_detail` or any beat describes the camera moving | yes |
| C2  | More than one primary camera movement described (movement + a different move in detail/beats) | yes |
| C3  | `time_of_day` incompatible with lighting (night + sunlight / golden-hour) | yes |
| C4  | `weather` incompatible with environment/atmosphere (heavy rain + dry dusty street) | yes |
| C5  | Same item in `must_include` and `must_not_include` | yes |
| C6  | `style.realism` contradicts `visual_style` (anime + photorealistic) | yes |
| C7  | Scene description changes a character's `consistency_lock` value without a note saying it is intentional | yes |
| C8  | `input_mode` needs a reference image (`first_frame`/`last_frame` role) that is missing | yes |
| C9  | Beats leave gaps/overlaps or do not end at `duration_s` | no — auto-fix and record |
| C10 | Beats exceed the budget in `video-storyboard` | no — warning |
| C11 | Close shot size but several environment `must_include` items | no — warning |
| C12 | Travelling subject + `static` camera + duration > 3 s (subject may leave frame) | no — warning |
| C13 | Duration above what the target adapters generate well (see each `adapter.md` → Duration) | no — warning |
| C14 | `timeline.first_frame` differs from previous scene's `last_frame` | no — warning |
| C15 | Referenced presets list each other in `avoid_with` | no — warning |
| C16 | `source.type: screenplay` and the timeline drops, adds or reorders the beats listed in `source.beats`, or beats are not contiguous | yes |
| C17 | A character marked `offscreen`/`mentioned` in the screenplay analysis appears as a subject | yes |

An explicit scene value that overrides a preset value is **not** a conflict —
that is how overrides work.

For each conflict write `{id, fields, description, blocking, resolution}`.
Blocking + unresolved → `resolution: pending user decision`.

**No-questions mode** (`--no-questions` / `--not-questions` on the request):
never ask. Resolve each blocking conflict by source priority
`screenplay` > `user` > `inferred` > `default` (same source: the latest
statement wins); C16 → restore the screenplay order; C17 → remove the
offscreen character from the subjects. Write
`resolution: "auto: <what was kept and why>"` and copy it into `warnings`.

### 4. Complexity and risk

Count subjects, simultaneous actions, camera moves, beats. Risk is `high` if
any: ≥ 2 subjects interacting physically, fine hand manipulation, face turning
toward camera in a close/medium shot, fast camera + fast subject; `medium` if
one of: hands visible in motion, head turn, `movement_speed: fast`,
crowd in background; else `low`. List `risk_reasons`, and copy each into
`warnings` with the specific beat/time.

### 5. Prioritization

Assign short phrases to tiers. **Each fact appears in one tier only.**

- **P1** — subject anchor + action, location + time + weather, shot size +
  angle + camera movement, every `must_include` item.
- **P2** — lighting, style/realism, later beats, key background elements,
  expression.
- **P3** — texture/grain, lens, depth of field, secondary background, atmosphere details.

### 6. Write

`shot-spec.yaml` from the template; `negatives` = `constraints.must_not_include`.
Copy `source` and add `derived_from.screenplay_analysis` for screenplay-derived scenes.
Dialogue text and sound cues stay in `audio`; they never become P1–P3 phrases
unless `audio.generate: true`.
Validate against `schemas/shot.schema.json` (required fields, enums, no
placeholders).

## Rules

1. Never change a `user` value to resolve a conflict. Ask — except in
   no-questions mode, where the source priority above decides and the
   decision is reported.
2. The shot-spec is derived: always regenerate it from the spec; never patch
   it by hand to change the video.
3. One primary camera movement per shot.
4. Warnings must be specific ("2.5–4 s: head turn toward camera in medium shot
   → identity drift risk"), never generic ("may have artifacts").

## Output

`<version>/shot-spec.yaml` and, when shot design filled gaps, an updated
`scene-spec.yaml`. Chat: count of conflicts (blocking / auto-fixed) and warnings.

## Failure handling

| Situation | Action |
|-----------|--------|
| Blocking conflict | Write the shot-spec with the conflict, then ask one question per conflict with 2–3 resolutions. After the answer, update `scene-spec.yaml` (tag `user`) and re-run. |
| Referenced preset or character file missing | Stop; name the missing file; offer to create it or remove the reference. |
| Version frozen | Read-only: verify the existing shot-spec; do not rewrite. |

## Examples

User's spec has `camera.movement: static` and `movement_detail: "handheld,
tracking the runner"` → C1 blocking:

```yaml
conflicts:
  - id: C1
    fields: [camera.movement, camera.movement_detail]
    description: Camera is static but the detail describes a handheld tracking move.
    blocking: true
    resolution: pending user decision
```

Question to the user: "Should the camera (a) stay still on a tripod, or (b)
follow the runner handheld?"

Clean result: `examples/tokyo-rain/scenes/scene-001/v001/shot-spec.yaml`.
