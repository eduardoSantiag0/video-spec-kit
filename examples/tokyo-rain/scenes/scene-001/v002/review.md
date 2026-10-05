# Review — scene-001 · v002 · run `wan-1`

**Date:** 2026-10-02
**Model:** Wan2.2-T2V-A14B · seed 428193

> Fictional review written for this example. No video is included.

## User observation (verbatim)

> Much better, her face stays the same now. The hand still flickers a little
> when she wipes the rain.

## Scorecard

| Dimension               | Result | Note |
|-------------------------|--------|------|
| Subject identity        | ok     | "her face stays the same now" |
| Subject action          | n.a.   | |
| Hands / anatomy         | issue  | slight flicker during the wipe |
| Camera                  | n.a.   | |
| Environment             | n.a.   | |
| Lighting                | n.a.   | |
| Style                   | n.a.   | |
| Temporal consistency    | ok     | follows from stable identity |
| Prompt adherence        | n.a.   | |
| Artifacts               | n.a.   | |

## Keep (do not change)

- `timeline.beats[1].description` — the v002 change fixed identity drift.
- Everything kept in v001: camera, weather/atmosphere, lighting preset.

## Issues

| ID | Issue | Category | Severity | Likely cause | Spec paths involved |
|----|-------|----------|----------|--------------|---------------------|
| I2 | Hand flickers slightly during the wipe (carried over from v001) | anatomy-hands | minor | One-handed brow wipe while riding (beat 1). | `timeline.beats[0].description` |

## Suggested changes (ranked)

1. **`timeline.beats[0].description`**: "She pedals steadily through the rain and wipes rain from her brow with her right hand, then returns it to the handlebar." → "She pedals steadily through the rain, both hands gripping the handlebars, rain running down her raincoat." — fixes I2. Hypothesis: no fine hand motion, no hand artifacts.
2. **`camera.shot_size`**: `medium` → `medium-wide` — hands become smaller in frame. Conflicts with nothing, but changes the look; try only if (1) fails.

## Recommended next experiment

Apply change 1 only, as v003. Keep everything else fixed, seed 428193.
