# ComfyUI notes — scene-001 · v002

These notes map this version's files onto a standard ComfyUI workflow.
Node names follow the official templates and may differ in custom workflows.

## Run `wan-1` (wan)

1. Load the template workflow: **Wan 2.2 14B Text to Video** (recorded in
   `generation-config.yaml → workflow`).
2. **Positive prompt** (text encode node): paste `prompts/wan.txt`.
3. **Negative prompt** (second text encode node): paste `prompts/wan.negative.txt`.
4. **Latent / size node:** width `1280`, height `720`, length `81`.
5. **Sampler(s):** seed `428193` (fixed — reuse it in later versions), total
   steps `20` split between the high-noise and low-noise samplers as in the
   template, cfg `3.5`, sampler `euler`, scheduler `simple`.
6. **Model-specific:** model sampling shift `8.0` on both experts.
7. **Output:** save at `16` fps, then interpolate to 24 fps (e.g. a RIFE/FILM
   frame-interpolation node). Copy the file to `outputs/` and record the path
   and seed in `generation-config.yaml`, then set `status: generated`.

## Run `ltx-1` (ltx)

1. Load the template workflow: **LTX-Video text to video**.
2. **Positive prompt:** paste `prompts/ltx.txt`.
3. **Negative prompt:** paste `prompts/ltx.negative.txt`.
4. **Latent / size node:** width `1216`, height `704`, length `121`.
5. **Sampler:** seed — pick one and record it, steps `30`, cfg `3.0`,
   sampler `euler`, scheduler `LTXV`.
6. **Model-specific:** set the conditioning frame rate to `24`.
7. **Output:** save at `24` fps. Copy to `outputs/`, record path and seed,
   set `status: generated`.
