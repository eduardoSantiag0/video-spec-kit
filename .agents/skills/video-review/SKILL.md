---
name: video-review
description: Turns the user's description of a generated clip into a structured diagnosis — what to keep, issues with likely causes tied to spec fields, and ranked minimal changes — and records the generation (seed, output) for reproducibility. Use after the user generates a clip and describes the result, or types $video-review.
---

# video-review

## Purpose

Diagnose, don't rewrite. Map what the user saw to the smallest spec changes
that are likely to fix it, while protecting what already works. The review is
the input of `video-iterate`.

## When to use

- The user describes a generated result ("the camera is good but the face changes").
- `$video-review "<observation>"`.
- Feedback flow of `video`.

## Inputs

- The user's observation, verbatim (any language).
- Optional: which run/model, seed, output path, settings that differed from the plan.
- Target version: current version of the scene in this conversation, unless named.
- That version's `scene-spec.yaml`, `shot-spec.yaml`, `generation-config.yaml`,
  `iteration.md` (if any). `templates/review.md`.

## Workflow

1. **Run.** Identify the run in `generation-config.yaml`. One planned run → that
   one. Several → the one the user named; if not named and not obvious, ask
   once: "Which model was it: wan or ltx?".
2. **Record the generation.** Set the run's `status: generated`,
   `generated_at`, and `seed` / `output` / changed settings if the user gave
   them. If the seed is unknown, keep `null` and add one line asking for it
   ("Without the seed, the next experiment can't isolate the change.") —
   do not block on it.
3. **Split the observation** into statements. Positive → **Keep** (map to spec
   paths). Negative → **Issues**. Do not add issues the user did not report;
   unmentioned scorecard dimensions are `n.a.`.
4. **Classify each issue** with the taxonomy below; pick the likely cause by
   checking the spec (e.g. a head turn in the beats explains identity drift).
5. **Severity:** `blocker` (clip unusable), `major` (clearly visible),
   `minor` (noticeable on close look). Use the user's wording ("ruins it" →
   blocker).
6. **Suggested changes,** ranked. Each one changes **one** spec path (or one
   generation parameter, listed as such). Rank by: severity of the issue it
   fixes → likelihood → smallest change. Never propose changing a **Keep** path.
7. **Recommended next experiment:** the top suggestion, with what stays fixed
   (all other spec fields, seed, model, settings).
8. **Write** `review.md` in the version folder from the template (English;
   the user observation stays verbatim). Second review of the same version
   (other run) → append a `## Run <id>` section instead of overwriting.
   Writing `review.md` freezes the version (`kit/conventions.md` §3).
9. **Close the loop.** If the version has an `iteration.md`, fill its
   *Observed result* and *Conclusion* (confirmed / rejected / inconclusive).
   Update the version's row in `history.md` (Result, Verdict, Best so far).
10. **Report** in the user's language: keep list, issues, recommended next
    experiment. Ask whether to create the next version with it.

## Issue taxonomy

| Category | Typical symptoms | Likely causes in spec | Minimal fixes (try in this order) |
|----------|------------------|-----------------------|-----------------------------------|
| `identity-drift` | face/hair/clothes change during clip | head turn or face angle change in beats; anchor too long/vague; close shot + motion; no reference | remove head turn from beats → shorten/sharpen `prompt_anchor` → `input_mode: image-to-video` with character ref → wider `shot_size` |
| `anatomy-hands` | flickering/melting fingers, extra limbs | fine hand action; hands moving near camera | simplify action (hands rest/grip) → reframe so hands are smaller → lower `movement_speed` |
| `motion-too-fast` | rushed, smeared movement | `movement_speed`/`pace` high; too many beats | lower `camera.movement_speed` or `motion.pace` → fewer beats |
| `motion-too-little` | nearly static clip | motion not described (common in LTX) | explicit `motion.subject_motion` / `background_motion` → raise `pace` |
| `camera-ignored` | camera did not do the planned move | vague `movement_detail`; two moves competing | explicit direction/speed in `movement_detail` → remove competing move |
| `camera-unwanted` | camera moved, should be still | no explicit static instruction | `camera.movement: static` + `movement_detail: "camera completely still"` |
| `temporal-flicker` | lighting/texture pulses | lighting change in beats; mixed sources | remove lighting change → simplify `lighting.type` |
| `background-warp` | buildings bend, objects morph | fast camera; dense background | lower `movement_speed` → fewer `background_elements` |
| `missing-element` | requested thing absent | element in P2/P3 or buried | add to `constraints.must_include` (→ P1) → remove competing details |
| `unwanted-element` | extra people, objects, text | not excluded; setting implies it | add to `constraints.must_not_include` → positive phrasing in environment ("empty street") |
| `style-drift` | look differs from intent | conflicting style refs; weak style | set/replace `presets.style` → remove conflicting `style.references` |
| `framing` | subject cut off, wrong size | framing/shot size unclear | `camera.framing` → `camera.shot_size` |
| `physics` | implausible motion, sliding feet | discrete or complex action | continuous action wording → simpler action |
| `quality` | blur, noise, low detail | generation settings | generation param: steps / resolution / profile (not a spec change) |

## Rules

1. Never invent observations. Unmentioned = not observed.
2. Never rewrite the scene. Suggest one-variable changes.
3. Protect **Keep** paths; say explicitly that they stay unchanged.
4. Distinguish spec changes from generation-parameter changes.
5. If the user's description is too vague to classify ("it's bad"), ask one
   question with options from the taxonomy (face? motion? camera? look?).

## Output

- `<version>/review.md`.
- Updated `generation-config.yaml` run (status, seed, output).
- Updated `history.md`, and `iteration.md` result/conclusion when present.

## Failure handling

| Situation | Action |
|-----------|--------|
| No scene exists yet | Explain that a review needs a spec; offer `$video` to create one from what they generated. |
| User reviewed an older version | Review that version; note it is not the current one. |
| Issue caused by something not in the spec (model bug, tool error) | Record it as `quality` / note; suggest a generation-parameter or model change, not a spec change. |

## Examples

Input: *"The camera movement is good, but the character's face changes and the
hand animation is unstable."*

- Keep: `camera.movement`, `camera.movement_detail`, lighting.
- I1 `identity-drift` (major) — cause: beat 2 has a head turn toward camera.
- I2 `anatomy-hands` (minor) — cause: beat 1 includes a one-handed wipe
  of rain from her brow.
- Suggested: (1) `timeline.beats[1].description` remove the head turn;
  (2) `timeline.beats[0].description` both hands stay on the handlebars;
  (3) `format.input_mode` → `image-to-video` with a character reference.
- Next experiment: (1) only, same seed.

Full file: `examples/tokyo-rain/scenes/scene-001/v001/review.md`.
