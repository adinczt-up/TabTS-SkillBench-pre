# Changelog

All notable release changes will be documented here.

## [Unreleased]

- Finalize benchmark-specific copyright ownership and license grants.
- Publish approved, versioned dataset acquisition paths.
- Publish the complete paper experiment matrix and result artifacts.
- Add a runtime Gold-leak canary test in the supported Linux sandbox.

## [0.1.0a1] - 2026-07-27

### Added

- Sanitized runner task view separated from evaluator-only task metadata.
- Fail-closed Bubblewrap mode for formal Linux evaluation.
- Input asset copy staging with pre/post SHA-256 verification.
- Explicit raw-versus-repaired scoring and infrastructure retry metrics.
- Precision-aware partial-credit diagnostics.
- Release verifier, CI workflow, evaluation protocol, security policy, data
  provenance registry, Benchmark Card, and community templates.
- Installable `tabts-skillbench` wheel and source distribution.

### Changed

- Default asset staging changed from hard links to independent copies.
- Public condition name changed to `annotated_preload`; `oracle_skill` remains an
  internal compatibility alias.
- Whole-task retries are restricted to infrastructure failures.
- Repository metadata and Docker image now describe the benchmark rather than
  the upstream Nanobot gateway.

### Known limitations

- This is a pre-release artifact and is not approved for leaderboard claims.
- Dataset redistribution and benchmark-specific licensing are not finalized.
- The complete paper reproduction package is not included.
