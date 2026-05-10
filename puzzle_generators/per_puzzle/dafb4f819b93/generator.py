"""Generator for a406ac07.

Rule: for each 0 cell, find unique color shared between its row's
non-zero values and col's non-zero values. If exactly one common color,
fill with it.

Combinatorial axes (8): grid_n, n_runs, palette_kind, run_length_kind,
last_row_layout, last_col_layout, anchor_corner, asymmetry_force.
Degenerates: monochrome_seq, all_zero, single_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dafb4f819b93"
VERSION = "1.1.0"
TASK_ID = "dafb4f819b93"
SUMMARY = "n×n; rule fills 0 cells via unique row∩col color."

INVARIANTS = [
    "n×n grid, n in [6, 12]",
    "right col and bottom row share the same run-length-encoded color sequence",
    "3-5 distinct non-bg colors in the sequence",
    "interior is bg=0 (the rule fills it)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "small")
RUN_LENGTH_KINDS = ("uniform", "varied", "ascending", "descending")
DEGENERATE_TEXTURES = ("monochrome_seq", "all_zero", "single_color")
HELPFUL_TEXTURES = RUN_LENGTH_KINDS

AXES = {
    "grid_n":            {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "n_runs":            {"type": "int", "default": "rng 3..5", "valid": "2..7"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "run_length_kind":   {"type": "str", "default": "rng helpful",
                          "valid": "|".join(RUN_LENGTH_KINDS)},
    "max_run_length":    {"type": "int", "default": "3", "valid": "2..5"},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "include_decoy":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for run_length_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        n_lo, n_hi = 6, 8
    elif difficulty == "hard":
        n_lo, n_hi = 11, 14
    else:
        n_lo, n_hi = 8, 12
    n = ctx.draw_int("grid_n", n_lo, n_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], n, rng)
    n_runs = int(overrides.get("n_runs",
                               ctx.draw_int("n_runs", 3, min(5, n))))
    n_runs = max(2, min(min(7, n), n_runs))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n_runs:
        extras = [c for c in [1, 2, 3, 4, 6, 7, 8, 9] if c not in pool]
        rng.shuffle(extras)
        pool += extras
    colors = pool[:n_runs]
    run_kind = (overrides.get("texture") or
                overrides.get("run_length_kind")
                or ctx.draw_choice("run_length_kind",
                                   list(RUN_LENGTH_KINDS)))
    runs = _draw_runs(run_kind, n, n_runs, rng)
    g = full_grid(n, n, 0)
    seq = []
    for color, length in zip(colors, runs):
        seq.extend([color] * length)
    seq = seq[:n]
    while len(seq) < n:
        seq.append(colors[-1])
    for i in range(n):
        g[i][n - 1] = seq[i]
        g[n - 1][i] = seq[i]
    if bool(overrides.get("anchor_corner", False)):
        g[0][0] = colors[0]
    return g


def _draw_runs(kind, n, n_runs, rng):
    runs = []
    if kind == "uniform":
        base = max(1, n // n_runs)
        runs = [base] * n_runs
        runs[0] += n - sum(runs)
    elif kind == "ascending":
        runs = [(i + 1) for i in range(n_runs)]
        s = sum(runs)
        if s > n:
            scale = n / s
            runs = [max(1, int(r * scale)) for r in runs]
            runs[0] += n - sum(runs)
        else:
            runs[-1] += n - sum(runs)
    elif kind == "descending":
        runs = [(n_runs - i) for i in range(n_runs)]
        s = sum(runs)
        if s > n:
            runs = [max(1, int(r * n / s)) for r in runs]
            runs[0] += n - sum(runs)
        else:
            runs[-1] += n - sum(runs)
    else:
        remaining = n
        for i in range(n_runs):
            if i == n_runs - 1:
                runs.append(remaining)
            else:
                max_take = remaining - (n_runs - 1 - i)
                take = rng.randint(1, min(3, max_take))
                runs.append(take)
                remaining -= take
    return [max(1, r) for r in runs]


def _draw_from_degenerate(name, n, rng):
    g = full_grid(n, n, 0)
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    if name == "monochrome_seq":
        for i in range(n):
            g[i][n - 1] = color
            g[n - 1][i] = color
        return g
    if name == "all_zero":
        return g
    if name == "single_color":
        c = color
        for i in range(n):
            g[i][n - 1] = c
            g[n - 1][i] = c
        return g
    return g
