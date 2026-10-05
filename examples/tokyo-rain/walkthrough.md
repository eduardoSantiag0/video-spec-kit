# Walkthrough — "A woman rides a bicycle through Tokyo at night during heavy rain"

The full loop, step by step, with the conversation and the files each step
produced. The review texts are fictional; no video is included.

```
IDEA → CLARIFY → SCENE SPEC → STORYBOARD → SHOT SPEC → PROMPTS
     → (user generates in ComfyUI) → REVIEW → ITERATE → (generate) → REVIEW
```

---

## 1. Idea

> **User:** `$video A woman rides a bicycle through Tokyo at night during heavy rain.`

## 2. Clarify (`video-clarify`)

What the agent extracted:

| Dimension | Status | Evidence / value |
|-----------|--------|------------------|
| Subject | STATED | "a woman" |
| Action | STATED | "rides a bicycle" |
| Setting | STATED | "Tokyo" |
| Time, weather | STATED | "at night", "heavy rain" |
| Look / realism | **MISSING → CRITICAL** | no style cue |
| Camera viewpoint | **MISSING → CRITICAL** | she travels through space |
| Appearance | MISSING → optional | new project, no other scenes |
| Duration, ratio, fps | MISSING → optional | defaults |
| Lighting | INFERABLE | night + city → artificial light (`neon-night` preset fits) |

Two questions, one message:

> **Agent:**
> A few choices change this video a lot:
>
> 1. What should it look like?
>    a) photorealistic, cinematic (recommended) b) documentary, handheld realism c) anime — or describe your own
> 2. Where is the camera?
>    a) tracking alongside her, medium shot (recommended — shows her and the city at once)
>    b) following from behind c) in front, she rides toward the camera d) static wide shot, she passes through
>
> I'll assume the rest — reply "change <item>" for anything you want different:
> - 5 seconds, 16:9
> - She gets a reusable look: late 20s, short black bob, translucent yellow raincoat, small red backpack
> - Neon signs and street lamps, wet reflective street
> - No other cyclists, umbrellas or pedestrians in the foreground (a lonely ride)

> **User:** `1a, 2a. She should look tired but determined.`

Result: `presets.style`, `camera.shot_size`, `camera.movement`,
`subjects[0].expression` → `user`. Everything else → `inferred` / `default`.

## 3. Character (`video-character`)

Main human subject → `characters/mika.yaml`, with a 31-word `prompt_anchor`
and a consistency lock on hair, outfit, colors and distinctive features.

## 4. Scene spec (`video-scene`)

`scenes/scene-001/v001/scene-spec.yaml`. Note what is **not** there: no
`lighting` and no `style` blocks — they come from the referenced presets
`neon-night` and `cinematic`. Writing defaults there would override the presets.

## 5. Storyboard (`video-storyboard`)

5 s → up to 2 beats. The agent added a human moment (a brow wipe, a glance
toward camera) and flagged both as risky in the Notes column.
→ `v001/storyboard.md`

## 6. Shot (`video-shot`)

Resolved everything into `v001/shot-spec.yaml`: anchor expanded, presets
merged, priorities P1/P2/P3. No conflicts. Risk **high**, with two specific
warnings (hand action at 0–2.5 s, head turn at 2.5–5 s) and a note that `text`
must not go into negative prompts because the background has neon signs.

## 7. Prompts (`video-prompt`)

Same shot, two compilations:

- `prompts/wan.txt` — 134 words, shot-first structure, P3 "35mm lens" dropped.
- `prompts/ltx.txt` — 174 words, chronological paragraph, explicit body and
  background motion; four P3 items dropped.
- Negatives: scene exclusions + adapter quality lists; `text` removed from both.
- `generation-config.yaml`: Wan 2.2 A14B 1280×720, 81 frames @16 fps (interpolate
  to 24); LTX 13B 1216×704, 121 frames @24 fps.
- `comfyui-notes.md` because `project.yaml` has `tool: comfyui`.

Report shown to the user (abridged):

> Scene ready: projects/tokyo-rain/scenes/scene-001/v001/
> You decided: cinematic photoreal · tracking alongside, medium shot · tired but determined
> I assumed: 5 s 16:9 · Mika's look · neon-night lighting · no other cyclists
> Warnings: hand action 0–2.5 s; head turn toward camera 2.5–5 s
> Next: paste prompts/wan.txt into ComfyUI, note the seed, tell me what you see.

## 8. Generate (outside the kit)

The user runs Wan in ComfyUI with seed 428193.

## 9. Review (`video-review`)

> **User:** `$video The camera movement is good and the rain looks great, but her face changes halfway through and her hand flickers when she wipes her face. Seed was 428193.`

→ `v001/review.md`: Keep camera + rain + lighting. I1 identity drift (major,
head turn), I2 hands (minor, brow wipe). Recommended: change only beat 2.
`generation-config.yaml` run `wan-1` → `status: generated`, seed recorded.

> **Agent:** Create v002 with this change? (yes / choose another suggestion / describe your own)
>
> **User:** `yes`

## 10. Iterate (`video-iterate`)

→ `v002/` with exactly one spec change:

```diff
  timeline.beats[1].description:
-   She glances toward the camera for a moment, then looks back at the road ahead as neon light slides across her raincoat.
+   She keeps her eyes on the road ahead and leans slightly into the pedals as neon light slides across her raincoat.
```

Same seed, same settings. One clause changed in each prompt.
→ `v002/iteration.md`, new row in `history.md`.

## 11. Review again

> **User:** `$video Much better, her face stays the same now. The hand still flickers a little when she wipes the rain.`

→ `v002/review.md`, `v002/iteration.md` conclusion **confirmed**, `history.md`
updated, next experiment queued (remove the brow wipe).

Compare the versions yourself:

```bash
git diff --no-index examples/tokyo-rain/scenes/scene-001/v001/scene-spec.yaml examples/tokyo-rain/scenes/scene-001/v002/scene-spec.yaml
```
