# Using the kit with ComfyUI

The kit does not control ComfyUI in V1. It produces everything you need to set
a workflow by hand, and records what you did so results are reproducible.

## Turn on ComfyUI notes

Set `tool: comfyui` in `projects/<id>/project.yaml` (or ask the agent for
ComfyUI notes). Each version then gets a `comfyui-notes.md` that maps the
files onto a standard workflow:

| Kit file / field | ComfyUI |
|------------------|---------|
| `prompts/<adapter>.txt` | Positive text encode node |
| `prompts/<adapter>.negative.txt` | Negative text encode node |
| `generation-config.yaml → width/height/num_frames` | Empty latent video / size node (width, height, length) |
| `seed, steps, cfg, sampler, scheduler` | Sampler node(s) |
| `params.shift` (Wan) | Model sampling shift node |
| `fps` | Conditioning frame rate (LTX) and the video save node |
| `params.interpolate_to_fps` | Frame interpolation node (e.g. RIFE/FILM) before saving |
| `reference_images` | Load image → image-to-video / first-last-frame nodes |

## Record what you ran

After generating, tell the agent (or edit the run yourself):

```yaml
status: generated
seed: 428193                  # the actual seed used
output: outputs/wan-1.mp4
workflow: ComfyUI template "Wan 2.2 14B Text to Video"   # name + version/date
```

If you changed anything in the workflow (a LoRA, a different sampler), put it
in `params` or `notes`. A result is only reproducible if the record matches
what ran.

## Tips

- Save the workflow JSON next to the version (`v002/workflow.json`) if you
  customized it. It is just another file in a self-contained version folder.
- Keep the seed fixed across versions while experimenting (`video-iterate`
  does this for you).
- Templates in ComfyUI change over time; node names in the notes follow the
  official templates and may differ in your build.

## Future integration

Planned (see the README roadmap): exporting a ready-to-load workflow from
`generation-config.yaml`, and importing settings from a workflow JSON. The
`generation-config.yaml → params` map is open-ended so these can be added
without changing the schema.
