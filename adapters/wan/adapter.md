# Wan adapter

How the `video` skill turns accumulated scene facts into a prompt for Wan
(Wan 2.1 / 2.2, open weights, runs locally e.g. in ComfyUI).

## Shape

One paragraph, present tense, in this order: **shot → subject → action →
environment → camera movement → lighting → style**. Target **80–150 words**,
never over 200 — below ~50 words results turn generic.

```
<shot size + angle>. <subject appearance> <action, present tense>. <environment>.
<camera movement, own sentence>. <lighting>. <style>.
```

- One main action, at most one secondary motion — 81 frames isn't room for more.
- One noun phrase per fact; don't stack synonyms ("cinematic, filmic, movie-like").
- Wan knows cinematography vocabulary well: shot sizes, "low angle", "rim
  light", "golden hour", "shallow depth of field". Avoid quality spam ("8k,
  masterpiece, best quality") in the positive prompt.
- `static` camera: write "Static camera, locked-off shot." `handheld`: "...
  with subtle natural shake" (Wan tends to over-shake without "subtle").
- Describe motion physically — prefer continuous actions (riding, walking)
  over discrete events (dropping, catching), which often land at the wrong
  time.
- Repeat a locked character description verbatim if the user set one earlier
  in the conversation, and keep lighting stable unless the change *is* the shot.

## Negative prompt

Build from the scene's explicit exclusions (if any), then this quality list —
drop any item that contradicts the scene (e.g. drop `static`/`motionless
frame` if the shot is meant to be still; drop `crowded background` if a
crowd is wanted):

```
oversaturated colors, overexposed, static, blurry details, subtitles, text, watermark,
painting, still image, overall gray, worst quality, low quality, jpeg compression artifacts,
ugly, incomplete, extra fingers, poorly drawn hands, poorly drawn face, deformed,
disfigured, malformed limbs, fused fingers, motionless frame, cluttered background,
three legs, crowded background, walking backwards
```

> With CFG = 1 (common with distilled/"lightning" workflows) the negative
> prompt has no effect — fold the important exclusions into positive
> phrasing instead (e.g. "an empty street" rather than negative "other people").

## Dialogue and sound

These checkpoints don't generate audio. Never put dialogue words or sound
effects in the prompt — show speech as a visible action ("she calls out")
and sound only through the reaction it causes.

## Duration and limitations

81 frames at 16 fps (≈5 s) for 14B/A14B models; frame counts must be `4n+1`.
Longer scenes degrade — split into another scene instead. Known weak spots:
hands/fingers in fine manipulation, legible text/logos, fast motion (smearing),
exact counts.

## Language

The kit writes prompts in English by default, or the language the user asked
for. Wan is well-supported in English and Chinese; other languages still
work but may follow instructions a bit less precisely — worth a one-line
heads-up if the user requests one.
