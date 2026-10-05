# Example: Tokyo Rain

A complete, versioned run of the kit for one idea:

> "A woman rides a bicycle through Tokyo at night during heavy rain."

Start with **[walkthrough.md](walkthrough.md)** — it shows the conversation and
points at each file as it is produced.

```
tokyo-rain/
  project.yaml
  characters/mika.yaml
  scenes/scene-001/
    history.md                 # experiment log: v001 → v002
    v001/                      # first attempt (reviewed → frozen)
      scene-spec.yaml          # source of truth
      storyboard.md
      shot-spec.yaml           # resolved + conflict-checked
      prompts/wan.txt  wan.negative.txt  ltx.txt  ltx.negative.txt
      generation-config.yaml   # seed 428193, Wan 2.2 A14B settings
      comfyui-notes.md
      review.md                # identity drift + hand flicker
    v002/                      # one-variable experiment (reviewed → frozen)
      ...same files...
      iteration.md             # the diff, the hypothesis, the conclusion
      review.md
```

This folder has the same layout as a real project under `projects/`. Copy it
to `projects/tokyo-rain/` to continue it with the agent ("$video next
experiment for tokyo-rain").
