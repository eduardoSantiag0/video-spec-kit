# Contributing to Video Spec Kit

Thanks for helping! The kit is Markdown — you don't need to be a programmer
to contribute.

## Most wanted

1. **Adapters** for more video models (HunyuanVideo, CogVideoX, Mochi,
   SkyReels, closed models whose prompts are just text…).
2. **Field reports**: "with model X, phrasing Y worked better" — these
   become adapter guidance.
3. **Doc translations.**
4. **Skill improvements** that make the conversation ask fewer, better
   questions, or produce better prompts.

## Ground rules

- **No mandatory paid dependency.** Every step must work with a free or
  local agent and an open-weight model.
- **No premature infrastructure.** No backend, database, web UI, versioning
  system or build step. If Markdown can do it, use Markdown.
- **Conversation over configuration.** If a change makes the user do more
  typing, filling forms, or understanding internal state to get a prompt,
  it's the wrong direction for this kit.
- **One source of truth.** Skills are edited only in `.agents/skills/`.
- **Be specific.** Rules an agent can apply literally beat general advice.

## How to

### Change or add a skill

1. Edit `.agents/skills/<name>/SKILL.md`.
2. Regenerate wrappers: `python tools/sync_agent_wrappers.py`.
3. Walk through the example in `examples/` mentally (or for real) and
   update it if the output would differ.

### Add an adapter

```bash
cp -r adapters/_template adapters/<model-id>
```

Fill in the sections with plain guidance an agent can follow directly —
see `adapters/wan/adapter.md` or `adapters/ltx/adapter.md` for the level of
detail expected.

## Before opening a pull request

- [ ] `python tools/sync_agent_wrappers.py --check` passes.
- [ ] Links between files are correct (paths are relative to the repo root).
- [ ] No placeholder text or empty files.
- [ ] `CHANGELOG.md` updated under an "Unreleased" heading.

## Commit and PR style

- Small, focused PRs. One adapter per PR.
- Present-tense commit subjects: "Add HunyuanVideo adapter".
- Explain *why* in the PR description, and for adapters, which model
  versions you tested.

## License

By contributing you agree that your contributions are licensed under the
[Apache License 2.0](LICENSE).
