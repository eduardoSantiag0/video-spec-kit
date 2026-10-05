# The Prompt Compiler

The Prompt Compiler turns the source of truth (`scene-spec.yaml`) into a
model-specific prompt. In V1 it is not a program — it is a procedure that the
agent follows, split across two skills. This page is the overview; the
normative steps are in the skill files.

```
 scene-spec.yaml ─┐
 characters/*.yaml┤                ┌─────────────── video-shot ───────────────┐
 presets/*.yaml ──┼──► 1 read ──► 2 shot design ──► 3 resolve ──► 4 conflicts ──► 5 priorities
 kit/defaults ────┘                                                                   │
                                                                              shot-spec.yaml (IR)
                                                                                      │
                     ┌──────────────────── video-prompt ────────────────────┐         │
   adapters/<id>/ ──►│ 6 select profile ──► 7 render slots ──► 8 lint ──► 9 write │◄────────┘
                     └──────────────────────────────────────────────────────┘
                                         │
                       prompts/<id>.txt, <id>.negative.txt, generation-config.yaml
```

## Stages

| # | Stage | Where | What happens |
|---|-------|-------|--------------|
| 1 | Read | `video-shot` | Load scene spec, characters, presets, defaults. |
| 2 | Shot design | `video-shot` | Fill framing, focus, movement detail, lens (unless a preset defines them); check first/last frame are achievable. |
| 3 | Resolve | `video-shot` | Merge layers: defaults → project → presets (style, camera, lighting) → character → scene. Record the winning source of every field. |
| 4 | Conflicts | `video-shot` | Run checks C1–C15. Blocking conflicts stop compilation and become questions. |
| 5 | Priorities | `video-shot` | Assign each fact to one tier: P1 (always), P2 (if room), P3 (only if room remains). |
| 6 | Profile | `video-prompt` | Pick the adapter profile (model, sizes, fps, steps, CFG). |
| 7 | Render | `video-prompt` | Fill the adapter's template slots in the adapter's order, P1 → P2 → P3 within the word budget. |
| 8 | Lint | `video-prompt` | Remove duplicates, synonym stacks, negations, quality spam, names, meta and cut language; enforce one camera sentence and present tense. |
| 9 | Write | `video-prompt` | Prompt files, negative prompt, generation config (frames computed from the frame rule). |

## The intermediate representation

`shot-spec.yaml` is the compiler's IR: fully resolved, model-agnostic,
conflict-checked. It exists so that:

- every adapter consumes the same, already-validated input;
- a frozen version records exactly what was compiled, even if a preset or
  character file changes later;
- reviews can point at resolved values ("the lighting came from the preset").

## Guarding against overprompting

Long prompts are not better prompts. Models weight early, concrete
information; repetition and contradictions dilute it. The compiler:

1. **Budgets words** per adapter (`target_words`, `max_words`).
2. **Prioritizes**: P1 is never dropped; P3 goes first.
3. **States each fact once** (each fact lives in exactly one tier).
4. **Detects contradictions before rendering** (stage 4), e.g.:

   ```yaml
   camera:
     movement: static
     movement_detail: handheld, tracking the runner   # ← C1: blocking
   ```

   The compiler asks: "Should the camera (a) stay still on a tripod, or (b)
   follow the runner handheld?" — and only compiles after the answer.
5. **Lints the output** (stage 8) with a fixed checklist.

## Determinism

The same `shot-spec.yaml` and adapter should give the same prompt. Agents get
close to that by following slot order, vocabulary phrases and lint rules
literally. A future executable compiler (roadmap) can implement the same
stages as code.
