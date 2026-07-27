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

## Data preparation

The standardized tables are not stored in Git history and are not distributed
as a combined archive. Users must obtain each source under its own upstream
terms. The tooling never accepts third-party terms on a user's behalf and never
automatically downloads sources marked `user_download_required`.

```bash
tabts-bench data guide
tabts-bench data prepare
tabts-bench data verify
```

`data prepare` preflights user-provided inputs, runs the deterministic
standardizer, and verifies the required 39 files against
`benchmark/manifests/assets_sha256.json`. H&M and Event require the user to
review and accept the applicable Kaggle competition rules and download the
source through the official Kaggle interface or their own authenticated CLI.
See `data/README.md`, `data_sources.yaml`, and `DATA_LICENSES.md`.

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

## Paper result reproduction

The authoritative aggregate results for the nine model-harness configurations,
the six task-paired ablations, and deterministic reconstruction scripts for
Table 2, Table 3, and Figures 4, 5, 7, and 8 are released under
`artifacts/paper/`.

```bash
python scripts/paper/reproduce_all.py
python tools/verify_paper_results.py
```

The package contains only the final 251-task benchmark and excludes raw model
responses, prompts, reasoning, commands, traces, dataset rows, credentials, and
private service endpoints.

## Security

This benchmark executes model-generated code. Do not run formal evaluation
without the configured sandbox, do not mount evaluator/Gold files into an
agent container, and never commit provider credentials. See `SECURITY.md`.

## Current release blockers

- Full fresh-clone reconstruction requires user-authorized upstream acquisition
  for sources governed by Kaggle competition terms.
- Dataset-specific redistribution and attribution records are incomplete.
- Benchmark-specific copyright ownership and license approval are incomplete;
  the root MIT notice currently covers the vendored Nanobot component.
- `CITATION.cff` still needs the approved author list and paper identifiers.
- A container-level Gold-leak canary and cross-platform CI remain to be completed.
