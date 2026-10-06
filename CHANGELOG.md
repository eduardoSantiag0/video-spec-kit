# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed — major simplification (breaking)

The kit is now a conversational assistant instead of a versioned
spec-and-compiler pipeline. Most of the previous architecture is gone:

- Replaced nine skills (`video-clarify`, `video-character`, `video-scene`,
  `video-storyboard`, `video-shot`, `video-prompt`, `video-review`,
  `video-iterate`, plus the `video` orchestrator) with three: `video`
  (now does understand/clarify/remember/update/generate itself, in one
  conversation loop), `video-screenplay` (simplified to feed the same
  conversation state instead of a separate analysis pipeline), and the new
  `video-reset`.
- Removed `kit/` (conventions, defaults, controlled vocabulary), `schemas/`
  (JSON Schema validation), `presets/` (style/camera/lighting YAML), and
  `tools/validate.py` — no schema validation, no preset system.
- Removed scene versioning (`v001`, `v002`...), `history.md`, `iteration.md`,
  `review.md`, `generation-config.yaml`, per-field provenance tagging, and
  the "one controlled variable at a time" experiment workflow.
- Replaced the per-version file tree (`scene-spec.yaml` → `storyboard.md` →
  `shot-spec.yaml` → `prompts/<adapter>.txt`) with a single conversational
  memory file, `.video/session.yaml`, not checked into git.
- Adapters (`adapters/wan/`, `adapters/ltx/`) simplified from a
  machine-readable compiler profile + prompt-template pair into one plain
  Markdown guidance file each; `video` reads them directly when composing
  a prompt, no compiler step.
- Replaced `examples/tokyo-rain`, `examples/screenplay-rooftop` and
  `examples/screenplay-kitchen` with `examples/conversation/` and
  `examples/screenplay/` — a chat transcript and the resulting prompt,
  instead of a versioned file tree.
- Consolidated `docs/philosophy.md`, `docs/workflow.md`,
  `docs/prompt-compiler.md`, `docs/screenplay.md`, `docs/agent-support.md`,
  `docs/comfyui.md` and `docs/extending.md` into a single `docs/how-it-works.md`.
- `AGENTS.md`, `README.md` and `README.pt-BR.md` rewritten for the new
  conversational flow.

### Why

The versioned, schema-validated pipeline added friction (files, provenance
tags, version folders) the typical user never asked for. The project is now
scoped to what most people actually want: describe a scene, refine it by
talking, get a prompt.

## [0.1.0] — 2026-10-05

### Added
- Nine Markdown skills: `video` (orchestrator), `video-clarify`, `video-character`,
  `video-scene`, `video-storyboard`, `video-shot`, `video-prompt`, `video-review`,
  `video-iterate`, plus `video-screenplay` (aliases `video_from_screenwright`,
  `video-from-screenplay`).
- Agent support: `.agents/skills/` (Codex, OpenCode, Gemini CLI), generated
  wrappers for Claude Code (`.claude/skills/`) and Gemini CLI slash commands
  (`.gemini/commands/`), `AGENTS.md`.
- JSON Schemas for scene, shot, character, generation config, preset, project.
- Prompt adapters: Wan, LTX; adapter template.
- Presets: 4 styles, 4 cameras, 4 lighting setups.
- Kit rules: conventions, defaults with inference rules, controlled vocabulary,
  language policy.
- Complete examples: `tokyo-rain` (v001 → review → v002 → review),
  `screenplay-rooftop`, `screenplay-kitchen`.
- Optional tools: `tools/validate.py`, `tools/sync_agent_wrappers.py`.
