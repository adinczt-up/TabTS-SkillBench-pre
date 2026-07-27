# Data Licenses and Redistribution Status

This repository does not redistribute standardized table binaries. Dataset
provenance and machine-readable release gates are recorded in
`data_sources.yaml`.

Current status:

| Dataset | Upstream | Recorded license | Redistribution status |
|---|---|---|---|
| `azure-pdm` | Microsoft Azure Predictive Maintenance sample | Unknown | `review_required` |
| `bdg2` | Building Data Genome Project 2 | CC BY-SA 4.0 | `review_required` |
| `rel-f1` | RelBench `rel-f1` | Original-data license not yet confirmed | `review_required` |
| `rel-stack` | RelBench `rel-stack` / Stack Exchange | CC BY-SA version depends on contribution date | `review_required` |
| `rel-hm` | H&M Kaggle competition | Competition-specific terms | `user_download_required` |
| `rel-event` | Event Recommendation Engine Kaggle competition | Competition-specific terms | `user_download_required` |

The RelBench software repository is MIT-licensed, but that software license
does not replace the terms governing each underlying dataset. RelBench itself
requires users to obtain the H&M and Event datasets through the corresponding
Kaggle competitions. Stack Exchange contributions span multiple CC BY-SA
versions based on contribution date.

Do not publish a combined data archive until every entry has a pinned upstream
version, retrieval date, raw checksum, verified attribution text, and an
approved redistribution decision. This file is release engineering metadata,
not legal advice.
