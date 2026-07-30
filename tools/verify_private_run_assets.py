#!/usr/bin/env python3
"""Validate private-run metadata and, optionally, downloaded release assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS_ROOT = ROOT / "private_runs"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_manifest(run_id: str, manifest: dict) -> None:
    if manifest["schema_version"] != 1:
        raise ValueError(f"{run_id}: unsupported schema_version")
    if manifest["run_id"] != run_id:
        raise ValueError(f"{run_id}: run_id mismatch")
    filename = manifest["asset"]["filename"]
    if filename != f"{run_id}.tar.gz":
        raise ValueError(f"{run_id}: asset filename must match run_id")
    if manifest["asset"]["format"] != "tar+gzip":
        raise ValueError(f"{run_id}: unsupported asset format")
    if len(manifest["asset"]["sha256"]) != 64:
        raise ValueError(f"{run_id}: invalid SHA-256")
    expected = (
        manifest["benchmark"]["task_count"]
        * len(manifest["benchmark"]["conditions"])
    )
    if manifest["contents"]["trace_records"] != expected:
        raise ValueError(f"{run_id}: trace_records != task_count * conditions")
    if manifest["contents"]["task_result_files"] != expected:
        raise ValueError(f"{run_id}: task_result_files != task_count * conditions")


def validate_asset(path: Path, manifest: dict) -> None:
    run_id = manifest["run_id"]
    if path.stat().st_size != manifest["asset"]["bytes"]:
        raise ValueError(f"{run_id}: byte size mismatch")
    if sha256(path) != manifest["asset"]["sha256"]:
        raise ValueError(f"{run_id}: SHA-256 mismatch")

    contents = manifest["contents"]
    with tarfile.open(path, "r:gz") as archive:
        names = archive.getnames()
        name_set = set(names)
        trace_path = contents["normalized_traces_jsonl"]
        if trace_path not in name_set:
            raise ValueError(f"{run_id}: missing {trace_path}")
        metrics_path = contents["task_metrics_jsonl"]
        if metrics_path is not None and metrics_path not in name_set:
            raise ValueError(f"{run_id}: missing {metrics_path}")
        result_count = sum(
            name.endswith(contents["task_result_suffix"]) for name in names
        )
        if result_count != contents["task_result_files"]:
            raise ValueError(f"{run_id}: task_result file count mismatch")
        trace_file = archive.extractfile(trace_path)
        if trace_file is None:
            raise ValueError(f"{run_id}: trace member is not a regular file")
        trace_count = sum(1 for line in trace_file if line.strip())
        if trace_count != contents["trace_records"]:
            raise ValueError(f"{run_id}: trace record count mismatch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assets-dir",
        type=Path,
        help="Directory containing downloaded private release assets",
    )
    args = parser.parse_args()

    index = load_json(RUNS_ROOT / "index.json")
    if index["schema_version"] != 1:
        raise ValueError("unsupported index schema_version")
    if index["asset_count"] != len(index["runs"]):
        raise ValueError("index asset_count mismatch")

    seen: set[str] = set()
    for entry in index["runs"]:
        run_id = entry["run_id"]
        if run_id in seen:
            raise ValueError(f"duplicate run_id: {run_id}")
        seen.add(run_id)
        manifest_path = RUNS_ROOT / entry["manifest"]
        manifest = load_json(manifest_path)
        validate_manifest(run_id, manifest)
        if args.assets_dir is not None:
            asset_path = args.assets_dir / manifest["asset"]["filename"]
            if not asset_path.is_file():
                raise FileNotFoundError(asset_path)
            validate_asset(asset_path, manifest)
        print(f"ok: {run_id}")

    mode = "metadata+assets" if args.assets_dir is not None else "metadata"
    print(f"validated {len(seen)} private runs ({mode})")


if __name__ == "__main__":
    main()
