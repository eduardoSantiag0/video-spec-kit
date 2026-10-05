# AGENTS.md — instructions for coding agents

This repository is **Video Spec Kit**: Markdown skills, schemas, templates and
prompt adapters that turn a video idea into a structured spec and
model-specific prompts. It does not generate video.

## Skills

Canonical skills live in `.agents/skills/<name>/SKILL.md`:

| Skill | Use |
|-------|-----|
| `video` | **Main entry point.** Idea → clarify → spec → storyboard → shot → prompts; routes feedback to review/iterate. |
| `video-clarify` | Ask only the questions that change the video. |
| `video-character` | Reusable character with a verbatim prompt anchor. |
| `video-scene` | Write `scene-spec.yaml` (source of truth) with provenance. |
| `video-storyboard` | First frame, timed beats, last frame. |
| `video-shot` | Shot design, resolution, conflict check → `shot-spec.yaml`. |
| `video-prompt` | Compile prompts per adapter (`wan`, `ltx`) + `generation-config.yaml`. |
| `video-review` | Diagnose a generated clip from the user's description. |
| `video-iterate` | New version with one controlled change, recorded diff. |
| `video-screenplay` | Screenplay excerpt → analysis → shot breakdown → standard scene specs → prompts. |

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

## Rules for every agent

- Shared rules: `kit/conventions.md` (layout, versioning, provenance, language
  policy, resolution order). Read it before writing any spec file.
- User work goes in `projects/`. Do not modify `kit/`, `schemas/`,
  `templates/`, `adapters/`, `presets/`, `examples/`, `docs/` or the skill
  folders during user work.
- Never call paid APIs or services. Never generate or download video.
- Converse in the user's language; write spec files in English; prompts in the
  language the adapter specifies.

## Maintaining the kit

- Edit skills only in `.agents/skills/`. Then run
  `python tools/sync_agent_wrappers.py` to regenerate `.claude/skills/` and
  `.gemini/commands/`.
- Optional validation: `python tools/validate.py` (needs `pyyaml`, `jsonschema`).
- See `CONTRIBUTING.md`.
