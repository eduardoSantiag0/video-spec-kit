# <Model> prompt template

Slots are filled from `shot-spec.yaml`. Describe the output file format
(`prompts/<model-id>.txt`) and, if `negative_prompt: true`,
`prompts/<model-id>.negative.txt`.

## Positive prompt

```
{SLOT_A}. {SLOT_B}. ...
```

| Slot     | Source in shot-spec.yaml | Tier (P1/P2/P3) | Rule |
|----------|--------------------------|-----------------|------|
| `SLOT_A` | <field paths>            | P1              | <how to phrase it> |

## Negative prompt

## Image-to-video variant
