# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- `video-screenplay` skill: screenplay excerpt (any language) → parse → visual
  extraction → clarify → standard scene specs (one per shot) → storyboard →
  shot spec → prompts. Aliases `video_from_screenwright` and `video-from-screenplay`.
- `screenplay-analysis.yaml` (schema + template) and verbatim `source-screenplay.md`.
- Scene `source` block; `environment.interior_exterior`; structured
  `audio.dialogue` lines and `audio.generate`; provenance source `screenplay`.
- Conflict checks C16 (screenplay beat order) and C17 (offscreen character rendered).
- "Dialogue and sound" section in adapters.
- Alias support in `tools/sync_agent_wrappers.py`; screenplay checks in `tools/validate.py`.
- Examples `screenplay-rooftop` (single shot) and `screenplay-kitchen` (PT-BR, three shots).
- `docs/screenplay.md`, `README.pt-BR.md`.
- `--no-questions` / `--not-questions` flag for `video` and `video-screenplay`:
  nothing is asked; `video-clarify` → *No-questions mode* picks the least-inventive
  option, tags it `inferred` and lists it under *Decided automatically*;
  `video-shot` auto-resolves blocking conflicts by source priority.

### Changed
- `audio.dialogue` is now a list of `{character, text, ...}` lines (was a string).
- `video-clarify` no longer caps the number of CRITICAL questions per round or
  the number of rounds; it asks every CRITICAL dimension and keeps asking
  further rounds for as long as an answer keeps introducing a new one.
- Prompts now default to the idea's language (`idea_language`) instead of
  always English. `shot-spec.yaml` carries `idea_language` from
  `scene-spec.yaml`; an adapter profile can still pin a fixed
  `prompt.language` when its target model needs one (`wan` and `ltx` default
  to `auto`). Negative-prompt quality terms are translated sense-for-sense
  into the compiled language. See `kit/conventions.md` §7 rule 5.

## [0.1.0] — 2026-10-05

### Added
- Nine Markdown skills: `video` (orchestrator), `video-clarify`, `video-character`,
  `video-scene`, `video-storyboard`, `video-shot`, `video-prompt`, `video-review`,
  `video-iterate`.
- Agent support: `.agents/skills/` (Codex, OpenCode, Gemini CLI), generated
  wrappers for Claude Code (`.claude/skills/`) and Gemini CLI slash commands
  (`.gemini/commands/`), `AGENTS.md`.
- JSON Schemas for scene, shot, character, generation config, preset, project.
- Prompt adapters: Wan, LTX; adapter template.
- Presets: 4 styles, 4 cameras, 4 lighting setups.
- Kit rules: conventions, defaults with inference rules, controlled vocabulary,
  language policy.
- Complete example `examples/tokyo-rain` (v001 → review → v002 → review).
- Optional tools: `tools/validate.py`, `tools/sync_agent_wrappers.py`.
