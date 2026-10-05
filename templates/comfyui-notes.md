<!-- TEMPLATE — comfyui-notes.md. Optional. Produced by video-prompt when project.yaml has `tool: comfyui` or the user asks. -->
# ComfyUI notes — <scene-id> · <version>

These notes map this version's files onto a standard ComfyUI workflow.
Node names follow the official templates and may differ in custom workflows.

## Run `<run-id>` (<adapter>)

1. Load the template workflow: **<template name>** (record its name/version in
   `generation-config.yaml → workflow`).
2. **Positive prompt** (text encode node): paste `prompts/<adapter>.txt`.
3. **Negative prompt** (second text encode node): paste
   `prompts/<adapter>.negative.txt` <or "leave empty — adapter has none">.
4. **Latent / size node:** width `<w>`, height `<h>`, length/frames `<n>`.
5. **Sampler:** seed `<seed or "random, then record it">`, steps `<steps>`,
   cfg `<cfg>`, sampler `<sampler>`, scheduler `<scheduler>`.
6. **Model-specific:** <shift, conditioning frame rate, image input...>.
7. **Output:** save at `<fps>` fps. Copy the file to `outputs/` and record the
   path and the seed in `generation-config.yaml`, then set `status: generated`.
