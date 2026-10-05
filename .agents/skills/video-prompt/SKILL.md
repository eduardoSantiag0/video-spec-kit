---
name: video-prompt
description: Compiles a resolved shot-spec.yaml into a model-specific prompt (and negative prompt) using a prompt adapter such as wan or ltx, lints it against overprompting and contradictions, and writes generation-config.yaml with reproducible settings. Second half of the Prompt Compiler. Use when the user types $video-prompt [adapter], wants prompts for another model, or after video-shot.
---

# video-prompt

## Purpose

Prompts are compiled artifacts. This skill renders the same shot for different
models without changing its meaning, keeps prompts short and coherent, and
records the settings needed to reproduce the generation.

Prompt Compiler stages handled here: (6) select adapter profile, (7) render,
(8) lint, (9) write. Stages 1–5 are in `video-shot`. Overview: `docs/prompt-compiler.md`.

## When to use

- Step 7 of `video` (once per adapter in the project).
- `$video-prompt` → all adapters in `project.yaml → adapters`.
- `$video-prompt wan` / `$video-prompt ltx` → that adapter only.
- `$video-prompt wan ti2v-5b` → that adapter with a specific profile.

## Inputs

- Target scene/version: the current version of the scene in this conversation
  unless the user names one.
- `shot-spec.yaml` of that version.
- `adapters/<id>/adapter.md` (frontmatter profile + guidance) and
  `adapters/<id>/prompt-template.md`.
- `project.yaml` (`tool`), `templates/generation-config.yaml`,
  `templates/comfyui-notes.md`.

## Workflow

1. **Freshness.** If the version is a draft, run `video-shot` first (it is
   idempotent). If frozen, use its `shot-spec.yaml` as-is.
2. **Gate.** If `shot-spec.yaml → conflicts` has any `blocking: true` entry with
   `resolution: pending user decision`, stop and report it. Do not compile.
3. **Adapter.** Unknown adapter id → list `adapters/*/` (excluding `_template`)
   and stop.
4. **Profile.** In order: profile named by the user → profile of an existing
   run for this adapter in `generation-config.yaml` → `default_profile`.
5. **Render the positive prompt** with `prompt-template.md`:
   - Fill every P1 slot. Add P2 slots. Add P3 slots while the word count stays
     ≤ the upper bound of `target_words`.
   - Use `image-to-video` variant when `format.input_mode` is not
     `text-to-video`.
   - Insert each subject `anchor` verbatim.
   - Use the language in the profile's `prompt.language` (`kit/conventions.md` §7).
6. **Lint** (fix, then re-check; max 3 passes):

   | Check | Fix |
   |-------|-----|
   | Words > `max_words` | Drop P3, then compress P2 phrases; never drop P1. |
   | Words < lower bound of `target_words` | Add P3 detail from the shot-spec; never invent facts. |
   | A fact appears twice (incl. synonyms: "rainy… wet with rain") | Keep the first occurrence. |
   | Synonym stacks ("cinematic, filmic, movie-like") | Keep one term. |
   | Negation in the positive prompt ("no people") | Move to negative prompt, or rephrase positively ("an empty street"). |
   | Quality spam ("8k", "masterpiece", "best quality", "ultra detailed") | Remove. |
   | More than one camera-movement sentence | Keep the one matching `camera.movement`. |
   | Camera words contradict `camera.*` (e.g. "zoom" when movement is `tracking-side`) | Rewrite from the shot-spec. |
   | Character names ("Mika") | Replace with the anchor or a pronoun — models do not know names. |
   | Meta language ("this video shows", "generate", "prompt") | Remove. |
   | Cut language ("cut to", "then the scene changes") | Rewrite as continuous change. |
   | Tense other than present | Rewrite in present tense. |

7. **Negative prompt** (only if the adapter has `negative_prompt: true` and the
   profile `cfg` > 1): `shot-spec → negatives` + the adapter's quality list,
   minus items that contradict the spec. Comma-separated, no duplicates.
8. **Write** `prompts/<adapter>.txt` (and `prompts/<adapter>.negative.txt`) —
   plain text, one paragraph, no markdown, trailing newline.
9. **generation-config.yaml.** Create from the template or update the run for
   this adapter (`id: <adapter>-1`):
   - `status: planned`, `model` from profile, `prompt_file`,
     `negative_prompt_file` (omit when no negative), `seed: null`.
   - `width`/`height`: profile `sizes[format.aspect_ratio]`; if missing, the
     closest ratio and a note.
   - `fps`: profile fps. `num_frames`: smallest count ≥ `duration_s × fps`
     that satisfies the adapter `frame_rule`. If it exceeds the profile's
     `num_frames`, keep the profile value, and warn that the clip will be
     shorter or should be split.
   - If spec fps ≠ profile fps: `params.interpolate_to_fps: <spec fps>`.
   - `steps`, `cfg`, `sampler`, `scheduler`, `params` from the profile.
   - `reference_images` from `shot-spec → references.images`.
   - Never overwrite a run with `status: generated`; add `<adapter>-2` instead.
10. **ComfyUI notes.** If `project.yaml → tool: comfyui` or the user asks,
    write `comfyui-notes.md` from the template (one section per run).
11. **Report** in the user's language: the prompt text (so the user can copy
    it), word count, dropped P3 items, warnings from the shot-spec, files
    written.

## Rules

1. Compile only from `shot-spec.yaml`. Never add facts that are not in it.
2. Never edit `scene-spec.yaml` from this skill.
3. The same shot-spec must produce the same prompt: follow slot order and
   wording rules literally; prefer vocabulary phrases from `kit/vocabulary.md`
   and the adapter.
4. If the user hand-edits a prompt and asks to keep it: set
   `prompt_override: true` and a reason in the run, and suggest the spec
   change that would produce the same effect.

## Output

- `<version>/prompts/<adapter>.txt`, optional `<adapter>.negative.txt`.
- `<version>/generation-config.yaml` (run for the adapter).
- Optional `<version>/comfyui-notes.md`.

## Failure handling

| Situation | Action |
|-----------|--------|
| Missing `shot-spec.yaml` on a frozen version | Report it; offer `video-iterate` to rebuild in a new version. |
| Aspect ratio not in profile sizes | Use the closest; write a `notes` line in the run. |
| P1 alone exceeds `max_words` | Do not truncate P1. Report the scene is too complex for one clip; suggest removing a subject/beat or splitting. |
| Adapter lacks a feature the spec needs (e.g. `first-last-frame`) | Compile the text-to-video variant, warn, record it in run `notes`. |

## Examples

`$video-prompt ltx` on the Tokyo scene → writes `prompts/ltx.txt` (≈150
words), `prompts/ltx.negative.txt`, adds run `ltx-1` (1216×704, 121 frames,
24 fps, 30 steps, CFG 3). Compare `prompts/wan.txt` and `prompts/ltx.txt` in
`examples/tokyo-rain/scenes/scene-001/v001/` to see one shot compiled two ways.
