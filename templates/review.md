<!-- TEMPLATE — review.md. Produced by video-review. Lives in the version folder it reviews. -->
# Review — <scene-id> · <version> · run `<run-id>`

**Date:** <YYYY-MM-DD>
**Model:** <model> · seed <seed>

## User observation (verbatim)

> <exactly what the user said>

## Scorecard

| Dimension               | Result | Note |
|-------------------------|--------|------|
| Subject identity        | <ok / issue / n.a.> | |
| Subject action          | | |
| Hands / anatomy         | | |
| Camera                  | | |
| Environment             | | |
| Lighting                | | |
| Style                   | | |
| Temporal consistency    | | |
| Prompt adherence        | | |
| Artifacts               | | |

Only dimensions the user mentioned or that follow directly from their words are
marked; the rest are `n.a.` (not observed). Never invent observations.

## Keep (do not change)

- <spec path> — <why it worked>

## Issues

| ID | Issue | Category | Severity | Likely cause | Spec paths involved |
|----|-------|----------|----------|--------------|---------------------|
| I1 | <issue> | <category> | <blocker / major / minor> | <cause> | <paths> |

## Suggested changes (ranked)

Each change touches one variable so its effect can be measured.

1. **<path>**: `<current>` → `<proposed>` — fixes I<n>. Hypothesis: <why>.
2. ...

## Recommended next experiment

<The single change for the next version, and what stays fixed (including the seed).>
