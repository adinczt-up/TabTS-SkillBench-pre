# Benchmark data

The standardized assets are not included in Git and this pre-release does not
yet provide a complete download/prepare command.

Required output layout:

```text
data/skillmtts/standardized/<dataset>/tables/*
```

Before a formal run:

1. Review `../data_sources.yaml`; do not redistribute entries marked
   `review_required` or `user_download_required`.
2. Obtain restricted sources directly from their upstream provider.
3. Run `tools/standardize_skillmtts_datasets.py` from the audited source
   workspace.
4. Validate every output against
   `../benchmark/manifests/assets_sha256.json`.

The manifest currently lists 39 standardized files. A fresh-clone,
one-command acquisition path remains a `v1.0.0` release blocker.
