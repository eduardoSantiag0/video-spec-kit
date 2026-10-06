# How it works

Video Spec Kit is a conversational assistant, not a pipeline you operate.
This page explains the mechanics behind the two skills in `.agents/skills/`.

## The loop

```
IDEA / SCREENPLAY
      ↓
CONVERSATION
      ↓
UNDERSTAND + CLARIFY
      ↓
REMEMBER
      ↓
USER REFINES
      ↓
GENERATE FINAL PROMPT
```

Every message you send is handled the same way: the agent reads it for new
or corrected facts, merges them into memory, asks at most a couple of
sharp questions if something important is still missing or ambiguous, and
otherwise just acknowledges and waits. When you ask it to generate, it
composes the final prompt from everything accumulated so far.

## Memory

Facts live in `.video/session.yaml`, created the first time you mention
something. It's working memory, not a deliverable — you never need to open
or edit it; the agent reads and rewrites it every turn. `templates/session.yaml`
documents the fields it understands (subject, action, environment, camera,
lighting, style) — none are required, and none are asked about unless they'd
meaningfully change the result.

A correction always replaces the old value; the agent never keeps two
contradictory facts about the same thing. `$video-reset` clears memory so
the next message starts a clean scene.

## Why so few questions

Earlier versions of this kit asked a fixed checklist (duration, lens, fps,
resolution, camera, style, lighting...) before doing anything. That's
friction, not rigor. The agent now asks only when:

1. the missing information would change the result significantly;
2. there's a real ambiguity;
3. generating now would produce something contradictory;
4. you ask for help developing the scene.

If you already stated several things in one sentence ("plano médio, câmera
fixa, altura dos olhos"), none of them get asked about again.

## Creative direction, not just facts

You can also give direction instead of facts ("deixa essa cena mais
tensa"). The agent offers a couple of concrete levers (camera, performance,
lighting) instead of silently guessing, and applies whichever you pick.

## Adapters

`adapters/wan/adapter.md` and `adapters/ltx/adapter.md` describe how each
model likes to be prompted — word budget, section order, negative-prompt
approach, known limitations. There's no compiler: the agent reads the
adapter file and writes the prompt directly from the accumulated facts. Ask
for "gera para Wan" / "gera para LTX" or just "gera" for a generic
high-quality prompt. Add a new model by copying `adapters/_template/`.

## Language

You converse in whatever language you write in. Internal state is
normalized to English so the agent reasons about it consistently, but you
never see it — it's never shown back to you in English. The final prompt
defaults to English (video models are best documented in it) unless you ask
for another language ("gera em português"). Proper names, exact dialogue,
and text that must appear on screen are never translated, regardless of
output language.

## From a screenplay

`$video-screenplay` reads a pasted excerpt once — sluglines, character
cues, action, dialogue — and extracts only what a camera would actually
record into the same `.video/session.yaml` memory `video` uses. From then
on it's the same conversation: you can correct or add facts, and "gera"
produces the prompt. It never turns a thought, memory or sound into a
literal image, and it never puts dialogue words into a silent model's
prompt — see the skill's Rules section for the exact handling.

If an excerpt clearly needs more than one shot, the skill says so, handles
the first one, and offers to continue with the rest one at a time.

## What this kit does not do

No versioning, no seeds, no experiment logs, no diffs between attempts, no
schema validation, no required reproducibility record. If you want to keep
notes on what worked, that's a `projects/` folder you manage yourself — the
kit doesn't require or generate one.
