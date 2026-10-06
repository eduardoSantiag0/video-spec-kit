---
# Machine-readable profile used by video-prompt. Guidance for humans and agents follows below.
id: wan
name: Wan (Wan-Video by Alibaba)
written_against: [Wan 2.1, Wan 2.2]
weights: open (Apache-2.0); runs locally (ComfyUI, diffusers, official repo)
prompt:
  form: single paragraph, present tense
  language: auto          # follows the idea's language (kit/conventions.md §7); well-supported: en, zh
  target_words: [80, 150]
  max_words: 200
  section_order: [shot, subject, action, environment, camera_movement, lighting, style, texture]
negative_prompt: true
supports:
  image_to_video: true    # Wan 2.1 I2V-14B, Wan 2.2 I2V-A14B / TI2V-5B
  first_last_frame: true  # Wan 2.1 FLF2V-14B
  audio: false            # not in the T2V/I2V checkpoints above
frame_rule: "num_frames = 4n + 1"
profiles:                 # starting points; the user's workflow may differ — record what was actually used
  - id: wan2.2-t2v-a14b
    model: Wan2.2-T2V-A14B
    fps: 16
    num_frames: 81
    sizes: { "16:9": [1280, 720], "9:16": [720, 1280], "1:1": [960, 960] }
    low_vram_sizes: { "16:9": [832, 480], "9:16": [480, 832] }
    steps: 20             # split between high-noise and low-noise experts in ComfyUI templates
    cfg: 3.5
    sampler: euler
    scheduler: simple
    params: { shift: 8.0 }
  - id: wan2.2-ti2v-5b
    model: Wan2.2-TI2V-5B
    fps: 24
    num_frames: 121
    sizes: { "16:9": [1280, 704], "9:16": [704, 1280] }
    steps: 30
    cfg: 5.0
    sampler: uni_pc
    scheduler: simple
    params: { shift: 8.0 }
  - id: wan2.1-t2v-14b
    model: Wan2.1-T2V-14B
    fps: 16
    num_frames: 81
    sizes: { "16:9": [1280, 720], "9:16": [720, 1280] }
    low_vram_sizes: { "16:9": [832, 480], "9:16": [480, 832] }
    steps: 30
    cfg: 5.0
    sampler: uni_pc
    scheduler: simple
    params: { shift: 5.0 }
default_profile: wan2.2-t2v-a14b
---

# Wan adapter

How to turn a resolved `shot-spec.yaml` into a Wan prompt. Read together with
`prompt-template.md` in this folder.

## Language

Well-supported: English and Chinese (the checkpoints were trained on captions
in both). The kit compiles in the idea's language by default
(`kit/conventions.md` §7); in any other language, `video-prompt` still
compiles the prompt but warns once that adherence may be weaker.

## Order of information

Wan responds best to a structured paragraph that follows its official formula
*subject → scene → motion → aesthetic control → stylization*. The adapter uses:

1. **Shot** — shot size + angle (+ lens when it matters): "Medium tracking shot, eye level, 35mm."
2. **Subject** — the character `anchor`, verbatim.
3. **Action** — one main action in present tense, with the physical detail that
   makes it unambiguous.
4. **Environment** — location, time, weather, 2–4 concrete background elements.
5. **Camera movement** — one sentence, explicit direction and speed.
6. **Lighting** — source, direction, color temperature, contrast.
7. **Style** — realism + visual style + color grade.
8. **Texture** — grain/sharpness, only if budget remains (P3).

## Level of detail

- Wan rewards specific, concrete description. Target **80–150 words**; never
  exceed 200. Below ~50 words results become generic.
- One noun phrase per fact. Do not stack synonyms ("cinematic, filmic, movie-like").
- Wan understands cinematographic vocabulary well: shot sizes, "low angle",
  "rim light", "golden hour", "warm tones", "shallow depth of field".
- Avoid quality spam ("8k, masterpiece, best quality") in the positive prompt —
  it adds noise; quality is handled by the negative prompt.

## Negative prompt

Wan uses a negative prompt and it matters. Build `wan.negative.txt` as:

1. scene `negatives` from `shot-spec.yaml` (from `constraints.must_not_include`), then
2. this quality list (an English rendering of the negative prompt shipped with
   the official Wan repository):

```
oversaturated colors, overexposed, static, blurry details, subtitles, text, watermark,
painting, still image, overall gray, worst quality, low quality, jpeg compression artifacts,
ugly, incomplete, extra fingers, poorly drawn hands, poorly drawn face, deformed,
disfigured, malformed limbs, fused fingers, motionless frame, cluttered background,
three legs, crowded background, walking backwards
```

Remove any item that contradicts the spec (e.g. drop `static` and
`motionless frame` if `camera.movement` is `static` **and** the subject is
meant to stay still; drop `crowded background` if a crowd is wanted).

> With CFG = 1 (common with step-distillation / "lightning" LoRAs) the negative
> prompt has no effect. Then move the most important exclusions into positive
> phrasing (e.g. "an empty street" instead of negative "other people").

## Camera

- State the camera movement in its own sentence, with direction and speed:
  "The camera tracks alongside her from the left at matching speed."
- One movement per clip. Two movements in 5 s ("pans then zooms") are often
  merged or ignored.
- `static`: write "Static camera, locked-off shot." Also keep `static` out of
  the negative prompt in that case.
- `handheld`: "handheld camera with subtle natural shake" — Wan may over-shake;
  add "subtle".
- `orbit` and `drone` work but tend to warp backgrounds at high speed; keep
  `movement_speed` slow.

## Motion

- Describe the motion physically: who moves, which direction, how fast.
- Prefer continuous actions (riding, walking, turning slowly) over discrete
  events (dropping, catching) — discrete events often happen at the wrong time
  or not at all.
- Background motion is worth one clause ("rain streaks fall diagonally,
  headlights pass in the background").
- In 81 frames, at most **one main action + one secondary motion**.

## Reference images (image-to-video / first-last-frame)

- I2V: the image defines appearance. The prompt should focus on **motion,
  camera and changes**; keep only a short subject anchor (40–80 words total).
  Do not describe appearance that contradicts the image.
- FLF2V: describe the transition between first and last frame as one
  continuous movement.
- Sizes must match the reference aspect ratio; record the image in
  `generation-config.yaml → reference_images`.

## Temporal consistency

- Repeat the character `anchor` verbatim across all scenes of a project.
- Keep lighting stable within a clip unless the change *is* the shot.
- Avoid cut language ("cut to", "then the scene changes") — Wan generates one
  continuous shot.
- Head turns toward camera and fast hand gestures are the most common sources
  of identity and anatomy drift.

## Dialogue and sound

The Wan checkpoints in this profile do not generate audio. Never put dialogue
words or sound effects in the prompt. Show speech as a visible action ("she
calls out", "his lips move as he whispers") and a sound only through the
reaction it causes, if the spec has one ("she freezes, eyes on the hallway").

## Duration

- Native: 81 frames at 16 fps (≈5 s) for 14B / A14B; 121 frames at 24 fps
  (≈5 s) for TI2V-5B. Frame counts must be `4n + 1`.
- Spec `fps: 24` with a 16 fps model: generate at 16 fps and interpolate later
  (e.g. RIFE/FILM in ComfyUI). Record both in `generation-config.yaml → params`.
- Longer than ~5 s degrades or loops. For longer scenes, split into several
  scenes and continue with I2V from the last frame of the previous clip.

## Known limitations

- Hands and fingers during fine manipulation.
- Legible text and logos.
- Fast motion produces smearing; crowds produce merged bodies.
- Exact counts ("three birds") are unreliable.

## Example

See `examples/tokyo-rain/scenes/scene-001/v001/prompts/wan.txt`.
