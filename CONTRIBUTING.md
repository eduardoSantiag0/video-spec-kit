# Contributing to Video Spec Kit

Thanks for helping! The kit is Markdown, YAML and JSON — you don't need to be
a programmer to contribute.

## Most wanted

1. **Adapters** for more video models (HunyuanVideo, CogVideoX, Mochi,
   SkyReels, closed models whose prompts are just text…).
2. **Field reports**: "with model X, change Y did Z" — with the version
   folders (`scene-spec.yaml`, `generation-config.yaml`, `iteration.md`).
   These become adapter guidance.
3. **Presets** for styles, camera moves and lighting setups.
4. **Doc translations** (the specs stay in English by design; the docs don't have to).
5. **Skill improvements** that make agents ask fewer, better questions.

## Ground rules

- **No mandatory paid dependency.** Every core step must work with a free or
  local agent and an open-weight model.
- **No premature infrastructure.** No backend, database, web UI, Docker or
  cloud service in V1. If Markdown can do it, use Markdown.
- **One source of truth.** Shared rules go in `kit/conventions.md`; skills
  reference them. Skills are edited only in `.agents/skills/`.
- **Specs stay semantic.** No model syntax in schemas, presets or examples —
  that belongs in `adapters/`.
- **Be specific.** Rules an agent can apply literally beat general advice.

## How to

### Change or add a skill

1. Edit `.agents/skills/<name>/SKILL.md`. Keep the sections: Purpose, When to
   use, Inputs, Workflow, Rules, Output, Failure handling, Examples.
2. Regenerate wrappers: `python tools/sync_agent_wrappers.py`.
3. Run the Tokyo example mentally (or for real) through your change and update
   `examples/` if the output would differ.

### Add an adapter or preset

Follow [docs/extending.md](docs/extending.md).

### Change a schema

1. Edit `schemas/*.schema.json` (keep `spec_version: 1` compatible, or bump it
   and document the migration in `CHANGELOG.md`).
2. Update the matching file in `templates/`, `kit/vocabulary.md` if enums
   changed, and the examples.
3. Validate: `pip install pyyaml jsonschema && python tools/validate.py`.

## Before opening a pull request

- [ ] `python tools/sync_agent_wrappers.py --check` passes.
- [ ] `python tools/validate.py` passes (if you touched YAML or schemas).
- [ ] Links between files are correct (paths are relative to the repo root).
- [ ] No placeholder text or empty files.
- [ ] `CHANGELOG.md` updated under an "Unreleased" heading.

## Commit and PR style

- Small, focused PRs. One adapter or one preset family per PR.
- Present-tense commit subjects: "Add HunyuanVideo adapter".
- Explain *why* in the PR description, and for adapters, which model versions
  you tested.

## License

By contributing you agree that your contributions are licensed under the
[Apache License 2.0](LICENSE).
