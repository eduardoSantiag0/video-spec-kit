# AGENTS.md — instructions for coding agents

This repository is **Video Spec Kit**: a conversational assistant, built as
Markdown skills, for turning a video idea into a polished prompt for AI
video models. It does not generate video.

## Skills

Canonical skills live in `.agents/skills/<name>/SKILL.md`:

| Skill | Use |
|-------|-----|
| `video` | **Main entry point.** Chat about an idea, get asked only what matters, refine in plain language, ask to generate when ready. |
| `video-screenplay` | Paste a screenplay excerpt; it extracts the visual scene into the same conversation, then behaves like `video`. |
| `video-reset` | Clear the current scene's memory and start a new one. |

When the user types `$video`, `/video`, or describes a video idea, read
`.agents/skills/video/SKILL.md` and follow it. Same for the other skills by
name. If your agent does not load skills automatically, read the file
yourself.

### Aliases

Treat these exactly like the skill they point to (same file, same arguments):

| Typed by the user | Skill |
|-------------------|-------|
| `$video_from_screenwright`, `/video_from_screenwright` | `video-screenplay` |
| `$video-from-screenplay`, `/video-from-screenplay` | `video-screenplay` |

A pasted screenplay excerpt (sluglines such as `INT.`/`EXT.`, CHARACTER cues)
also goes to `video-screenplay`.

## How it works

The whole kit is one idea: **conversation before prompting**. There is no
versioning, no experiment log, no seed tracking, no formal review step —
just a running memory of the current scene (`.video/session.yaml`, written
and read by the skills, never meant for the user to edit) that accumulates
facts, gets corrected in plain language, and gets compiled into a prompt on
request. Details: `docs/how-it-works.md`.

## Rules for every agent

- Converse in the user's language; normalize `.video/session.yaml` to
  English internally; default the final prompt to English unless the user
  asks for another language.
- Ask only questions that would meaningfully change the result — never a
  fixed checklist, never more than 1–3 per turn, never about something
  already stated.
- Never invent a narratively important detail (who's there, what happens);
  small non-critical visual filler is fine when needed to make a prompt concrete.
- A correction replaces the old value; never hold two contradictory facts.
- Never call paid APIs or services. Never generate or download video.
- Don't modify `adapters/`, `templates/`, `docs/` or the skill folders during
  user work. Anything the user wants to keep (notes, reference images) is
  theirs to put under `projects/` if they want one — the kit doesn't require it.

## Maintaining the kit

- Edit skills only in `.agents/skills/`. Then run
  `python tools/sync_agent_wrappers.py` to regenerate `.claude/skills/` and
  `.gemini/commands/`.
- See `CONTRIBUTING.md`.
