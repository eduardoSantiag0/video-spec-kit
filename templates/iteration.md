<!-- TEMPLATE — iteration.md. Produced by video-iterate in every version from v002 on. -->
# Iteration <version> — <scene-id>

| Field     | Value |
|-----------|-------|
| Version   | <vNNN> |
| Parent    | <vNNN> |
| Date      | <YYYY-MM-DD> |
| Type      | <experiment (one variable) / revision (several, justified)> |
| Addresses | <review issue ids, e.g. I1> |

## Changed

```diff
  <spec path>:
-   <previous value>
+   <new value>
```

## Held constant

- Everything else in `scene-spec.yaml` (unchanged)
- Seed: <seed> (same as parent)
- Model, resolution, frames, steps, CFG, sampler: unchanged
- <anything else worth stating>

## Derived files regenerated

- <storyboard.md / shot-spec.yaml / prompts/*.txt / generation-config.yaml>

## Hypothesis

<If we change X, we expect Y, because Z.>

## Observed result

<Filled after the user generates and reviews this version. Otherwise: "pending".>

## Conclusion

<Confirmed / rejected / inconclusive + what we learned. Otherwise: "pending".>
