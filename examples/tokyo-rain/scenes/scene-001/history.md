# History — scene-001 · Night ride in the rain

**Current version:** v002
**Best so far:** v002 — stable identity; only a minor hand flicker remains.

| Version | Date | Changed | Hypothesis | Result | Verdict |
|---------|------|---------|------------|--------|---------|
| v001 | 2026-10-01 | initial spec | — | Camera and rain good; face changes at ≈2.5 s; hand flickers during wipe | baseline |
| v002 | 2026-10-02 | `timeline.beats[1].description`: glance toward camera → eyes on the road | Head turn causes identity drift | Face stable; slight hand flicker remains | confirmed |

## Queued experiments

1. `timeline.beats[0].description`: remove the brow wipe, both hands on the handlebars (from `v002/review.md`).
2. If identity matters across several scenes: `format.input_mode` → `image-to-video` with a still of Mika (from `v001/review.md`).

## Learnings

- Wan 2.2 A14B, medium shot: a head turn toward camera mid-clip re-generates the face → identity drift. Keep the face angle constant, or condition on an image.
- The shot-spec warnings predicted both issues before generation — read them before spending GPU time.
