# Review — scene-001 · v001 · run `wan-1`

**Date:** 2026-10-01
**Model:** Wan2.2-T2V-A14B · seed 428193

> Fictional review written for this example. No video is included.

## User observation (verbatim)

> The camera movement is good and the rain looks great, but her face changes
> halfway through and her hand flickers when she wipes her face. Seed was 428193.

## Scorecard

| Dimension               | Result | Note |
|-------------------------|--------|------|
| Subject identity        | issue  | face changes halfway through |
| Subject action          | n.a.   | |
| Hands / anatomy         | issue  | hand flickers during the wipe |
| Camera                  | ok     | "camera movement is good" |
| Environment             | ok     | "rain looks great" |
| Lighting                | n.a.   | |
| Style                   | n.a.   | |
| Temporal consistency    | issue  | follows from the identity change |
| Prompt adherence        | n.a.   | |
| Artifacts               | n.a.   | |

## Keep (do not change)

- `camera.movement`, `camera.movement_detail`, `camera.movement_speed` — the user likes the tracking move.
- `environment.weather`, `environment.atmosphere` — "rain looks great".
- `presets.lighting` (neon-night) — not criticized; changing it would confound the experiment.

## Issues

| ID | Issue | Category | Severity | Likely cause | Spec paths involved |
|----|-------|----------|----------|--------------|---------------------|
| I1 | Face changes halfway through | identity-drift | major | Beat 2 (2.5–5 s) turns her head toward the camera; the face is re-generated at a new angle mid-clip. Matches the shot-spec warning. | `timeline.beats[1].description` |
| I2 | Hand flickers during the wipe | anatomy-hands | minor | Fine one-handed action near the face while riding (beat 1). Matches the shot-spec warning. | `timeline.beats[0].description` |

## Suggested changes (ranked)

Each change touches one variable so its effect can be measured.

1. **`timeline.beats[1].description`**: "She glances toward the camera for a moment, then looks back at the road ahead…" → "She keeps her eyes on the road ahead and leans slightly into the pedals as neon light slides across her raincoat." — fixes I1. Hypothesis: without the head turn, the face angle stays constant and identity holds.
2. **`timeline.beats[0].description`**: remove the brow wipe; both hands stay on the handlebars — fixes I2. Hypothesis: no fine hand motion, no hand artifacts.
3. **`format.input_mode`**: `text-to-video` → `image-to-video` with a still of Mika as first frame — stronger fix for I1 if (1) is not enough. Bigger change: needs a reference image.

Generation-parameter changes: none suggested — the issues are explained by the spec.

## Recommended next experiment

Apply change 1 only, as v002. Keep everything else fixed: all other spec
fields, seed 428193, Wan2.2-T2V-A14B, 1280×720, 81 frames, 20 steps, CFG 3.5,
euler/simple, shift 8.0. Change 2 is queued for the following version.
