---
name: video-storyboard
description: Designs what happens over time inside one clip — first frame, 1–3 timed beats, last frame — writes it into the scene spec's timeline and renders a readable storyboard.md. Use after the scene spec exists, when the user types $video-storyboard, or wants to change the sequence of events.
---

# video-storyboard

## Purpose

Make time explicit. Video models need to know the starting image, the change,
and the ending image. Writing them down prevents overloaded clips and gives
continuity points for neighbouring scenes.

## When to use

- Step 5 of `video`.
- `$video-storyboard` on an existing scene.
- The user wants to change "what happens" in a draft version.

## Inputs

- `scene-spec.yaml` of the target version.
- Neighbour scenes' `scene-spec.yaml` when `continuity.previous_scene` /
  `next_scene` are set.
- `templates/storyboard.md`.

## Workflow

1. **Beat budget** from `format.duration_s`:

   | Duration | Beats |
   |----------|-------|
   | ≤ 3 s    | 1     |
   | 3–6 s    | 1–2   |
   | 6–10 s   | 2–3   |
   | > 10 s   | 3 max — and recommend splitting the scene |

2. **First frame.** One still-image description: subject position and pose,
   framing, background, light. If `previous_scene` exists, it must match that
   scene's `timeline.last_frame` (same position, wardrobe, light) — copy and
   adapt it.
3. **Beats.** Contiguous `start_s`/`end_s` covering 0 → `duration_s` with no
   gaps or overlaps. Each beat = one visible change that follows from the
   action. Prefer continuous progressions over discrete events.
4. **Last frame.** Still-image description of the end state. If `next_scene`
   exists, design it as a clean hand-off (subject still in frame, stable pose).
5. **Camera consistency.** Beats describe subject/environment change; the
   camera behaviour per beat must follow `camera.movement` (a `static` shot has
   no camera change in any beat).
6. **Write** `timeline` into `scene-spec.yaml`; tag its paths `inferred`
   unless the user dictated them (`user`).
7. **Render** `storyboard.md` from the template. The Camera column repeats the
   camera behaviour per beat in plain words. Add 2–4 design notes explaining
   choices against the `intent`.

## Rules

0. **Given beats.** If the spec has `source.type: screenplay`, the beats are
   fixed by the screenplay: do not add, drop, merge, rephrase the action of,
   or reorder them. Only set `start_s`/`end_s` and design the first/last
   frames. Sound and dialogue in the shot go in the Notes column at their time.
1. Never exceed the beat budget.
2. No cuts inside a scene. Never write "cut to", "meanwhile", "later".
3. First and last frames are images, not actions: describe states.
4. Beats must not introduce new subjects or props that are not in the spec;
   add them to the spec first (with provenance) if needed.
5. Describe risky moments honestly in the Notes column (head turns, hands near
   camera, fast moves) — `video-shot` uses them for warnings.

## Output

- `timeline` block in `scene-spec.yaml` (+ provenance).
- `storyboard.md` in the same version folder.

## Failure handling

| Situation | Action |
|-----------|--------|
| The action cannot fit the duration | Propose: longer duration (if ≤ adapter max), fewer beats, or split into scenes. Ask the user to pick. |
| Continuity first frame conflicts with this scene's spec (e.g. different outfit) | Do not silently change either; report it as a conflict for `video-shot`. |
| Version is frozen | Hand over to `video-iterate`. |

## Examples

5-second ride after one iteration (`examples/tokyo-rain/scenes/scene-001/v002/storyboard.md`):

| Time    | What happens | Camera |
|---------|--------------|--------|
| 0–2.5 s | She pedals steadily through the rain and wipes rain from her brow with her right hand, then returns it to the handlebar | tracks alongside from the left at her speed |
| 2.5–5 s | She keeps her eyes on the road ahead and leans slightly into the pedals as neon light slides across her raincoat | keeps tracking, framing unchanged |

Compare with `v001/storyboard.md`, where beat 2 had a head turn toward the
camera — flagged in Notes as an identity-drift risk, and confirmed by the review.
