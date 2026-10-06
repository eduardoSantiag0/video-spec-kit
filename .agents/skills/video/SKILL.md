---
name: video
description: Main entry point of Video Spec Kit. Turns a video idea into a versioned scene spec, storyboard, shot spec and model-specific prompts (Wan, LTX) by asking only the questions that matter. Also routes feedback about a generated clip to review and iteration. Use when the user describes a video or scene idea, types $video or /video, or reports how a generated clip turned out. Does not generate video.
---

# video — orchestrator

## Purpose

Take a user from a vague idea to ready-to-use files with one command:
idea → clarify → scene spec → storyboard → shot spec → prompts. Then, after the
user generates the clip in their own tool, route their feedback to review and
iteration. Most users only ever call this skill; the `video-*` skills it calls
exist for fine control.

## When to use

- The user describes a video, shot or scene they want ("a samurai walks through Tokyo...").
- The user types `$video`, `/video`, or asks to "spec"/"plan" an AI video.
- The user reports how a generated clip turned out ("the face changed...").
- The user asks to continue a project ("next scene", "now she arrives home").

Do **not** use for: generating video, editing video files, or questions about
the kit itself (answer those directly from `README.md`).

## Inputs

| Input            | Required | Source |
|------------------|----------|--------|
| User message     | yes      | Text after `$video` / `/video`, or the conversation |
| `--no-questions` / `--not-questions` | no | Ask nothing; pass the mode to `video-clarify` / `video-screenplay` and list every auto-decision in the report |
| Existing project | no       | `projects/*/project.yaml` |
| Kit files        | yes      | `kit/conventions.md`, `kit/defaults.yaml`, `kit/vocabulary.md` |

Read `kit/conventions.md` before writing any file. It defines layout, naming,
versioning, provenance and value resolution for every step below.

## Workflow

### Step 0 — Route the request

Classify the user message, first match wins:

| Message looks like                                        | Route |
|-----------------------------------------------------------|-------|
| Empty / only "$video"                                      | Ask: "Describe the video in one or two sentences — who/what, doing what, where." Show one example. Stop. |
| Feedback on a generated clip (mentions result, face, camera "was", "looks", "changed", "artifacts") **and** a scene exists | Go to **Feedback flow**. |
| "next scene", "continue", references an earlier scene      | **New scene flow** in the same project with `continuity` set. |
| Screenplay excerpt (sluglines `INT.`/`EXT.`, CHARACTER cues with dialogue, or several numbered/ordered actions) | Run `.agents/skills/video-screenplay/SKILL.md`. |
| "status", "where are we", "what's next"                    | Summarize each scene: current version, run status, last review verdict. Stop. |
| Anything describing visual content                         | **New scene flow**. |

### New scene flow

1. **Project.** Pick the project:
   - the project already used in this conversation, else
   - a project whose id, title or character is named in the message, else
   - create `projects/<id>/` with `project.yaml` from `templates/project.yaml`.
     Derive `<id>` from 2–3 key nouns of the idea (`tokyo-rain`). Do not ask.
   Next scene id = next free `scene-NNN`. Version = `v001`.
2. **Clarify.** Run `.agents/skills/video-clarify/SKILL.md` (in no-questions
   mode when the flag is present). Result: a clarification record
   (path → value → source). At most two question rounds; zero in no-questions mode.
3. **Characters.** For each subject that needs a stable identity, run
   `.agents/skills/video-character/SKILL.md` (criteria are in that skill).
4. **Scene spec.** Run `.agents/skills/video-scene/SKILL.md` →
   `scenes/<scene-id>/v001/scene-spec.yaml`.
5. **Storyboard.** Run `.agents/skills/video-storyboard/SKILL.md` → adds
   `timeline` to the spec and writes `storyboard.md`.
6. **Shot.** Run `.agents/skills/video-shot/SKILL.md` → `shot-spec.yaml`.
   If it reports a **blocking conflict**, ask the user to resolve it (one
   question per conflict, with options), update the spec, and re-run this step.
7. **Prompts.** Run `.agents/skills/video-prompt/SKILL.md` for every adapter in
   `project.yaml → adapters` (default: `kit/defaults.yaml → adapters`).
8. **History.** Create `scenes/<scene-id>/history.md` from
   `templates/history.md` with the `v001` row (Result: `pending`).
9. **Update project.** Append the scene id to `project.yaml → scenes` and any new
   character ids to `characters`.
10. **Report** using the format in *Output*. Stop and wait for the user.

### Feedback flow

1. Identify the scene (the one in this conversation, or the most recently
   modified one) and its current version. If ambiguous, ask once which scene.
2. Run `.agents/skills/video-review/SKILL.md` with the user's words.
3. Show the review summary and the recommended next experiment, then ask:
   "Create v00N with this change? (yes / choose another suggestion / describe your own)".
4. On confirmation, run `.agents/skills/video-iterate/SKILL.md`.

## Rules

1. Never generate, download or upload video. Never call a paid API or service.
2. Ask questions only through `video-clarify`. Never ask about something the
   user already stated. Zero questions is a valid outcome.
3. Write user work only under `projects/`. Never modify kit files (list in
   `kit/conventions.md` §8).
4. Language policy (`kit/conventions.md` §7): accept any input language,
   preserve intent, converse in the user's language, normalize specs to
   English, and write prompts in the same language as the user's idea by
   default (an adapter can pin a different `prompt.language` only when its
   target model needs one).
5. Never present a value the agent chose as if the user chose it. Every value
   carries provenance.
6. Run sub-steps in order; do not skip storyboard or shot — prompts compile
   from `shot-spec.yaml` only.
7. Keep the chat output short: the files hold the detail.

## Output

Files (new scene): `project.yaml` (new or updated), `characters/<id>.yaml`
(when created), and in `scenes/<scene-id>/`: `history.md`,
`v001/scene-spec.yaml`, `v001/storyboard.md`, `v001/shot-spec.yaml`,
`v001/prompts/<adapter>.txt` (+ `.negative.txt`), `v001/generation-config.yaml`,
and `v001/comfyui-notes.md` when `project.yaml → tool: comfyui`.

Chat report (new scene), written in the user's language (labels below are
shown in English for reference), in this order:

```
Scene ready: projects/<project>/scenes/<scene-id>/v001/

Files
- scene-spec.yaml — source of truth
- storyboard.md — beats over time
- shot-spec.yaml — resolved shot (N warnings)
- prompts/wan.txt, prompts/ltx.txt (+ negatives)
- generation-config.yaml — recommended settings

You decided: <3–6 short items tagged user>
I assumed:   <3–6 most impactful inferred/default items> — say "change <item>" to adjust
Decided automatically: <only with --no-questions: every auto-decision>

Warnings: <from shot-spec, or "none">

Next
1. Paste prompts/<adapter>.txt into your tool (see comfyui-notes.md if present).
2. Use the settings in generation-config.yaml and note the seed.
3. Tell me what you see: "$video the face changes and the camera is too fast".
```

## Failure handling

| Situation | Action |
|-----------|--------|
| Idea has no subject or no action ("something cool") | Ask one question for subject + action; offer 3 concrete example ideas. |
| Idea needs several shots ("she enters, sits, then the car explodes") | Explain one scene = one continuous clip. Propose a split into scenes; spec the first one now and list the rest in `project.yaml → notes`. |
| User asks for an adapter that does not exist | List `adapters/*/` ids; offer to draft one from `adapters/_template/` (only if the user asks). |
| User says "just go" / "use defaults" | Skip questions; use recommended options; tag them `inferred` or `default`. |
| User wants to change something after the report | If the version is a draft (no review, no generated seed), edit `scene-spec.yaml` in place, move the path to `user` provenance, re-run steps 5–7. Otherwise run `video-iterate`. |
| A sub-skill fails (missing file, invalid value) | Stop, report which file and field, propose the fix. Do not continue with a broken spec. |

## Examples

**New idea, two questions**

> User: `$video A woman rides a bicycle through Tokyo at night during heavy rain.`
>
> Agent (via video-clarify): asks about look (photoreal / anime / ...) and
> camera viewpoint (alongside / behind / in front / static wide), lists
> assumptions (5 s, 16:9, reusable character in a yellow raincoat...).
>
> User: `1 photoreal cinematic, 2 alongside. She should look tired but determined.`
>
> Agent: writes all files, prints the report.

Full walkthrough: `examples/tokyo-rain/walkthrough.md`.

**Feedback**

> User: `$video the camera is great but her face changes halfway and the hands flicker`
>
> Agent: runs video-review on the current version, recommends one change,
> asks to create v002, runs video-iterate on "yes".
