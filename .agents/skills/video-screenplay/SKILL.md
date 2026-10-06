---
name: video-screenplay
description: Turns a screenplay excerpt (sluglines, action, dialogue, in any language) into the same conversational scene state used by the video skill — extracting what's visual, who's on screen, the setting and the action — then hands off to normal conversation so the user can refine it and ask for the prompt. Use when the user pastes a screenplay or script excerpt, or types $video-screenplay, $video_from_screenwright or $video-from-screenplay.
metadata:
  aliases: video_from_screenwright, video-from-screenplay
---

# video-screenplay

Aliases: `$video_from_screenwright` (original request name), `$video-from-screenplay`.

## Purpose

Read a screenplay excerpt once, pull out everything a camera would actually
record, and drop it straight into `.video/session.yaml` — the same state
`video` uses. From that point on it's an ordinary conversation: the user can
correct, add, or ask for the prompt, exactly as in `video`.

```
SCREENPLAY → EXTRACT VISUAL INFO → SAVE TO .video/session.yaml → normal conversation → GENERATE
```

No separate analysis file, no shot list, no storyboard document — only the
state, unless the excerpt genuinely needs more than one scene (see
*Multiple scenes* below).

## When to use

- The user pastes text with screenplay structure: sluglines (`INT.`/`EXT.`),
  CHARACTER cues, dialogue — in any language.
- `$video-screenplay`, `$video_from_screenwright`, `$video-from-screenplay`,
  with the excerpt in the same message or the next one.
- `video` routes here when the message looks like a screenplay excerpt
  rather than a one-line idea.

Not for a plain idea (use `video`), and not for writing or rewriting the
screenplay itself.

## Workflow

### 1. Read the excerpt

If there's no excerpt yet, ask the user to paste it and stop. Otherwise read
it like an assistant director: where and when, who's on screen, what
actually happens, in what order.

### 2. Extract what's visual

Classify each line:

| Element | Recognize by |
|---|---|
| Scene heading | `INT.`/`EXT.`/`INT./EXT.` (any case/language) → location + interior/exterior + time of day |
| Character cue | Short capitalized line, optionally `(V.O.)`/`(O.S.)`, followed by dialogue |
| Dialogue | Lines right after a cue, kept **verbatim**, original language |
| Camera direction | `CLOSE ON`, `POV`, `WIDE`, `PLANO DETALHE`, etc. → camera hints |
| Sound | "a noise", "BANG", capitalized sound words → affects reaction/timing only |
| Action / description | Everything else — split into visible beats, in order |

Then decide, per non-visual statement (an inner thought, a memory, a feeling
stated as fact):

- already shown by another beat → skip it;
- can be shown with subtle performance only (expression, posture, pause) →
  add it as a small, clearly-assumed detail;
- central to the scene and needs a real narrative device (flashback, insert,
  voice-over) → ask the user how they want it represented;
- irrelevant to the image → drop it.

Never invent a narratively important event, character, or object that isn't
in the text. Neutral cinematic detail (lens feel, ambient dressing
consistent with the heading) is fine and should be flagged as assumed.

### 3. Save to session state

Populate `.video/session.yaml` (same shape `video` uses — see
`templates/session.yaml`):

- `environment.location` / `interior_exterior` / `time_of_day` from the heading;
- `subject` for each on-screen character (appearance only from what's
  stated or already in a reusable description the user gave earlier in this
  conversation — don't redesign a character you've already locked in);
- `action.primary` / `secondary` from the ordered visible beats;
- `camera` from any camera direction in the text;
- dialogue is kept verbatim as a short note (`meta.dialogue`) — it's for
  continuity only, never spoken by the video model unless the user
  explicitly asks for an audio-capable adapter and wants it voiced.

Keep the original excerpt language for dialogue and proper names; normalize
everything else into the state the same way `video` does.

### 4. Ask only what's really missing

After extraction, ask at most 1–3 questions — only for things the
screenplay genuinely doesn't answer and that would meaningfully change the
result (commonly: camera position/movement, overall look). Never re-ask
anything the text already states.

### 5. Continue as a normal conversation

From here, behave exactly like `video`: the user refines facts in plain
language, corrections overwrite old values, and "gera" / "gera para Wan" /
etc. produces the final prompt from accumulated state.

## Multiple scenes

A screenplay excerpt is sometimes clearly more than one continuous shot (a
scene heading change, a hard location/time jump, or far more visible action
than a single clip could hold). When that happens:

1. Say so in one line and propose splitting at the natural break points.
2. Handle the **first** scene now (steps 2–5 above).
3. Offer to continue with the next one — each one gets its own state. Tell
   the user to run `$video-reset` between scenes so facts don't bleed across
   them (a locked character description is the one thing worth carrying
   over by hand).

Don't build a shot-by-shot breakdown document for this — it's a one-line
heads-up and a queue of scenes to go through one at a time.

## Rules

1. **Fidelity first.** Never add events, characters, objects, or outcomes
   the text doesn't support. Cinematic detail that doesn't change the story
   is fine, and gets flagged as assumed.
2. **Order is sacred.** Visible beats keep screenplay order.
3. **Visible only.** Prompts describe what a camera records — thoughts,
   sounds and dialogue words are never turned into literal images.
4. **Dialogue is preserved, not voiced.** Exact text is kept verbatim for
   continuity; it isn't put in a silent model's prompt.
5. **Don't translate** proper names or on-screen text; dialogue stays in its
   original language.
6. **Reuse characters** the user already described earlier in the
   conversation instead of redesigning them.

## Example

> `$video-screenplay`
> ```
> INT. COZINHA - NOITE
> Maria entra lentamente.
> A luz da geladeira ilumina seu rosto.
> Ela percebe um copo quebrado no chão.
> ```
>
> Agent: "Entendi — cozinha, noite, Maria encontra um copo quebrado. Só
> faltam duas coisas: como a câmera está posicionada, e que aparência visual
> você quer?"
>
> User: `Quero que a cozinha seja velha e pequena. A câmera começa atrás dela.`
>
> Agent: updates the state.
>
> User: `Gera o prompt.`
>
> Agent: outputs the final prompt built from the screenplay plus the user's additions.

Full example: `examples/screenplay/`.
