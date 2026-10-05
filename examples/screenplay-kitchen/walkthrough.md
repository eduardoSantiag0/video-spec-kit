# Walkthrough — Portuguese screenplay excerpt → three shots

A Portuguese excerpt with six beats, dialogue and a sound cue, requested
as a 5-second generation. Shows the duration warning, the split into shots,
dialogue preservation, sound handling, and fidelity safeguards. The
conversation is in Portuguese (the user's language); the files are in English
except for the verbatim source text.

## 1. Input

> **User:**
> ```
> $video-screenplay --duration 5
>
> INT. COZINHA - NOITE
>
> Maria entra lentamente na cozinha.
>
> A luz da geladeira aberta ilumina seu rosto.
>
> Ela percebe um copo quebrado no chão.
>
> MARIA
> João?
>
> Um barulho vem do corredor.
>
> Maria congela.
> ```

Saved verbatim → `screenplay/excerpt-001/source-screenplay.md`.

## 2. Parse

| Line | Element | Read as |
|------|---------|---------|
| 1 | Scene heading | `interior`, kitchen (`COZINHA`), night (`NOITE`) |
| 3 | Action | Maria enters slowly |
| 5 | Action (reveal) | refrigerator light on her face |
| 7 | Action (reveal) | she notices a broken glass |
| 9–10 | Character cue + dialogue | `MARIA: "João?"` |
| 12 | Action — **sound** | a noise from the hallway |
| 14 | Action (reaction) | Maria freezes |

## 3. Visual extraction

- **On screen:** Maria (new). **Mentioned only:** João → never rendered.
- **Key objects:** open refrigerator, broken glass on the floor.
- **Beats (order preserved):** 1 enters (2.5 s) · 2 light on face (2 s) ·
  3 notices glass (2 s) · 4 calls "João?" (1.5 s) · 5 noise (sound, 0.5 s) ·
  6 freezes (2 s) → **5 visual beats, ~10.5 s**.
- **Dialogue:** `"João?"` kept verbatim; visual consequence: she calls out.
- **Sound cue:** "Um barulho vem do corredor." → not an image; it motivates the
  freeze and her gaze toward the hallway (beat 6).
- **Non-visual:** none.
- **Duration check:** 5 visual beats vs. a 5 s clip (budget: 2) →
  *"This excerpt contains 5 visual beats (~10.5 s) and is unlikely to work as a
  single 5-second generation."*

## 4. Clarify — two questions, in Portuguese

> **Agent:**
> Duas escolhas mudam bastante este vídeo:
>
> 1. O trecho tem 5 beats visuais (~10,5 s); em uma geração de 5 s não cabe tudo. O que prefere?
>    a) dividir em 3 shots de até 5 s (recomendado): entrada na luz da geladeira · o copo quebrado · chamado, barulho e congela
>    b) um único shot de 5 s só com "percebe o copo → congela" (perde a entrada, a luz no rosto e o chamado)
>    c) uma geração única de ~10 s (funciona no LTX; o Wan degrada depois de ~5 s)
> 2. Qual visual?
>    a) fotorrealista, cinematográfico de suspense (recomendado)  b) noir em preto e branco  c) animação 2D
>
> Vou assumir o resto — responda "mude <item>" para ajustar:
> - Maria: 30 e poucos anos, cabelo castanho-escuro preso, camiseta cinza larga (o roteiro não a descreve)
> - Única luz: a geladeira aberta; o resto da cozinha no escuro
> - "João?" fica guardado exatamente como está, mas não é falado pelo modelo (sem áudio)
> - Ninguém aparece no corredor; o barulho é só som
>
> **User:** `1a, 2a`

Nothing the screenplay states was asked (place, interior, night, who is present, actions).

## 5. Shot breakdown

| Shot | Scene | Beats | Duration | Camera (inferred) |
|------|-------|-------|----------|-------------------|
| 1 | scene-001 | 1–2 | 5 s | medium, static — she walks out of the dark into the refrigerator light |
| 2 | scene-002 | 3 | 3 s | POV close-up, slow tilt down to the shards (Maria not in frame) |
| 3 | scene-003 | 4–6 | 5 s | medium close-up, static — calls out, (noise), freezes |

Cut points follow the screenplay: the object reveal (beat 3) becomes an
insert, and the call/noise/freeze stays together because the noise only
matters through her reaction. Three shots, not six.

## 6. Fidelity safeguards (visible in the specs)

- `must_not_include`: `other people` in every shot; `a figure in the hallway`
  in shot 3 (João is only named, the noise source is unknown); `blood` in shot 2
  (the screenplay mentions only a broken glass); `a lamp or ceiling light turned on`
  in shot 1 (the only light named is the refrigerator).
- `audio.dialogue` keeps `"João?"`; `audio.generate: false`; no prompt contains the word.
- The noise exists only in `audio.sfx` and the storyboard Notes ("add the sound in editing").
- `source.beats` keeps beats contiguous and in order; `video-shot` (C16/C17) and
  `tools/validate.py` would reject a reordering or a rendered offscreen character.

## 7. Files

```
screenplay/excerpt-001/{source-screenplay.md, screenplay-analysis.yaml}
characters/maria.yaml                   # designed once, reused by shots 1 and 3
scenes/scene-001/ scene-002/ scene-003/ # one standard scene per shot, linked by continuity
  history.md
  v001/{scene-spec.yaml, storyboard.md, shot-spec.yaml, prompts/*, generation-config.yaml}
```

Frames per run: Wan 81 (5 s) / 49 (3 s) at 16 fps; LTX 121 (5 s) / 73 (3 s) at 24 fps.

## 8. Next

Generate the three shots, cut them in order, add the dialogue and the noise in
editing, then review any shot with `$video-review` — they are ordinary scenes.
