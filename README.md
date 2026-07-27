# TabTS-SkillBench

> **Pre-release research artifact (`0.1.0a1`).** Data distribution, dataset
> licensing review, authorship metadata, and full paper-reproduction artifacts
> are not yet complete. Do not use this snapshot for public leaderboard claims.

TabTS-SkillBench evaluates skill-aware agents on 251 multi-table temporal
data-analysis tasks. The repository contains deterministic evaluator contracts,
Gold outputs, a 47-module Skill library, and the Nanobot evaluation adapter.

The Skill library contains 47 modules: 43 include executable scripts, 25 are
assigned as benchmark-active routed Skills, and 23 are required-execution
Skills. These counts describe different release properties and are not
interchangeable.

## Repository layout

- `benchmark/tasks/tasks_public_251.jsonl`: agent-visible tasks without Gold or Skill labels.
- `benchmark/evaluator/`: evaluator-only contracts, Gold, and full task records.
- `benchmark/manifests/task_set_251.json`: versioned identity of the final task set.
- `skills/`: the 47-module Skill library.
- `benchmark_eval/`: validation, collection, scoring, statistics, and reporting.
- `isolated_benchmark_runner/`: per-task workspace preparation and Nanobot execution.

The 251 tasks in `benchmark/manifests/task_set_251.json` constitute the complete
TabTS-SkillBench release task set. Reported results must identify this task-set
version and preserve its exact membership.

## Installation and static validation

Python 3.11 or 3.12 is recommended.

```bash
python -m pip install -e ".[dev]"
python tools/verify_public_release.py --root .
python -m pytest
```

For data preparation and scoring dependencies:

```bash
python -m pip install -e ".[benchmark,dev]"
```

For Nanobot execution:

```bash
python -m pip install -e ".[benchmark,runner,dev]"
```

## Data status

The standardized tables are not stored in Git history, and this snapshot does
not yet provide a working versioned download URL. Consequently, the full
benchmark cannot currently be reproduced from a fresh clone.

See `data/README.md` and `benchmark/manifests/assets_sha256.json` for the
required 39-file layout and checksums. Do not redistribute a combined data
archive until `DATA_LICENSES.md` records a verified license and redistribution
decision for every upstream dataset.

## Formal execution

Formal Gold-sensitive runs require Linux and Bubblewrap (`bwrap`). The runner
generates a minimal task view for framework wrappers, stages inputs using
ordinary copies, verifies their SHA-256 values, disables web/MCP access, and
fails closed if the configured OS-level sandbox is unavailable.

```bash
export BENCHMARK_PYTHON="$PWD/.venv/bin/python"
export NANOBOT_CONFIG="$HOME/.nanobot/config.json"
python -m benchmark_eval.cli pipeline \
  --experiment configs/core251.yaml \
  --models-config configs/models.example.yaml \
  --stages validate,run,collect,score,report
```

The default `core251.yaml` is a smoke/release configuration, not the complete
paper experiment matrix. Its public condition name is `annotated_preload`;
`oracle_skill` remains only as an internal compatibility alias. Read
`EVALUATION_PROTOCOL.md` before interpreting scores.

## Security

This benchmark executes model-generated code. Do not run formal evaluation
without the configured sandbox, do not mount evaluator/Gold files into an
agent container, and never commit provider credentials. See `SECURITY.md`.

## Current release blockers

- No one-command, license-cleared data acquisition path.
- Dataset-specific redistribution and attribution records are incomplete.
- Benchmark-specific copyright ownership and license approval are incomplete;
  the root MIT notice currently covers the vendored Nanobot component.
- Full paper model/harness/repeat configurations and result tables are absent.
- `CITATION.cff` still needs the approved author list and paper identifiers.
- A container-level Gold-leak canary and cross-platform CI remain to be completed.
