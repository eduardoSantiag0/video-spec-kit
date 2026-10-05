---
# Machine-readable profile used by video-prompt. Guidance for humans and agents follows below.
id: ltx
name: LTX-Video (Lightricks)
written_against: [LTX-Video 0.9.x (2B / 13B), LTX-2]
weights: open weights; runs locally (ComfyUI, diffusers, official repo) — check the license of the checkpoint you use
prompt:
  form: single chronological paragraph, present tense, literal
  language: en
  target_words: [100, 180]
  max_words: 200
  section_order: [action, subject, movement_detail, environment, camera, lighting, events, audio]
negative_prompt: true      # only effective with CFG > 1 (not with distilled checkpoints)
supports:
  image_to_video: true
  first_last_frame: true   # keyframe conditioning at arbitrary frames
  audio: true              # LTX-2 only; ignored by LTX-Video 0.9.x
frame_rule: "num_frames = 8n + 1; width and height divisible by 32"
profiles:                  # starting points; record what you actually used
  - id: ltxv-13b-dev
    model: LTX-Video 13B (dev)
    fps: 24
    num_frames: 121
    sizes: { "16:9": [1216, 704], "9:16": [704, 1216], "1:1": [768, 768] }
    low_vram_sizes: { "16:9": [768, 512], "9:16": [512, 768] }
    steps: 30
    cfg: 3.0
    sampler: euler
    scheduler: LTXV
    params: {}
  - id: ltxv-13b-distilled
    model: LTX-Video 13B (distilled)
    fps: 24
    num_frames: 121
    sizes: { "16:9": [1216, 704], "9:16": [704, 1216] }
    steps: 8
    cfg: 1.0
    sampler: euler
    scheduler: LTXV
    params: {}
default_profile: ltxv-13b-dev
---

# LTX adapter

How to turn a resolved `shot-spec.yaml` into an LTX-Video prompt. Read together
with `prompt-template.md` in this folder.

## Order of information

LTX's official prompting guidance is: start with the main action in one
sentence, then movements and gestures, then precise appearance, then background
and environment, then camera angle and movement, then lighting and color, then
any change or sudden event. Write it like a cinematographer describing the shot,
in chronological order:

1. **Main action** — one sentence with subject + action.
2. **Subject detail** — the character `anchor`, verbatim, folded into a second sentence.
3. **Movement detail** — how the body moves.
4. **Environment** — location, time, weather, background elements and their motion.
5. **Camera** — shot size, angle, movement, speed.
6. **Lighting & color** — sources, temperature, grade.
7. **Change over time** — the timeline beats, in order ("As she reaches...").
8. **Audio** — LTX-2 only, one sentence, when `audio` exists.

## Level of detail

- LTX needs long, literal, descriptive prompts. Short prompts produce static or
  generic clips. Target **100–180 words**; the official guidance is to stay
  within 200 words.
- Literal beats poetic: "rain falls in thin diagonal streaks" beats "a melancholic downpour".
- Describe what is visible, not what it means.

## Negative prompt

Use with CFG > 1 (dev checkpoints). Distilled checkpoints run at CFG 1, where
the negative prompt is ignored — then rely on positive phrasing only.

`ltx.negative.txt` = scene `negatives` + this list:

```
worst quality, low quality, inconsistent motion, blurry, jittery, distorted,
deformed, disfigured, motion smear, motion artifacts, fused fingers, bad anatomy,
extra limbs, watermark, text
```

## Camera

- Put camera in its own sentence **after** the environment: "The camera tracks
  alongside her at eye level in a medium shot, moving at her speed."
- LTX follows clear movement verbs (tracks, pushes in, pans, orbits, rises).
  Always name the direction.
- Without any camera sentence LTX often drifts slowly; for a locked shot write
  "The camera remains completely still."

## Motion

- LTX tends toward low motion. State motion explicitly for subject AND
  background ("her legs pedal steadily", "cars pass behind her").
- Chronology matters: describe events in the order they happen.
- Fast motion degrades faces; prefer `movement_speed` slow/moderate for
  close shots.

## Reference images (image-to-video / first-last-frame)

- I2V: the image is conditioning at frame 0. Describe what happens next and the
  camera; keep appearance short and consistent with the image.
- First-last-frame: condition the first and last frames with keyframes; the
  prompt describes the continuous change between them.
- Resize references to the generation size (divisible by 32) before use.

## Temporal consistency

- Repeat the `anchor` verbatim across scenes.
- One continuous shot, no cuts.
- Keep the number of described changes ≤ the number of beats (max 3 in 5 s).

## Dialogue and sound

LTX-Video 0.9.x is silent: show speech and sound only as visible action and
reaction. LTX-2 can generate audio — use it only when `audio.generate: true`
in the spec. Then the `AUDIO` slot describes ambience and effects in one
sentence and quotes dialogue verbatim with its speaker ("The woman calls out:
\"João?\""). Otherwise no words or sounds in the prompt.

## Duration

- Frames must be `8n + 1` (e.g. 97, 121, 161, 257). Width/height divisible by 32.
- 24 fps native; 121 frames ≈ 5 s. Quality is best below ~257 frames and
  ≤ 1280 px on the long side.
- Pass the same fps to the conditioning (frame rate) as to the output.

## Known limitations

- Faces and hands degrade in fast motion and at small sizes.
- Tends to under-animate if motion is not described.
- Text and logos are unreliable.

## Example

See `examples/tokyo-rain/scenes/scene-001/v001/prompts/ltx.txt`.
