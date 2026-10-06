# Extending the kit

Three things are designed to be added by the community: **prompt adapters**,
**presets**, and **vocabulary terms**. None needs code.

---

## Create a prompt adapter

An adapter teaches the compiler how one video model wants its prompt. It is a
folder with two files.

1. Copy the template:

   ```bash
   cp -r adapters/_template adapters/<model-id>
   ```

   `<model-id>` is lowercase, short, and becomes the command argument
   (`$video-prompt <model-id>`) and the prompt file name
   (`prompts/<model-id>.txt`).

2. Fill the **frontmatter profile** in `adapter.md` — the machine-readable
   part the compiler uses:

   | Field | Meaning |
   |-------|---------|
   | `prompt.form`, `language` | Paragraph / tags / sections; prompt language. Use `auto` to follow the idea's language (the default — see `kit/conventions.md` §7); pin a fixed code only if this model needs a specific language. |
   | `prompt.target_words`, `max_words` | Word budget. P3 is dropped first when over. |
   | `prompt.section_order` | Order of slots in the prompt. |
   | `negative_prompt` | Whether the model uses one. |
   | `supports` | `image_to_video`, `first_last_frame`, `audio`. |
   | `frame_rule` | Constraints on frames and sizes (e.g. `4n + 1`). |
   | `profiles[]` | Checkpoints with fps, frames, sizes per aspect ratio, steps, CFG, sampler, scheduler, extra `params`. |
   | `default_profile` | Profile used when the user names none. |

3. Write the **guidance** sections in `adapter.md`. All are required:
   language, order of information, level of detail, negative prompt, camera,
   motion, reference images, temporal consistency, dialogue and sound,
   duration, known limitations, example. The language section states which
   languages the model is well-supported in, used by `video-prompt` to decide
   whether to add a weaker-adherence warning when compiling in another one.
   Write rules an agent can apply literally ("Put the camera in its own
   sentence after the environment"), not impressions ("the model is good with
   cameras").

4. Write `prompt-template.md`: the slot line, a slot table (source fields in
   `shot-spec.yaml`, tier, phrasing rule), the negative prompt recipe, and the
   image-to-video variant.

5. Test it: compile the Tokyo example with your adapter
   (`$video-prompt <model-id>` on a copy in `projects/`), generate, and add
   what you learned to *Known limitations*.

6. Add the id to `kit/defaults.yaml → adapters` only if it should be compiled
   by default for everyone.

Guidelines:

- Base claims on the model's official documentation or on repeated tests;
  say which in the section.
- Record versions in `written_against`. Models change; stale advice is worse
  than none.
- Never require a paid API in the adapter. Closed or hosted models can have
  adapters (the prompt is just text), but the kit must not depend on them.

---

## Create a preset

A preset is a partial scene spec that scenes reference and can override.

```yaml
# presets/lighting/blue-hour.yaml
spec_version: 1
id: blue-hour
kind: lighting                  # style | camera | lighting
description: Deep blue twilight after sunset; city lights just turning on.
values:
  lighting:
    type: residual skylight after sunset plus early street lights
    direction: soft top light from the sky, warm points from practicals
    quality: soft
    contrast: medium
    color_temperature: mixed
good_for: [city establishing shots, quiet endings]
avoid_with: [lighting/golden-hour, styles/documentary at noon]
```

Rules:

- `values` may contain only the sections allowed for its kind:
  style → `style`, `motion`; camera → `camera`, `motion`; lighting → `lighting`
  (enforced by `schemas/preset.schema.json`).
- Use `kit/vocabulary.md` terms for enum fields.
- Describe the look, not a model's syntax (no "8k", no weights).
- One idea per preset. Two presets that are always used together are a sign
  that one of them is doing too much.

Scenes use it with `presets: { lighting: blue-hour }`. A project can keep
private presets in `projects/<id>/presets/<kind>/` — they win over kit presets
with the same id.

---

## Add a vocabulary term

1. Add the value to the `enum` in `schemas/common.schema.json`.
2. Add a row to `kit/vocabulary.md` with definition and neutral phrase.
3. If an adapter phrases it differently, mention it in that adapter's
   *Camera* or *Motion* section.

---

## Add or change a skill

1. Edit or add `.agents/skills/<name>/SKILL.md` with the required sections:
   Purpose, When to use, Inputs, Workflow, Rules, Output, Failure handling,
   Examples. `name` must match the folder.
2. Put rules shared by several skills in `kit/conventions.md`, not in each skill.
3. Run `python tools/sync_agent_wrappers.py`.
