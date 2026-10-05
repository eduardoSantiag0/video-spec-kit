# projects/

Your work lives here. The `video` skill creates one folder per video:

```
projects/<project-id>/
  project.yaml
  characters/<id>.yaml
  refs/                      # your reference images (optional)
  scenes/<scene-id>/
    history.md
    v001/ v002/ ...
```

Layout and rules: `kit/conventions.md`. A complete example:
`examples/tokyo-rain/`.

Generated videos (`outputs/`, `*.mp4`) are ignored by git by default — see
`.gitignore`.
