---
name: video-scene
description: Writes scene-spec.yaml — the structured, model-agnostic source of truth for one scene — from a clarification record, applying presets, inference rules and defaults, and tagging every value with provenance (user / inferred / default). Use after clarification, when the user types $video-scene, or to edit a draft scene's spec.
---

# video-scene

## Purpose

Produce the single file that defines the scene. Every later artifact
(storyboard, shot spec, prompts) is derived from it, so it must be complete,
specific, schema-valid and honest about what the user said versus what the
agent chose.

## When to use

- Step 4 of `video`.
- `$video-scene` with an idea or a clarification record.
- Editing a draft version's spec (not frozen — see `kit/conventions.md` §3).

## Inputs

- Clarification record from `video-clarify` (or the user's explicit values).
- Character ids from `video-character`.
- `projects/<id>/project.yaml` (defaults, presets).
- `presets/<kind>/<id>.yaml` (and project-local presets).
- `kit/defaults.yaml`, `kit/vocabulary.md`, `templates/scene-spec.yaml`,
  `schemas/scene.schema.json`.

## Workflow

1. **Target file.** New scene: `scenes/<scene-id>/v001/scene-spec.yaml`.
   Draft edit: the current version's file. Frozen version: stop and hand over
   to `video-iterate`.
2. **Header.** `spec_version: 1`, `id`, `project`, `version`, `title`
   (≤ 6 words, English), `idea` (verbatim, original language),
   `idea_language`, `intent` (one English sentence about what the viewer
   should feel; `user` if stated, else `inferred`). Screenplay-derived scenes
   also get `source` (`excerpt`, `shot`, `beats`) and `idea` = the excerpt lines
   this shot covers.
3. **Presets.** Reference a preset when the user named a matching look
   (`user`) or when one clearly fits the stated setting (`inferred`; e.g.
   neon-lit city at night → `lighting: neon-night`). Then add
   `project.yaml → defaults.presets` for kinds not yet set (`default`).
   Note which fields each referenced preset defines.
4. **User values.** Write every `user` value from the clarification record at
   its path, normalized to English with the user's meaning preserved
   (`kit/conventions.md` §7); map to vocabulary terms when one fits
   (`"alongside"` / `"ao lado"` → `camera.movement: tracking-side`). A
   translated value is still `user`.
5. **Inference rules.** Apply `kit/defaults.yaml → inference_rules` top to
   bottom → `inferred`. Skip a field if it is already set or a referenced
   preset defines it.
6. **Agent design choices.** Fill what makes the shot concrete and is not
   covered yet → `inferred`: `subjects[].position`, `camera.movement_detail`,
   `environment.background_elements` (2–4 concrete items),
   `environment.atmosphere`, `motion.subject_motion`,
   `motion.background_motion`.
7. **Defaults.** Fill remaining fields from `project.yaml → defaults`, then
   `kit/defaults.yaml` → `default`. **Skip any field a referenced preset
   defines** (otherwise the default would override the preset).
8. **Subjects.** Main subjects reference `character_id`. Add `expression`
   (scene-specific emotion) here, not in the character file.
9. **Constraints.** `must_include`: things the user insisted on.
   `must_not_include`: user exclusions, plus intrusions that are likely for
   this setting and would break the intent (e.g. other cyclists in a "lonely
   ride") → `inferred`. Do not add generic quality negatives — adapters do.
10. **Timeline.** Leave out; `video-storyboard` writes it. Exception: for
    screenplay-derived scenes, write the shot's beats (descriptions from
    `screenplay-analysis.yaml → beats[].visual`, provenance `screenplay`) and
    let `video-storyboard` time them.
11. **Provenance.** List every explicit leaf path in exactly one group
    (`screenplay`, `user`, `inferred`, `default`). A section name may stand
    for all its fields when they share one source.
12. **Self-check** before saving:
    - all required fields present (`schemas/scene.schema.json`);
    - enum fields use `kit/vocabulary.md` values;
    - no `<placeholder>`, no empty values, no null;
    - every leaf path appears once in `provenance`;
    - one primary action per subject; ≤ 3 subjects.

## Rules

1. Semantic, not prompt syntax: no "8k", "masterpiece", "trending", no weights
   like `(word:1.3)`, no model names.
2. Specific over generic: "narrow side street with vending machines" not
   "a street".
3. Actions must be physically simple and continuous for a single clip.
4. Never overwrite a `user` value with an inferred or default one.
5. Never copy preset values into the spec; reference the preset. Write a field
   that a preset also defines only to override it on purpose (tag the reason's
   source).

## Output

`projects/<project-id>/scenes/<scene-id>/<version>/scene-spec.yaml`, valid
against `schemas/scene.schema.json`. Chat (when invoked directly): file path
and a 3-line summary of user / inferred / default counts.

## Failure handling

| Situation | Action |
|-----------|--------|
| A required field has no value and no default | Stop; ask one question for that field. |
| User value is not in the vocabulary (e.g. "whip pan") | Use the closest enum (`pan`) and keep the nuance in `movement_detail`. |
| More than 3 subjects | Keep the 3 most important; move the rest to `environment.background_elements`; warn. |
| More than one primary action per subject | Keep the first in `action`; propose splitting into scenes. |

## Examples

Excerpt for the Tokyo idea (full file:
`examples/tokyo-rain/scenes/scene-001/v001/scene-spec.yaml`):

```yaml
presets: { style: cinematic, lighting: neon-night }
camera:
  shot_size: medium
  movement: tracking-side
  movement_detail: tracks alongside her from the left at matching speed, keeping her centered
provenance:
  user: [camera.movement, presets.style, environment.weather, environment.time_of_day]
  inferred: [presets.lighting, camera.movement_detail]
  default: [format.duration_s, format.aspect_ratio, format.fps]
```
