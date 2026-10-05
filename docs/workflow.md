# Workflow

```
 IDEA ──► CLARIFY ──► SCENE SPEC ──► STORYBOARD ──► SHOT SPEC ──► PROMPTS
  │       video-       video-scene    video-         video-shot    video-prompt
  │       clarify      (+ video-      storyboard                   (wan, ltx, ...)
  │                    character)                                       │
  │                                                                       ▼
  │                                         USER GENERATES THE CLIP (ComfyUI, ...)
  │                                                                       │
  │                                                                       ▼
  └──────────────────────────── ITERATE ◄──────────────────────────── REVIEW
                                video-iterate                         video-review
```

Most users only type `$video` (or `/video`). The orchestrator runs every step
and comes back for the next action. The other skills exist for fine control.

## Step by step

| # | Step | Skill | Reads | Writes |
|---|------|-------|-------|--------|
| 1 | Clarify | `video-clarify` | idea, project, defaults | clarification record (in chat) |
| 2 | Characters | `video-character` | record, existing characters | `characters/<id>.yaml` |
| 3 | Scene spec | `video-scene` | record, presets, defaults | `vNNN/scene-spec.yaml` |
| 4 | Storyboard | `video-storyboard` | scene spec | `timeline` in spec, `vNNN/storyboard.md` |
| 5 | Shot | `video-shot` | spec, characters, presets, defaults | `vNNN/shot-spec.yaml` |
| 6 | Prompts | `video-prompt` | shot spec, adapters | `vNNN/prompts/*.txt`, `generation-config.yaml`, `comfyui-notes.md` |
| 7 | Generate | *you* | prompts, config | a video file |
| 8 | Review | `video-review` | your description, spec, config | `vNNN/review.md`, `history.md` |
| 9 | Iterate | `video-iterate` | parent version, review | `vNNN+1/…`, `iteration.md`, `history.md` |

## Fine-control commands

| Command | What it does |
|---------|--------------|
| `$video-clarify <idea>` | Shows what is ambiguous; writes nothing. |
| `$video-character` | Create or edit a reusable character. |
| `$video-scene` | Write/edit the scene spec of a draft version. |
| `$video-storyboard` | Redesign the beats of a draft version. |
| `$video-shot` | Re-resolve and conflict-check. |
| `$video-prompt wan` | Compile for one adapter (or all, without argument). |
| `$video-review "<what you saw>"` | Diagnose a generation. |
| `$video-iterate "<change>"` | New version with that change. |
| `$video-screenplay [--model] [--duration]` + excerpt | Screenplay excerpt → analysis → shots → specs → prompts. Aliases: `$video_from_screenwright`, `$video-from-screenplay`. See [screenplay.md](screenplay.md). |

Agents that use `/` instead of `$` (Claude Code, Gemini CLI): `/video`,
`/video-prompt wan`, etc. See [agent-support.md](agent-support.md).

## Draft vs frozen versions

A version is a **draft** until it is reviewed or a generation with a known
seed is recorded. Drafts can be edited in place ("make it 8 seconds" →
updated `v001`). Once **frozen**, changes always create a new version, so
every reviewed result stays reproducible. Rules: `kit/conventions.md` §3.

## Multi-scene videos

One scene = one continuous clip. For a sequence, run `$video next scene …`:
the new scene gets `continuity.previous_scene`, its first frame is designed to
match the previous last frame, and characters are reused by id. Automatic
multi-shot generation is on the roadmap.

## Example

The whole loop, with real files: [examples/tokyo-rain/walkthrough.md](../examples/tokyo-rain/walkthrough.md).
