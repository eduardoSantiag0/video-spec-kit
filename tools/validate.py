#!/usr/bin/env python3
"""Optional validator for Video Spec Kit files.

The kit works without this script: agents follow the schemas in schemas/.
Use it to double-check files, in CI, or after editing specs by hand.

Requires:  pip install pyyaml jsonschema
Usage:     python tools/validate.py [path ...]     (default: projects/ examples/ presets/)

Checks
  1. JSON Schema validation by file name:
       scene-spec.yaml → scene, shot-spec.yaml → shot,
       generation-config.yaml → generation-config, project.yaml → project,
       characters/*.yaml → character, presets/<kind>/*.yaml → preset
  2. Provenance: every explicit leaf field of a scene/character spec is listed
     in exactly one provenance group (kit/conventions.md §6).
  3. References: character_id, presets and prompt files exist.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:
    sys.exit("This optional tool needs: pip install pyyaml jsonschema")

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
HEADER_FIELDS = {"spec_version", "id", "project", "version", "idea", "idea_language", "notes", "provenance"}


def load_registry() -> Registry:
    registry = Registry()
    for path in SCHEMAS.glob("*.schema.json"):
        registry = registry.with_resource(path.name, Resource.from_contents(json.loads(path.read_text(encoding="utf-8"))))
    return registry


REGISTRY = load_registry()


def validator(name: str) -> Draft202012Validator:
    schema = json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema, registry=REGISTRY)


def schema_for(path: Path) -> str | None:
    if path.name == "scene-spec.yaml":
        return "scene"
    if path.name == "shot-spec.yaml":
        return "shot"
    if path.name == "generation-config.yaml":
        return "generation-config"
    if path.name == "project.yaml":
        return "project"
    if path.parent.name == "characters":
        return "character"
    if path.parent.parent.name == "presets":
        return "preset"
    return None


def leaf_paths(node, prefix: str = "") -> list[str]:
    if isinstance(node, dict):
        out = []
        for key, value in node.items():
            out += leaf_paths(value, f"{prefix}.{key}" if prefix else key)
        return out
    if isinstance(node, list) and any(isinstance(item, dict) for item in node):
        out = []
        for i, item in enumerate(node):
            out += leaf_paths(item, f"{prefix}[{i}]")
        return out
    return [prefix]


def covers(entry: str, path: str) -> bool:
    return path == entry or path.startswith(entry + ".") or path.startswith(entry + "[")


def check_provenance(data: dict) -> list[str]:
    errors = []
    groups = {k: v for k, v in (data.get("provenance") or {}).items() if isinstance(v, list)}
    content = {k: v for k, v in data.items() if k not in HEADER_FIELDS}
    for path in leaf_paths(content):
        hits = [g for g, entries in groups.items() if any(covers(e, path) for e in entries)]
        if not hits:
            errors.append(f"provenance: '{path}' is not listed in any group")
        elif len(hits) > 1:
            errors.append(f"provenance: '{path}' is listed in several groups: {hits}")
    return errors


def project_root(path: Path) -> Path | None:
    for parent in path.parents:
        if (parent / "project.yaml").exists():
            return parent
    return None


def check_references(path: Path, kind: str, data: dict) -> list[str]:
    errors = []
    proj = project_root(path)
    if kind == "scene" and proj:
        for subject in data.get("subjects", []):
            cid = subject.get("character_id")
            if cid and not (proj / "characters" / f"{cid}.yaml").exists():
                errors.append(f"character '{cid}' not found in {proj / 'characters'}")
        for preset_kind, preset_id in (data.get("presets") or {}).items():
            folder = {"style": "styles", "camera": "cameras", "lighting": "lighting"}[preset_kind]
            local = proj / "presets" / folder / f"{preset_id}.yaml"
            kit = ROOT / "presets" / folder / f"{preset_id}.yaml"
            if not local.exists() and not kit.exists():
                errors.append(f"preset {preset_kind}/{preset_id} not found")
    if kind == "generation-config":
        for run in data.get("runs", []):
            for key in ("prompt_file", "negative_prompt_file"):
                if run.get(key) and not (path.parent / run[key]).exists():
                    errors.append(f"run {run.get('id')}: {key} '{run[key]}' not found")
    return errors


def validate(path: Path) -> list[str]:
    kind = schema_for(path)
    if kind is None:
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"invalid YAML: {exc}"]
    errors = [
        f"{'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message}"
        for e in validator(kind).iter_errors(data)
    ]
    if kind in ("scene", "character") and not errors:
        errors += check_provenance(data)
    if not errors:
        errors += check_references(path, kind, data)
    return errors


def main(argv: list[str]) -> int:
    targets = [Path(a) for a in argv] or [ROOT / "projects", ROOT / "examples", ROOT / "presets"]
    files = []
    for target in targets:
        files += [target] if target.is_file() else sorted(target.rglob("*.yaml"))
    failed = checked = 0
    for path in files:
        if schema_for(path) is None:
            continue
        checked += 1
        errors = validate(path)
        shown = path.resolve().relative_to(ROOT) if path.resolve().is_relative_to(ROOT) else path
        if errors:
            failed += 1
            print(f"FAIL {shown}")
            for err in errors:
                print(f"     - {err}")
        else:
            print(f"ok   {shown}")
    print(f"\n{checked} file(s) checked, {failed} with errors")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
