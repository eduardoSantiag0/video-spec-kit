# Iteration v002 — scene-001

| Field     | Value |
|-----------|-------|
| Version   | v002 |
| Parent    | v001 |
| Date      | 2026-10-02 |
| Type      | experiment (one variable) |
| Addresses | I1 (identity drift) from `v001/review.md` |

## Changed

```diff
  timeline.beats[1].description:
-   She glances toward the camera for a moment, then looks back at the road ahead as neon light slides across her raincoat.
+   She keeps her eyes on the road ahead and leans slightly into the pedals as neon light slides across her raincoat.
```

Provenance: `timeline.beats[1].description` moved from `inferred` to `user`
(the user approved the change).

## Held constant

- Everything else in `scene-spec.yaml` (unchanged — including the brow wipe in beat 1, queued as the next experiment)
- Seed: 428193 (same as parent)
- Model Wan2.2-T2V-A14B, 1280×720, 81 frames, 16 fps, 20 steps, CFG 3.5, euler/simple, shift 8.0: unchanged
- Character `mika` and presets `style/cinematic`, `lighting/neon-night`: unchanged

## Derived files regenerated

- `storyboard.md` — beat 2 row and one design note
- `shot-spec.yaml` — beat 2, P2 phrase for beat 2, risk high → medium, head-turn warning removed
- `prompts/wan.txt` — one clause:
  - before: "…then glancing toward the camera before looking back at the road."
  - after: "…then leaning slightly into the pedals with her eyes on the road ahead."
- `prompts/ltx.txt` — one sentence:
  - before: "As she continues, she glances toward the camera, then looks back at the road ahead."
  - after: "As she continues, she keeps her eyes on the road ahead and leans slightly into the pedals."
- Negative prompts, `generation-config.yaml` settings: unchanged

## Hypothesis

If the rider does not turn her head toward the camera, the face angle stays
constant through the clip, so the model keeps her identity stable — because in
v001 the face changed exactly when the head turned (≈2.5 s).

## Observed result

Face stays consistent for the whole clip. The hand still flickers slightly
during the brow wipe (0–2.5 s). Camera and rain unchanged, as expected.

## Conclusion

**Confirmed.** The head turn was the cause of identity drift in this shot.
Learning: with Wan 2.2 at medium shot size, avoid head turns toward camera
when identity matters, or use image-to-video. I2 remains → next experiment.
