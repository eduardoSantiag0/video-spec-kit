---
name: video-iterate
description: Creates the next version of a scene as a controlled experiment — copies the parent version, changes only the requested variable (one by default), recompiles derived files, keeps the seed, and records the exact diff, hypothesis and result slot in iteration.md and history.md. Use after a review, when the user asks to change something in a frozen version, or types $video-iterate.
---

# video-iterate

## Purpose

Make every new attempt teach something. Change one variable, hold everything
else (including the seed) constant, and record what changed and why, so the
user learns how each variable affects the model.

## When to use

- After `video-review`, when the user accepts a suggested change.
- The user asks for a change on a frozen version ("make the camera slower").
- `$video-iterate "<change>"` or `$video-iterate` (uses the review's
  recommended next experiment).

For a draft version (not frozen), edit it in place instead (see `video` →
Failure handling).

## Inputs

- Parent version: current version of the scene (or the one the user names).
- Change request: a review suggestion number, or the user's words.
- Parent's files: `scene-spec.yaml`, `review.md`, `generation-config.yaml`.
- `templates/iteration.md`, `templates/history.md`.

## Workflow

1. **New version** = parent + 1 (`v001` → `v002`).
2. **Change set.** Map the request to spec paths and new values.
   - One path → `type: experiment`.
   - Several paths: if the user explicitly asked for all of them →
     `type: revision` (state why in `iteration.md`). Otherwise ask once:
     "One change at a time teaches more about what works. Apply only
     `<first>` now and queue the others? (yes / apply all)".
   - A generation parameter (steps, CFG, profile, resolution) is a valid
     single variable; it changes `generation-config.yaml`, not the spec.
3. **Copy** the parent folder to the new version: `scene-spec.yaml`,
   `storyboard.md`, `shot-spec.yaml`, `prompts/`, `generation-config.yaml`,
   `comfyui-notes.md`. Do **not** copy `review.md`, `iteration.md`, `outputs/`.
4. **Apply** the change in the new `scene-spec.yaml`: set `version`, write the
   new value(s), move each changed path to provenance `user` (the user
   approved it). Touch nothing else.
5. **Recompile** in the new version: `video-storyboard` (only if `timeline`
   or `format.duration_s` changed; otherwise just update the header line),
   then `video-shot`, then `video-prompt` for every adapter that has a run.
6. **Reset runs.** In the new `generation-config.yaml`: every run
   `status: planned`, `output` removed, `generated_at` removed. **Keep the
   parent's seed** — copy it from the parent's generated run. Keep all other
   settings unless the experiment variable is one of them.
7. **Diff check.** Compare new vs parent `scene-spec.yaml`. Allowed
   differences: `version`, the change-set paths, their provenance entries, and
   derived timeline text only if the change touched the timeline. Anything else
   → revert it. Then compare prompts sentence by sentence and list the
   sentences that changed.
8. **Write** `iteration.md` from the template: changed (diff block with
   previous → new), held constant (explicit list incl. seed), derived files
   regenerated, hypothesis (from the review suggestion or the user), observed
   result `pending`, conclusion `pending`.
9. **History.** Add a row to `history.md` (`Changed` = `path: old → new`,
   `Result: pending`); set **Current version**.
10. **Report** in the user's language: the spec diff, the prompt sentences
    that changed, the seed to reuse, and "generate, then tell me what you see".

## Rules

1. Never edit a frozen version. Always create a new one.
2. Default to one variable per version.
3. Always keep the seed for experiments; changing the seed is itself an
   experiment (`generation-config: seed`) and must be the only change.
4. Never "improve" unrelated fields while iterating, even if they look weak —
   suggest them as future experiments instead.
5. Derived files are regenerated, never patched by hand.

## Output

- `scenes/<scene-id>/<new-version>/` with all files listed in step 3 (updated)
  plus `iteration.md`.
- Updated `scenes/<scene-id>/history.md`.

## Failure handling

| Situation | Action |
|-----------|--------|
| Parent seed unknown | Proceed; write `seed: null` and in *Held constant*: "seed unknown — results not strictly comparable". |
| Requested change conflicts with a Keep item from the review | Point it out; proceed only if the user confirms. |
| Change creates a blocking conflict in `video-shot` | Resolve it with the user before writing prompts; record the resolution as part of the change set (`type: revision`). |
| User wants to go back to an older version | Create a new version copied from that older one (`Parent` = the older version); never delete versions. |

## Examples

From `examples/tokyo-rain/scenes/scene-001/v002/iteration.md`:

```diff
  timeline.beats[1].description:
-   She glances toward the camera, then looks back at the road ...
+   She keeps her eyes on the road and leans slightly into the pedals ...
```

Held constant: everything else in the spec, seed `428193`, model, resolution,
frames, steps, CFG, sampler. Hypothesis: the head turn exposes the face at
changing angles and causes identity drift.
