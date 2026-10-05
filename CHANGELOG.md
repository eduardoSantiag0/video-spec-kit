# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

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
