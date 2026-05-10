# ARC-AGI-2 puzzle data attribution

The 1,000 ARC training tasks under `source: training` in
`data/canonical/puzzles.jsonl` (and the corresponding solution files
in `data/base/solutions/training/`) are derived from the public
ARC-AGI-2 competition dataset hosted on Kaggle:

- Competition: <https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2>

Each task carries its original Kaggle task_id in the `legacy_task_id`
field for traceability. Use the upstream Kaggle license terms as the
authoritative source for permitted use of those grids.

The 461 augmented variants under `source: augmented` were derived
from those ARC training tasks by re-rolling input grids while
preserving the rule. They inherit the same upstream license.

The remaining 2,889 puzzles (banks + custom) were authored by this
project's contributors and are released under the project's MIT
license (see `LICENSE`).

The Racket `program_solution` field on every canonical row is
authored by this project's contributors and is MIT-licensed
regardless of the puzzle's origin.

## How to fetch the upstream Kaggle data

This repository does NOT ship the raw `arc-agi_*.json` files; only the
canonical/derived form. To fetch the originals (e.g. to rebuild
`data/canonical/puzzles.jsonl` from scratch):

```bash
# Requires Kaggle CLI authenticated against your account.
python3 scripts/fetch_arc_data.py
```
