---
name: video-reset
description: Clears the current scene's conversation state (.video/session.yaml) so the next message starts a brand-new scene. Use when the user wants to start over, begin an unrelated scene, or types $video-reset.
---

# video-reset

## Purpose

Forget the current scene so `video` / `video-screenplay` start clean on the
next message.

## When to use

- The user says "começa de novo", "nova cena", "esquece isso", "start over",
  "new scene" (unrelated to the current one).
- `$video-reset`.

## Workflow

1. If `.video/session.yaml` exists and has content, show a one-line summary
   of what's about to be cleared (e.g. "limpando: homem na estrada rural,
   câmera fixa, visual cinematográfico").
2. Delete `.video/session.yaml` (or overwrite it with an empty `scene: {}`).
3. Confirm in one line that the next message starts a new scene.

Don't ask for confirmation first — this is cheap and reversible only in the
sense that nothing outside the chat is lost; if the user immediately regrets
it, the facts are still visible earlier in the conversation and can be
restated.

## Output

One line, e.g.: "Pronto, comecei uma cena nova." / "Done — starting fresh."
