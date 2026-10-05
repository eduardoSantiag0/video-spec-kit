---
name: video-character
description: Creates or updates a reusable character file (characters/<id>.yaml) with stable visual traits, a consistency lock, and a short prompt anchor reused verbatim in every prompt so the character looks the same across scenes. Use when a scene has a main person/creature, when the user describes a character, or types $video-character.
---

# video-character

## Purpose

Give each recurring subject one canonical, visual description. Identity drift
between clips is mostly caused by describing the same person differently each
time; the `prompt_anchor` prevents that.

## When to use

Create a character file when **any** is true:

- the subject is the main human, animal or creature of the scene;
- the user describes the subject's appearance;
- the project has (or will have) more than one scene with this subject;
- the user types `$video-character` or asks to create/edit a character.

Use an inline `subjects[].description` instead (no file) for background
extras and objects.

## Inputs

- Subject description from the idea / clarification record.
- Setting and style of the scene (for coherent wardrobe).
- Existing `projects/<id>/characters/*.yaml`.
- `templates/character.yaml`, `schemas/character.schema.json`.

## Workflow

1. **Reuse check.** If an existing character matches by id, name, or the user
   says "the same woman" → reuse it. Apply only requested changes (step 6).
2. **Id.** Use the name if given (`maria`), else a short descriptive id
   (`rider`, `old-fisherman`). Kebab-case, unique in the project.
3. **Fill stated traits** → provenance `user`.
4. **Infer the minimum** needed for a stable look → provenance `inferred`:
   age range, hair (color, length), one outfit with 1–2 dominant colors, and
   one distinctive feature. Make choices coherent with setting and weather
   (rain → raincoat) and readable at the planned shot size (a bold colored
   garment survives a wide shot; earrings do not).
5. **Consistency lock.** Default: `hair.color`, `hair.style`,
   `wardrobe.outfit`, `wardrobe.colors`, `distinctive_features`. Add anything
   the user calls essential.
6. **Prompt anchor.** Compose 15–35 words:
   `a/an <age> <person/creature> with <hair>, <face detail if distinctive>, wearing <outfit with colors>, <distinctive feature>`.
   - Only visible attributes. No name, no personality, no emotion, no camera.
   - Most distinctive attributes first (color + garment).
   - Concrete nouns and colors; no vague words ("beautiful", "stylish").
7. **Write** `projects/<id>/characters/<character-id>.yaml` from the template;
   omit fields with no value; include `provenance`.
8. **Updates.** If an existing character changes, regenerate `prompt_anchor`
   and warn: "Scenes that reference <id> will use the new look the next time
   they are compiled. Frozen versions keep their own copy in shot-spec.yaml."

## Rules

1. Describe appearance, never identity of real people. If the user asks for a
   real, identifiable private person or a celebrity likeness, describe a
   fictional person with the requested *style* instead and say so.
2. Ethnicity, gender presentation and age are stated only when the user gave
   them or when the setting makes the choice a sensible inference; when
   inferred, list them in "I assumed" so the user sees and can change them.
3. One outfit per character file. A costume change is a scene-level
   `subjects[].description` addition plus a note.
4. `prompt_anchor` must stay ≤ 35 words — it is repeated in every prompt.

## Output

`projects/<project-id>/characters/<character-id>.yaml`, valid against
`schemas/character.schema.json`. Chat: one line with the anchor.

## Failure handling

| Situation | Action |
|-----------|--------|
| Two subjects would get the same id | Suffix with role (`maria-young`). |
| User gives contradictory traits | Latest statement wins; tag `user`; mention it. |
| Requested trait unreadable at the shot size (tiny tattoo in a wide shot) | Keep it in the file but leave it out of the anchor; warn once. |

## Examples

Idea "a woman rides a bicycle through Tokyo at night during heavy rain", user
adds "tired but determined" (that is an expression → goes to the scene, not the
character). Result: `examples/tokyo-rain/characters/mika.yaml`, anchor:

> a Japanese woman in her late 20s with a short black bob, wearing a translucent
> yellow raincoat over a charcoal hoodie, dark jeans and white sneakers, carrying
> a small red backpack
