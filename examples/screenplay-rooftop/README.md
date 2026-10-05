# Example: screenplay → single shot

`video-screenplay` (invoked with the alias `$video_from_screenwright`) on a
3-line English excerpt that fits one 5-second generation. Highlights: a
non-visual line ("Elena has waited all winter…") shown only as subtle
performance, screenplay-stated character traits, one clarification question.

Start with **[walkthrough.md](walkthrough.md)**.

```
screenplay-rooftop/
  project.yaml
  characters/elena.yaml
  screenplay/excerpt-001/
    source-screenplay.md        # verbatim excerpt
    screenplay-analysis.yaml    # parse, beats, non-visual, shot breakdown
  scenes/scene-001/             # the single shot — a standard scene
    history.md
    v001/ scene-spec.yaml  storyboard.md  shot-spec.yaml  prompts/  generation-config.yaml
```
