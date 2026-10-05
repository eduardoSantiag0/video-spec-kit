# Walkthrough — screenplay excerpt → one shot

A short excerpt that fits a single 5-second generation. Shows parsing, a
non-visual line handled as subtle performance, and the alias
`$video_from_screenwright`.

```
SCREENPLAY → PARSE → VISUAL EXTRACTION → CLARIFY → SCENE SPEC → STORYBOARD → SHOT SPEC → PROMPTS
```

## 1. Input

> **User:**
> ```
> $video_from_screenwright
>
> EXT. ROOFTOP GARDEN - DAWN
>
> ELENA (60s), in a grey wool cardigan, waters a row of tomato plants.
>
> She pauses and looks out over the waking city.
>
> Elena has waited all winter for this morning.
> ```

The alias resolves to the `video-screenplay` skill. The excerpt is saved
verbatim → `screenplay/excerpt-001/source-screenplay.md`.

## 2. Parse

| Line | Element | Read as |
|------|---------|---------|
| 1 | Scene heading | `exterior`, rooftop garden, dawn |
| 3 | Action | Elena (60s, grey wool cardigan) waters tomato plants |
| 5 | Action | she pauses and looks out over the city |
| 7 | Action line — **non-visual** | backstory: "has waited all winter" |

## 3. Visual extraction

- **On screen:** Elena (new character; age and cardigan from the screenplay; "she" → woman).
- **Objects:** row of tomato plants (key), watering can (implied by "waters").
- **Beats:** 1 waters the plants (~2.5 s) · 2 pauses, looks out over the city (~2.5 s).
- **Non-visual NV1:** "Elena has waited all winter for this morning." → can be
  shown with subtle performance only → `visible-behavior`: *a quiet, content
  expression*. No flashback, no props, no added event. Status `assumed`.
- **Shot breakdown:** 2 visual beats, ~5 s, clip 5 s (default) → **fits a single shot**.

## 4. Clarify — one question

The screenplay already states place, interior/exterior, time, character and
actions, so none of them is asked.

> **Agent:**
> One choice changes this video a lot:
> 1. What should it look like?
>    a) photorealistic, cinematic (recommended) b) soft documentary c) 2D animation
>
> I'll assume the rest — reply "change <item>" to adjust:
> - one 5-second shot, 16:9
> - Elena: silver hair in a low bun, warm lined face (her cardigan comes from the screenplay)
> - "has waited all winter" shown only as a quiet, content expression
> - medium shot with a slow push-in; warm low sunrise light
>
> **User:** `a`

## 5. Files

```
screenplay/excerpt-001/source-screenplay.md     # verbatim
screenplay/excerpt-001/screenplay-analysis.yaml # parse + beats + NV1 + breakdown
characters/elena.yaml                           # screenplay: age, cardigan · inferred: hair, face
scenes/scene-001/v001/scene-spec.yaml           # same format as any other scene, + source block
scenes/scene-001/v001/storyboard.md
scenes/scene-001/v001/shot-spec.yaml
scenes/scene-001/v001/prompts/{wan,ltx}.txt (+ negatives)
scenes/scene-001/v001/generation-config.yaml
```

In `scene-spec.yaml`, the provenance shows what came from where:

- `screenplay`: action, location, exterior, dawn, both beat descriptions, the tomato plants;
- `user`: the cinematic style;
- `inferred`: expression (NV1), camera move, lighting (sunrise inference rule), haze, framing;
- `default`: 5 s, 16:9, 24 fps, eye level, 35mm.

## 6. Prompts

- `prompts/wan.txt` — 109 words.
- `prompts/ltx.txt` — 129 words, chronological; beat 2 closes the paragraph.

Neither prompt says "she has waited all winter": the line is not visual.

## 7. Next

Generate, then `$video-review "…"` on `scene-001` — the scene is an ordinary
scene, so review and iteration work unchanged.
