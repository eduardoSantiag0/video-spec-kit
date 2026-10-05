# LTX prompt template

Slots are filled from `shot-spec.yaml`. Write the result as ONE chronological
paragraph in `prompts/ltx.txt` (no slot names, no line breaks, no markdown).

## Positive prompt

```
{MAIN_ACTION}. {SUBJECT_DETAIL}. {MOVEMENT_DETAIL}. {ENVIRONMENT}. {CAMERA}. {LIGHTING_AND_COLOR}. {CHANGE_OVER_TIME}. {STYLE} {AUDIO}
```

| Slot                 | Source in shot-spec.yaml                              | Tier | Rule |
|----------------------|-------------------------------------------------------|------|------|
| `MAIN_ACTION`        | subjects[0] short noun + action                       | P1   | "A young woman rides a bicycle down a narrow street" |
| `SUBJECT_DETAIL`     | subjects[].anchor, expression                         | P1   | "She is {anchor without leading article}" or similar; keep anchor words verbatim. |
| `MOVEMENT_DETAIL`    | motion.subject_motion                                 | P1   | Body mechanics, literal. |
| `ENVIRONMENT`        | environment.* + motion.background_motion              | P1   | Include what moves in the background. |
| `CAMERA`             | camera.*                                              | P1   | Shot size, angle, movement, direction, speed in one sentence. |
| `LIGHTING_AND_COLOR` | lighting.*, style.color_grade                         | P2   | Sources first, then color. |
| `CHANGE_OVER_TIME`   | timeline.beats[1..]                                   | P2   | "As ..., ..." in order. Omit if one beat. |
| `STYLE`              | style.realism, visual_style, texture                  | P3   | Short closing clause: "The scene looks like {style}." |
| `AUDIO`              | audio.*                                               | P3   | Only if `audio.generate: true` and the checkpoint supports audio (LTX-2). Dialogue quoted verbatim, original language. |

## Negative prompt (`prompts/ltx.negative.txt`)

```
{SCENE_NEGATIVES}, {LTX_QUALITY_NEGATIVES}
```

Skip writing the file when the selected profile has `cfg: 1.0`; mention it in
`generation-config.yaml → notes`.

## Image-to-video variant

```
{SUBJECT_SHORT} {ACTION}. {MOVEMENT_DETAIL}. {BACKGROUND_MOTION}. {CAMERA}. {CHANGE_OVER_TIME}.
```

Target 60–120 words. Do not restate appearance that is visible in the image.
