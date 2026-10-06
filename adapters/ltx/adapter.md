# LTX adapter

How the `video` skill turns accumulated scene facts into a prompt for
LTX-Video (open weights, runs locally e.g. in ComfyUI).

## Shape

One chronological, literal paragraph, present tense, in this order: **main
action → subject detail → movement detail → environment → camera → lighting
& color → any change over time**. Target **100–180 words**, stay within 200.

```
<subject + main action, one sentence>. <subject appearance, folded in>.
<how the body moves>. <environment + background motion>.
<camera: shot size, angle, movement, speed>. <lighting, color>.
<any change over the shot, in order>.
```

- LTX needs long, literal, descriptive prompts — short ones produce static
  or generic clips. "Rain falls in thin diagonal streaks" beats "a melancholic downpour."
- State motion explicitly for subject **and** background ("her legs pedal
  steadily", "cars pass behind her") — LTX tends toward low motion otherwise.
- Camera goes in its own sentence, after the environment, with a clear verb
  (tracks, pushes in, pans, orbits). Without one, LTX often drifts slowly;
  for a locked shot write "The camera remains completely still."
- Chronology matters — describe events in the order they happen; keep the
  number of described changes small (≤3 in a 5 s clip).
- Repeat a locked character description verbatim if the user set one earlier.

## Negative prompt

Only effective with CFG > 1 (not with distilled/fast checkpoints, which run
at CFG 1). Build from the scene's explicit exclusions, then:

```
worst quality, low quality, inconsistent motion, blurry, jittery, distorted,
deformed, disfigured, motion smear, motion artifacts, fused fingers, bad anatomy,
extra limbs, watermark, text
```

## Dialogue and sound

LTX-Video 0.9.x is silent — show speech and sound only as visible action and
reaction, never as words. LTX-2 can generate audio; use that only if the
user explicitly wants an audio-capable render, describing ambience/effects
in one sentence and quoting dialogue verbatim with its speaker.

## Duration and limitations

Frames must be `8n+1` (97, 121, 161...), width/height divisible by 32; 24 fps
native, 121 frames ≈ 5 s. Best quality below ~257 frames. Known weak spots:
faces/hands in fast motion or small sizes, under-animation if motion isn't
described, unreliable text/logos.

## Language

The kit writes prompts in English by default, or the language the user asked
for. LTX is best documented for English; other languages still work but may
follow instructions a bit less precisely — worth a one-line heads-up if the
user requests one.
