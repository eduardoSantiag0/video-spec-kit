# Wan prompt template

Slots are filled from `shot-spec.yaml`. Write the result as ONE paragraph in
`prompts/wan.txt` (no slot names, no line breaks, no markdown).

## Positive prompt

```
{SHOT}. {SUBJECT_ANCHOR} {ACTION}. {ENVIRONMENT}. {CAMERA_MOVEMENT}. {LIGHTING}. {STYLE}. {TEXTURE}.
```

| Slot               | Source in shot-spec.yaml                                   | Tier | Rule |
|--------------------|------------------------------------------------------------|------|------|
| `SHOT`             | camera.shot_size, camera.angle, camera.lens                | P1   | "Medium shot, eye level, 35mm lens" |
| `SUBJECT_ANCHOR`   | subjects[].anchor                                           | P1   | Verbatim. Starts with "A"/"An". |
| `ACTION`           | subjects[].action + expression + motion.subject_motion     | P1   | Present tense, one main action. |
| `ENVIRONMENT`      | environment.*                                              | P1   | Location + time + weather first, then ≤4 background elements. |
| `CAMERA_MOVEMENT`  | camera.movement, movement_detail, movement_speed           | P1   | Own sentence. Vocabulary phrase + direction. |
| `LIGHTING`         | lighting.*                                                 | P2   | Source, direction, temperature, contrast. |
| `STYLE`            | style.realism, visual_style, color_grade                   | P2   | ≤ 2 phrases. |
| `TEXTURE`          | style.texture, depth_of_field                              | P3   | Drop first when over budget. |

`timeline.beats`: if there are 2+ beats, express them inside `ACTION` as a
single continuous progression ("...rides steadily, then rises slightly off the
saddle as she reaches the crossing"). Never more than two clauses of change.

## Negative prompt (`prompts/wan.negative.txt`)

```
{SCENE_NEGATIVES}, {WAN_QUALITY_NEGATIVES}
```

- `SCENE_NEGATIVES` = `negatives` from shot-spec, short nouns, comma-separated.
- `WAN_QUALITY_NEGATIVES` = the list in `adapter.md`, minus items that
  contradict the spec.

## Image-to-video variant

```
{SUBJECT_SHORT} {ACTION}. {CAMERA_MOVEMENT}. {BACKGROUND_MOTION}. {LIGHTING_CHANGE_IF_ANY}.
```

`SUBJECT_SHORT` = "The woman" / "The rider" (the image already carries the
appearance). Target 40–80 words.
