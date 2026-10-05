# Philosophy

Video Spec Kit applies the ideas of specification-driven development to AI
video. Code generation got better when people stopped "vibe prompting" and
started writing down intent, constraints and acceptance criteria before
asking a model for output. Video generation has the same problem, with an
extra twist: every model wants its prompt shaped differently, and every
generation costs minutes of GPU time.

These ten principles drive every design decision in the kit.

## 1. Specify before prompting

A prompt is the last step, not the first. The kit first captures *what* the
clip must show — subject, action, setting, camera, light, time — in a
structured spec. Writing the spec surfaces the gaps that would otherwise be
filled randomly by the model.

*In the kit:* `video` always runs clarify → scene → storyboard → shot before
any prompt is written.

## 2. Separate intent from model syntax

"A tired rider, tracked from the side, in neon rain" is intent. "Medium tracking
shot at eye level…" for Wan and "A woman rides a bicycle steadily…" for LTX are
syntax. Keep them apart, and switching models — or updating an adapter when a
model changes — does not lose the work.

*In the kit:* `scene-spec.yaml` contains no model names, quality tags or prompt
weights. Model knowledge lives only in `adapters/`.

## 3. Clarify only what matters

Twenty questions is not rigor; it is friction. Ask only what would change the
video completely and has no sensible default. Everything else is assumed —
visibly — and can be changed with one sentence.

*In the kit:* `video-clarify` separates CRITICAL from OPTIONAL dimensions, asks
at most four questions per round, and never re-asks what the user said.

## 4. Prefer structured specifications

Structure makes intent comparable, diffable and checkable. A YAML field can be
validated, inherited from a preset, overridden, and changed in isolation. A
paragraph cannot.

*In the kit:* JSON Schemas, a controlled vocabulary for camera and style terms,
and reusable presets and characters.

## 5. Prompts are compiled artifacts

Like a binary compiled from source, a prompt is derived from the spec by a
deterministic procedure — and is regenerated, not hand-patched. The compiler
removes redundancy, orders information by priority, and refuses to compile
contradictions.

*In the kit:* the Prompt Compiler (`video-shot` + `video-prompt`), described
in [prompt-compiler.md](prompt-compiler.md).

## 6. Preserve continuity

A video is usually more than one clip. Characters, wardrobe, light and screen
direction must survive across scenes. Continuity is designed, not hoped for.

*In the kit:* character files with a `consistency_lock` and a verbatim
`prompt_anchor`; `continuity` links between scenes; first/last frame design.

## 7. Change one variable at a time

When a clip fails, rewriting the whole prompt teaches nothing: something
improves, something else breaks, and nobody knows why. Change one thing, keep
the seed, compare.

*In the kit:* `video-review` proposes one-variable changes; `video-iterate`
creates a new version with exactly that change and verifies the diff.

## 8. Record experiments

Every attempt is data. A hypothesis, the change, the observed result and the
conclusion — written down — turn trial and error into knowledge about how a
model behaves.

*In the kit:* `iteration.md` per version, `history.md` per scene, with a
*Learnings* section.

## 9. Make generation reproducible

A result you cannot reproduce cannot be improved deliberately. Model,
checkpoint, seed, size, frames, steps, guidance, sampler and workflow are part
of the result.

*In the kit:* `generation-config.yaml` per version, self-contained version
folders that are frozen once reviewed.

## 10. Remain model-agnostic

Models change every few months. The spec format should outlive any of them, and
no step should depend on a paid service.

*In the kit:* adapters are plain Markdown + a small profile; adding a model
means adding a folder. Everything runs with free or local agents and local,
open-weight video models.
