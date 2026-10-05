# Example: screenplay (PT-BR) → three shots

`video-screenplay --duration 5` on a Portuguese excerpt with 6 beats, a line of
dialogue and a sound cue. Highlights: the duration warning, split / reduce /
lengthen options, a 3-shot breakdown that keeps the screenplay order, dialogue
kept verbatim but not voiced, a sound cue used only for timing, and exclusions
that stop the model from inventing story.

Start with **[walkthrough.md](walkthrough.md)**.

```
screenplay-kitchen/
  project.yaml
  characters/maria.yaml
  screenplay/excerpt-001/
    source-screenplay.md        # verbatim, Portuguese
    screenplay-analysis.yaml    # 6 beats, dialogue, sound cue, 3-shot breakdown
  scenes/
    scene-001/  # shot 1 — beats 1–2: enters into the refrigerator light
    scene-002/  # shot 2 — beat 3: POV insert of the broken glass
    scene-003/  # shot 3 — beats 4–6: "João?", the noise, she freezes
```
