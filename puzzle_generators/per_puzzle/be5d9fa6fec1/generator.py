"""Generator for 22a4bbc2.

Rule: count transitions (rows different from row above). If running
count of distinct-row groups so far has index mod 3 == 0, recolor
non-zero cells in that row to 2.

Combinatorial axes (8): grid_w, n_blocks, block_height, eight_density,
mix_density, palette_kind, transition_pattern, perturbation_density.
Degenerates: all_same_row, single_block, no_eight_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "be5d9fa6fec1"
VERSION = "1.1.0"
TASK_ID = "be5d9fa6fec1"
SUMMARY = "Stack of row-blocks alternating between 8-rows and 0/1-mix rows."

INVARIANTS = [
    "≥6 row-blocks total",
    "≥1 block of all-8 rows (or 8-dominant)",
    "≥1 block whose rows have both 0s and 1s",
    "consecutive blocks have different row content (real transitions)",
]

TRANSITION_PATTERNS = ("alternating", "random", "eight_heavy", "mix_heavy")
DEGENERATE_TEXTURES = ("all_same_row", "single_block", "no_eight_rows")
HELPFUL_TEXTURES = TRANSITION_PATTERNS

AXES = {
    "grid_w":               {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "n_blocks":             {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "block_height":         {"type": "str", "default": "rng uniform|varied",
                             "valid": "uniform|varied"},
    "eight_density":        {"type": "float", "default": "rng 0..0.3",
                             "valid": "0..0.5"},
    "mix_density":          {"type": "float", "default": "rng 0.3..0.7",
                             "valid": "0..1"},
    "transition_pattern":   {"type": "str", "default": "rng helpful",
                             "valid": "|".join(TRANSITION_PATTERNS)},
    "min_block_h":          {"type": "int", "default": "1", "valid": "1..3"},
    "max_block_h":          {"type": "int", "default": "3", "valid": "1..4"},
    "texture":              {"type": "str", "default": "alias for transition_pattern",
                             "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        w_lo, w_hi, n_lo, n_hi = 3, 4, 5, 6
    elif difficulty == "hard":
        w_lo, w_hi, n_lo, n_hi = 5, 7, 9, 12
    else:
        w_lo, w_hi, n_lo, n_hi = 4, 6, 6, 10
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], w, rng)
    n_blocks = int(overrides.get("n_blocks",
                                 ctx.draw_int("n_blocks", n_lo, n_hi)))
    n_blocks = max(5, min(14, n_blocks))
    pattern = (overrides.get("texture") or overrides.get("transition_pattern")
               or ctx.draw_choice("transition_pattern",
                                  list(TRANSITION_PATTERNS)))
    block_h_kind = overrides.get("block_height",
                                 ctx.draw_choice("block_height",
                                                 ["uniform", "varied"]))
    eight_density = float(overrides.get("eight_density",
                                        ctx.draw_rng("eight_density")
                                        .uniform(0.0, 0.3)))
    mix_density = float(overrides.get("mix_density",
                                      ctx.draw_rng("mix_density")
                                      .uniform(0.3, 0.7)))
    min_bh = int(overrides.get("min_block_h", 1))
    max_bh = int(overrides.get("max_block_h", 3))
    rows = []
    prev = None
    forced_h = rng.randint(min_bh, max_bh) if block_h_kind == "uniform" else None
    last_kind = None
    for bi in range(n_blocks):
        kind = _pick_kind(pattern, last_kind, rng)
        last_kind = kind
        for _ in range(20):
            row = _make_row(kind, w, eight_density, mix_density, rng)
            if row != prev:
                break
        bh = forced_h if forced_h is not None else rng.randint(min_bh, max_bh)
        for _ in range(bh):
            rows.append(list(row))
        prev = row
    if not any(any(v == 8 for v in r) for r in rows):
        rows[0] = [8] * w
    if not any(0 in r and 1 in r for r in rows):
        target = rows[len(rows) // 2]
        target[0] = 0; target[-1] = 1
    return rows


def _pick_kind(pattern, last, rng):
    if pattern == "alternating":
        return "mix" if last == "eight" else "eight"
    if pattern == "eight_heavy":
        return "eight" if rng.random() < 0.7 else "mix"
    if pattern == "mix_heavy":
        return "mix" if rng.random() < 0.7 else "eight"
    return rng.choice(["eight", "mix"])


def _make_row(kind, w, eight_density, mix_density, rng):
    if kind == "eight":
        row = [8] * w
        n_zero = max(0, int(w * eight_density))
        for _ in range(min(n_zero, w - 1)):
            row[rng.randint(0, w - 1)] = 0
        return row
    row = [(1 if rng.random() < mix_density else 0) for _ in range(w)]
    if all(v == 0 for v in row):
        row[rng.randint(0, w - 1)] = 1
    return row


def _draw_from_degenerate(name, w, rng):
    if name == "all_same_row":
        row = [1] * w
        return [list(row) for _ in range(8)]
    if name == "single_block":
        row = [rng.choice([0, 1]) for _ in range(w)]
        if all(v == 0 for v in row):
            row[0] = 1
        return [list(row) for _ in range(5)]
    if name == "no_eight_rows":
        rows = []
        for _ in range(8):
            row = [(1 if rng.random() < 0.5 else 0) for _ in range(w)]
            if all(v == 0 for v in row):
                row[0] = 1
            rows.append(row)
        return rows
    return [[0]]
