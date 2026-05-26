# Convergence Logs

Append-only JSONL files tracking solver iteration results. One file per solver run.

- **Schema**: see `docs/design/convergence-tracking.md`
- **Format**: one JSON object per line (JSONL)
- **Naming**: `run-YYYY-MM-DD-HHMMSS.jsonl`
- **Policy**: never edit or delete — these are the audit trail for solver behavior
- **Repo-tracked**: yes — commit convergence logs so paths are reproducible
